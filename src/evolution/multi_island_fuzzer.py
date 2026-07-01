"""
Multi-Island Evolutionary Orchestrator.

Implements the mathematical speciation and soft-migration policies from the FunFuzz framework.
Orchestrates parallel asynchronous islands to prevent genetic trajectory collapse.
Evaluates algorithmic degradation via fitness-proportionate selection.
"""

import math
import uuid
import asyncio
import logging
from typing import List, Dict, Any, Tuple

# Local imports
from src.sandbox.sandbox_models import TestCase, ExecutionResult, ExecutionStatus
from src.sandbox.compiler import CompilationResult
from src.sandbox.telemetry_runner import SecureSandbox
from src.llm_engine.async_llm_agent import LlamaFuzzerAgent
from src.ast_analyzer.cfg_parser import CppAstMetadata

logger = logging.getLogger(__name__)

class EvolutionaryIsland:
    """
    An isolated genetic population representing a single LLM attack strategy.
    """
    def __init__(self, island_id: str, strategy_prompt: str, population_size: int = 5):
        self.island_id = island_id
        self.strategy_prompt = strategy_prompt
        self.population_size = population_size
        
        # The genetic pool: stores the evaluated ExecutionResults of this island
        self.population: List[ExecutionResult] = []
        self.highest_fitness: float = 0.0

    def update_population(self, new_results: List[ExecutionResult]):
        """Integrates new test cases, strictly sorting by the mathematical fitness score."""
        self.population.extend(new_results)
        # Sort descending by fitness score (CPU Time + Cache Misses)
        self.population.sort(key=lambda r: r.telemetry.fitness_score, reverse=True)
        
        # Enforce population cap (Truncation Selection)
        self.population = self.population[:self.population_size]
        
        if self.population:
            self.highest_fitness = self.population[0].telemetry.fitness_score

    def get_elite_pool(self, top_k: int = 3) -> List[Dict[str, Any]]:
        """Extracts the best payloads to feed back into the LLM's context window."""
        elites = []
        for res in self.population[:top_k]:
            elites.append({
                "payload": res.stdout.decode('utf-8', errors='replace') if res.stdout else res.test_case_id, # Fallback ID
                "cpu_time_ms": res.telemetry.cpu_user_time_ms
            })
        return elites

    def prune_weak(self, bottom_percent: float = 0.30):
        """Kills off the lowest performing inputs to make room for cross-island migrants."""
        kill_count = math.ceil(len(self.population) * bottom_percent)
        if kill_count > 0:
            self.population = self.population[:-kill_count]


class FuzzOrchestrator:
    """
    The Global Fuzzer. Runs the islands in parallel, evaluates fitness, and executes migrations.
    """
    def __init__(self, sandbox: SecureSandbox, llm_agent: LlamaFuzzerAgent, n_constraint: int):
        self.sandbox = sandbox
        self.llm_agent = llm_agent
        self.n_constraint = n_constraint
        
        # Initialize 3 distinct genetic islands
        self.islands = [
            EvolutionaryIsland("Island_Alpha", "EXTREMIST: Use array boundary bounds, MAX_INT, MIN_INT, or 0."),
            EvolutionaryIsland("Island_Beta", "DUPLICATOR: Use dense repetition. Maximize identical array elements to force hash collisions."),
            EvolutionaryIsland("Island_Gamma", "REVERSER: Generate strictly descending or monotonically structured sequences.")
        ]
        
    async def process_island_generation(
        self, 
        session: Any, 
        island: EvolutionaryIsland, 
        ast_meta: CppAstMetadata, 
        comp_result: CompilationResult,
        generation: int
    ) -> bool:
        """Runs a single generation for a single island asynchronously."""
        # 1. Get Elite Context from the Island's history
        elite_context = island.get_elite_pool(top_k=3)
        
        # 2. Ask LLM to mutate (Awaits network I/O without blocking other islands)
        logger.info(f"[{island.island_id}] Gen {generation}: Querying LLM...")
        mutated_payloads = await self.llm_agent.generate_mutations(
            session=session,
            ast_meta=ast_meta,
            elite_telemetry=elite_context,
            n_constraint=self.n_constraint,
            island_strategy=island.strategy_prompt
        )
        
        if not mutated_payloads:
            return False

        # 3. Compile payloads to TestCase objects & Execute in Sandbox
        generation_results = []
        for payload_str in mutated_payloads:
            tc = TestCase(
                id=uuid.uuid4().hex[:8],
                payload=payload_str.encode('utf-8'),
                generation=generation,
                n_constraint=self.n_constraint
            )
            
            # Synchronous CPU Execution (Fast, isolated via OS limits)
            exec_result = self.sandbox.evaluate(comp_result, tc)
            generation_results.append(exec_result)
            
            # FAST FAIL / WIN CONDITION: Did we TLE the program?
            if exec_result.is_algodos_triggered:
                logger.critical(f"🚨 ALGODOS ACHIEVED ON {island.island_id}! 🚨 Payload ID: {tc.id}")
                return True

        # 4. Update Island Genetic Pool
        island.update_population(generation_results)
        logger.info(f"[{island.island_id}] Gen {generation} Complete. Peak CPU Time: {island.highest_fitness}ms")
        return False

    def perform_soft_migration(self):
        """
        The FunFuzz Algorithm.
        Rank islands by coverage (fitness). Top island is Strong. Rest are Weak.
        Weak islands prune bottom 30% of population. Strong island donates top 20% to weak islands.
        """
        logger.info("--- Initiating Cross-Island Soft Migration ---")
        # Rank islands by their highest fitness
        ranked = sorted(self.islands, key=lambda i: i.highest_fitness, reverse=True)
        
        strong_island = ranked[0]
        weak_islands = ranked[1:]
        
        # Extract the elite 20% from the strong island (Migrants)
        migrant_count = max(1, math.ceil(len(strong_island.population) * 0.20))
        migrants = strong_island.population[:migrant_count]
        
        for weak in weak_islands:
            # Prune bottom 30% of the weak island
            weak.prune_weak(bottom_percent=0.30)
            
            # Inject strong migrants into the weak island
            # We copy them by reference because they are @dataclass(frozen=True)
            weak.population.extend(migrants)
            
            # Re-sort the weak island
            weak.update_population([]) 
            logger.info(f"Migrated {migrant_count} elite genomes from {strong_island.island_id} -> {weak.island_id}")