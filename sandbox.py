"""
sandbox.py
Person A's Phase 1 deliverable.

Takes a piece of C++ source code and a text input, compiles it,
runs it, and returns how long it took (in milliseconds) — or tells
you it timed out (TLE).

Why this file matters: everything later (the LLM fuzzer) depends on
this function being 100% reliable. If this crashes, the whole
overnight run dies. So every step here has a guard around it.
"""

import subprocess
import tempfile
import time
import os
import shutil

# ---- CONFIG ----
TIMEOUT_SECONDS = 3.0      # Kill switch: if the C++ program runs longer than
                            # this, we assume it's stuck (infinite loop) and
                            # kill it instead of letting it hang forever.
NUM_RUNS = 3                # We run the same input 3 times and keep the
                            # MINIMUM time. This is the "noise reduction"
                            # failsafe -- your laptop has background processes
                            # (antivirus, browser, etc.) that randomly slow
                            # things down. The minimum of 3 runs is much
                            # closer to the program's true speed than any
                            # single run.


class SandboxResult:
    """
    A small container so the rest of the code doesn't have to deal with
    raw tuples or dictionaries. Check `result.status` first, always.
    """
    def __init__(self, status, time_ms=None, error_message=None):
        self.status = status          # one of: "OK", "TLE", "COMPILE_ERROR", "RUNTIME_ERROR"
        self.time_ms = time_ms        # float, only meaningful if status == "OK"
        self.error_message = error_message

    def __repr__(self):
        if self.status == "OK":
            return f"<SandboxResult OK {self.time_ms:.2f}ms>"
        return f"<SandboxResult {self.status}: {self.error_message}>"


def compile_cpp(cpp_code: str, work_dir: str):
    """
    Compiles cpp_code (a string of C++ source) into an executable
    inside work_dir.

    Returns (success: bool, message: str).
    message is either the path to the compiled binary, or the compiler
    error text if it failed.

    FAILSAFE: -O2 flag. The blueprint is explicit about this -- Codeforces
    judges compile with -O2 optimization. If you compile without it,
    your timing numbers will not match what actually happens on
    Codeforces, and your whole "did we beat the human hacker" comparison
    becomes meaningless.
    """
    source_path = os.path.join(work_dir, "submission.cpp")
    binary_path = os.path.join(work_dir, "submission.exe" if os.name == "nt" else "submission")

    with open(source_path, "w", encoding="utf-8") as f:
        f.write(cpp_code)

    try:
        compile_proc = subprocess.run(
            ["g++", "-O2", source_path, "-o", binary_path],
            capture_output=True,
            text=True,
            timeout=20,  # compiling itself should never take long; 20s is generous
        )
    except subprocess.TimeoutExpired:
        return False, "Compiler itself hung for 20+ seconds (unusual -- check for a g++ install issue)."
    except FileNotFoundError:
        return False, "g++ was not found. Did you install MinGW and add it to PATH? Run 'g++ --version' in a terminal to check."

    if compile_proc.returncode != 0:
        # Compilation failed -- this is NOT a sandbox bug, it means the
        # C++ code itself has a syntax error. Return the compiler's
        # own error message so you can see what's wrong.
        return False, compile_proc.stderr

    return True, binary_path


def run_single(binary_path: str, input_text: str) -> SandboxResult:
    """
    Runs one compiled binary once, feeding it input_text on stdin.

    FAILSAFE: timeout=TIMEOUT_SECONDS. This is the kill switch from the
    blueprint. subprocess.run's timeout parameter forcibly terminates
    the child process if it runs too long, so an infinite loop in the
    C++ code cannot freeze your machine -- it just gets killed and
    reported as TLE.
    """
    start = time.perf_counter()
    try:
        result = subprocess.run(
            [binary_path],
            input=input_text,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return SandboxResult(status="TLE", error_message=f"Exceeded {TIMEOUT_SECONDS}s")

    elapsed_ms = (time.perf_counter() - start) * 1000

    if result.returncode != 0:
        # The program compiled fine but crashed while running
        # (e.g. segfault, divide by zero, array out of bounds).
        return SandboxResult(
            status="RUNTIME_ERROR",
            error_message=f"Exit code {result.returncode}. stderr: {result.stderr[:300]}",
        )

    return SandboxResult(status="OK", time_ms=elapsed_ms)


def run_with_noise_reduction(binary_path: str, input_text: str) -> SandboxResult:
    """
    Runs the binary NUM_RUNS times and returns the result with the
    MINIMUM execution time among the successful runs.

    FAILSAFE: noise reduction. A single timing run on a normal laptop
    is noisy -- if Windows decides to do a background update check
    mid-run, that one run looks artificially slow. Taking the minimum
    across 3 runs filters that noise out, because the noise can only
    make a run slower, never faster than its true speed.

    If even ONE of the runs comes back as TLE, we report TLE
    immediately -- a program that times out even once on test data is
    a program we care about, no need to keep probing it.
    """
    best_result = None

    for _ in range(NUM_RUNS):
        result = run_single(binary_path, input_text)

        if result.status == "TLE":
            return result  # short-circuit: TLE is the headline finding
        if result.status == "RUNTIME_ERROR":
            return result  # short-circuit: a crash is also worth stopping on

        if best_result is None or result.time_ms < best_result.time_ms:
            best_result = result

    return best_result


def evaluate(cpp_code: str, input_text: str) -> SandboxResult:
    """
    The main entry point. This is the only function the rest of your
    project (fuzzer.py) should call.

    Handles its own temp directory and cleans up after itself, so
    callers don't need to manage files manually.
    """
    work_dir = tempfile.mkdtemp(prefix="sandbox_")
    try:
        compiled_ok, info = compile_cpp(cpp_code, work_dir)
        if not compiled_ok:
            return SandboxResult(status="COMPILE_ERROR", error_message=info)

        binary_path = info
        return run_with_noise_reduction(binary_path, input_text)
    finally:
        # Always clean up the temp folder, even if something above
        # raised an exception. Otherwise an overnight run leaves
        # thousands of stray folders on disk.
        shutil.rmtree(work_dir, ignore_errors=True)


# ---- SELF TEST ----
# Run this file directly (python sandbox.py) to confirm everything works
# on YOUR machine before you wire it up to anything else.
if __name__ == "__main__":
    print("Running sandbox.py self-test...\n")

    # Test 1: a normal, fast program
    fast_code = """
    #include <iostream>
    int main() {
        int n;
        std::cin >> n;
        std::cout << n * 2 << std::endl;
        return 0;
    }
    """
    print("Test 1 (should be OK, fast):")
    print(evaluate(fast_code, "21\n"))

    # Test 2: a program that infinite-loops (tests the kill switch)
    infinite_loop_code = """
    #include <iostream>
    int main() {
        while (true) { }
        return 0;
    }
    """
    print("\nTest 2 (should be TLE after ~3 seconds):")
    print(evaluate(infinite_loop_code, ""))

    # Test 3: a program with a compile error (tests error handling)
    broken_code = """
    #include <iostream>
    int main() {
        std::cout << "missing semicolon"
        return 0;
    }
    """
    print("\nTest 3 (should be COMPILE_ERROR):")
    print(evaluate(broken_code, ""))

    print("\nIf Test 1 = OK, Test 2 = TLE, Test 3 = COMPILE_ERROR, sandbox.py is working correctly.")