"""
Dataset Automator & Benchmark Normalizer for CF-Fuzz.

Ingests raw C++ problem sources and normalizes them into immutable, standardized benchmarks
annotated with formal metadata headers:
- [TIME_LIMIT_MS]: int (execution timeout ceiling)
- [MEMORY_LIMIT_MB]: int (RAM limit)
- [N_CONSTRAINT]: int (upper bound on input size)
- [INPUT_FORMAT]: str (formal structure specification)
"""

import os
import re
import logging
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Dict, Any, List

logger = logging.getLogger("CF-Fuzz.DatasetAutomator")

@dataclass
class BenchmarkMetadata:
    filename: str
    category: str
    n_constraint: int
    time_limit_ms: int
    memory_limit_mb: int
    input_format: str
    source_code: str


class DatasetAutomator:
    """Normalizes, validates, and annotates benchmark victim files."""

    def __init__(self, dataset_dir: str = "dataset"):
        self.dataset_dir = Path(dataset_dir)
        self.dataset_dir.mkdir(exist_ok=True, parents=True)

    def parse_metadata(self, file_path: Path) -> BenchmarkMetadata:
        """Parses annotated metadata headers from a C++ victim file with flexible ordering."""
        content = file_path.read_text(encoding="utf-8", errors="replace")

        # Independent regex search for all supported headers
        n_match = re.search(r"//\s*\[N_CONSTRAINT\]:\s*(\d+)", content)
        tl_match = re.search(r"//\s*\[TIME_LIMIT_MS\]:\s*(\d+)", content)
        mem_match = re.search(r"//\s*\[MEMORY_LIMIT_MB\]:\s*(\d+)", content)
        fmt_match = re.search(r"//\s*\[INPUT_FORMAT\]:\s*(.+)", content)

        n_constraint = int(n_match.group(1)) if n_match else 100000
        time_limit_ms = int(tl_match.group(1)) if tl_match else 2000
        memory_limit_mb = int(mem_match.group(1)) if mem_match else 256
        input_format = fmt_match.group(1).strip() if fmt_match else "First line contains N, followed by N space-separated integers."

        # Extract category from filename e.g. victim_002_dp.cpp -> DYNAMIC PROGRAMMING
        stem = file_path.stem.lower()
        if "_dp" in stem or "dp" in stem:
            category = "DYNAMIC PROGRAMMING"
        elif "_graph" in stem or "graph" in stem or "bfs" in stem or "dfs" in stem:
            category = "GRAPH THEORY"
        elif "_greedy" in stem or "greedy" in stem or "sorting" in stem:
            category = "GREEDY"
        elif "_math" in stem or "math" in stem or "number" in stem:
            category = "MATHEMATICS"
        elif "_ds" in stem or "treap" in stem or "set" in stem:
            category = "DATA STRUCTURES"
        elif "_string" in stem or "string" in stem:
            category = "STRING PROCESSING"
        elif "_bitmask" in stem:
            category = "BITMASK"
        elif "_geometry" in stem:
            category = "COMPUTATIONAL GEOMETRY"
        elif "_adhoc" in stem or "_constructive" in stem:
            category = "CONSTRUCTIVE"
        elif "_bruteforce" in stem:
            category = "BRUTEFORCE"
        elif "_linearalgebra" in stem:
            category = "LINEAR BASIS"
        else:
            category = "GENERAL"

        return BenchmarkMetadata(
            filename=file_path.name,
            category=category,
            n_constraint=n_constraint,
            time_limit_ms=time_limit_ms,
            memory_limit_mb=memory_limit_mb,
            input_format=input_format,
            source_code=content
        )

    def annotate_file(self, file_path: Path, n_constraint: int, time_limit_ms: int, memory_limit_mb: int, input_format: str):
        """Standardizes metadata headers at the top of a victim C++ file."""
        content = file_path.read_text(encoding="utf-8", errors="replace")
        
        # Clean existing header lines
        clean_lines = [line for line in content.splitlines() if not line.strip().startswith("// [")]
        clean_content = "\n".join(clean_lines).lstrip()
        
        header = (
            f"// [TIME_LIMIT_MS]: {time_limit_ms}\n"
            f"// [MEMORY_LIMIT_MB]: {memory_limit_mb}\n"
            f"// [N_CONSTRAINT]: {n_constraint}\n"
            f"// [INPUT_FORMAT]: {input_format}\n\n"
        )
        
        file_path.write_text(header + clean_content, encoding="utf-8")
        logger.info(f"Standardized {file_path.name} headers.")

    def scan_all_benchmarks(self) -> List[BenchmarkMetadata]:
        """Discovers and parses all C++ benchmarks in the dataset directory."""
        cpp_files = sorted(list(self.dataset_dir.glob("*.cpp")))
        return [self.parse_metadata(f) for f in cpp_files]


if __name__ == "__main__":
    automator = DatasetAutomator()
    benchmarks = automator.scan_all_benchmarks()
    print(f"Discovered {len(benchmarks)} benchmark files in dataset/")
    for bm in benchmarks[:5]:
        print(f" - {bm.filename} | Category: {bm.category} | N: {bm.n_constraint} | TL: {bm.time_limit_ms}ms | Mem: {bm.memory_limit_mb}MB | Format: {bm.input_format}")
