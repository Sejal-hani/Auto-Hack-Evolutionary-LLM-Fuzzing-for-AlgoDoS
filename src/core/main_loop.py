"""
CF-Fuzz Command Center & Campaign Orchestrator.

Orchestrates the complete lifecycle of the AlgoDoS discovery pipeline:
1. Ingests and parses AST Machine Vision via tree-sitter.
2. Formulates domain-specific speciation across 10 isolated evolutionary islands.
3. Coordinates 3 parallel LLM workers per generation via UCB1 Multi-Armed Bandit scheduling.
4. Executes native Generative Metaprogramming with Self-Healing syntax repair loops.
5. Measures microsecond CPU User Time inside POSIX Sandbox with I/O Starvation Defense.
6. Records granular per-generation telemetry: 10 Islands, Tokens_Used_This_Gen, Cumulative_Tokens, Status.
7. Synthesizes Explainable AI (XAI) Post-Mortem causal reports.
"""

import os
import csv
import sys
import time
import asyncio
import logging
import argparse
from pathlib import Path
from typing import Optional, List

# High-performance async HTTP client
import aiohttp

# Local imports
from src.sandbox.compiler import CppCompiler
from src.sandbox.sandbox_models import OptimizationLevel
from src.sandbox.telemetry_runner import SecureSandbox
from src.ast_analyzer.cfg_parser import AstAnalyzer
from src.evolution.multi_island_fuzzer import FuzzOrchestrator
from src.core.dataset_automator import DatasetAutomator, BenchmarkMetadata
from src.core.xai_engine import XaiPostMortemEngine
from src.core.telemetry_tracker import GlobalTelemetryTracker

# Production-grade logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("CF-Fuzz")


class FuzzSession:
    """Manages the end-to-end execution of a fuzzing campaign against a specific victim."""
    
    def __init__(self, victim_cpp_path: str, max_generations: int = 30):
        self.victim_file = Path(victim_cpp_path)
        self.max_generations = max_generations
        self.migration_interval = 3
        
        # Ingest benchmark metadata
        automator = DatasetAutomator()
        self.meta: BenchmarkMetadata = automator.parse_metadata(self.victim_file)
        
        # Output artifacts
        self.output_dir = Path("cf_fuzz_output")
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.csv_path = self.output_dir / f"telemetry_{self.victim_file.stem}_{int(time.time())}.csv"
        self.xai_engine = XaiPostMortemEngine()
        self.tracker = GlobalTelemetryTracker()

    async def execute(self) -> bool:
        """The Main Evolutionary Loop with UCB1 Bandit Scheduling & Token Accounting."""
        logger.info(f"🚀 INITIATING CF-FUZZ CAMPAIGN TARGETING: {self.victim_file.name}")
        logger.info(f"Category: {self.meta.category} | Constraint N: {self.meta.n_constraint} | Time Limit: {self.meta.time_limit_ms}ms")
        
        if not self.victim_file.exists():
            logger.error(f"Victim C++ file not found: {self.victim_file}")
            return False
            
        source_code = self.victim_file.read_text(encoding='utf-8', errors='replace')
        
        # 1. Extract AST Machine Vision
        logger.info("Parsing Abstract Syntax Tree (AST) & CFG...")
        ast_analyzer = AstAnalyzer()
        ast_meta = ast_analyzer.analyze_code(source_code)
        logger.info(f"AST Extracted: Loop Depth={ast_meta.max_loop_depth} | STLs={ast_meta.vulnerable_stls} | Recursion={ast_meta.recursive_functions}")
        
        # 2. Cryptographic Compilation Forge
        logger.info("Compiling Victim Binary (-O2 Optimization, 256MB Stack)...")
        compiler = CppCompiler()
        comp_result = compiler.compile(source_code, opt_level=OptimizationLevel.O2)
        
        if not comp_result.is_success:
            logger.critical("Compilation Failed. Is the Codeforces C++ code valid?")
            logger.error(comp_result.compiler_stderr)
            return False
            
        logger.info(f"Binary Forge Success. SHA-256: {comp_result.source_hash[:12]}")
        
        # 3. Setup Deterministic Sandbox with I/O Starvation Defense
        sandbox = SecureSandbox(time_limit_ms=self.meta.time_limit_ms, memory_limit_mb=256)
        
        # 4. Multi-Key Distributed API Configuration
        master_key = os.environ.get("GROQ_API_KEY", "MOCK_KEY_FOR_LOCAL_OFFLINE")
        island_keys = [
            os.environ.get("GROQ_API_KEY_ALPHA", master_key),
            os.environ.get("GROQ_API_KEY_BETA", master_key),
            os.environ.get("GROQ_API_KEY_GAMMA", master_key)
        ]
        
        orchestrator = FuzzOrchestrator(
            sandbox=sandbox,
            island_keys=island_keys,
            n_constraint=self.meta.n_constraint,
            input_format=self.meta.input_format
        )
        
        self.tracker.start_session()
        
        # 5. Open Real-Time CSV Logger with full 10 islands and token telemetry
        all_island_names = [isl.island_id for isl in orchestrator.islands]
        with open(self.csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([
                "Generation", "Active_Islands"
            ] + all_island_names + [
                "Status", "Target_Time_Limit_MS", "Tokens_Used_This_Gen", "Cumulative_Tokens"
            ])
            
            connector = aiohttp.TCPConnector(limit=10)
            async with aiohttp.ClientSession(connector=connector) as session:
                start_time = time.time()
                tle_triggered = False
                
                for gen in range(1, self.max_generations + 1):
                    logger.info(f"\n{'='*20} GENERATION {gen}/{self.max_generations} {'='*20}")
                    
                    # UCB1 Multi-Armed Bandit Scheduling: Select 3 active islands
                    active_islands = orchestrator.select_active_islands_ucb1(k=3)
                    island_names = [isl.island_id for isl in active_islands]
                    logger.info(f"UCB1 Selected Active Islands: {', '.join(island_names)}")
                    
                    # Concurrently evaluate active workers
                    tasks = [
                        orchestrator.process_island_generation(session, island, ast_meta, comp_result, gen)
                        for island in active_islands
                    ]
                    
                    island_results = await asyncio.gather(*tasks)
                    
                    # Compute differential token consumption for this generation
                    token_diff = self.tracker.get_generation_differential_tokens()
                    
                    # Collect peak fitness for all 10 islands
                    island_fitness_row = [round(isl.highest_fitness, 3) for isl in orchestrator.islands]
                    status = "TLE_ACHIEVED" if any(r[0] for r in island_results) else "EVOLVING"
                    
                    # Write row to CSV
                    row_data = [
                        gen, ";".join(island_names)
                    ] + island_fitness_row + [
                        status, self.meta.time_limit_ms, token_diff['gen_tokens'], token_diff['cumulative_tokens']
                    ]
                    csv_writer.writerow(row_data)
                    csv_file.flush()
                    
                    # Check for Win Condition (AlgoDoS Triggered)
                    for triggered, exec_res, winning_code in island_results:
                        if triggered and exec_res:
                            winning_island = active_islands[island_results.index((triggered, exec_res, winning_code))].island_id
                            logger.critical(f"🏆 ASYMPTOTIC ALGODOS ACHIEVED AT GENERATION {gen} BY {winning_island}! 🏆")
                            tle_triggered = True
                            
                            # Trigger Layer 6: Explainable AI Post-Mortem Engine
                            self.xai_engine.generate_explanation(
                                category=self.meta.category,
                                target_file=self.meta.filename,
                                n_constraint=self.meta.n_constraint,
                                time_limit_ms=self.meta.time_limit_ms,
                                exec_result=exec_res,
                                winning_code=winning_code,
                                ast_meta=ast_meta,
                                generation=gen,
                                island_id=winning_island
                            )
                            break
                            
                    if tle_triggered:
                        break
                        
                    # Cross-Island Soft Migration every 3 generations
                    if gen % self.migration_interval == 0 and gen != self.max_generations:
                        orchestrator.perform_soft_migration()
                
                elapsed = time.time() - start_time
                self.tracker.persist()
                logger.info("\n" + "="*50)
                logger.info(f"CAMPAIGN TERMINATED in {elapsed:.2f} seconds.")
                logger.info(f"Telemetry saved to: {self.csv_path}")
                if tle_triggered:
                    logger.info("VERDICT: VULNERABILITY CONFIRMED (Algorithm mathematically degraded).")
                else:
                    logger.info("VERDICT: ALGORITHM RESILIENT (Failed to breach time bounds).")
                logger.info("="*50 + "\n")
                
                return tle_triggered


async def run_batch_campaign():
    """Executes an unattended batch fuzzing campaign across all dataset benchmarks."""
    automator = DatasetAutomator()
    benchmarks = automator.scan_all_benchmarks()
    logger.info(f"Starting Master Campaign across {len(benchmarks)} targets...")
    
    breached = 0
    for idx, bm in enumerate(benchmarks):
        logger.info(f"\n>>> TARGET [{idx+1}/{len(benchmarks)}]: {bm.filename} ({bm.category})")
        session = FuzzSession(f"dataset/{bm.filename}", max_generations=15)
        success = await session.execute()
        if success:
            breached += 1
            
    logger.info(f"\n==========================================")
    logger.info(f"BATCH CAMPAIGN SUMMARY: {breached}/{len(benchmarks)} targets breached ({breached/max(1, len(benchmarks))*100:.2f}%)")
    logger.info(f"==========================================")


if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    parser = argparse.ArgumentParser(description="CF-Fuzz Autonomous AlgoDoS Fuzzing Engine")
    parser.add_argument("--target", type=str, default="dataset/victim_hashmap.cpp", help="Path to C++ victim file")
    parser.add_argument("--batch", action="store_true", help="Run master batch campaign across all targets in dataset/")
    parser.add_argument("--generations", type=int, default=30, help="Maximum evolutionary generations")
    args = parser.parse_args()

    if args.batch:
        asyncio.run(run_batch_campaign())
    else:
        session_runner = FuzzSession(args.target, max_generations=args.generations)
        try:
            asyncio.run(session_runner.execute())
        except KeyboardInterrupt:
            logger.warning("\nFuzzer manually halted by operator.")