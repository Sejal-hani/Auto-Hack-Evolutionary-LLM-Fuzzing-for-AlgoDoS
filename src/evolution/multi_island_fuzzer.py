import math
import sys
import uuid
import asyncio
import logging
import subprocess
from typing import List, Dict, Any

from src.sandbox.sandbox_models import TestCase, ExecutionResult, ExecutionStatus
from src.sandbox.compiler import CompilationResult
from src.sandbox.telemetry_runner import SecureSandbox
from src.llm_engine.async_llm_agent import LlamaFuzzerAgent
from src.ast_analyzer.cfg_parser import CppAstMetadata

logger = logging.getLogger(__name__)

class EvolutionaryIsland:
    def __init__(self, island_id: str, strategy_prompt: str, llm_agent: LlamaFuzzerAgent, population_size: int = 5):
        self.island_id = island_id
        self.strategy_prompt = strategy_prompt
        self.llm_agent = llm_agent
        self.population_size = population_size
        self.population: List[ExecutionResult] = []
        self.highest_fitness: float = 0.0

    def update_population(self, new_results: List[ExecutionResult]):
        self.population.extend(new_results)
        self.population.sort(key=lambda r: r.telemetry.fitness_score, reverse=True)
        self.population = self.population[:self.population_size]
        if self.population: self.highest_fitness = self.population[0].telemetry.fitness_score

    def get_elite_pool(self, top_k: int = 3) -> List[Dict[str, Any]]:
        elites = []
        for res in self.population[:top_k]:
            payload_str = res.stdout.decode('utf-8', errors='replace') if res.stdout else res.test_case_id
            elites.append({
                "payload_preview": payload_str[:100] + "... [TRUNCATED]", 
                "cpu_time_ms": res.telemetry.cpu_user_time_ms
            })
        return elites

    def prune_weak(self, bottom_percent: float = 0.30):
        kill_count = math.ceil(len(self.population) * bottom_percent)
        if kill_count > 0: self.population = self.population[:-kill_count]

class FuzzOrchestrator:
    def __init__(self, sandbox: SecureSandbox, island_keys: List[str], n_constraint: int):
        self.sandbox = sandbox
        self.n_constraint = n_constraint
        self.input_format = ""
        self.islands = [
            EvolutionaryIsland("Island_Alpha", "EXTREMIST: Use array boundary bounds, MAX_INT, MIN_INT, or 0.", LlamaFuzzerAgent(island_keys[0])),
            EvolutionaryIsland("Island_Beta", "DUPLICATOR: Use dense repetition. Maximize identical array elements to force hash collisions.", LlamaFuzzerAgent(island_keys[1])),
            EvolutionaryIsland("Island_Gamma", "REVERSER: Generate strictly descending or monotonically structured sequences.", LlamaFuzzerAgent(island_keys[2]))
        ]
        
    async def process_island_generation(self, session: Any, island: EvolutionaryIsland, ast_meta: CppAstMetadata, comp_result: CompilationResult, generation: int) -> bool:
        elite_context = island.get_elite_pool(top_k=3)
        healing_feedback = ""
        
        # SELF HEALING LOOP: Gives the AI 3 tries to fix its own errors
        for repair_attempt in range(3):
            if repair_attempt > 0: logger.warning(f"[{island.island_id}] 🛠️ SELF-HEALING ATTEMPT {repair_attempt}...")
            else: logger.info(f"[{island.island_id}] Gen {generation}: Requesting Generator...")

            generated_codes = await island.llm_agent.generate_mutations(
                session=session, ast_meta=ast_meta, elite_telemetry=elite_context,
                n_constraint=self.n_constraint, island_strategy=island.strategy_prompt, 
                input_format=self.input_format, healing_feedback=healing_feedback
            )
            
            if not generated_codes: return False
            python_script = generated_codes[0]
            
            try:
                proc = subprocess.run([sys.executable, "-c", python_script], capture_output=True, text=True, timeout=2.0)
                if proc.returncode != 0:
                    healing_feedback = f"Your Python code crashed with error: {proc.stderr[-200:]}. Fix the syntax."
                    continue
                payload_str = proc.stdout.strip()
            except subprocess.TimeoutExpired:
                healing_feedback = "Your Python code took too long to run. Make it faster."
                continue

            tc = TestCase(id=uuid.uuid4().hex[:8], payload=payload_str.encode('utf-8'), generation=generation, n_constraint=self.n_constraint)
            exec_result = self.sandbox.evaluate(comp_result, tc)
            
            # CATCH THE 0.0MS INPUT FORMAT ERROR
            if exec_result.telemetry.cpu_user_time_ms < 2.0 and not exec_result.is_algodos_triggered:
                healing_feedback = "The C++ program exited in 0.0ms! This means your Python output did NOT match the [INPUT_FORMAT] exactly, causing C++ 'cin' to fail instantly. Fix your print statements."
                continue
            
            # If it survived without errors, update population and exit healing loop
            island.update_population([exec_result])
            if exec_result.is_algodos_triggered:
                logger.critical(f"🚨 ALGODOS ACHIEVED ON {island.island_id}! 🚨")
                return True

            logger.info(f"[{island.island_id}] Gen {generation} Complete. Peak CPU Time: {island.highest_fitness}ms")
            return False
            
    def perform_soft_migration(self):
        ranked = sorted(self.islands, key=lambda i: i.highest_fitness, reverse=True)
        strong_island = ranked[0]
        weak_islands = ranked[1:]
        migrant_count = max(1, math.ceil(len(strong_island.population) * 0.20))
        migrants = strong_island.population[:migrant_count]
        
        for weak in weak_islands:
            weak.prune_weak(bottom_percent=0.30)
            weak.population.extend(migrants)
            weak.update_population([])












# """
# Multi-Island Evolutionary Orchestrator (Metaprogramming Edition).

# Implements the mathematical speciation and soft-migration policies from the FunFuzz framework.
# Orchestrates parallel asynchronous islands to prevent genetic trajectory collapse.
# Features a Distributed Multi-Key API architecture and Native Metaprogramming Execution
# to bypass LLM token limits and instantly generate massive algorithmic payloads.
# """

# import math
# import sys
# import uuid
# import asyncio
# import logging
# import subprocess
# from typing import List, Dict, Any

# # Local imports
# from src.sandbox.sandbox_models import TestCase, ExecutionResult, ExecutionStatus
# from src.sandbox.compiler import CompilationResult
# from src.sandbox.telemetry_runner import SecureSandbox
# from src.llm_engine.async_llm_agent import LlamaFuzzerAgent
# from src.ast_analyzer.cfg_parser import CppAstMetadata

# logger = logging.getLogger(__name__)

# class EvolutionaryIsland:
#     """
#     An isolated genetic population representing a single LLM attack strategy.
#     Now equipped with its own dedicated LLM Agent (and API Key) for distributed parallel API calls.
#     """
#     def __init__(self, island_id: str, strategy_prompt: str, llm_agent: LlamaFuzzerAgent, population_size: int = 5):
#         self.island_id = island_id
#         self.strategy_prompt = strategy_prompt
#         self.llm_agent = llm_agent
#         self.population_size = population_size
        
#         # The genetic pool: stores the evaluated ExecutionResults of this island
#         self.population: List[ExecutionResult] = []
#         self.highest_fitness: float = 0.0

#     def update_population(self, new_results: List[ExecutionResult]):
#         """Integrates new test cases, strictly sorting by the mathematical fitness score."""
#         self.population.extend(new_results)
#         # Sort descending by fitness score (CPU Time + Cache Misses)
#         self.population.sort(key=lambda r: r.telemetry.fitness_score, reverse=True)
        
#         # Enforce population cap (Truncation Selection)
#         self.population = self.population[:self.population_size]
        
#         if self.population:
#             self.highest_fitness = self.population[0].telemetry.fitness_score

#     def get_elite_pool(self, top_k: int = 3) -> List[Dict[str, Any]]:
#         """Extracts the best payloads to feed back into the LLM's context window."""
#         elites = []
#         for res in self.population[:top_k]:
#             # We truncate the payload in the context window so the LLM doesn't waste tokens reading 5000 numbers
#             payload_str = res.stdout.decode('utf-8', errors='replace') if res.stdout else res.test_case_id
#             elites.append({
#                 "payload_preview": payload_str[:100] + "... [TRUNCATED]", 
#                 "cpu_time_ms": res.telemetry.cpu_user_time_ms
#             })
#         return elites

#     def prune_weak(self, bottom_percent: float = 0.30):
#         """Kills off the lowest performing inputs to make room for cross-island migrants."""
#         kill_count = math.ceil(len(self.population) * bottom_percent)
#         if kill_count > 0:
#             self.population = self.population[:-kill_count]


# class FuzzOrchestrator:
#     """
#     The Global Fuzzer. Runs the islands in parallel, executes the LLM's Python scripts natively,
#     evaluates fitness in the Sandbox, and executes Cross-Island migrations.
#     """
#     def __init__(self, sandbox: SecureSandbox, island_keys: List[str], n_constraint: int):
#         self.sandbox = sandbox
#         self.n_constraint = n_constraint
        
#         # Initialize 3 distinct genetic islands, injecting a UNIQUE API KEY into each one
#         self.islands = [
#             EvolutionaryIsland(
#                 "Island_Alpha", 
#                 "EXTREMIST: Use array boundary bounds, MAX_INT, MIN_INT, or 0.", 
#                 LlamaFuzzerAgent(island_keys[0])
#             ),
#             EvolutionaryIsland(
#                 "Island_Beta", 
#                 "DUPLICATOR: Use dense repetition. Maximize identical array elements to force hash collisions.", 
#                 LlamaFuzzerAgent(island_keys[1])
#             ),
#             EvolutionaryIsland(
#                 "Island_Gamma", 
#                 "REVERSER: Generate strictly descending or monotonically structured sequences.", 
#                 LlamaFuzzerAgent(island_keys[2])
#             )
#         ]
        
#     async def process_island_generation(
#         self, 
#         session: Any, 
#         island: EvolutionaryIsland, 
#         ast_meta: CppAstMetadata, 
#         comp_result: CompilationResult,
#         generation: int
#     ) -> bool:
#         """Runs a single generation for a single island asynchronously (Metaprogramming Execution)."""
#         # 1. Get Elite Context from the Island's history
#         elite_context = island.get_elite_pool(top_k=3)
        
#         # 2. Ask the Island's dedicated LLM to write a Python Generator Script
#         logger.info(f"[{island.island_id}] Gen {generation}: Requesting Python Metaprogram from LLM...")
#         generated_codes = await island.llm_agent.generate_mutations(
#             session=session,
#             ast_meta=ast_meta,
#             elite_telemetry=elite_context,
#             n_constraint=self.n_constraint,
#             island_strategy=island.strategy_prompt
#         )
        
#         if not generated_codes:
#             return False

#         python_script = generated_codes[0]
        
#         # 3. Native Execution: Run the LLM's Python code to instantly generate the massive payload
#         try:
#             proc = subprocess.run(
#                 [sys.executable, "-c", python_script],
#                 capture_output=True,
#                 text=True,
#                 timeout=2.0  # The Python math script should run in <0.1s. If it loops infinitely, kill it.
#             )
#             payload_str = proc.stdout.strip()
            
#             if proc.returncode != 0:
#                 logger.error(f"[{island.island_id}] LLM's Python script crashed! Error: {proc.stderr[:150]}")
#                 return False
                
#             if not payload_str:
#                 logger.error(f"[{island.island_id}] LLM's Python script ran successfully but printed nothing.")
#                 return False
                
#         except subprocess.TimeoutExpired:
#             logger.error(f"[{island.island_id}] LLM's Python script exceeded 2.0s execution time limit.")
#             return False

#         # 4. Compile the generated payload & Execute in C++ Sandbox
#         tc = TestCase(
#             id=uuid.uuid4().hex[:8],
#             payload=payload_str.encode('utf-8'),
#             generation=generation,
#             n_constraint=self.n_constraint
#         )
        
#         # Synchronous CPU Execution (Isolated via OS Limits)
#         exec_result = self.sandbox.evaluate(comp_result, tc)
        
#         # FAST FAIL / WIN CONDITION: Did we TLE the C++ program?
#         if exec_result.is_algodos_triggered:
#             logger.critical(f"🚨 ALGODOS ACHIEVED ON {island.island_id}! 🚨 Payload ID: {tc.id}")
#             return True

#         # 5. Update Island Genetic Pool
#         island.update_population([exec_result])
#         logger.info(f"[{island.island_id}] Gen {generation} Complete. Peak CPU Time: {island.highest_fitness}ms")
        
#         return False

#     def perform_soft_migration(self):
#         """
#         The FunFuzz Algorithm.
#         Rank islands by coverage (fitness). Top island is Strong. Rest are Weak.
#         Weak islands prune bottom 30% of population. Strong island donates top 20% to weak islands.
#         """
#         logger.info("--- Initiating Cross-Island Soft Migration ---")
#         # Rank islands by their highest fitness
#         ranked = sorted(self.islands, key=lambda i: i.highest_fitness, reverse=True)
        
#         strong_island = ranked[0]
#         weak_islands = ranked[1:]
        
#         # Extract the elite 20% from the strong island (Migrants)
#         migrant_count = max(1, math.ceil(len(strong_island.population) * 0.20))
#         migrants = strong_island.population[:migrant_count]
        
#         for weak in weak_islands:
#             # Prune bottom 30% of the weak island
#             weak.prune_weak(bottom_percent=0.30)
            
#             # Inject strong migrants into the weak island
#             # Copied by reference because they are @dataclass(frozen=True)
#             weak.population.extend(migrants)
            
#             # Re-sort the weak island
#             weak.update_population([]) 
#             logger.info(f"Migrated {migrant_count} elite genomes from {strong_island.island_id} -> {weak.island_id}")