"""
fuzzer.py
Phase 3 -- "The Evolutionary Loop". This is the brain of the whole project.

What it does, per problem in dataset.json:
  Generation 0: ask the LLM for 5 random valid arrays of size N.
  Run all 5 through sandbox.py, time them.
  Sort by execution time (slowest = most "fit").
  Generation 1+: tell the LLM "here are the 2 slowest arrays and their
    times -- analyze why, then mutate the slowest one into 5 new arrays
    that should be even slower."
  Repeat for up to MAX_GENERATIONS, or stop early if we hit a TLE.

Every step that touches the LLM's output is treated as untrusted --
wrong size, garbage, or an empty response are all expected and handled,
never allowed to crash the loop.
"""

import json
import random
import csv
import os
from datetime import datetime

import sandbox
import llm_api

MAX_GENERATIONS = 30
ARRAYS_PER_GENERATION = 5
RESULTS_CSV_PATH = "results.csv"


def random_array(size: int, low: int = 1, high: int = 100000) -> list:
    """
    FAILSAFE: Mutation Fallback support function.
    Generates a random valid array of the exact required size. Used both
    for Generation 0 (if you want a non-LLM baseline) and as the
    fallback whenever the LLM produces something we can't use.
    """
    return [random.randint(low, high) for _ in range(size)]


def array_to_input_text(array: list) -> str:
    """
    Converts a Python list into the text format the C++ program expects
    on stdin. This assumes the common Codeforces format:
        line 1: N
        line 2: the N numbers, space separated

    If your dataset's problems expect a different input format (multiple
    arrays, a different first line, etc.), this is the one function you
    need to edit -- everything else stays the same.
    """
    n = len(array)
    numbers = " ".join(str(x) for x in array)
    return f"{n}\n{numbers}\n"


def evaluate_array(cpp_code: str, array: list) -> sandbox.SandboxResult:
    """Thin wrapper so fuzzer.py doesn't need to know sandbox.py's internals."""
    input_text = array_to_input_text(array)
    return sandbox.evaluate(cpp_code, input_text)


def get_initial_population(problem: dict) -> list:
    """
    Generation 0. Asks the LLM for ARRAYS_PER_GENERATION random valid
    arrays. If the LLM gives us fewer valid arrays than we asked for
    (or none at all), we top up the population with random arrays so
    the loop always has a full generation to work with.
    """
    n = problem["fixed_N"]

    system_instruction = (
        "You are a Codeforces Hacker. Do not output any explanatory text. "
        "Output only a valid JSON array of arrays. Each inner array MUST "
        f"have exactly {n} integers."
    )
    user_prompt = (
        f"Generate {ARRAYS_PER_GENERATION} random valid arrays of exactly "
        f"{n} integers each, with values between 1 and 100000. These will "
        f"be used as test input for a C++ program solving: "
        f"{problem.get('algorithm_type', 'an algorithmic problem')}. "
        "Respond with only the JSON array of arrays."
    )

    arrays = llm_api.generate_arrays(
        system_instruction, user_prompt,
        expected_size=n, expected_count=ARRAYS_PER_GENERATION,
    )

    # FAILSAFE: Mutation Fallback (applied to generation 0 too).
    # Top up with random arrays if the LLM under-delivered.
    while len(arrays) < ARRAYS_PER_GENERATION:
        arrays.append(random_array(n))
        print(f"[fuzzer] Gen 0: topped up population with 1 random array "
              f"(LLM gave {len(arrays)-1}/{ARRAYS_PER_GENERATION}).")

    return arrays[:ARRAYS_PER_GENERATION]


def get_next_generation(problem: dict, ranked_results: list) -> list:
    """
    Generations 1+. Takes the current generation's results (already
    sorted slowest-first), shows the LLM the top 2 slowest arrays, and
    asks it to mutate the single slowest one into a new population.

    ranked_results is a list of dicts: {"array": [...], "time_ms": float}
    sorted with the SLOWEST first.
    """
    n = problem["fixed_N"]
    cpp_code = problem["cpp_code"]

    slowest = ranked_results[0]
    second_slowest = ranked_results[1] if len(ranked_results) > 1 else ranked_results[0]

    system_instruction = (
        "You are a Codeforces Hacker performing adversarial test-case "
        "mutation. Do not output any explanatory text. Output only a "
        f"valid JSON array of arrays. Each inner array MUST have exactly "
        f"{n} integers."
    )
    user_prompt = (
        f"This C++ code is being attacked:\n{cpp_code}\n\n"
        f"Array A took {second_slowest['time_ms']:.2f}ms: {second_slowest['array']}\n"
        f"Array B took {slowest['time_ms']:.2f}ms: {slowest['array']}\n\n"
        "Analyze the C++ code and explain to yourself (but do not output "
        "the explanation) why Array B was slower. Then mutate Array B to "
        f"create {ARRAYS_PER_GENERATION} new arrays of exactly {n} "
        "integers each that are likely to run even slower than Array B. "
        "Respond with only the JSON array of arrays."
    )

    arrays = llm_api.generate_arrays(
        system_instruction, user_prompt,
        expected_size=n, expected_count=ARRAYS_PER_GENERATION,
    )

    # FAILSAFE: Mutation Fallback. This is the exact scenario the blueprint
    # calls out: if the LLM breaks and gives us the wrong size (or nothing),
    # we don't crash and we don't stall -- we throw away the bad ones and
    # fill the rest with random arrays so evolution can keep going.
    while len(arrays) < ARRAYS_PER_GENERATION:
        arrays.append(random_array(n))

    if len(arrays) < ARRAYS_PER_GENERATION:
        print(f"[fuzzer] WARNING: had to pad generation with random arrays.")

    return arrays[:ARRAYS_PER_GENERATION]


def run_generation(cpp_code: str, arrays: list) -> list:
    """
    Runs every array in this generation through the sandbox and returns
    a list of {"array": ..., "time_ms": ..., "status": ...} dicts,
    sorted SLOWEST FIRST (the blueprint's "Fitness Sort").

    If ANY array in the generation triggers a TLE, that's reported
    immediately in the results -- the caller decides whether to stop
    the whole run early.
    """
    results = []
    for array in arrays:
        result = evaluate_array(cpp_code, array)

        if result.status == "TLE":
            results.append({"array": array, "time_ms": 3000.0, "status": "TLE"})
        elif result.status == "OK":
            results.append({"array": array, "time_ms": result.time_ms, "status": "OK"})
        else:
            # COMPILE_ERROR or RUNTIME_ERROR -- this array is unusable for
            # ranking. We log it but give it a time of 0 so it sorts to
            # the bottom (least "fit") instead of accidentally looking
            # like a winner.
            print(f"[fuzzer] Array discarded ({result.status}): {result.error_message}")
            results.append({"array": array, "time_ms": 0.0, "status": result.status})

    results.sort(key=lambda r: r["time_ms"], reverse=True)
    return results


def run_problem(problem: dict, csv_writer) -> None:
    """
    Runs the full evolutionary loop for a single problem from
    dataset.json, logging every generation to the CSV as it goes
    (so even a crash partway through preserves everything found so far).
    """
    problem_id = problem["id"]
    cpp_code = problem["cpp_code"]

    print(f"\n=== Starting problem {problem_id} ===")

    population = get_initial_population(problem)

    for generation in range(MAX_GENERATIONS):
        results = run_generation(cpp_code, population)
        best = results[0]

        tle_reached = best["status"] == "TLE"

        csv_writer.writerow({
            "problem_id": problem_id,
            "generation": generation,
            "max_time_ms": round(best["time_ms"], 2),
            "tle_reached": tle_reached,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        })

        print(f"[{problem_id}] Gen {generation}: best={best['time_ms']:.2f}ms "
              f"status={best['status']}")

        if tle_reached:
            print(f"[{problem_id}] TLE reached at generation {generation}. Stopping early.")
            break

        # Use the surviving population (real OK results) to breed the next
        # generation. If everything in this generation errored out, fall
        # back to a fresh random population instead of breeding garbage.
        ok_results = [r for r in results if r["status"] == "OK"]
        if len(ok_results) < 2:
            print(f"[{problem_id}] Not enough valid results to breed from -- "
                  f"reseeding with a fresh random population.")
            n = problem["fixed_N"]
            population = [random_array(n) for _ in range(ARRAYS_PER_GENERATION)]
        else:
            population = get_next_generation(problem, ok_results)


def load_dataset(path: str = "dataset.json") -> list:
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"{path} not found. Build it from real Codeforces problems "
            "when ready. Use the sample problem below for testing until then."
        )

    with open(path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # FAILSAFE: an empty or whitespace-only file is just as "not ready"
    # as a missing file -- don't let json.load() crash on it.
    if not raw_text.strip():
        raise FileNotFoundError(
            f"{path} exists but is empty. Fill it in with real problems "
            "when ready. Use the sample problem below for testing until then."
        )

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise FileNotFoundError(
            f"{path} exists but isn't valid JSON ({e}). Check for a missing "
            "comma, bracket, or quote. Falling back to the sample problem."
        )

    if not isinstance(data, list) or len(data) == 0:
        raise FileNotFoundError(
            f"{path} parsed fine but contains no problems (expected a "
            "JSON array with at least one problem object)."
        )

    return data


def main():
    try:
        dataset = load_dataset()
    except FileNotFoundError as e:
        print(f"[fuzzer] {e}")
        print("[fuzzer] Falling back to a single built-in sample problem for testing.")
        dataset = [SAMPLE_PROBLEM]

    file_exists = os.path.exists(RESULTS_CSV_PATH)
    with open(RESULTS_CSV_PATH, "a", newline="", encoding="utf-8") as csv_file:
        fieldnames = ["problem_id", "generation", "max_time_ms", "tle_reached", "timestamp"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        for problem in dataset:
            try:
                run_problem(problem, writer)
                csv_file.flush()  # write to disk immediately, don't wait for buffer
            except Exception as e:
                # FAILSAFE: a crash on ONE problem (e.g. a malformed dataset
                # entry) must not kill the overnight run for the other 14.
                print(f"[fuzzer] ERROR on problem {problem.get('id', '?')}: {e}")
                print("[fuzzer] Skipping to next problem.")
                continue

    print(f"\nDone. Results written to {RESULTS_CSV_PATH}")


# A minimal sample problem so you (Person A) can test the WHOLE pipeline
# right now, before Person B's real dataset.json exists. This is a classic
# bubble-sort-style O(N^2) target: an already-sorted array is fast, but a
# reverse-sorted array is slow for some naive sorts. Replace this with real
# Codeforces problems once dataset.json is ready -- nothing else changes.
SAMPLE_PROBLEM = {
    "id": "SAMPLE_BUBBLESORT",
    "algorithm_type": "Bubble Sort",
    "fixed_N": 2000,
    "cpp_code": """
#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    for (int i = 0; i < n; i++)
        for (int j = 0; j < n - 1; j++)
            if (a[j] > a[j+1])
                swap(a[j], a[j+1]);

    cout << a[0] << " " << a[n-1] << endl;
    return 0;
}
""",
}


if __name__ == "__main__":
    main()