"""
Multi-Island Evolutionary Orchestrator (10-Island UCB1 & Self-Healing Edition).

Implements:
1. Complete 10-Island Speciation Taxonomy (Table 3.1)
2. UCB1 Multi-Armed Bandit Scheduling (Score_i = x_i + c * sqrt(2*ln(N)/n_i))
3. Native Generative Metaprogramming Execution
4. Self-Healing Syntax & Execution Loop with Traceback Feedback (up to 3 retries)
5. Epistemic Reflection for Stagnating Islands
6. FunFuzz-Style Cross-Island Soft Migration
"""

import math
import sys
import uuid
import asyncio
import logging
import subprocess
from typing import List, Dict, Any, Optional, Tuple

# Local imports
from src.sandbox.sandbox_models import TestCase, ExecutionResult, ExecutionStatus
from src.sandbox.compiler import CompilationResult
from src.sandbox.telemetry_runner import SecureSandbox
from src.llm_engine.async_llm_agent import LlamaFuzzerAgent
from src.ast_analyzer.cfg_parser import CppAstMetadata

logger = logging.getLogger("CF-Fuzz.Evolution")


class EvolutionaryIsland:
    """An isolated genetic population representing a specialized algorithmic attack vector."""
    
    def __init__(self, island_id: str, category: str, strategy_prompt: str, llm_agent: LlamaFuzzerAgent, population_size: int = 5):
        self.island_id = island_id
        self.category = category
        self.strategy_prompt = strategy_prompt
        self.llm_agent = llm_agent
        self.population_size = population_size
        
        # Genetic pool
        self.population: List[ExecutionResult] = []
        self.highest_fitness: float = 0.0
        self.fitness_history: List[float] = []
        
        # Bandit Metrics
        self.selection_count: int = 0
        self.total_reward: float = 0.0
        self.last_winning_code: Optional[str] = None

    def update_population(self, new_results: List[ExecutionResult]):
        """Integrates new test cases, strictly sorting by fitness score."""
        self.population.extend(new_results)
        self.population.sort(key=lambda r: r.telemetry.fitness_score, reverse=True)
        self.population = self.population[:self.population_size]
        
        if self.population:
            peak = self.population[0].telemetry.fitness_score
            self.highest_fitness = peak
            self.fitness_history.append(peak)

    def get_elite_pool(self, top_k: int = 3) -> List[Dict[str, Any]]:
        """Extracts top genomes for prompt context."""
        elites = []
        for res in self.population[:top_k]:
            payload_str = res.stdout.decode('utf-8', errors='replace') if res.stdout else res.test_case_id
            elites.append({
                "payload_preview": payload_str[:120] + "... [TRUNCATED]",
                "cpu_time_ms": res.telemetry.cpu_user_time_ms,
                "fitness_score": res.telemetry.fitness_score
            })
        return elites

    def prune_weak(self, bottom_percent: float = 0.30):
        """Kills off the lowest-performing inputs."""
        kill_count = math.ceil(len(self.population) * bottom_percent)
        if kill_count > 0:
            self.population = self.population[:-kill_count]

    def is_stagnant(self, window: int = 3, threshold: float = 0.01) -> bool:
        """Checks if island fitness has plateaued with <1% gain over the last N generations."""
        if len(self.fitness_history) < window:
            return False
        recent = self.fitness_history[-window:]
        if recent[0] <= 0:
            return False
        gain = (recent[-1] - recent[0]) / (recent[0] + 1e-6)
        return gain < threshold


class FuzzOrchestrator:
    """
    10-Island UCB1 Orchestrator with Self-Healing Execution.
    """
    
    TAXONOMY = [
        # HASHMAP
        ("Alpha_HashCollision", "HASHMAP", "Dense repetitions separated by exact powers of 2 to defeat MurmurHash / bucket distributions."),
        ("Beta_ModuloStep", "HASHMAP", "Generate keys formatted as X * 107897 (large primes) to force O(N) linked-list bucket collisions."),
        ("Gamma_LoadFactor", "HASHMAP", "Wide-range uniform integers maximizing rehash and reallocation overhead."),
        # GRAPH
        ("Alpha_StarGraph", "GRAPH", "Connect Node 1 to all other nodes (1-2, 1-3...) maximizing BFS/DFS queue and memory depth."),
        ("Beta_LineChain", "GRAPH", "Connect nodes linearly (1-2, 2-3, 3-4... N) to force maximum call-stack recursion depth."),
        ("Gamma_Disconnected", "GRAPH", "Sparse, isolated subgraphs and components triggering boundary-condition loop traps."),
        # SORTING
        ("Alpha_Reversed", "SORTING", "Strictly descending sequences to trigger O(N^2) worst-case QuickSort."),
        ("Beta_AllEqual", "SORTING", "Generate identical array elements to break naive median-of-three pivot logic."),
        ("Gamma_Sawtooth", "SORTING", "Alternating high-low sequence (MAX, MIN, MAX...) forcing maximum element comparison swaps."),
        # GENERAL/MATH
        ("Delta_Extremist", "GENERAL/MATH", "Boundary scalars (INT_MAX, 0, -1, sparse spikes) triggering arithmetic overflow / cache misses.")
    ]

    def __init__(self, sandbox: SecureSandbox, island_keys: List[str], n_constraint: int = 100000, input_format: Optional[str] = None):
        self.sandbox = sandbox
        self.n_constraint = n_constraint
        self.input_format = input_format
        self.total_bandit_selections: int = 0
        self.c_exploration: float = 1.414
        
        # Round-robin key distribution across 10 islands
        self.islands: List[EvolutionaryIsland] = []
        for i, (name, category, directive) in enumerate(self.TAXONOMY):
            key = island_keys[i % len(island_keys)]
            agent = LlamaFuzzerAgent(key)
            self.islands.append(EvolutionaryIsland(name, category, directive, agent))

    def select_active_islands_ucb1(self, k: int = 3) -> List[EvolutionaryIsland]:
        """
        UCB1 Multi-Armed Bandit Selection:
        Score_i = x_i + c * sqrt(2 * ln(N) / n_i)
        """
        self.total_bandit_selections += 1
        N = self.total_bandit_selections

        # Cold start: ensure each island gets sampled once
        unvisited = [i for i in self.islands if i.selection_count == 0]
        if unvisited:
            chosen = unvisited[:k]
            for c in chosen:
                c.selection_count += 1
            # Fill remaining slots if any
            if len(chosen) < k:
                remaining = self.select_active_islands_ucb1(k - len(chosen))
                chosen.extend(remaining)
            return chosen

        # Calculate max fitness across all islands for normalization
        max_fit = max((i.highest_fitness for i in self.islands), default=1.0)
        max_fit = max_fit if max_fit > 0 else 1.0

        scores: List[Tuple[float, EvolutionaryIsland]] = []
        for island in self.islands:
            norm_reward = island.highest_fitness / max_fit
            ucb_val = norm_reward + self.c_exploration * math.sqrt((2 * math.log(N)) / island.selection_count)
            scores.append((ucb_val, island))

        scores.sort(key=lambda s: s[0], reverse=True)
        selected = [s[1] for s in scores[:k]]
        
        # Track bandit exploitation efficiency
        from src.core.telemetry_tracker import GlobalTelemetryTracker
        tracker = GlobalTelemetryTracker()
        for idx, s in enumerate(selected):
            s.selection_count += 1
            tracker.record_ucb1_decision(is_exploitation=(idx == 0))
            
        return selected

    async def execute_generator_with_self_healing(
        self,
        session: Any,
        island: EvolutionaryIsland,
        initial_script: str,
        ast_meta: CppAstMetadata,
        max_retries: int = 3
    ) -> Optional[Tuple[str, str]]:
        """
        Runs Python script in isolated subprocess.
        If it crashes, feeds traceback to LLM for up to 3 self-healing attempts.
        Returns (payload_str, winning_script) or None.
        """
        from src.core.telemetry_tracker import GlobalTelemetryTracker
        tracker = GlobalTelemetryTracker()
        current_script = initial_script

        for attempt in range(max_retries + 1):
            try:
                proc = subprocess.run(
                    [sys.executable, "-c", current_script],
                    capture_output=True,
                    text=True,
                    timeout=3.0
                )
                payload_str = proc.stdout.strip()
                
                if proc.returncode == 0 and payload_str:
                    island.last_winning_code = current_script
                    if attempt > 0:
                        tracker.record_self_heal_event()
                    return payload_str, current_script

                # Script failed or returned empty output
                err_msg = proc.stderr if proc.stderr else "Script exited 0 but produced empty stdout."
                logger.warning(f"[{island.island_id}] Self-Healing Triggered (Attempt {attempt+1}/{max_retries+1}): {err_msg[:100]}...")
                
                if attempt < max_retries:
                    healed_script = await island.llm_agent.self_heal_script(
                        session=session,
                        broken_script=current_script,
                        error_traceback=err_msg,
                        ast_meta=ast_meta,
                        n_constraint=self.n_constraint,
                        island_strategy=island.strategy_prompt,
                        input_format=self.input_format
                    )
                    if healed_script:
                        current_script = healed_script
                    else:
                        break
            except subprocess.TimeoutExpired:
                logger.warning(f"[{island.island_id}] Python script timed out (>3s). Requesting repair...")
                if attempt < max_retries:
                    healed_script = await island.llm_agent.self_heal_script(
                        session=session,
                        broken_script=current_script,
                        error_traceback="Execution timed out (>3.0 seconds). Use fast vectorized O(N) generation.",
                        ast_meta=ast_meta,
                        n_constraint=self.n_constraint,
                        island_strategy=island.strategy_prompt,
                        input_format=self.input_format
                    )
                    if healed_script:
                        current_script = healed_script
            except Exception as e:
                logger.error(f"[{island.island_id}] Subprocess execution exception: {e}")
                break

        return None

    async def process_island_generation(
        self, 
        session: Any, 
        island: EvolutionaryIsland, 
        ast_meta: CppAstMetadata, 
        comp_result: CompilationResult,
        generation: int
    ) -> Tuple[bool, Optional[ExecutionResult], Optional[str]]:
        """
        Runs one generation for an island:
        1. Context extraction & Epistemic reflection if stagnant
        2. Prompt generation
        3. Native script execution + Self-healing loop
        4. C++ sandbox execution + I/O Starvation Defense check
        5. Population update
        """
        # Epistemic Reflection Check
        if island.is_stagnant(window=3):
            logger.info(f"[{island.island_id}] Stagnation detected. Triggering Epistemic Reflection...")
            island.strategy_prompt = await island.llm_agent.reflect_strategy(
                session=session,
                stagnant_island_id=island.island_id,
                current_strategy=island.strategy_prompt,
                ast_meta=ast_meta,
                history_fitness=island.fitness_history[-3:]
            )

        elite_context = island.get_elite_pool(top_k=3)

        generated_codes = await island.llm_agent.generate_mutations(
            session=session,
            ast_meta=ast_meta,
            elite_telemetry=elite_context,
            n_constraint=self.n_constraint,
            island_strategy=island.strategy_prompt,
            input_format=self.input_format
        )
        
        if not generated_codes:
            return False, None, None

        # Execute with Self-Healing loop
        exec_res = await self.execute_generator_with_self_healing(
            session, island, generated_codes[0], ast_meta, max_retries=3
        )
        
        if not exec_res:
            return False, None, None

        payload_str, winning_code = exec_res

        # Evaluate inside C++ Sandbox
        tc = TestCase(
            id=uuid.uuid4().hex[:8],
            payload=payload_str.encode('utf-8'),
            generation=generation,
            n_constraint=self.n_constraint,
            time_limit_ms=self.sandbox.time_limit_ms
        )
        
        eval_result = self.sandbox.evaluate(comp_result, tc)

        # Update island fitness pool
        island.update_population([eval_result])

        if eval_result.is_algodos_triggered:
            logger.critical(f"🏆 ALGODOS CONFIRMED ON {island.island_id} (Peak: {eval_result.telemetry.cpu_user_time_ms}ms)!")
            return True, eval_result, winning_code

        return False, eval_result, winning_code

    def perform_soft_migration(self):
        """
        FunFuzz-inspired cross-island genetic migration policy.
        Ranks islands by peak fitness score.
        Dominant island donates top 20% elite genomes to weak islands.
        Weak islands prune bottom 30% to maintain genetic diversity.
        """
        ranked = sorted(self.islands, key=lambda i: i.highest_fitness, reverse=True)
        strong_island = ranked[0]
        weak_islands = ranked[1:]

        migrant_count = max(1, math.ceil(len(strong_island.population) * 0.20))
        migrants = strong_island.population[:migrant_count]

        for weak in weak_islands:
            weak.prune_weak(bottom_percent=0.30)
            weak.population.extend(migrants)
            weak.update_population([])  # Re-sorts population descending by fitness score

        logger.info(f"Soft Migration: Donated {migrant_count} elite genomes from {strong_island.island_id} to other islands.")