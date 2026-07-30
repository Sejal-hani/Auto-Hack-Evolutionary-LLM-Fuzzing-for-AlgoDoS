import os
import re
import json
import aiohttp
import asyncio
import logging
import hashlib
from pathlib import Path

# The log name is DIFFERENT so you can see if you are running the right file
logging.basicConfig(level=logging.INFO, format="%(asctime)s | REAL-DEAL | %(message)s", datefmt="%H:%M:%S")

async def main():
    print("\n" + "="*50)
    print("CHECK YOUR SCREEN: IF IT DOES NOT SAY 'REAL-DEAL' BELOW,")
    print("YOU ARE RUNNING THE WRONG FILE!")
    print("="*50 + "\n")

    # 1. API KEY CHECK
    key = os.environ.get("GROQ_API_KEY_ONE")
    if not key:
        print("❌ STOP! You didn't set your API key in this terminal.")
        print("Run this first: $env:GROQ_API_KEY_ONE = 'your_key_here'")
        return

    # 2. FILE SETUP
    raw_dir = Path("raw_submissions")
    raw_dir.mkdir(exist_ok=True)
    cache_path = Path(".final_cache.json")
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}

    # 3. DUMP CHECK
    if not Path("massive_dump.txt").exists():
        print("❌ massive_dump.txt is missing from this folder!")
        return
    
    text = Path("massive_dump.txt").read_text(encoding='utf-8')
    # Simple split
    chunks = [c.strip() for c in re.split(r'(?=time limit per test|time limit:)', text, flags=re.IGNORECASE) if len(c) > 100]
    
    print(f"✅ Found {len(chunks)} problems. Starting slow-and-steady mode...")

    async with aiohttp.ClientSession() as session:
        # THE ONLY LOOP: ONE AT A TIME.
        for i, chunk in enumerate(chunks):
            c_hash = hashlib.md5(chunk.encode()).hexdigest()

            # SKIP if already done
            if c_hash in cache and (raw_dir / cache[c_hash]).exists():
                logging.info(f"⏭️  Problem {i+1} exists. Skipping.")
                continue

            logging.info(f"⚙️  STARTING PROBLEM {i+1}...")

            payload = {
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": f"Format this Codeforces problem into PROBLEM STATEMENT, LIMITS, and CODE. First line must be [FILENAME]: name.txt\n\n{chunk}"}],
                "temperature": 0.1
            }

            try:
                async with session.post("https://api.groq.com/openai/v1/chat/completions", 
                                        headers={"Authorization": f"Bearer {key}"}, json=payload) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        body = data['choices'][0]['message']['content']
                        
                        # Find filename
                        f_match = re.search(r"\[FILENAME\]:\s*(.*\.txt)", body)
                        filename = f_match.group(1).strip() if f_match else f"p_{i+1}.txt"
                        
                        # Save it
                        (raw_dir / filename).write_text(body, encoding='utf-8')
                        cache[c_hash] = filename
                        cache_path.write_text(json.dumps(cache, indent=4))
                        
                        logging.info(f"✅ SUCCESS: Saved {filename}")
                        
                        # THE 30-SECOND REST
                        logging.info("🕒 Sleeping 30 seconds to stay under API limits...")
                        await asyncio.sleep(30) 
                    
                    elif resp.status == 429:
                        logging.warning("🚨 API BUSY. Waiting 60 seconds...")
                        await asyncio.sleep(60)
                    else:
                        logging.error(f"❌ API rejected request: {resp.status}")
                        await asyncio.sleep(5)
            except Exception as e:
                logging.error(f"⚠️ Connection error: {e}")
                await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())




