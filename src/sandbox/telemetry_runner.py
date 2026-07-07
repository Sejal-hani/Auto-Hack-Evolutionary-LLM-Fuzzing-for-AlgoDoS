"""
OS-Level Execution Engine & Hardware Telemetry Spy.

Executes compiled C++ binaries within a strictly enforced OS container.
Utilizes POSIX resource limits (RLIMIT) on Linux to prevent fork bombs and OOM crashes.
Extracts pure CPU User Time via `rusage` to eliminate OS background noise from fitness scoring.
"""

import os
import sys
import time
import signal
import logging
import subprocess
from pathlib import Path
from typing import Optional, Tuple

# Local imports
from .sandbox_models import ExecutionResult, ExecutionStatus, HardwareTelemetry, TestCase
from .compiler import CompilationResult

logger = logging.getLogger(__name__)

# Try to import Linux-specific resource limits for kernel-level sandboxing
try:
    import resource
    LINUX_MODE = True
except ImportError:
    import psutil
    LINUX_MODE = False
    logger.warning("POSIX `resource` module not found. Falling back to psutil (Windows/Mac mode).")


class SecureSandbox:
    """
    The Isolated Execution Environment.
    Evaluates mutated payloads against the compiled C++ AlgoDoS target.
    """

    def __init__(self, time_limit_ms: int = 2000, memory_limit_mb: int = 256):
        self.time_limit_ms = time_limit_ms
        self.time_limit_sec = max(1, time_limit_ms // 1000) # For OS soft-kills
        self.memory_limit_bytes = memory_limit_mb * 1024 * 1024

    def _set_linux_limits(self):
        """
        Executed in the child process immediately after os.fork() and before os.exec().
        Cages the C++ binary at the Linux Kernel level.
        """
        if not LINUX_MODE:
            return

        # 1. Hard lock the Virtual Memory (RAM)
        # If the C++ code creates an infinite vector, the OS intercepts the malloc and throws SIGSEGV.
        resource.setrlimit(resource.RLIMIT_AS, (self.memory_limit_bytes, self.memory_limit_bytes))
        
        # 2. Hard lock the CPU Time 
        # If it enters an infinite while-loop, the OS sends SIGKILL. 
        # We add 1 second grace period to allow our Python timeout to catch it gracefully first.
        cpu_limit = self.time_limit_sec + 1
        resource.setrlimit(resource.RLIMIT_CPU, (cpu_limit, cpu_limit))
        
        # 3. Prevent Fork Bombs (Malicious C++ calling system("fork()"))
        resource.setrlimit(resource.RLIMIT_NPROC, (0, 0))

    def evaluate(self, comp_result: CompilationResult, test_case: TestCase) -> ExecutionResult:
        """
        Executes the binary with the LLM's payload, tracks telemetry, and classifies the exit state.
        """
        if not comp_result.is_success or not comp_result.binary_path:
            return self._build_fail_result(test_case, ExecutionStatus.COMPILE_ERROR, b"Compilation failed prior to execution.")

        binary_cmd = [str(comp_result.binary_path)]
        
        # Pre-execution hooks for rusage tracking
        if LINUX_MODE:
            usage_start = resource.getrusage(resource.RUSAGE_CHILDREN)
            
        start_wall_time = time.perf_counter()
        
        try:
            # Launch the C++ binary
            # We use preexec_fn to inject the OS limits right before execution.
            process = subprocess.Popen(
                binary_cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=self._set_linux_limits if LINUX_MODE else None,
            )

            # Inject the LLM's mutated array payload via standard input
            # communicate() handles buffer deadlocks automatically.
            stdout_data, stderr_data = process.communicate(
                input=test_case.payload, 
                timeout=(self.time_limit_ms / 1000.0)
            )
            
            end_wall_time = time.perf_counter()
            exit_code = process.returncode

            # Telemetry Extraction (The "Quant" Math)
            wall_time_ms = (end_wall_time - start_wall_time) * 1000
            cpu_user_ms, peak_mem_bytes = self._extract_telemetry(usage_start if LINUX_MODE else None, wall_time_ms, process)

            # Exit Status Classification
            status = self._classify_exit_code(exit_code)

            telemetry = HardwareTelemetry(
                wall_time_ms=wall_time_ms,
                cpu_user_time_ms=cpu_user_ms,
                peak_memory_bytes=peak_mem_bytes,
            )

            return ExecutionResult(
                test_case_id=test_case.id,
                status=status,
                exit_code=exit_code,
                telemetry=telemetry,
                stdout=stdout_data,
                stderr=stderr_data
            )

        except subprocess.TimeoutExpired:
            # THE ULTIMATE WIN CONDITION: ALGODOS TRIGGERED
            process.kill()
            stdout_data, stderr_data = process.communicate()
            
            telemetry = HardwareTelemetry(
                wall_time_ms=float(self.time_limit_ms),
                cpu_user_time_ms=float(self.time_limit_ms), # Assume maxed out CPU
                peak_memory_bytes=0 # Irrelevant on TLE
            )
            
            return ExecutionResult(
                test_case_id=test_case.id,
                status=ExecutionStatus.TIME_LIMIT_EXCEEDED,
                # exit_code=-signal.SIGKILL, linux one i dont have it
                exit_code=-9,
                telemetry=telemetry,
                stdout=stdout_data,
                stderr=stderr_data
            )
            
        except Exception as e:
            logger.error(f"Sandbox crash during execution: {e}")
            return self._build_fail_result(test_case, ExecutionStatus.SYSTEM_FAILURE, str(e).encode())

    def _extract_telemetry(self, usage_start, wall_time_ms: float, process: subprocess.Popen) -> Tuple[float, int]:
        """Calculates precise CPU time and memory."""
        if LINUX_MODE and usage_start:
            # resource.RUSAGE_CHILDREN accurately tracks the dead C++ child process
            usage_end = resource.getrusage(resource.RUSAGE_CHILDREN)
            cpu_user_ms = (usage_end.ru_utime - usage_start.ru_utime) * 1000
            
            # ru_maxrss is in Kilobytes on Linux, convert to Bytes
            peak_mem_bytes = usage_end.ru_maxrss * 1024 
            
            # Fallback: if CP code runs too fast, OS might register 0ms CPU time. Use wall_time instead.
            cpu_user_ms = cpu_user_ms if cpu_user_ms > 0 else wall_time_ms
            return round(cpu_user_ms, 3), peak_mem_bytes
        else:
            # Windows/Mac Fallback
            return round(wall_time_ms, 3), 0

    def _classify_exit_code(self, exit_code: int) -> ExecutionStatus:
        """Maps POSIX exit codes to Codeforces-style verdicts."""
        if exit_code == 0:
            return ExecutionStatus.SUCCESS
        elif exit_code == -signal.SIGSEGV or exit_code == 139:
            return ExecutionStatus.MEMORY_LIMIT_EXCEEDED
        elif exit_code == -signal.SIGABRT or exit_code == -signal.SIGFPE:
            return ExecutionStatus.RUNTIME_ERROR
        return ExecutionStatus.RUNTIME_ERROR

    def _build_fail_result(self, test_case: TestCase, status: ExecutionStatus, stderr: bytes) -> ExecutionResult:
        return ExecutionResult(
            test_case_id=test_case.id,
            status=status,
            exit_code=-1,
            telemetry=HardwareTelemetry(0.0, 0.0, 0),
            stdout=b"",
            stderr=stderr
        )