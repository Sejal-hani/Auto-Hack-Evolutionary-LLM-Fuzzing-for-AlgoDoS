"""
CF-Fuzz Batch Dataset Automator.

Reads raw text files containing Codeforces Problem Descriptions + C++ Code.
Uses Groq Llama-3 to automatically extract the exact constraints and format the C++ files.
Saves production-ready targets into the dataset/ directory.
"""

import os
import sys
import aiohttp
import asyncio
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s", datefmt="%H:%M:%S")

async def process_raw_file(session: aiohttp.ClientSession, api_key: str, txt_path: Path):
    raw_content = txt_path.read_text(encoding='utf-8')
    logging.info(f"🧠 Analyzing: {txt_path.name}...")

    system_prompt = """You are an expert Competitive Programming Architect.
The user is giving you a text containing BOTH a Codeforces Problem Description and a vulnerable C++ submission.
Your job is to format it for our Automated Fuzzer.

INSTRUCTIONS:
1. Read the Problem Description to find the EXACT input format and the MAX limits (e.g., if n <= 2*10^5, the max limit is 200000).
2. Set the [N_CONSTRAINT] comment to that exact maximum limit.
3. Set the [INPUT_FORMAT] comment to precisely describe the input structure based on the Problem Description (e.g., "Three integers N N N, followed by 3 arrays of size N").
4. Output ONLY the fixed C++ code. Make sure the code reads the input cleanly in main(). Do NOT output any markdown blocks like ```cpp, just the raw code.

OUTPUT FORMAT MUST START EXACTLY LIKE THIS:
// [N_CONSTRAINT]: <exact_number>
// [INPUT_FORMAT]: <precise_description>
#include <iostream>
... rest of code ..."""

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Here is the problem and code:\n\n{raw_content}"}
        ],
        "temperature": 0.1 # Very low temperature for maximum logical precision
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            async with session.post("https://api.groq.com/openai/v1/chat/completions", 
                                    headers={"Authorization": f"Bearer {api_key}"}, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    clean_code = data['choices'][0]['message']['content'].strip()
                    
                    # Strip markdown if the LLM hallucinated it
                    if clean_code.startswith("```cpp"):
                        clean_code = clean_code[6:-3].strip()
                    elif clean_code.startswith("```"):
                        clean_code = clean_code[3:-3].strip()

                    # Save to dataset folder
                    output_name = txt_path.stem + ".cpp"
                    out_path = Path("dataset") / output_name
                    out_path.parent.mkdir(exist_ok=True)
                    out_path.write_text(clean_code, encoding='utf-8')
                    
                    logging.info(f"✅ SUCCESS: Formatted and saved {output_name}")
                    return
                elif response.status == 429:
                    await asyncio.sleep(2 ** attempt)
                else:
                    logging.error(f"❌ API Error on {txt_path.name}: {await response.text()}")
                    return
        except Exception as e:
            await asyncio.sleep(2)
            
    logging.error(f"❌ Failed to process {txt_path.name} after multiple attempts.")

async def run_automator():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        logging.error("CRITICAL: Set your GROQ_API_KEY in the terminal first!")
        return

    raw_dir = Path("raw_submissions")
    raw_dir.mkdir(exist_ok=True)
    
    txt_files = list(raw_dir.glob("*.txt"))
    if not txt_files:
        logging.error("No .txt files found in 'raw_submissions/'. Please add your problems there.")
        return

    logging.info(f"🚀 Found {len(txt_files)} raw submissions. Booting Llama-3 Automator...")

    async with aiohttp.ClientSession() as session:
        # Process all text files simultaneously
        tasks = [process_raw_file(session, api_key, txt_file) for txt_file in txt_files]
        await asyncio.gather(*tasks)
        
    logging.info("🎉 All datasets formatted and moved to dataset/ folder perfectly.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_automator())