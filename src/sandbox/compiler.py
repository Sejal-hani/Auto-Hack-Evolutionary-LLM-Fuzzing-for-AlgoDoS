"""
Cryptographic C++ Compiler Forge.

Handles high-throughput, thread-safe compilation of C++ source codes.
Utilizes SHA-256 hashing to memoize compilation steps across evolutionary islands.
Employs atomic POSIX operations to prevent cross-thread binary corruption.
"""

import os
import sys
import hashlib
import tempfile
import subprocess
import logging
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List

# Local imports
from .sandbox_models import OptimizationLevel

logger = logging.getLogger(__name__)

@dataclass(frozen=True, slots=True)
class CompilationResult:
    """Immutable record of a compilation attempt."""
    is_success: bool
    binary_path: Optional[Path]
    compiler_stderr: str
    source_hash: str


class CppCompiler:
    """
    Singleton-patterned compiler orchestrator.
    Manages binary caching and OS-level compilation threads.
    """
    
    def __init__(self, cache_dir: str = ".cf_fuzz_cache/binaries"):
        self.cache_path = Path(cache_dir)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        self.platform = sys.platform
        self.stack_flags = self._get_os_stack_flags()

    def _get_os_stack_flags(self) -> List[str]:
        """Injects extended stack sizes into the linker based on the OS."""
        if self.platform.startswith('linux'):
            return ["-Wl,-z,stack-size=268435456"]
        elif self.platform == 'win32':
            return ["-Wl,--stack,268435456"]
        elif self.platform == 'darwin':
            return ["-Wl,-stack_size,0x10000000"]
        return []

    def _generate_hash(self, source_code: str, opt_level: OptimizationLevel) -> str:
        """Generates a deterministic SHA-256 fingerprint."""
        hasher = hashlib.sha256()
        hasher.update(source_code.encode('utf-8'))
        hasher.update(opt_level.value.encode('utf-8'))
        hasher.update(self.platform.encode('utf-8'))
        return hasher.hexdigest()

    def compile(self, source_code: str, opt_level: OptimizationLevel = OptimizationLevel.O2) -> CompilationResult:
        """Executes the thread-safe compilation pipeline with standard fallbacks."""
        code_hash = self._generate_hash(source_code, opt_level)
        final_binary_name = f"{code_hash}.out" if self.platform != 'win32' else f"{code_hash}.exe"
        final_binary_path = self.cache_path / final_binary_name

        # Fast path: O(1) cache hit
        if final_binary_path.exists():
            return CompilationResult(
                is_success=True,
                binary_path=final_binary_path,
                compiler_stderr="",
                source_hash=code_hash
            )

        # Slow path: Compile in temp directory
        with tempfile.TemporaryDirectory(dir=self.cache_path) as tmp_dir:
            tmp_path = Path(tmp_dir)
            source_file = tmp_path / f"{code_hash}.cpp"
            tmp_binary = tmp_path / final_binary_name

            source_file.write_text(source_code, encoding='utf-8')

            standards_to_try = ["-std=c++17", "-std=c++14", "-std=c++11", "-std=c++20"]
            last_stderr = ""
            compilation_succeeded = False

            for cpp_std in standards_to_try:
                compile_cmd = [
                    "g++",
                    cpp_std,
                    opt_level.value,
                    "-fno-omit-frame-pointer", 
                    "-o", str(tmp_binary),
                    str(source_file)
                ] + self.stack_flags

                try:
                    process = subprocess.run(
                        compile_cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        timeout=15.0,
                        text=True
                    )
                    if process.returncode == 0:
                        compilation_succeeded = True
                        last_stderr = process.stderr
                        break
                    else:
                        last_stderr = process.stderr
                except subprocess.TimeoutExpired:
                    return CompilationResult(
                        is_success=False,
                        binary_path=None,
                        compiler_stderr="FATAL: Compiler Time Limit Exceeded (>15s).",
                        source_hash=code_hash
                    )
                except Exception as e:
                    last_stderr = str(e)

            if not compilation_succeeded:
                return CompilationResult(
                    is_success=False,
                    binary_path=None,
                    compiler_stderr=last_stderr,
                    source_hash=code_hash
                )

            # Atomic replace into cache
            os.replace(tmp_binary, final_binary_path)
            try:
                final_binary_path.chmod(0o755)
            except Exception:
                pass

            return CompilationResult(
                is_success=True,
                binary_path=final_binary_path,
                compiler_stderr=last_stderr,
                source_hash=code_hash
            )