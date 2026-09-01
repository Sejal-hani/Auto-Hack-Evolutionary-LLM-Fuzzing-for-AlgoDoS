"""
OS-Level Execution Engine & Hardware Telemetry Runner.

Executes compiled C++ binaries within a strictly enforced OS container.
Utilizes POSIX resource limits (RLIMIT) on Linux to prevent fork bombs and OOM crashes.
Extracts pure CPU User Time via `rusage` to eliminate OS background noise from fitness scoring.
Features the I/O Starvation Defense filter to eliminate false-positive timeouts.
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
    Includes I/O Starvation Defense to filter unread stdin false positives.
    """

    def __init__(self, time_limit_ms: int = 2000, memory_limit_mb: int = 256):
        self.time_limit_ms = time_limit_ms
        self.time_limit_sec = max(1, time_limit_ms // 1000)
        self.memory_limit_bytes = memory_limit_mb * 1024 * 1024

    def _set_linux_limits(self):
        """
        Executed in child process before exec.
        Cages the C++ binary at the Linux Kernel level.
        """
        if not LINUX_MODE:
            return

        # 1. Hard lock Virtual Memory (RAM)
        resource.setrlimit(resource.RLIMIT_AS, (self.memory_limit_bytes, self.memory_limit_bytes))
        
        # 2. Hard lock CPU Time (1s grace period for Python timeout handler)
        cpu_limit = self.time_limit_sec + 1
        resource.setrlimit(resource.RLIMIT_CPU, (cpu_limit, cpu_limit))
        
        # 3. Prevent Fork Bombs
        resource.setrlimit(resource.RLIMIT_NPROC, (0, 0))

    def evaluate(self, comp_result: CompilationResult, test_case: TestCase) -> ExecutionResult:
        """
        Executes the binary with the LLM's payload, tracks telemetry, and classifies exit state.
        Enforces I/O Starvation Defense on timeouts.
        """
        if not comp_result.is_success or not comp_result.binary_path:
            return self._build_fail_result(test_case, ExecutionStatus.COMPILE_ERROR, b"Compilation failed prior to execution.")

        binary_cmd = [str(comp_result.binary_path)]
        effective_limit_ms = test_case.time_limit_ms if hasattr(test_case, 'time_limit_ms') and test_case.time_limit_ms else self.time_limit_ms
        
        usage_start = None
        if LINUX_MODE:
            usage_start = resource.getrusage(resource.RUSAGE_CHILDREN)
            
        start_wall_time = time.perf_counter()
        
        try:
            process = subprocess.Popen(
                binary_cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=self._set_linux_limits if LINUX_MODE else None,
            )

            stdout_data, stderr_data = process.communicate(
                input=test_case.payload, 
                timeout=(effective_limit_ms / 1000.0)
            )
            
            end_wall_time = time.perf_counter()
            exit_code = process.returncode

            wall_time_ms = (end_wall_time - start_wall_time) * 1000.0
            cpu_user_ms, peak_mem_bytes = self._extract_telemetry(usage_start, wall_time_ms)

            status = self._classify_exit_code(exit_code)

            telemetry = HardwareTelemetry(
                wall_time_ms=round(wall_time_ms, 2),
                cpu_user_time_ms=round(cpu_user_ms, 2),
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
            # Handle Timeout - Apply I/O Starvation Defense
            try:
                process.kill()
                stdout_data, stderr_data = process.communicate()
            except Exception:
                stdout_data, stderr_data = b"", b""

            wall_time_ms = float(effective_limit_ms)
            cpu_user_ms, peak_mem_bytes = self._extract_telemetry(usage_start, wall_time_ms)

            # I/O Starvation Defense Filter:
            # If CPU user time is < 10% of time limit, the process was idling on cin/scanf
            starvation_threshold = 0.10 * effective_limit_ms
            if cpu_user_ms < starvation_threshold:
                logger.warning(
                    f"⚠️ I/O Starvation Intercepted on payload {test_case.id}: "
                    f"CPU User Time {cpu_user_ms:.2f}ms < {starvation_threshold:.2f}ms threshold. Discarding false-positive."
                )
                try:
                    from src.core.telemetry_tracker import GlobalTelemetryTracker
                    GlobalTelemetryTracker().record_io_starvation()
                except Exception:
                    pass
                telemetry = HardwareTelemetry(
                    wall_time_ms=wall_time_ms,
                    cpu_user_time_ms=round(cpu_user_ms, 2),
                    peak_memory_bytes=peak_mem_bytes
                )
                return ExecutionResult(
                    test_case_id=test_case.id,
                    status=ExecutionStatus.RUNTIME_ERROR,
                    exit_code=-signal.SIGKILL if hasattr(signal, 'SIGKILL') else -9,
                    telemetry=telemetry,
                    stdout=stdout_data,
                    stderr=b"I/O Starvation Anomaly: Premature EOF on input stream."
                )

            # Verified genuine AlgoDoS
            telemetry = HardwareTelemetry(
                wall_time_ms=wall_time_ms,
                cpu_user_time_ms=round(cpu_user_ms if cpu_user_ms > 0 else wall_time_ms, 2),
                peak_memory_bytes=peak_mem_bytes
            )
            return ExecutionResult(
                test_case_id=test_case.id,
                status=ExecutionStatus.TIME_LIMIT_EXCEEDED,
                exit_code=-signal.SIGKILL if hasattr(signal, 'SIGKILL') else -9,
                telemetry=telemetry,
                stdout=stdout_data,
                stderr=stderr_data
            )
            
        except Exception as e:
            logger.error(f"Sandbox crash during execution: {e}")
            return self._build_fail_result(test_case, ExecutionStatus.SYSTEM_FAILURE, str(e).encode())

    def _extract_telemetry(self, usage_start, wall_time_ms: float) -> Tuple[float, int]:
        """Calculates precise CPU user time and peak memory."""
        if LINUX_MODE and usage_start is not None:
            usage_end = resource.getrusage(resource.RUSAGE_CHILDREN)
            cpu_user_ms = (usage_end.ru_utime - usage_start.ru_utime) * 1000.0
            peak_mem_bytes = usage_end.ru_maxrss * 1024 
            cpu_user_ms = cpu_user_ms if cpu_user_ms > 0 else wall_time_ms
            return round(cpu_user_ms, 3), peak_mem_bytes
        else:
            # Fallback estimation for Windows/Mac
            return round(wall_time_ms, 3), 0

    def _classify_exit_code(self, exit_code: int) -> ExecutionStatus:
        """Maps POSIX exit codes to Codeforces-style verdicts."""
        if exit_code == 0:
            return ExecutionStatus.SUCCESS
        elif exit_code in (-signal.SIGSEGV, 139) if hasattr(signal, 'SIGSEGV') else exit_code == 139:
            return ExecutionStatus.MEMORY_LIMIT_EXCEEDED
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