"""
Asynchronous LLM Fuzzing Agent.

Interfaces with the free Groq API (Llama-3 70B).
Engineered for high-concurrency multi-island evolutionary loops.
Features strict JSON schema enforcement, Markdown stripping, and HTTP 429 Exponential Backoff.
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
    Translates hardware telemetry and AST metadata into adversarial prompts.
    """

    def __init__(self, api_key: str = None, model: str = "llama3-70b-8192"):
        # Expects the GROQ_API_KEY environment variable if not passed directly
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("CRITICAL: GROQ_API_KEY environment variable is missing. Obtain it free from console.groq.com")
            
        self.model = model
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _build_system_prompt(self, ast_meta: CppAstMetadata, n_constraint: int, island_strategy: str) -> str:
        """
        The Master Prompt. Injects static analysis directly into the LLM's brain.
        Island Strategies: 'REVERSER', 'EXTREMIST', 'DUPLICATOR'
        """
        return f"""You are an elite automated vulnerability fuzzer targeting Algorithmic Denial of Service (AlgoDoS).
Your goal is to generate test cases that maximize CPU Execution Time (Time Limit Exceeded).

CONSTRAINT LOCK: You MUST generate exactly an array of size N = {n_constraint}.
ISLAND MUTATION STRATEGY: {island_strategy}
(Apply this strategy: e.g., if EXTREMIST, use INT_MAX/INT_MIN. If DUPLICATOR, maximize hash collisions).

{ast_meta.to_llm_prompt_context()}

OUTPUT FORMAT:
You must return strictly valid JSON. No markdown formatting, no explanations, no yapping.
Format:
{{
    "mutations": [
        "10 20 30 ...", 
        "99 99 99 ..."
    ]
}}
Each string in the "mutations" array is one complete test case payload."""

    def _clean_json_response(self, raw_text: str) -> Dict[str, Any]:
        """
        LLMs are notorious for wrapping JSON in Markdown (```json ... ```) 
        even when told not to. This regex rips the pure JSON out of the response.
        """
        # Strip markdown code blocks
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
        Async API call with Exponential Backoff for Free-Tier Rate Limits.
        elite_telemetry contains the top 3 test cases from the previous generation and their CPU times.
        """
        system_prompt = self._build_system_prompt(ast_meta, n_constraint, island_strategy)
        
        # Build the Evolutionary Context
        user_content = "PREVIOUS GENERATION ELITE TEST CASES (Learn from these):\n"
        for idx, elite in enumerate(elite_telemetry):
            user_content += f"Test Case {idx+1} | CPU Time: {elite['cpu_time_ms']}ms | Payload Preview: {elite['payload'][:100]}...\n"
            
        user_content += "\nAnalyze the telemetry. Mutate these arrays to cause even higher CPU time. Output 5 new mutations in JSON."

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.8, # High temperature for creative adversarial attacks
            "response_format": {"type": "json_object"}
        }

        # Exponential Backoff Loop
        max_retries = 5
        base_delay = 2.0

        for attempt in range(max_retries):
            try:
                async with session.post(self.api_url, headers=self.headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        raw_content = data['choices'][0]['message']['content']
                        parsed_json = self._clean_json_response(raw_content)
                        return parsed_json.get("mutations", [])
                        
                    elif response.status == 429:
                        # Rate Limit Hit. We must wait.
                        wait_time = base_delay * (2 ** attempt)
                        logger.warning(f"Groq API Rate Limit Hit (429). Retrying in {wait_time}s...")
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        error_text = await response.text()
                        logger.error(f"API Error {response.status}: {error_text}")
                        return []
                        
            except aiohttp.ClientError as e:
                logger.error(f"Network error communicating with LLM: {e}")
                await asyncio.sleep(base_delay)
                
        logger.error("Max retries exceeded. LLM Agent failed to generate mutations.")
        return []