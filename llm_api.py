"""
llm_api.py
Person A's Phase 2 deliverable.

Wraps the Gemini API so the rest of the project never has to deal with:
  - the LLM rambling in English instead of giving pure data
  - rate limit (429) errors crashing the whole overnight run
  - network errors crashing the whole overnight run

The only thing fuzzer.py should ever call is generate_arrays().
"""

import os
import re
import json
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()  # reads the .env file and loads GEMINI_API_KEY into the environment

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY not found. Did you create a .env file with "
        "GEMINI_API_KEY=your_key_here in the project root?"
    )

client = genai.Client(api_key=API_KEY)

# FAILSAFE: Model Fallback Chain.
# gemini-3.5-flash is the most heavily-used model and gets hit hardest by
# Google's "high demand" 503 errors. If it's overloaded, we fall back to
# trying other models before giving up entirely -- a slower/older model
# that's actually up beats a fast one that's down.
MODEL_FALLBACK_CHAIN = ["gemini-3.5-flash", "gemini-2.5-flash", "gemini-2.5-flash-lite"]
MAX_RETRIES_PER_MODEL = 3
BASE_RETRY_DELAY_SECONDS = 8

# FAILSAFE: Call Pacing.
# Free-tier Gemini keys have a requests-per-minute cap. Rather than only
# reacting to 429 errors after they happen, we proactively wait at least
# this many seconds between the START of one call and the START of the
# next. This means fuzzer.py's overnight run trips the rate limit far
# less often in the first place, instead of relying entirely on retries.
# Raise this number if you're still seeing frequent 429s; lower it once
# you're on a paid tier with a higher per-minute allowance.
MIN_SECONDS_BETWEEN_CALLS = 12

_last_call_started_at = None


def _wait_for_pacing():
    """Blocks just long enough to keep calls spaced at least
    MIN_SECONDS_BETWEEN_CALLS apart. A no-op on the very first call."""
    global _last_call_started_at
    if _last_call_started_at is not None:
        elapsed = time.time() - _last_call_started_at
        remaining = MIN_SECONDS_BETWEEN_CALLS - elapsed
        if remaining > 0:
            print(f"[llm_api] Pacing: waiting {remaining:.1f}s before next call "
                  f"to stay under the rate limit.")
            time.sleep(remaining)
    _last_call_started_at = time.time()



def _extract_json_array(raw_text: str):
    """
    FAILSAFE: The Regex Cleaner.

    LLMs love to wrap their answer in explanation, e.g.:
        "Here is the array you requested: [1, 2, 3, 4, 5]"
    or wrap it in markdown code fences:
        ```json
        [1, 2, 3]
        ```

    This function strips all of that away and returns ONLY the JSON array
    text, or None if it genuinely can't find one anywhere in the response.

    We always try this even when we ASKED for pure JSON (structured output),
    because models occasionally ignore instructions, and this project's
    entire philosophy is "assume nothing works."
    """
    if raw_text is None:
        return None

    # Strip markdown code fences if present
    cleaned = re.sub(r"```json|```", "", raw_text).strip()

    # Find the first [ ... ] block, including nested arrays like [[1,2],[3,4]]
    match = re.search(r"\[.*\]", cleaned, re.DOTALL)
    if not match:
        # FAILSAFE: distinguish "no brackets at all" from "starts with a
        # bracket but never closes" -- the latter means the response got
        # cut off (truncated) rather than the model refusing to use JSON.
        # Different root cause, different fix (raise max_output_tokens),
        # so the log message should say which one happened.
        if cleaned.lstrip().startswith("["):
            print(f"[llm_api] Response looks TRUNCATED (starts with '[' but "
                  f"never closes). Consider raising max_output_tokens. "
                  f"Last 80 chars: ...{cleaned[-80:]}")
        return None

    return match.group(0)



def _call_gemini_with_retry(prompt: str, system_instruction: str) -> str:
    """
    FAILSAFE: The Rate Limit Loop + Model Fallback Chain.

    Calls Gemini. If it gets rate-limited (HTTP 429) or hits a transient
    server error (503 "high demand" is common with the free tier), it
    waits and retries with backoff. If a model is consistently
    unavailable, it moves on to the next model in MODEL_FALLBACK_CHAIN
    instead of giving up entirely. This matters because your fuzzer.py
    will be making dozens of calls per problem, across many problems,
    possibly overnight -- a single overloaded model should never end
    the whole run.
    """
    last_error = None

    for model_name in MODEL_FALLBACK_CHAIN:
        for attempt in range(1, MAX_RETRIES_PER_MODEL + 1):
            _wait_for_pacing()
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        # FAILSAFE: Structured Output. We ask Gemini to restrict
                        # itself to a JSON-shaped response at the API level,
                        # which is more reliable than just asking nicely in
                        # the prompt text.
                        response_mime_type="application/json",
                        temperature=0.9,  # some randomness so generation 0 arrays aren't all identical
                        # FAILSAFE: explicit output token budget. Without this,
                        # the model can silently truncate mid-array when asked
                        # for many large arrays (e.g. 5 arrays x 2000 integers
                        # = up to ~10,000 numbers as JSON text). A truncated
                        # response looks like garbage to the JSON parser even
                        # though the model "succeeded" from its own point of
                        # view. 32768 is generous headroom for N up to ~5000.
                        max_output_tokens=32768,
                    ),
                )
                if model_name != MODEL_FALLBACK_CHAIN[0]:
                    print(f"[llm_api] Succeeded using fallback model: {model_name}")
                return response.text

            except Exception as e:
                error_text = str(e)
                last_error = error_text

                # FAILSAFE: a "limit: 0" quota error means this model is
                # NOT enabled at all for this key/tier -- waiting and
                # retrying can never help, unlike a normal rate limit
                # which recovers over time. Skip straight to the next
                # model instead of burning 3 retries (and ~48s) on
                # something that will never succeed.
                is_zero_quota = "limit: 0" in error_text

                is_rate_limit = "429" in error_text or "RESOURCE_EXHAUSTED" in error_text
                is_server_error = "503" in error_text or "UNAVAILABLE" in error_text or "500" in error_text

                if is_zero_quota:
                    print(f"[llm_api] {model_name} has ZERO quota on this key/tier "
                          f"(will never succeed). Skipping straight to next model.")
                    break
                elif is_rate_limit or is_server_error:
                    wait_time = BASE_RETRY_DELAY_SECONDS * attempt
                    print(f"[llm_api] {model_name} attempt {attempt}/{MAX_RETRIES_PER_MODEL} failed "
                          f"({'rate limit' if is_rate_limit else 'server overloaded'}). "
                          f"Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                    continue
                else:
                    # Not a retryable error (e.g. bad API key, malformed
                    # request). Retrying the SAME model won't help, but a
                    # different model in the chain might still be worth
                    # trying, so don't raise yet -- just stop retrying
                    # this one and move to the next model.
                    print(f"[llm_api] {model_name} gave a non-retryable error: {error_text[:150]}")
                    break

        print(f"[llm_api] Giving up on {model_name}, trying next model in fallback chain...")

    raise RuntimeError(
        f"Gemini API failed on every model in {MODEL_FALLBACK_CHAIN}. Last error: {last_error}"
    )



def generate_arrays(system_instruction: str, user_prompt: str, expected_size: int, expected_count: int):
    """
    The main entry point fuzzer.py will call.

    Asks Gemini to produce `expected_count` arrays, each of length
    `expected_size`. Returns a Python list of lists of integers.

    FAILSAFE: This function NEVER raises an exception for "bad LLM output."
    If parsing fails completely, it returns an empty list — it is the
    CALLER's job (fuzzer.py, per the blueprint's Mutation Fallback) to
    detect an empty/wrong-shaped result and substitute random arrays
    instead. This function's only job is: try hard to parse, and tell
    the truth about whether it succeeded.
    """
    raw_text = _call_gemini_with_retry(user_prompt, system_instruction)

    json_text = _extract_json_array(raw_text)
    if json_text is None:
        print(f"[llm_api] WARNING: could not find any JSON array in response: {raw_text[:200]}")
        return []

    try:
        parsed = json.loads(json_text)
    except json.JSONDecodeError as e:
        print(f"[llm_api] WARNING: found bracket text but it wasn't valid JSON: {e}")
        return []

    # We expect a list of arrays, e.g. [[1,2,3], [4,5,6]].
    # But sometimes the model returns a single flat array when we only
    # asked for one. Normalize both cases into a list-of-lists.
    if len(parsed) > 0 and isinstance(parsed[0], list):
        arrays = parsed
    else:
        arrays = [parsed]

    # Validate each array's size. Don't silently keep bad ones -- drop them
    # and let fuzzer.py's Mutation Fallback fill the gap with random data.
    valid_arrays = [arr for arr in arrays if isinstance(arr, list) and len(arr) == expected_size]

    if len(valid_arrays) < len(arrays):
        print(f"[llm_api] WARNING: dropped {len(arrays) - len(valid_arrays)} array(s) "
              f"with wrong size (expected {expected_size}).")

    return valid_arrays


# ---- SELF TEST ----
if __name__ == "__main__":
    print("Running llm_api.py self-test...\n")

    system_prompt = (
        "You are a Codeforces Hacker. Do not output text. Output only a "
        "valid JSON array of arrays. Each inner array MUST have exactly "
        "5 integers."
    )
    user_prompt = (
        "Generate 3 arrays of exactly 5 integers each, where each array "
        "is sorted in strictly decreasing order. Respond with only the "
        "JSON array of arrays, nothing else."
    )

    result = generate_arrays(system_prompt, user_prompt, expected_size=5, expected_count=3)

    print(f"Got {len(result)} valid array(s):")
    for arr in result:
        print(" ", arr)

    if result:
        print("\nllm_api.py is working correctly.")
    else:
        print("\nNo valid arrays returned -- check your API key and the error messages above.")