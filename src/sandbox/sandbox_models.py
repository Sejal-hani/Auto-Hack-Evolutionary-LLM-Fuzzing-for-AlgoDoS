"""
Core Data Models for CF-Fuzz Sandbox.

Engineered for high-throughput concurrency. Utilizes __slots__ for memory density
and frozen dataclasses to ensure thread-safe immutability across Evolutionary Islands.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, Optional


class ExecutionStatus(Enum):
    """Strict taxonomy of C++ process exit states based on POSIX signals."""
    SUCCESS = auto()                 # Exit code 0
    COMPILE_ERROR = auto()           # Failed at g++ phase
    TIME_LIMIT_EXCEEDED = auto()     # SIGKILL via timeout (The AlgoDoS Goal)
    MEMORY_LIMIT_EXCEEDED = auto()   # SIGSEGV or OS OOM Killer
    RUNTIME_ERROR = auto()           # SIGFPE, SIGABRT, unhandled exceptions
    SYSTEM_FAILURE = auto()          # Python Sandbox internal crash


class OptimizationLevel(Enum):
    """GCC Optimization flags for baseline and resilient testing."""
    O0 = "-O0"
    O1 = "-O1"
    O2 = "-O2"
    O3 = "-O3"
    OFAST = "-Ofast"


@dataclass(frozen=True, slots=True)
class TestCase:
    """
    Represents an immutable LLM-generated payload.
    Frozen to prevent cross-island mutation bleeding during parallel evaluation.
    """
    id: str
    payload: bytes  # Stored as bytes to prevent UTF-8 overhead/corruption
    generation: int
    n_constraint: int
    
    @property
    def payload_str(self) -> str:
        """Safe decoding for LLM context injection."""
        return self.payload.decode('utf-8', errors='replace')


@dataclass(frozen=True, slots=True)
class HardwareTelemetry:
    """
    Captures OS and kernel-level metrics for mathematical fitness scoring.
    """
    wall_time_ms: float
    cpu_user_time_ms: float
    peak_memory_bytes: int
    branch_misses: Optional[int] = None
    cache_misses: Optional[int] = None
    
    @property
    def peak_memory_mb(self) -> float:
        return self.peak_memory_bytes / (1024 * 1024)

    @property
    def fitness_score(self) -> float:
        """
        Calculates the asymptotic pressure.
        Prioritizes CPU User Time over Wall Time to ignore OS background noise.
        """
        base_score = self.cpu_user_time_ms
        if self.cache_misses:
            # Heavily penalize cache thrashing (O(N^2) memory access patterns)
            base_score += (self.cache_misses * 0.0001) 
        return round(base_score, 4)


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    """
    The deterministic output of a Sandbox run.
    """
    test_case_id: str
    status: ExecutionStatus
    exit_code: int
    telemetry: HardwareTelemetry
    stdout: bytes
    stderr: bytes
    
    @property
    def is_algodos_triggered(self) -> bool:
        """True if the fuzzer successfully broke the algorithm's time bounds."""
        return self.status == ExecutionStatus.TIME_LIMIT_EXCEEDED

    def get_safe_stderr(self) -> str:
        """
        C++ segfaults often spit binary garbage to stderr. 
        We use 'replace' to prevent Python's UnicodeDecodeError from crashing the Fuzzer.
        """
        return self.stderr.decode('utf-8', errors='replace')