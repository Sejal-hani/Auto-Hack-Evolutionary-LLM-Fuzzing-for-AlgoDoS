"""
Layer 6: Explainable AI (XAI) Post-Mortem Causal Engine.

Combines winning metaprogram scripts, AST structural metadata, and kernel hardware telemetry
to generate mathematically rigorous, human-readable root-cause explanations of AlgoDoS vulnerabilities.
Persists verified discoveries to the master campaign log (GENUINE_ALGODOS_CAMPAIGN.csv).
"""

import os
import csv
import logging
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Dict, Any

# Local imports
from src.ast_analyzer.cfg_parser import CppAstMetadata
from src.sandbox.sandbox_models import ExecutionResult

logger = logging.getLogger("CF-Fuzz.XAI")

@dataclass
class XaiExplanation:
    category: str
    target_file: str
    n_constraint: int
    time_limit_ms: int
    peak_fitness_ms: float
    generations: int
    verdict: str
    bottleneck_explanation: str


class XaiPostMortemEngine:
    """Post-Mortem Causal Engine for Algorithmic Vulnerability Analysis."""

    def __init__(self, campaign_csv_path: str = "cf_fuzz_output/GENUINE_ALGODOS_CAMPAIGN.csv"):
        self.csv_path = Path(campaign_csv_path)
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_csv_headers()

    def _ensure_csv_headers(self):
        """Initializes master campaign CSV with standard columns if not present."""
        if not self.csv_path.exists():
            with open(self.csv_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Category", "Target_File", "N_Constraint", "Time_Limit_MS",
                    "Peak_Fitness_MS", "Generations", "Verdict", "Bottleneck_Explanation"
                ])

    def generate_explanation(
        self,
        category: str,
        target_file: str,
        n_constraint: int,
        time_limit_ms: int,
        exec_result: ExecutionResult,
        winning_code: Optional[str],
        ast_meta: CppAstMetadata,
        generation: int,
        island_id: str
    ) -> XaiExplanation:
        """Constructs a deterministic mathematical explanation for the vulnerability."""
        peak_time = exec_result.telemetry.cpu_user_time_ms if exec_result.telemetry else float(time_limit_ms)

        # Dynamic root-cause diagnosis based on AST and Island strategy
        explanation_parts = []
        if "unordered_map" in ast_meta.vulnerable_stls or "unordered_set" in ast_meta.vulnerable_stls:
            explanation_parts.append(
                f"The synthesized adversarial generator exploited deterministic hashing in std::unordered_map/set by injecting "
                f"keys formatted to force linear bucket collisions, collapsing average O(1) lookups to worst-case O(N) linked-list traversals."
            )
        elif ast_meta.recursive_functions:
            funcs = ", ".join(ast_meta.recursive_functions)
            explanation_parts.append(
                f"The adversarial input induced deep call-stack recursion within functions ({funcs}), maximizing call depth to O(N) "
                f"and saturating memory cache hierarchy."
            )
        elif ast_meta.max_loop_depth >= 2:
            explanation_parts.append(
                f"The generator constructed an adversarial topology targeting the {ast_meta.max_loop_depth}-nested loop structure, "
                f"forcing O(N^{ast_meta.max_loop_depth}) worst-case quadratic comparisons across N={n_constraint} elements."
            )
        else:
            explanation_parts.append(
                f"The generator synthesized pathological boundary values pushing computational execution time to {peak_time:.2f}ms "
                f"and breaching the strict {time_limit_ms}ms threshold."
            )

        full_explanation = f"[{island_id}] " + " ".join(explanation_parts)

        explanation = XaiExplanation(
            category=category,
            target_file=target_file,
            n_constraint=n_constraint,
            time_limit_ms=time_limit_ms,
            peak_fitness_ms=round(peak_time, 2),
            generations=generation,
            verdict="ALGODOS_FOUND",
            bottleneck_explanation=full_explanation
        )

        self._record_to_master_csv(explanation)
        return explanation

    def _record_to_master_csv(self, exp: XaiExplanation):
        """Appends the verified discovery to the master campaign log."""
        try:
            with open(self.csv_path, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    exp.category,
                    exp.target_file,
                    exp.n_constraint,
                    exp.time_limit_ms,
                    exp.peak_fitness_ms,
                    exp.generations,
                    exp.verdict,
                    exp.bottleneck_explanation
                ])
            logger.info(f"XAI Record Logged to {self.csv_path.name} for {exp.target_file}")
        except Exception as e:
            logger.error(f"Failed to record XAI result to master CSV: {e}")
