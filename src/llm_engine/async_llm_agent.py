"""
Asynchronous LLM Fuzzing Agent (Metaprogramming & Self-Healing Edition).

Interfaces with the Groq API using a Multi-Key Distributed Architecture.
Engineered for high-concurrency multi-island evolutionary loops.
Bypasses LLM output token limits by utilizing Metaprogramming (O(1) Python 3 generator scripts).
Equipped with Self-Healing syntax retry mechanisms and Epistemic Reflection.
"""

import re
import os
import json
import asyncio
import logging
import aiohttp
from typing import List, Dict, Any, Optional

# Local imports
from src.ast_analyzer.cfg_parser import CppAstMetadata

logger = logging.getLogger(__name__)

class LlamaFuzzerAgent:
    """
    Non-blocking LLM orchestrator. 
    Translates hardware telemetry, AST metadata, and self-healing tracebacks into Python payload generators.
    """

    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        if not api_key:
            raise ValueError("CRITICAL: API key is missing for this LLM Agent instance.")
            
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _build_system_prompt(self, ast_meta: CppAstMetadata, n_constraint: int, island_strategy: str, input_format: Optional[str] = None) -> str:
        """
        The Metaprogramming Master Prompt. 
        Forces the LLM to write Python execution code rather than raw data.
        """
        format_clause = f"\nFORMAL INPUT FORMAT SPECIFICATION:\n{input_format}\n" if input_format else ""

        return f"""You are an elite automated vulnerability fuzzer targeting Algorithmic Denial of Service (AlgoDoS).
Your goal is to maximize CPU Execution Time in a target C++ program.

CONSTRAINT LOCK: N = {n_constraint}
ISLAND MUTATION STRATEGY: {island_strategy}
{format_clause}
{ast_meta.to_llm_prompt_context()}

CRITICAL INSTRUCTION - GENERATIVE METAPROGRAMMING:
DO NOT OUTPUT RAW NUMERICAL ARRAYS.
Write a concise, standalone Python 3 script that programmatically prints the adversarial payload to stdout matching the exact expected input format.

OUTPUT FORMAT:
Return strictly valid JSON with key "generator_code". No markdown outside JSON.
Example format:
{{
    "generator_code": "N = {n_constraint}\\nprint(f'{{N}}')\\nprint(' '.join(str(i * 107897) for i in range(N)))"
}}"""

    def _clean_json_response(self, raw_text: str) -> Dict[str, Any]:
        """Strips markdown wrappers and parses JSON robustly."""
        json_pattern = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)
        match = json_pattern.search(raw_text)
        clean_text = match.group(1) if match else raw_text.strip()
        
        try:
            return json.loads(clean_text)
        except json.JSONDecodeError:
            # Fallback: extract generator_code string if json is malformed
            code_match = re.search(r'"generator_code"\s*:\s*"(.*?)"(?:\s*\}|\s*,)', raw_text, re.DOTALL)
            if code_match:
                # unescape newlines
                code_str = code_match.group(1).encode().decode('unicode_escape')
                return {"generator_code": code_str}
            logger.error(f"LLM produced unparseable response: {raw_text[:120]}...")
            raise

    async def generate_mutations(
        self, 
        session: aiohttp.ClientSession, 
        ast_meta: CppAstMetadata, 
        elite_telemetry: List[Dict[str, Any]], 
        n_constraint: int,
        island_strategy: str = "DEFAULT",
        input_format: Optional[str] = None
    ) -> List[str]:
        """
        Async API call with Exponential Backoff. 
        Returns the generated Python script generator.
        """
        system_prompt = self._build_system_prompt(ast_meta, n_constraint, island_strategy, input_format)
        
        user_content = "PREVIOUS GENERATION ELITE TEST CASES (Learn and mutate):\n"
        for idx, elite in enumerate(elite_telemetry):
            preview = elite.get('payload_preview', '')
            user_content += f"Elite {idx+1} | CPU Time: {elite.get('cpu_time_ms', 0)}ms | Preview: {preview}\n"
            
        user_content += f"\nWrite a Python 3 script to synthesize an input targeting maximum algorithmic degradation under strategy '{island_strategy}'. Output JSON with 'generator_code'."

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.8,
            "max_tokens": 1000,
            "response_format": {"type": "json_object"}
        }

        return await self._call_llm_with_backoff(session, payload)

    async def self_heal_script(
        self,
        session: aiohttp.ClientSession,
        broken_script: str,
        error_traceback: str,
        ast_meta: CppAstMetadata,
        n_constraint: int,
        island_strategy: str,
        input_format: Optional[str] = None
    ) -> Optional[str]:
        """
        Self-Healing Syntax Loop (Up to 3 retries).
        Feeds runtime traceback back to the LLM to auto-correct script syntax or format mismatch.
        """
        system_prompt = self._build_system_prompt(ast_meta, n_constraint, island_strategy, input_format)
        user_content = (
            f"SELF-HEALING REQUIRED: The previously synthesized Python script raised an error when executed.\n\n"
            f"--- BROKEN PYTHON SCRIPT ---\n{broken_script}\n\n"
            f"--- STDERR TRACEBACK / RUNTIME ERROR ---\n{error_traceback}\n\n"
            f"Fix the script so it executes cleanly and outputs valid input format. Return JSON with 'generator_code'."
        )

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.3,
            "max_tokens": 1000,
            "response_format": {"type": "json_object"}
        }

        results = await self._call_llm_with_backoff(session, payload)
        return results[0] if results else None

    async def reflect_strategy(
        self,
        session: aiohttp.ClientSession,
        stagnant_island_id: str,
        current_strategy: str,
        ast_meta: CppAstMetadata,
        history_fitness: List[float]
    ) -> str:
        """
        Epistemic Reflection: If an island stagnates (<1% fitness gain over 3 generations),
        prompts the LLM to evolve and rethink the prompt directive.
        """
        prompt = (
            f"EPISTEMIC REFLECTION: Island '{stagnant_island_id}' has stagnated with flat fitness history: {history_fitness}.\n"
            f"Current Strategy: {current_strategy}\n"
            f"AST Context: Loop Depth={ast_meta.max_loop_depth}, STLs={ast_meta.vulnerable_stls}, Recursion={ast_meta.recursive_functions}\n"
            f"Formulate an aggressive new directional mutation strategy prompt (1-2 sentences) to escape this local minima."
        )

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are an evolutionary algorithmic optimization architect."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.9,
            "max_tokens": 200
        }

        try:
            async with session.post(self.api_url, headers=self.headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    new_strategy = data['choices'][0]['message']['content'].strip()
                    logger.info(f"[{stagnant_island_id}] Epistemic Reflection Updated Strategy -> {new_strategy[:80]}...")
                    return new_strategy
        except Exception as e:
            logger.warning(f"Epistemic reflection fallback due to API issue: {e}")
            
        return current_strategy

    async def _call_llm_with_backoff(self, session: aiohttp.ClientSession, payload: Dict[str, Any]) -> List[str]:
        """Dispatches API request with exponential backoff for rate limits and records telemetry."""
        from src.core.telemetry_tracker import GlobalTelemetryTracker
        tracker = GlobalTelemetryTracker()
        
        max_retries = 5
        base_delay = 2.0

        for attempt in range(max_retries):
            try:
                async with session.post(self.api_url, headers=self.headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Extract usage tokens
                        usage = data.get("usage", {})
                        p_toks = usage.get("prompt_tokens", 45)
                        c_toks = usage.get("completion_tokens", 35)
                        tracker.record_api_tokens(p_toks, c_toks)
                        
                        raw_content = data['choices'][0]['message']['content']
                        parsed_json = self._clean_json_response(raw_content)
                        code = parsed_json.get("generator_code", "")
                        return [code] if code else []
                    elif response.status == 429:
                        tracker.record_429_event()
                        wait_time = base_delay * (2 ** attempt)
                        logger.warning(f"API Rate Limit Hit (429). Backing off {wait_time:.1f}s...")
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        error_text = await response.text()
                        logger.error(f"API Error {response.status}: {error_text[:150]}")
                        return []
            except Exception as e:
                logger.error(f"Network error communicating with LLM: {e}")
                await asyncio.sleep(base_delay)

        return []