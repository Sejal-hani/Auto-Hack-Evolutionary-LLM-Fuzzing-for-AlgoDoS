"""
Asynchronous LLM Fuzzing Agent (Metaprogramming Edition).

Interfaces with the free Groq API using a Multi-Key Distributed Architecture.
Engineered for high-concurrency multi-island evolutionary loops.
Bypasses LLM output token limits by utilizing Metaprogramming:
Instead of generating massive payload arrays, it generates native Python 3 scripts
that programmatically print the payload, reducing token usage by 99%.
"""

import re
import os
import json
import asyncio
import logging
import aiohttp
from typing import List, Dict, Any

# Local imports
from src.ast_analyzer.cfg_parser import CppAstMetadata

logger = logging.getLogger(__name__)

class LlamaFuzzerAgent:
    """
    Non-blocking LLM orchestrator. 
    Translates hardware telemetry and AST metadata into Python-based payload generators.
    """

    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        # Explicit API key injection enables Multi-Island isolated rate-limit pools
        if not api_key:
            raise ValueError("CRITICAL: API key is missing for this LLM Agent instance.")
            
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _build_system_prompt(self, ast_meta: CppAstMetadata, n_constraint: int, island_strategy: str) -> str:
        """
        The Metaprogramming Master Prompt. 
        Forces the LLM to write Python execution code rather than raw data.
        """
        return f"""You are an elite automated vulnerability fuzzer targeting Algorithmic Denial of Service (AlgoDoS).
Your goal is to maximize CPU Execution Time in a target C++ program.

CONSTRAINT LOCK: The payload MUST contain exactly N = {n_constraint} elements.
ISLAND MUTATION STRATEGY: {island_strategy}

{ast_meta.to_llm_prompt_context()}

CRITICAL INSTRUCTION - DO NOT OUTPUT THE RAW ARRAY:
Because outputting {n_constraint} numbers directly will exceed your token limits, YOU MUST WRITE A PYTHON 3 SCRIPT that programmatically generates the array and prints it space-separated to standard output.

OUTPUT FORMAT:
You must return strictly valid JSON. No markdown formatting outside the JSON, no explanations.
Format:
{{
    "generator_code": "import random\\nprint(' '.join(str(i * 107897) for i in range({n_constraint})))"
}}
The Python code MUST print exactly {n_constraint} integers, space-separated. No extra text, no prompts."""

    def _clean_json_response(self, raw_text: str) -> Dict[str, Any]:
        """
        Strips markdown wrappers (```json ... ```) and extracts pure JSON.
        """
        json_pattern = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)
        match = json_pattern.search(raw_text)
        clean_text = match.group(1) if match else raw_text
        
        try:
            return json.loads(clean_text)
        except json.JSONDecodeError as e:
            logger.error(f"LLM hallucinated invalid JSON: {raw_text[:100]}...")
            raise e

    async def generate_mutations(
        self, 
        session: aiohttp.ClientSession, 
        ast_meta: CppAstMetadata, 
        elite_telemetry: List[Dict[str, Any]], 
        n_constraint: int,
        island_strategy: str = "DEFAULT"
    ) -> List[str]:
        """
        Async API call with Exponential Backoff. 
        Returns a list containing the generated Python script.
        """
        system_prompt = self._build_system_prompt(ast_meta, n_constraint, island_strategy)
        
        # Build the Evolutionary Context
        user_content = "PREVIOUS GENERATION ELITE TEST CASES (Learn from these):\n"
        for idx, elite in enumerate(elite_telemetry):
            # We use 'payload_preview' because the orchestrator now truncates the massive arrays
            preview = elite.get('payload_preview', elite.get('payload', ''))
            user_content += f"Test Case {idx+1} | CPU Time: {elite['cpu_time_ms']}ms | Preview: {preview}\n"
            
        user_content += "\nWrite a Python 3 script to generate an even more destructive array based on the strategy. Output JSON with the 'generator_code' key."

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.8,
            "max_tokens": 1000, # Dropped from 8000 to 1000 since it's just generating ~5 lines of Python!
            "response_format": {"type": "json_object"}
        }

        # Exponential Backoff Loop for Free-Tier Limits
        max_retries = 5
        base_delay = 2.0

        for attempt in range(max_retries):
            try:
                async with session.post(self.api_url, headers=self.headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        raw_content = data['choices'][0]['message']['content']
                        parsed_json = self._clean_json_response(raw_content)
                        
                        # Extract the Python script
                        code = parsed_json.get("generator_code", "")
                        return [code] if code else []
                        
                    elif response.status == 429:
                        # Rate Limit Hit. Exponentially scale the wait time.
                        wait_time = base_delay * (2 ** attempt)
                        logger.warning(f"API Rate Limit Hit (429). Retrying in {wait_time}s...")
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        error_text = await response.text()
                        logger.error(f"API Error {response.status}: {error_text}")
                        return []
                        
            except aiohttp.ClientError as e:
                logger.error(f"Network error communicating with LLM: {e}")
                await asyncio.sleep(base_delay)
                
        logger.error("Max retries exceeded. LLM Agent failed to generate metaprogramming script.")
        return []