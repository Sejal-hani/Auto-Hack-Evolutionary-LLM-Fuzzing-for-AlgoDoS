import os
import re
import sys
import json
import hashlib
import logging
import asyncio
import shutil
from pathlib import Path
import aiohttp

# Professional Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s | AUTOMATOR | %(message)s", datefmt="%H:%M:%S")

# Directories
RAW_DIR = Path("raw_submissions")
DATASET_DIR = Path("dataset")
PYTHON_DIR = Path("python_files")
STAGING_RAW = Path("staging_raw")
STAGING_DATASET = Path("staging_dataset")

async def get_smart_meta(session, key, cpp_code):
    """AI deduces constraints and input format directly from the C++ code."""
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    prompt = f"""You are an expert C++ Competitive Programmer.
Analyze this C++ code and determine its metadata carefully.
1. Determine the algorithmic 'category' (dp, math, graph, string, greedy, sorting, bitmask, trie).
2. Deduce the HIGHLY PRECISE 'input_format'. Look extremely closely at the `cin >>` or `scanf` variables and loops in `main()`. Take your time. Describe exactly what is being read (e.g., "An integer T (test cases). For each test case: integers N and K, followed by an array of N integers, then a string S").
3. Deduce a safe 'n_constraint' (look at array sizes or loop limits, e.g., 100000 or 200000).

CODE:
{cpp_code[:3000]}

Return ONLY a JSON object exactly like this, nothing else:
{{"category": "dp", "input_format": "T test cases, then N and M, then an array A of N integers", "n_constraint": 200000, "time_ms": 2000, "mem_mb": 256}}
"""
    
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"},
        "temperature": 0.1
    }
    
    for attempt in range(4):
        try:
            async with session.post(url, headers={"Authorization": f"Bearer {key}"}, json=payload, timeout=20) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    meta = json.loads(data['choices'][0]['message']['content'])
                    # Fallbacks
                    meta['time_ms'] = meta.get('time_ms', 2000)
                    meta['mem_mb'] = meta.get('mem_mb', 256)
                    meta['n_constraint'] = meta.get('n_constraint', 100000)
                    meta['category'] = meta.get('category', 'algo').lower()
                    meta['input_format'] = meta.get('input_format', 'Unknown input format')
                    return meta
                elif resp.status == 429:
                    await asyncio.sleep(4 * (2 ** attempt))
        except Exception as e:
            await asyncio.sleep(2)
            
    return {"category": "algo", "input_format": "Generic input", "n_constraint": 100000, "time_ms": 2000, "mem_mb": 256}

def extract_pure_cpp(content: str) -> str:
    """Strips meta headers from CPP files to get pure code for hashing."""
    lines = content.split('\n')
    pure_lines = [l for l in lines if not l.startswith('// [')]
    return '\n'.join(pure_lines).strip()

def extract_code_from_txt(txt_content: str) -> str:
    """Finds the C++ code block inside a raw text file."""
    # Try finding markdown code block
    match = re.search(r'```(?:cpp|c)?\s*(.*?)\s*```', txt_content, re.DOTALL | re.IGNORECASE)
    if match: return match.group(1).strip()
    
    # Try finding after "CODE:"
    match = re.search(r'CODE:\s*(.*)', txt_content, re.DOTALL | re.IGNORECASE)
    if match: return match.group(1).strip()
    
    # Fallback to the whole text if it looks like code
    return txt_content.strip()

def get_code_hash(code: str) -> str:
    """Normalizes whitespace to ensure identical codes hash to the same value."""
    normalized = re.sub(r'\s+', ' ', code).strip()
    return hashlib.md5(normalized.encode('utf-8')).hexdigest()

def isolate_python_files():
    """Moves and renames all Python files to a separate folder."""
    PYTHON_DIR.mkdir(exist_ok=True)
    py_files = list(RAW_DIR.glob("*.py")) + list(DATASET_DIR.glob("*.py"))
    
    for py_file in py_files:
        # Strip numbers and 'victim_' prefix
        clean_name = re.sub(r'^(victim_)?\d+_', '', py_file.name)
        if clean_name == py_file.name and '_' in clean_name:
            clean_name = clean_name.split('_', 1)[-1] # try to remove prefix
            
        target_path = PYTHON_DIR / clean_name
        counter = 1
        while target_path.exists():
            target_path = PYTHON_DIR / f"{target_path.stem}_{counter}.py"
            counter += 1
            
        shutil.move(str(py_file), str(target_path))
        logging.info(f"🐍 Moved Python file: {py_file.name} -> {target_path.name}")

async def run_master_organizer():
    api_key = os.environ.get("GROQ_API_KEY_ONE") or os.environ.get("GROQ_API_KEY")
    if not api_key:
        logging.error("❌ GROQ_API_KEY_ONE is not set!")
        return

    # 1. Purge Python Files
    isolate_python_files()

    # 2. Setup Staging Directories
    if STAGING_RAW.exists(): shutil.rmtree(STAGING_RAW)
    if STAGING_DATASET.exists(): shutil.rmtree(STAGING_DATASET)
    STAGING_RAW.mkdir()
    STAGING_DATASET.mkdir()

    # Dictionary to hold our deduplicated problems
    # code_hash -> {"cpp_code": "...", "txt_content": "..."}
    problems_db = {}

    # 3. Read & Hash TXT Files
    logging.info("📥 Scanning raw TXT files...")
    for txt_file in RAW_DIR.glob("*.txt"):
        content = txt_file.read_text(encoding='utf-8', errors='ignore')
        cpp_code = extract_code_from_txt(content)
        if len(cpp_code) < 20: continue # Skip empty/invalid
        
        c_hash = get_code_hash(cpp_code)
        if c_hash not in problems_db:
            problems_db[c_hash] = {"cpp_code": cpp_code, "txt_content": content}

    # 4. Read & Hash CPP Files (From both directories)
    logging.info("📥 Scanning CPP files...")
    cpp_files = list(RAW_DIR.glob("*.cpp")) + list(DATASET_DIR.glob("*.cpp"))
    for cpp_file in cpp_files:
        content = cpp_file.read_text(encoding='utf-8', errors='ignore')
        pure_code = extract_pure_cpp(content)
        if len(pure_code) < 20: continue
        
        c_hash = get_code_hash(pure_code)
        if c_hash not in problems_db:
            # ORPHAN CPP FOUND: It has no TXT! We create a placeholder TXT content.
            orphan_txt_content = f"[FILENAME]: recovered_orphan.txt\n\n**PROBLEM STATEMENT**\nRecovered from orphan CPP file.\n\n**CODE**\n```cpp\n{pure_code}\n```"
            problems_db[c_hash] = {"cpp_code": pure_code, "txt_content": orphan_txt_content}

    logging.info(f"🧬 Deduplication complete. Found {len(problems_db)} UNIQUE problems.")

    # 5. Process with AI and Write to Staging (The 1:1 Mapping)
    async with aiohttp.ClientSession() as session:
        for index, (c_hash, data) in enumerate(problems_db.items(), start=1):
            logging.info(f"🧠 Processing Problem {index:03d}...")
            
            # Analyze code to fix/generate input format and constraints
            meta = await get_smart_meta(session, api_key, data["cpp_code"])
            
            # Build C++ Header
            header = (
                f"// [TIME_LIMIT_MS]: {meta['time_ms']}\n"
                f"// [MEMORY_LIMIT_MB]: {meta['mem_mb']}\n"
                f"// [N_CONSTRAINT]: {meta['n_constraint']}\n"
                f"// [INPUT_FORMAT]: {meta['input_format']}\n\n"
            )
            final_cpp_content = header + data["cpp_code"]
            final_txt_content = data["txt_content"] # 100% UNMODIFIED text content
            
            # Define 1:1 Filenames
            base_name = f"victim_{index:03d}_{meta['category']}"
            cpp_filename = f"{base_name}.cpp"
            txt_filename = f"{base_name}.txt"
            
            # Write to Staging
            (STAGING_DATASET / cpp_filename).write_text(final_cpp_content, encoding='utf-8')
            (STAGING_RAW / txt_filename).write_text(final_txt_content, encoding='utf-8')
            
            await asyncio.sleep(2.5) # Prevent API rate limits

    # 6. The Final Commit (Swap folders)
    logging.info("💾 Applying changes to workspace...")
    shutil.rmtree(RAW_DIR)
    shutil.rmtree(DATASET_DIR)
    
    STAGING_RAW.rename(RAW_DIR)
    STAGING_DATASET.rename(DATASET_DIR)
    
    logging.info("✅ DONE! 1:1 Mapping Restored. Bad formats fixed. Duplicates destroyed. TXT contents preserved.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_master_organizer())




    
    # import os
# import re
# import json
# import aiohttp
# import asyncio
# import logging
# from pathlib import Path

# logging.basicConfig(level=logging.INFO, format="%(asctime)s | AUTOMATOR | %(message)s", datefmt="%H:%M:%S")

# async def process_to_cpp(session, key, txt_content, filename):
#     url = "https://api.groq.com/openai/v1/chat/completions"
    
#     # This prompt tells the AI to act as a Senior Competitive Programmer
#     system_prompt = """You are a C++ Automation Tool. 
# The user will provide a Codeforces problem description and its C++ code.

# TASKS:
# 1. Extract Time Limit (convert to MS, e.g., 2.0s = 2000).
# 2. Extract Memory Limit (convert to MB).
# 3. Determine a 'Fuzzing N': If the problem N is 200,000, set N_CONSTRAINT to 10000 (enough to TLE an O(N^2) solution).
# 4. Identify the INPUT_FORMAT string.
# 5. Wrap the provided logic into a work() function and a main() function.

# OUTPUT FORMAT (Strictly C++ code starting with tags):
# // [TIME_LIMIT_MS]: <ms>
# // [MEMORY_LIMIT_MB]: <mb>
# // [N_CONSTRAINT]: <n>
# // [INPUT_FORMAT]: <format>

# #include <iostream>
# #include <vector>
# #include <algorithm>
# using namespace std;

# void work() {
#     // Wrapped logic here
# }

# int main() {
#     ios::sync_with_stdio(0); cin.tie(0);
#     work();
#     return 0;
# }
# """

#     payload = {
#         "model": "llama-3.1-70b-versatile", # Using 70B for better reasoning on constraints
#         "messages": [
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": f"Convert this problem to a fuzzer-ready C++ file:\n\n{txt_content}"}
#         ],
#         "temperature": 0.1
#     }

#     headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}

#     try:
#         async with session.post(url, headers=headers, json=payload) as resp:
#             if resp.status == 200:
#                 data = await resp.json()
#                 return data['choices'][0]['message']['content']
#             elif resp.status == 429: return "RATE"
#             else: return None
#     except Exception: return None

# async def main():
#     key = os.environ.get("GROQ_API_KEY_ONE")
#     raw_dir = Path("raw_submissions")
#     dataset_dir = Path("dataset")
#     dataset_dir.mkdir(exist_ok=True)

#     txt_files = list(raw_dir.glob("*.txt"))
#     logging.info(f"📂 Found {len(txt_files)} clean problems to automate.")

#     async with aiohttp.ClientSession() as session:
#         for txt_file in txt_files:
#             cpp_name = txt_file.stem + ".cpp"
#             if (dataset_dir / cpp_name).exists():
#                 logging.info(f"⏭️  {cpp_name} already exists. Skipping.")
#                 continue

#             logging.info(f"⚙️  Analyzing and Wrapping: {txt_file.name}...")
#             content = txt_file.read_text(encoding='utf-8')
            
#             result = await process_to_cpp(session, key, content, txt_file.name)

#             if result == "RATE":
#                 logging.warning("🚨 Rate limit! Cooling down 60s...")
#                 await asyncio.sleep(60)
#                 continue

#             if result:
#                 # Clean up markdown if the LLM accidentally added it
#                 clean_cpp = result.replace("```cpp", "").replace("```", "").strip()
#                 (dataset_dir / cpp_name).write_text(clean_cpp, encoding='utf-8')
#                 logging.info(f"✅ CREATED: dataset/{cpp_name}")
                
#                 # Safety delay between files
#                 await asyncio.sleep(25)
#             else:
#                 logging.error(f"❌ Failed logic extraction for {txt_file.name}")

# if __name__ == "__main__":
#     asyncio.run(main())




# # """
# # Stage 1: Dump to TXT Separator (Multi-Key ONE/TWO/THREE Edition).

# # Uses Llama 8B (Higher API limits), Multi-Key Round-Robin, and Staggered Launches 
# # to perfectly slice and format the massive dump without hitting Groq TPM limits.
# # """

# # import os
# # import re
# # import sys
# # import json
# # import aiohttp
# # import asyncio
# # import logging
# # import hashlib
# # from pathlib import Path

# # logging.basicConfig(level=logging.INFO, format="%(asctime)s | STAGE-1 | %(message)s", datefmt="%H:%M:%S")

# # def auto_segment_dump(raw_text: str) -> list:
# #     lines = raw_text.split('\n')
# #     split_indices = []
# #     for i, line in enumerate(lines):
# #         if "time limit per test" in line.lower() or "time limit:" in line.lower():
# #             cut_index = i
# #             for j in range(i-1, max(-1, i-6), -1):
# #                 prev_line = lines[j].strip()
# #                 if prev_line == "}" or prev_line.endswith(";") or "return" in prev_line:
# #                     cut_index = j + 1
# #                     break
# #                 if prev_line == "": cut_index = j + 1
# #             if cut_index == i: cut_index = max(0, i - 2)
# #             split_indices.append(cut_index)
            
# #     clean_indices = []
# #     for idx in split_indices:
# #         if not clean_indices or idx - clean_indices[-1] > 10:
# #             clean_indices.append(idx)
            
# #     if not clean_indices: return [raw_text]
# #     if clean_indices[0] != 0: clean_indices.insert(0, 0)
# #     clean_indices.append(len(lines))
    
# #     chunks = []
# #     for i in range(len(clean_indices) - 1):
# #         chunk = "\n".join(lines[clean_indices[i]:clean_indices[i+1]]).strip()
# #         if len(chunk) > 50: chunks.append(chunk)
# #     return chunks

# # async def process_chunk_to_txt(session: aiohttp.ClientSession, api_key: str, chunk_text: str, chunk_hash: str, index: int, delay: float):
# #     # Staggered launch to avoid sending 3 massive requests in the same millisecond
# #     await asyncio.sleep(delay)
# #     logging.info(f"🧠 Formatting New Problem #{index}...")
    
# #     system_prompt = """You are a Data Formatting Engine.
# # The user is providing a messy text chunk containing ONE Codeforces Problem and its C++ code.

# # INSTRUCTIONS:
# # 1. Generate a descriptive filename ending in .txt (e.g., "dfs_graph_trap.txt").
# # 2. Extract the Problem Statement.
# # 3. Extract the Time Limit and Memory Limit.
# # 4. Format the C++ code properly.

# # CRITICAL OUTPUT FORMAT:
# # You MUST output EXACTLY in this format, with NO markdown formatting:

# # [FILENAME]: <descriptive_name.txt>
# # [START_CONTENT]
# # PROBLEM STATEMENT:
# # <Cleaned problem description>

# # TIME LIMIT: <Exact time limit>
# # MEMORY LIMIT: <Exact memory limit>

# # CODE:
# # <Perfectly formatted C++ code>
# # [END_CONTENT]
# # """
# #     # 8B Model is used here for massive TPM (Token Per Minute) allowance!
# #     payload = {
# #         "model": "llama-3.1-8b-instant",
# #         "messages": [
# #             {"role": "system", "content": system_prompt},
# #             {"role": "user", "content": f"Format this chunk:\n\n{chunk_text}"}
# #         ],
# #         "temperature": 0.1 
# #     }

# #     for attempt in range(5):
# #         try:
# #             async with session.post("https://api.groq.com/openai/v1/chat/completions", 
# #                                     headers={"Authorization": f"Bearer {api_key}"}, json=payload) as response:
# #                 if response.status == 200:
# #                     data = await response.json()
# #                     res_text = data['choices'][0]['message']['content'].strip()
                    
# #                     filename_match = re.search(r"\[FILENAME\]:\s*(.+?\.txt)", res_text)
# #                     content_match = re.search(r"\[START_CONTENT\](.*?)\[END_CONTENT\]", res_text, re.DOTALL)
                    
# #                     if filename_match and content_match:
# #                         filename = filename_match.group(1).strip()
# #                         clean_content = content_match.group(1).strip()
                        
# #                         out_path = Path("raw_submissions") / filename
# #                         out_path.parent.mkdir(parents=True, exist_ok=True)
# #                         out_path.write_text(clean_content, encoding='utf-8')
                        
# #                         logging.info(f"✅ SUCCESS: Saved {filename}")
# #                         return (chunk_hash, filename)
# #                     else:
# #                         logging.warning(f"⚠️ [Problem {index}]: Format deviation. Retrying...")
# #                         continue
# #                 elif response.status == 429:
# #                     wait_time = 5.0 * (2 ** attempt)
# #                     logging.warning(f"⏳ Rate Limit hit for Problem {index}. Waiting {wait_time}s...")
# #                     await asyncio.sleep(wait_time)
# #                 else:
# #                     return None
# #         except Exception:
# #             await asyncio.sleep(2.0)
# #     logging.error(f"❌ Failed to process Problem {index} after maximum attempts.")
# #     return None

# # async def run_stage_1():
# #     # LOADING YOUR SPECIFIC ONE, TWO, THREE KEYS
# #     master_key = os.environ.get("GROQ_API_KEY") # Fallback just in case
# #     keys = [
# #         os.environ.get("GROQ_API_KEY_ONE", master_key),
# #         os.environ.get("GROQ_API_KEY_TWO", master_key),
# #         os.environ.get("GROQ_API_KEY_THREE", master_key)
# #     ]
    
# #     valid_keys = [k for k in keys if k]
# #     if not valid_keys:
# #         logging.error("CRITICAL: Set GROQ_API_KEY_ONE in your terminal!")
# #         return

# #     dump_file = Path("massive_dump.txt")
# #     if not dump_file.exists():
# #         logging.error("CRITICAL: 'massive_dump.txt' not found!")
# #         return

# #     raw_text = dump_file.read_text(encoding='utf-8')
# #     valid_chunks = auto_segment_dump(raw_text)
    
# #     if not valid_chunks:
# #         logging.error("No valid problems found.")
# #         return

# #     cache_file = Path(".stage1_cache.json")
# #     cache = json.loads(cache_file.read_text()) if cache_file.exists() else {}
    
# #     unprocessed_chunks = []
# #     for idx, chunk in enumerate(valid_chunks):
# #         chunk_hash = hashlib.md5(chunk.encode('utf-8')).hexdigest()
# #         if chunk_hash in cache and (Path("raw_submissions") / cache[chunk_hash]).exists():
# #             logging.info(f"⏭️ Skipping Problem #{idx+1} (Already saved)")
# #         else:
# #             unprocessed_chunks.append((chunk, chunk_hash, idx+1))

# #     if not unprocessed_chunks:
# #         logging.info("🎉 All problems in the dump file are already processed!")
# #         return

# #     logging.info(f"🚀 INITIATING STAGE 1: Processing {len(unprocessed_chunks)} NEW problems...")

# #     BATCH_SIZE = len(valid_keys) # Dynamically matches how many keys you provided
# #     COOLDOWN_SEC = 20 # 20 seconds cooldown to safely refresh the free tier limits

# #     async with aiohttp.ClientSession() as session:
# #         for i in range(0, len(unprocessed_chunks), BATCH_SIZE):
# #             batch = unprocessed_chunks[i : i + BATCH_SIZE]
# #             logging.info(f"\n{'='*40}\n⚙️  STARTING BATCH {i//BATCH_SIZE + 1}\n{'='*40}")
            
# #             tasks = []
# #             for j, (chunk_text, chunk_hash, original_idx) in enumerate(batch):
# #                 key = valid_keys[j % len(valid_keys)]
# #                 delay = j * 2.0 # 2-second stagger between each request
# #                 tasks.append(process_chunk_to_txt(session, key, chunk_text, chunk_hash, original_idx, delay))
                
# #             results = await asyncio.gather(*tasks)
            
# #             for res in results:
# #                 if res:
# #                     c_hash, c_filename = res
# #                     cache[c_hash] = c_filename
# #             cache_file.write_text(json.dumps(cache, indent=4))
            
# #             if i + BATCH_SIZE < len(unprocessed_chunks):
# #                 logging.info(f"💤 Batch complete. Sleeping for {COOLDOWN_SEC} seconds...")
# #                 await asyncio.sleep(COOLDOWN_SEC)
        
# #     logging.info("\n🎉 STAGE 1 COMPLETE. New files added to raw_submissions/!")

# # if __name__ == "__main__":
# #     if sys.platform == 'win32':
# #         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# #     asyncio.run(run_stage_1())




# # # """
# # # STAGE 2: CF-Fuzz Taxonomic Dataset Automator (Smart-Skip & Batch Cooldown Edition).

# # # Reads formatted .txt files from raw_submissions/.
# # # Extracts limits, calculates N_CONSTRAINT, and categorizes into dataset/ subfolders.
# # # Uses Smart-Skip caching to NEVER re-process a successful file, and Batch Cooldowns to bypass rate limits.
# # # """

# # # import os
# # # import re
# # # import sys
# # # import json
# # # import aiohttp
# # # import asyncio
# # # import logging
# # # from pathlib import Path

# # # CURRENT_DIR = Path(__file__).resolve().parent
# # # ROOT_DIR = CURRENT_DIR
# # # while not (ROOT_DIR / "requirements.txt").exists() and ROOT_DIR.parent != ROOT_DIR:
# # #     ROOT_DIR = ROOT_DIR.parent

# # # logging.basicConfig(level=logging.INFO, format="%(asctime)s | STAGE-2 | %(message)s", datefmt="%H:%M:%S")

# # # async def process_raw_file(session: aiohttp.ClientSession, api_key: str, txt_path: Path):
# # #     raw_content = txt_path.read_text(encoding='utf-8')
# # #     logging.info(f"🧠 Analyzing limits and category for: {txt_path.name}...")

# # #     system_prompt = """You are an expert Competitive Programming Architect.
# # # The user is providing a text file containing a Codeforces Problem Description and a vulnerable C++ submission.

# # # INSTRUCTIONS:
# # # 1. Determine the CATEGORY (e.g., Graphs, HashMaps, Strings, Sorting, Math, Greedy).
# # # 2. Extract Time Limit and convert to MILLISECONDS (e.g., "4.5 seconds" -> 4500). Default to 2000.
# # # 3. Extract Memory Limit and convert to MEGABYTES (e.g., "512 megabytes" -> 512). Default to 256.
# # # 4. Calculate a safe [N_CONSTRAINT] to trigger AlgoDoS.
# # # 5. Formulate the [INPUT_FORMAT] (precise description of how to print the input).
# # # 6. Create a descriptive filename ending in .cpp (e.g., "quicksort_pivot.cpp").

# # # CRITICAL OUTPUT FORMAT:
# # # You MUST output EXACTLY in this format:

# # # [CATEGORY]: <Category_Name>
# # # [FILENAME]: <descriptive_name.cpp>
# # # [CODE_START]
# # # // [CATEGORY]: <Category_Name>
# # # // [TIME_LIMIT_MS]: <time_in_ms>
# # # // [MEMORY_LIMIT_MB]: <memory_in_mb>
# # # // [N_CONSTRAINT]: <exact_number>
# # # // [INPUT_FORMAT]: <precise_description>
# # # <the fixed C++ code starts here>
# # # [CODE_END]
# # # """

# # #     payload = {
# # #         "model": "llama-3.3-70b-versatile",
# # #         "messages": [
# # #             {"role": "system", "content": system_prompt},
# # #             {"role": "user", "content": f"Here is the problem and code:\n\n{raw_content}"}
# # #         ],
# # #         "temperature": 0.1 
# # #     }

# # #     for attempt in range(5):
# # #         try:
# # #             async with session.post("https://api.groq.com/openai/v1/chat/completions", 
# # #                                     headers={"Authorization": f"Bearer {api_key}"}, json=payload) as response:
# # #                 if response.status == 200:
# # #                     data = await response.json()
# # #                     res_text = data['choices'][0]['message']['content'].strip()
                    
# # #                     cat_match = re.search(r"\[CATEGORY\]:\s*(.+)", res_text)
# # #                     filename_match = re.search(r"\[FILENAME\]:\s*(.+?\.cpp)", res_text)
# # #                     code_match = re.search(r"\[CODE_START\](.*?)\[CODE_END\]", res_text, re.DOTALL)
                    
# # #                     if cat_match and filename_match and code_match:
# # #                         folder_name = re.sub(r'[^a-zA-Z0-9]', '_', cat_match.group(1).strip()).lower()
# # #                         filename = filename_match.group(1).strip()
# # #                         clean_code = code_match.group(1).strip()
                        
# # #                         if clean_code.startswith("```cpp"): clean_code = clean_code[6:].strip()
# # #                         if clean_code.endswith("```"): clean_code = clean_code[:-3].strip()
                        
# # #                         out_path = ROOT_DIR / "dataset" / folder_name / filename
# # #                         out_path.parent.mkdir(parents=True, exist_ok=True)
# # #                         out_path.write_text(clean_code, encoding='utf-8')
                        
# # #                         logging.info(f"✅ SUCCESS: Spawned {filename} in dataset/{folder_name}/")
# # #                         return txt_path.name # Return the name of the txt file so we can cache it as a success!
# # #                     else:
# # #                         logging.warning(f"⚠️ [{txt_path.name}]: LLM format deviation. Retrying...")
# # #                         continue
# # #                 elif response.status == 429:
# # #                     wait_time = 4.0 * (2 ** attempt)
# # #                     logging.warning(f"⏳ Rate Limit hit for {txt_path.name}. Waiting {wait_time}s...")
# # #                     await asyncio.sleep(wait_time)
# # #                 else:
# # #                     return None
# # #         except Exception:
# # #             await asyncio.sleep(2)
            
# # #     logging.error(f"❌ Failed to process {txt_path.name}")
# # #     return None

# # # async def run_automator():
# # #     api_key = os.environ.get("GROQ_API_KEY")
# # #     if not api_key:
# # #         logging.error("CRITICAL: Set GROQ_API_KEY first!")
# # #         return

# # #     raw_dir = ROOT_DIR / "raw_submissions"
# # #     raw_dir.mkdir(parents=True, exist_ok=True)
    
# # #     txt_files = list(raw_dir.glob("*.txt"))
# # #     if not txt_files:
# # #         logging.error(f"No .txt files found in '{raw_dir}'. Run Stage 1 first!")
# # #         return

# # #     # --- CACHE LOGIC: REMEMBER SUCCESSES ---
# # #     cache_file = ROOT_DIR / ".stage2_cache.json"
# # #     processed_files = set(json.loads(cache_file.read_text())) if cache_file.exists() else set()
    
# # #     unprocessed_files = [f for f in txt_files if f.name not in processed_files]
    
# # #     if len(unprocessed_files) < len(txt_files):
# # #         logging.info(f"⏭️ Skipped {len(txt_files) - len(unprocessed_files)} files that were already successfully formatted.")

# # #     if not unprocessed_files:
# # #         logging.info("🎉 All .txt files have already been successfully processed into dataset/!")
# # #         return

# # #     logging.info(f"🚀 INITIATING STAGE 2: Converting {len(unprocessed_files)} NEW files into C++ targets...")

# # #     # --- BATCH COOLDOWN LOGIC ---
# # #     BATCH_SIZE = 4
# # #     COOLDOWN_SEC = 25

# # #     async with aiohttp.ClientSession() as session:
# # #         for i in range(0, len(unprocessed_files), BATCH_SIZE):
# # #             batch = unprocessed_files[i : i + BATCH_SIZE]
# # #             logging.info(f"\n{'='*40}\n⚙️  STARTING BATCH {i//BATCH_SIZE + 1} (Processing {len(batch)} files)\n{'='*40}")
            
# # #             tasks = [process_raw_file(session, api_key, txt_file) for txt_file in batch]
# # #             results = await asyncio.gather(*tasks)
            
# # #             # Save successful files to cache immediately
# # #             for res in results:
# # #                 if res:
# # #                     processed_files.add(res)
# # #             cache_file.write_text(json.dumps(list(processed_files), indent=4))
            
# # #             # Trigger cooldown
# # #             if i + BATCH_SIZE < len(unprocessed_files):
# # #                 logging.info(f"💤 Batch complete. Sleeping for {COOLDOWN_SEC} seconds to reset API limits...")
# # #                 for remaining in range(COOLDOWN_SEC, 0, -5):
# # #                     logging.info(f"   ... resuming in {remaining} seconds")
# # #                     await asyncio.sleep(min(5, remaining))
        
# # #     logging.info("🎉 STAGE 2 COMPLETE. Check your dataset/ folder!")

# # # if __name__ == "__main__":
# # #     if sys.platform == 'win32':
# # #         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# # #     asyncio.run(run_automator())


# # # # """
# # # # CF-Fuzz Batch Dataset Automator (Throttled API Edition).

# # # # Reads raw text files containing Codeforces Problem Descriptions + C++ Code.
# # # # Uses an asyncio.Semaphore to prevent Groq API Rate Limit crashes (Thundering Herd problem).
# # # # Skips already formatted files to save API tokens.
# # # # """

# # # # import os
# # # # import sys
# # # # import aiohttp
# # # # import asyncio
# # # # import logging
# # # # from pathlib import Path

# # # # logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s", datefmt="%H:%M:%S")

# # # # async def process_raw_file(session: aiohttp.ClientSession, api_key: str, txt_path: Path, semaphore: asyncio.Semaphore):
# # # #     # 1. SMART SKIP: If we already formatted this file, don't waste API calls!
# # # #     output_name = txt_path.stem + ".cpp"
# # # #     out_path = Path("dataset") / output_name
# # # #     if out_path.exists():
# # # #         logging.info(f"⏭️ Skipping {txt_path.name} (Already formatted in dataset/)")
# # # #         return

# # # #     # 2. THROTTLE: Wait for permission to use the API (max 3 at a time)
# # # #     async with semaphore:
# # # #         raw_content = txt_path.read_text(encoding='utf-8')
# # # #         logging.info(f"🧠 Analyzing: {txt_path.name}...")

# # # #         system_prompt = """You are an expert Competitive Programming Architect.
# # # # The user is giving you a text containing BOTH a Codeforces Problem Description and a vulnerable C++ submission.
# # # # Your job is to format it for our Automated Fuzzer.

# # # # INSTRUCTIONS:
# # # # 1. Read the Problem Description to find the EXACT input format and the MAX limits (e.g., if n <= 2*10^5, the max limit is 200000).
# # # # 2. Set the [N_CONSTRAINT] comment to that exact maximum limit.
# # # # 3. Set the [INPUT_FORMAT] comment to precisely describe the input structure based on the Problem Description.
# # # # 4. Extract the exact Time Limit from the text and convert it to MILLISECONDS (e.g., "4.5 seconds" -> 4500, "1 second" -> 1000). Default to 2000.
# # # # 5. Extract the exact Memory Limit from the text and convert it to MEGABYTES (e.g., "512 megabytes" -> 512). Default to 256.
# # # # 6. Output ONLY the fixed C++ code. Make sure the code reads the input cleanly in main(). Do NOT output markdown blocks, just the raw code.

# # # # OUTPUT FORMAT MUST START EXACTLY LIKE THIS:
# # # # // [TIME_LIMIT_MS]: <time_in_ms>
# # # # // [MEMORY_LIMIT_MB]: <memory_in_mb>
# # # # // [N_CONSTRAINT]: <exact_number>
# # # # // [INPUT_FORMAT]: <precise_description>
# # # # #include <iostream>
# # # # ... rest of code ..."""

# # # #         payload = {
# # # #             "model": "llama-3.3-70b-versatile",
# # # #             "messages": [
# # # #                 {"role": "system", "content": system_prompt},
# # # #                 {"role": "user", "content": f"Here is the problem and code:\n\n{raw_content}"}
# # # #             ],
# # # #             "temperature": 0.1 
# # # #         }

# # # #         # Increased to 6 retries with a longer wait time to survive Groq's 1-minute timeout penalty
# # # #         max_retries = 6 
# # # #         for attempt in range(max_retries):
# # # #             try:
# # # #                 async with session.post("https://api.groq.com/openai/v1/chat/completions", 
# # # #                                         headers={"Authorization": f"Bearer {api_key}"}, json=payload) as response:
# # # #                     if response.status == 200:
# # # #                         data = await response.json()
# # # #                         clean_code = data['choices'][0]['message']['content'].strip()
                        
# # # #                         if clean_code.startswith("```cpp"):
# # # #                             clean_code = clean_code[6:-3].strip()
# # # #                         elif clean_code.startswith("```"):
# # # #                             clean_code = clean_code[3:-3].strip()

# # # #                         out_path.parent.mkdir(exist_ok=True)
# # # #                         out_path.write_text(clean_code, encoding='utf-8')
                        
# # # #                         logging.info(f"✅ SUCCESS: Formatted and saved {output_name}")
# # # #                         return
# # # #                     elif response.status == 429:
# # # #                         wait_time = 3.0 * (2 ** attempt) # Waits 3s, 6s, 12s, 24s...
# # # #                         logging.warning(f"⏳ Rate Limit Hit for {txt_path.name}. Retrying in {wait_time}s...")
# # # #                         await asyncio.sleep(wait_time)
# # # #                     else:
# # # #                         logging.error(f"❌ API Error on {txt_path.name}: {await response.text()}")
# # # #                         return
# # # #             except Exception as e:
# # # #                 await asyncio.sleep(3)
                
# # # #         logging.error(f"❌ Failed to process {txt_path.name} after {max_retries} attempts.")

# # # # async def run_automator():
# # # #     api_key = os.environ.get("GROQ_API_KEY")
# # # #     if not api_key:
# # # #         logging.error("CRITICAL: Set your GROQ_API_KEY in the terminal first!")
# # # #         return

# # # #     raw_dir = Path("raw_submissions")
# # # #     raw_dir.mkdir(exist_ok=True)
    
# # # #     txt_files = list(raw_dir.glob("*.txt"))
# # # #     if not txt_files:
# # # #         logging.error("No .txt files found in 'raw_submissions/'. Please add your problems there.")
# # # #         return

# # # #     logging.info(f"🚀 Found {len(txt_files)} raw submissions. Booting Throttled Automator...")

# # # #     # Set the Semaphore to 3. This means only 3 files will hit the Groq API at the exact same time.
# # # #     semaphore = asyncio.Semaphore(3)

# # # #     async with aiohttp.ClientSession() as session:
# # # #         tasks = [process_raw_file(session, api_key, txt_file, semaphore) for txt_file in txt_files]
# # # #         await asyncio.gather(*tasks)
        
# # # #     logging.info("🎉 All datasets formatted and moved to dataset/ folder perfectly.")

# # # # if __name__ == "__main__":
# # # #     if sys.platform == 'win32':
# # # #         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# # # #     asyncio.run(run_automator())





# # # # # """
# # # # # CF-Fuzz Batch Dataset Automator (Time Limit & Memory Limit Edition).

# # # # # Reads raw text files containing Codeforces Problem Descriptions + C++ Code.
# # # # # Uses Groq Llama-3 to automatically extract the exact constraints, time limits, memory limits, and format the C++ files.
# # # # # Saves production-ready targets into the dataset/ directory.
# # # # # """

# # # # # import os
# # # # # import sys
# # # # # import aiohttp
# # # # # import asyncio
# # # # # import logging
# # # # # from pathlib import Path

# # # # # logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s", datefmt="%H:%M:%S")

# # # # # async def process_raw_file(session: aiohttp.ClientSession, api_key: str, txt_path: Path):
# # # # #     raw_content = txt_path.read_text(encoding='utf-8')
# # # # #     logging.info(f"🧠 Analyzing: {txt_path.name}...")

# # # # #     system_prompt = """You are an expert Competitive Programming Architect.
# # # # # The user is giving you a text containing BOTH a Codeforces Problem Description and a vulnerable C++ submission.
# # # # # Your job is to format it for our Automated Fuzzer.

# # # # # INSTRUCTIONS:
# # # # # 1. Read the Problem Description to find the EXACT input format and the MAX limits (e.g., if n <= 2*10^5, the max limit is 200000).
# # # # # 2. Set the [N_CONSTRAINT] comment to that exact maximum limit.
# # # # # 3. Set the [INPUT_FORMAT] comment to precisely describe the input structure based on the Problem Description (e.g., "Three integers N N N, followed by 3 arrays of size N").
# # # # # 4. Extract the exact Time Limit from the text and convert it to MILLISECONDS (e.g., "4.5 seconds" -> 4500, "1 second" -> 1000). If not explicitly stated, default to 2000.
# # # # # 5. Extract the exact Memory Limit from the text and convert it to MEGABYTES (e.g., "512 megabytes" -> 512). If not explicitly stated, default to 256.
# # # # # 6. Output ONLY the fixed C++ code. Make sure the code reads the input cleanly in main(). Do NOT output any markdown blocks like ```cpp, just the raw code.

# # # # # OUTPUT FORMAT MUST START EXACTLY LIKE THIS:
# # # # # // [TIME_LIMIT_MS]: <time_in_ms>
# # # # # // [MEMORY_LIMIT_MB]: <memory_in_mb>
# # # # # // [N_CONSTRAINT]: <exact_number>
# # # # # // [INPUT_FORMAT]: <precise_description>
# # # # # #include <iostream>
# # # # # ... rest of code ..."""

# # # # #     payload = {
# # # # #         "model": "llama-3.3-70b-versatile",
# # # # #         "messages": [
# # # # #             {"role": "system", "content": system_prompt},
# # # # #             {"role": "user", "content": f"Here is the problem and code:\n\n{raw_content}"}
# # # # #         ],
# # # # #         "temperature": 0.1 # Very low temperature for maximum logical precision
# # # # #     }

# # # # #     max_retries = 3
# # # # #     for attempt in range(max_retries):
# # # # #         try:
# # # # #             async with session.post("https://api.groq.com/openai/v1/chat/completions", 
# # # # #                                     headers={"Authorization": f"Bearer {api_key}"}, json=payload) as response:
# # # # #                 if response.status == 200:
# # # # #                     data = await response.json()
# # # # #                     clean_code = data['choices'][0]['message']['content'].strip()
                    
# # # # #                     # Strip markdown if the LLM hallucinated it
# # # # #                     if clean_code.startswith("```cpp"):
# # # # #                         clean_code = clean_code[6:-3].strip()
# # # # #                     elif clean_code.startswith("```"):
# # # # #                         clean_code = clean_code[3:-3].strip()

# # # # #                     # Save to dataset folder (keeps the original text file's name)
# # # # #                     output_name = txt_path.stem + ".cpp"
# # # # #                     out_path = Path("dataset") / output_name
# # # # #                     out_path.parent.mkdir(exist_ok=True)
# # # # #                     out_path.write_text(clean_code, encoding='utf-8')
                    
# # # # #                     logging.info(f"✅ SUCCESS: Formatted and saved {output_name}")
# # # # #                     return
# # # # #                 elif response.status == 429:
# # # # #                     await asyncio.sleep(2 ** attempt)
# # # # #                 else:
# # # # #                     logging.error(f"❌ API Error on {txt_path.name}: {await response.text()}")
# # # # #                     return
# # # # #         except Exception as e:
# # # # #             await asyncio.sleep(2)
            
# # # # #     logging.error(f"❌ Failed to process {txt_path.name} after multiple attempts.")

# # # # # async def run_automator():
# # # # #     api_key = os.environ.get("GROQ_API_KEY")
# # # # #     if not api_key:
# # # # #         logging.error("CRITICAL: Set your GROQ_API_KEY in the terminal first!")
# # # # #         return

# # # # #     raw_dir = Path("raw_submissions")
# # # # #     raw_dir.mkdir(exist_ok=True)
    
# # # # #     txt_files = list(raw_dir.glob("*.txt"))
# # # # #     if not txt_files:
# # # # #         logging.error("No .txt files found in 'raw_submissions/'. Please add your problems there.")
# # # # #         return

# # # # #     logging.info(f"🚀 Found {len(txt_files)} raw submissions. Booting Llama-3 Automator...")

# # # # #     async with aiohttp.ClientSession() as session:
# # # # #         # Process all text files simultaneously
# # # # #         tasks = [process_raw_file(session, api_key, txt_file) for txt_file in txt_files]
# # # # #         await asyncio.gather(*tasks)
        
# # # # #     logging.info("🎉 All datasets formatted and moved to dataset/ folder perfectly.")

# # # # # if __name__ == "__main__":
# # # # #     if sys.platform == 'win32':
# # # # #         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# # # # #     asyncio.run(run_automator())

# # # # # # """
# # # # # # CF-Fuzz Batch Dataset Automator.

# # # # # # Reads raw text files containing Codeforces Problem Descriptions + C++ Code.
# # # # # # Uses Groq Llama-3 to automatically extract the exact constraints and format the C++ files.
# # # # # # Saves production-ready targets into the dataset/ directory.
# # # # # # """

# # # # # # import os
# # # # # # import sys
# # # # # # import aiohttp
# # # # # # import asyncio
# # # # # # import logging
# # # # # # from pathlib import Path

# # # # # # logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s", datefmt="%H:%M:%S")

# # # # # # async def process_raw_file(session: aiohttp.ClientSession, api_key: str, txt_path: Path):
# # # # # #     raw_content = txt_path.read_text(encoding='utf-8')
# # # # # #     logging.info(f"🧠 Analyzing: {txt_path.name}...")

# # # # # #     system_prompt = """You are an expert Competitive Programming Architect.
# # # # # # The user is giving you a text containing BOTH a Codeforces Problem Description and a vulnerable C++ submission.
# # # # # # Your job is to format it for our Automated Fuzzer.

# # # # # # INSTRUCTIONS:
# # # # # # 1. Read the Problem Description to find the EXACT input format and the MAX limits (e.g., if n <= 2*10^5, the max limit is 200000).
# # # # # # 2. Set the [N_CONSTRAINT] comment to that exact maximum limit.
# # # # # # 3. Set the [INPUT_FORMAT] comment to precisely describe the input structure based on the Problem Description (e.g., "Three integers N N N, followed by 3 arrays of size N").
# # # # # # 4. Output ONLY the fixed C++ code. Make sure the code reads the input cleanly in main(). Do NOT output any markdown blocks like ```cpp, just the raw code.

# # # # # # OUTPUT FORMAT MUST START EXACTLY LIKE THIS:
# # # # # # // [N_CONSTRAINT]: <exact_number>
# # # # # # // [INPUT_FORMAT]: <precise_description>
# # # # # # #include <iostream>
# # # # # # ... rest of code ..."""

# # # # # #     payload = {
# # # # # #         "model": "llama-3.3-70b-versatile",
# # # # # #         "messages": [
# # # # # #             {"role": "system", "content": system_prompt},
# # # # # #             {"role": "user", "content": f"Here is the problem and code:\n\n{raw_content}"}
# # # # # #         ],
# # # # # #         "temperature": 0.1 # Very low temperature for maximum logical precision
# # # # # #     }

# # # # # #     max_retries = 3
# # # # # #     for attempt in range(max_retries):
# # # # # #         try:
# # # # # #             async with session.post("https://api.groq.com/openai/v1/chat/completions", 
# # # # # #                                     headers={"Authorization": f"Bearer {api_key}"}, json=payload) as response:
# # # # # #                 if response.status == 200:
# # # # # #                     data = await response.json()
# # # # # #                     clean_code = data['choices'][0]['message']['content'].strip()
                    
# # # # # #                     # Strip markdown if the LLM hallucinated it
# # # # # #                     if clean_code.startswith("```cpp"):
# # # # # #                         clean_code = clean_code[6:-3].strip()
# # # # # #                     elif clean_code.startswith("```"):
# # # # # #                         clean_code = clean_code[3:-3].strip()

# # # # # #                     # Save to dataset folder
# # # # # #                     output_name = txt_path.stem + ".cpp"
# # # # # #                     out_path = Path("dataset") / output_name
# # # # # #                     out_path.parent.mkdir(exist_ok=True)
# # # # # #                     out_path.write_text(clean_code, encoding='utf-8')
                    
# # # # # #                     logging.info(f"✅ SUCCESS: Formatted and saved {output_name}")
# # # # # #                     return
# # # # # #                 elif response.status == 429:
# # # # # #                     await asyncio.sleep(2 ** attempt)
# # # # # #                 else:
# # # # # #                     logging.error(f"❌ API Error on {txt_path.name}: {await response.text()}")
# # # # # #                     return
# # # # # #         except Exception as e:
# # # # # #             await asyncio.sleep(2)
            
# # # # # #     logging.error(f"❌ Failed to process {txt_path.name} after multiple attempts.")

# # # # # # async def run_automator():
# # # # # #     api_key = os.environ.get("GROQ_API_KEY")
# # # # # #     if not api_key:
# # # # # #         logging.error("CRITICAL: Set your GROQ_API_KEY in the terminal first!")
# # # # # #         return

# # # # # #     raw_dir = Path("raw_submissions")
# # # # # #     raw_dir.mkdir(exist_ok=True)
    
# # # # # #     txt_files = list(raw_dir.glob("*.txt"))
# # # # # #     if not txt_files:
# # # # # #         logging.error("No .txt files found in 'raw_submissions/'. Please add your problems there.")
# # # # # #         return

# # # # # #     logging.info(f"🚀 Found {len(txt_files)} raw submissions. Booting Llama-3 Automator...")

# # # # # #     async with aiohttp.ClientSession() as session:
# # # # # #         # Process all text files simultaneously
# # # # # #         tasks = [process_raw_file(session, api_key, txt_file) for txt_file in txt_files]
# # # # # #         await asyncio.gather(*tasks)
        
# # # # # #     logging.info("🎉 All datasets formatted and moved to dataset/ folder perfectly.")

# # # # # # if __name__ == "__main__":
# # # # # #     if sys.platform == 'win32':
# # # # # #         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# # # # # #     asyncio.run(run_automator())