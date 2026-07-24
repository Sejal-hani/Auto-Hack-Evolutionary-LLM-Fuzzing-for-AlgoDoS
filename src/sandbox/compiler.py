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
    Manages the binary cache and OS-level compilation threads.
    """
    
    def __init__(self, cache_dir: str = ".cf_fuzz_cache/binaries"):
        self.cache_path = Path(cache_dir)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        # Determine OS-specific linker flags for Codeforces simulation
        # Codeforces grants a 256MB stack to prevent deep recursion SIGSEGVs.
        # We must mirror this to accurately test Graph/Tree algorithms.
        self.platform = sys.platform
        self.stack_flags = self._get_os_stack_flags()

    def _get_os_stack_flags(self) -> List[str]:
        """Injects massive stack sizes into the linker based on the OS."""
        if self.platform.startswith('linux'):
            # Linux ld flag for 256MB stack
            return ["-Wl,-z,stack-size=268435456"]
        elif self.platform == 'win32':
            # MinGW/Windows flag for 256MB stack
            return ["-Wl,--stack,268435456"]
        elif self.platform == 'darwin':
            # macOS clang flag
            return ["-Wl,-stack_size,0x10000000"]
        return []

    def _generate_hash(self, source_code: str, opt_level: OptimizationLevel) -> str:
        """
        Generates a deterministic SHA-256 fingerprint of the payload.
        Ensures we never compile the exact same mutation twice.
        """
        hasher = hashlib.sha256()
        hasher.update(source_code.encode('utf-8'))
        hasher.update(opt_level.value.encode('utf-8'))
        hasher.update(self.platform.encode('utf-8'))
        return hasher.hexdigest()

    def compile(self, source_code: str, opt_level: OptimizationLevel = OptimizationLevel.O2) -> CompilationResult:
        """
        Executes the thread-safe compilation pipeline.
        """
        code_hash = self._generate_hash(source_code, opt_level)
        final_binary_name = f"{code_hash}.out" if self.platform != 'win32' else f"{code_hash}.exe"
        final_binary_path = self.cache_path / final_binary_name

        # FAST PATH: Binary already exists (O(1) Cache Hit)
        if final_binary_path.exists():
            return CompilationResult(
                is_success=True,
                binary_path=final_binary_path,
                compiler_stderr="",
                source_hash=code_hash
            )

        # SLOW PATH: We must compile.
        # Use a secure temporary directory to prevent namespace collisions.
        with tempfile.TemporaryDirectory(dir=self.cache_path) as tmp_dir:
            tmp_path = Path(tmp_dir)
            source_file = tmp_path / f"{code_hash}.cpp"
            tmp_binary = tmp_path / final_binary_name

            # Write the C++ code to disk safely
            source_file.write_text(source_code, encoding='utf-8')

            # Build the GCC/Clang command
            # -std=c++20: Match modern Codeforces standards
            # -fno-omit-frame-pointer: Leave hooks for OS-level CPU profiling
            compile_cmd = [
                "g++",
                "-std=c++17",
                opt_level.value,
                "-fno-omit-frame-pointer", 
                "-o", str(tmp_binary),
                str(source_file)
            ] + self.stack_flags

            try:
                # Execute g++ as an isolated subprocess
                process = subprocess.run(
                    compile_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=15.0, # 15 second max compilation time
                    text=True
                )

                if process.returncode != 0:
                    return CompilationResult(
                        is_success=False,
                        binary_path=None,
                        compiler_stderr=process.stderr,
                        source_hash=code_hash
                    )

                # ATOMIC RENAME (The Thread-Safe Magic)
                # By renaming the temporary binary to the final cache path,
                # we guarantee that if two threads compile the same file simultaneously,
                # only a fully formed, uncorrupted binary is ever exposed to the sandbox.
                # os.replace is atomic on POSIX systems.
                os.replace(tmp_binary, final_binary_path)

                # Set executable permissions (crucial for Linux/macOS)
                final_binary_path.chmod(0o755)

                return CompilationResult(
                    is_success=True,
                    binary_path=final_binary_path,
                    compiler_stderr=process.stderr,
                    source_hash=code_hash
                )

            except subprocess.TimeoutExpired:
                return CompilationResult(
                    is_success=False,
                    binary_path=None,
                    compiler_stderr="FATAL: Compiler Time Limit Exceeded (>15s).",
                    source_hash=code_hash
                )
            except Exception as e:
                logger.error(f"Sandbox Internal Error during compilation: {e}")
                return CompilationResult(
                    is_success=False,
                    binary_path=None,
                    compiler_stderr=f"SYSTEM ERROR: {str(e)}",
                    source_hash=code_hash
                )