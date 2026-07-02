"""
CF-Fuzz Command Center.

Orchestrates the complete lifecycle of the AlgoDoS discovery pipeline.
Wires together AST Static Analysis, OS Sandboxing, and Multi-Island LLM Evolution.
Implements highly concurrent execution loops, multi-key API routing, 
and real-time CSV telemetry persistence.
"""

import os
import csv
import sys
import time
import asyncio
import logging
from pathlib import Path

# High-performance async HTTP client
import aiohttp

# Local imports (The arsenal)
from src.sandbox.compiler import CppCompiler
from src.sandbox.sandbox_models import OptimizationLevel
from src.sandbox.telemetry_runner import SecureSandbox
from src.ast_analyzer.cfg_parser import AstAnalyzer
from src.evolution.multi_island_fuzzer import FuzzOrchestrator

# Setup production-grade terminal logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("CF-Fuzz")

class FuzzSession:
    """Manages the end-to-end execution of a fuzzing campaign against a specific victim."""
    
    def __init__(self, victim_cpp_path: str, n_constraint: int = 5000):
        self.victim_file = Path(victim_cpp_path)
        self.n_constraint = n_constraint
        self.max_generations = 30
        self.migration_interval = 3
        
        # Output artifacts directory
        self.output_dir = Path("cf_fuzz_output")
        self.output_dir.mkdir(exist_ok=True)
        self.csv_path = self.output_dir / f"telemetry_{self.victim_file.stem}_{int(time.time())}.csv"

    async def execute(self):
        """The Main Fuzzing Loop (The Matrix Run)."""
        logger.info(f"🚀 INITIATING CF-FUZZ CAMPAIGN TARGETING: {self.victim_file.name}")
        
        # 1. Read Victim Source
        if not self.victim_file.exists():
            logger.error(f"Victim C++ file not found: {self.victim_file}")
            sys.exit(1)
        source_code = self.victim_file.read_text(encoding='utf-8')
        
        # 2. Extract AST Machine Vision
        logger.info("Parsing Abstract Syntax Tree (AST) & CFG...")
        ast_analyzer = AstAnalyzer()
        ast_meta = ast_analyzer.analyze_code(source_code)
        logger.info(f"AST Metadata Extracted: Max Loop Depth: {ast_meta.max_loop_depth} | Vulnerable STLs: {ast_meta.vulnerable_stls}")
        
        # 3. Cryptographic Compilation
        logger.info("Compiling Victim Binary (-O2 Optimization)...")
        compiler = CppCompiler()
        comp_result = compiler.compile(source_code, opt_level=OptimizationLevel.O2)
        
        if not comp_result.is_success:
            logger.critical("Compilation Failed. Is the Codeforces C++ code valid?")
            logger.error(comp_result.compiler_stderr)
            sys.exit(1)
            
        logger.info(f"Binary Forge Success. SHA-256: {comp_result.source_hash[:12]}")
        
        # 4. Initialize Multi-Key Engines
        sandbox = SecureSandbox(time_limit_ms=2000, memory_limit_mb=256)
        
        # Smart API Key Routing (Allows fallback to a single master key if 3 aren't available yet)
        master_key = os.environ.get("GROQ_API_KEY")
        island_keys = [
            os.environ.get("GROQ_API_KEY_ALPHA", master_key),
            os.environ.get("GROQ_API_KEY_BETA", master_key),
            os.environ.get("GROQ_API_KEY_GAMMA", master_key)
        ]
        
        if not all(island_keys):
            logger.error("CRITICAL: API keys missing! Set GROQ_API_KEY, or set ALPHA/BETA/GAMMA keys individually.")
            sys.exit(1)
            
        orchestrator = FuzzOrchestrator(sandbox, island_keys, self.n_constraint)
        
        # 5. Open Real-Time CSV Logger
        with open(self.csv_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Generation", "Island_Alpha_Peak_MS", "Island_Beta_Peak_MS", "Island_Gamma_Peak_MS", "Status"])
            
            # Connection pooling for high-throughput LLM API calls
            connector = aiohttp.TCPConnector(limit=10)
            async with aiohttp.ClientSession(connector=connector) as session:
                
                start_time = time.time()
                tle_triggered = False
                
                # --- THE MATRIX LOOP ---
                for gen in range(1, self.max_generations + 1):
                    logger.info(f"\n{'='*20} GENERATION {gen}/{self.max_generations} {'='*20}")
                    
                    # Concurrently execute all 3 islands (Metaprogramming generation)
                    tasks = [
                        orchestrator.process_island_generation(session, island, ast_meta, comp_result, gen)
                        for island in orchestrator.islands
                    ]
                    
                    # Wait for all 3 LLM calls + Python Executions + Sandboxes to finish
                    island_results = await asyncio.gather(*tasks)
                    
                    # Extract the peak fitness (CPU ms) for graphing
                    alpha_ms = orchestrator.islands[0].highest_fitness
                    beta_ms = orchestrator.islands[1].highest_fitness
                    gamma_ms = orchestrator.islands[2].highest_fitness
                    
                    # Write to CSV and flush to disk immediately
                    status = "TLE_ACHIEVED" if any(island_results) else "EVOLVING"
                    csv_writer.writerow([gen, alpha_ms, beta_ms, gamma_ms, status])
                    csv_file.flush()
                    
                    # Check for Ultimate Win Condition
                    if any(island_results):
                        logger.critical(f"🏆 ASYMPTOTIC ALGODOS ACHIEVED AT GENERATION {gen}! 🏆")
                        tle_triggered = True
                        break
                        
                    # Execute Cross-Island Soft Migration
                    if gen % self.migration_interval == 0 and gen != self.max_generations:
                        orchestrator.perform_soft_migration()
                
                # Post-Run Summary
                elapsed = time.time() - start_time
                logger.info("\n" + "="*50)
                logger.info("CAMPAIGN TERMINATED.")
                logger.info(f"Total Wall Time: {elapsed:.2f} seconds")
                logger.info(f"Telemetry saved to: {self.csv_path}")
                if tle_triggered:
                    logger.info("VERDICT: VULNERABILITY CONFIRMED (Algorithm mathematically degraded).")
                else:
                    logger.info("VERDICT: ALGORITHM RESILIENT (Failed to exceed 2000ms limit).")
                logger.info("="*50 + "\n")


if __name__ == "__main__":
    # Ensure asyncio uses the optimal event loop policy based on OS
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    # Standard Execution Hook
    target_cpp = "dataset/victim_hashmap.cpp" 
    
    # We are using 5000 as constraint because the LLM writes a Python loop now!
    session_runner = FuzzSession(target_cpp, n_constraint=5000)
    
    try:
        asyncio.run(session_runner.execute())
    except KeyboardInterrupt:
        logger.warning("\nFuzzer manually halted by operator. CSV telemetry is safe.")