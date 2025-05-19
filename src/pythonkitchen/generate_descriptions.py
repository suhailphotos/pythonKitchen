# generate_descriptions.py

import os
import re
import json
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd
import openai
from dotenv import load_dotenv

# —————————————————————————————
# HELPER: Determine package name dynamically
# —————————————————————————————
def get_package_name() -> str:
    if __package__:
        return __package__.split('.')[0]
    return Path(__file__).resolve().parent.name

PACKAGE_NAME = get_package_name()

# —————————————————————————————
# CONFIGURE ENV-FILE LOADING
# —————————————————————————————
GLOBAL_ENV_FILE = globals().get("GLOBAL_ENV_FILE", [])
_loaded = False
for env_path in GLOBAL_ENV_FILE:
    p = Path(env_path)
    if p.is_file():
        load_dotenv(dotenv_path=p)
        _loaded = True
        break
if not _loaded:
    p = Path.home() / f".{PACKAGE_NAME}" / ".env"
    if p.is_file():
        load_dotenv(dotenv_path=p)
        _loaded = True
if not _loaded:
    load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("OPENAI_API_KEY not found in environment or .env file")

# —————————————————————————————
# HELPER: Extract a clean lesson name from the URL
# —————————————————————————————
def extract_lesson_name(url: str) -> str:
    path = urlparse(url).path.rstrip('/')
    last = path.split('/')[-1]
    no_pref = re.sub(r'^\d+[_-]?', '', last)
    no_suf = re.sub(r'[-_]\d+$', '', no_pref)
    text = re.sub(r'[-_]+', ' ', no_suf).strip()
    return text.title()

# —————————————————————————————
# DESCRIPTION GENERATOR HELPER
# —————————————————————————————
def generate_lesson_description(chapter_desc: str, lesson_name: str) -> str:
    system = {
        "role": "system",
        "content": (
            "You are a documentation assistant.  "
            "Your job is to write a **two-sentence**, purely factual description of a *single* lesson.  "
            "Only use the chapter description if it directly informs this lesson; "
            "otherwise, ignore it and focus solely on the lesson title.  "
            "Never repeat unrelated chapter-level topics, and do not use any marketing language."
        )
    }
    user = {
        "role": "user",
        "content": (
            f"Chapter context (for reference only):\n{chapter_desc}\n\n"
            f"Lesson title:\n{lesson_name}\n\n"
            "Based on the lesson title (and chapter context *only if relevant*), "
            "write a concise, two-sentence description."
        )
    }
    resp = openai.chat.completions.create(
        model="gpt-4o",
        messages=[system, user],
        max_completion_tokens=100,
    )
    return resp.choices[0].message.content.strip()

# —————————————————————————————
# ENTRYPOINT: LOAD JSON & CSV, GENERATE DESCRIPTIONS
# —————————————————————————————
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate lesson descriptions based on chapter JSON and lessons.csv"
    )
    parser.add_argument(
        "chapters_json",
        help="Path to the JSON file containing chapter descriptions"
    )
    parser.add_argument(
        "lessons_csv",
        help="Path to the CSV file listing lessons with 'chapter_index' and 'link'"
    )
    parser.add_argument(
        "-o", "--output",
        default="lessons_with_descriptions.csv",
        help="Output CSV path"
    )
    parser.add_argument(
        "-r", "--range",
        help="Optional chapter range to process (e.g. 2-3)",
        default=None
    )
    args = parser.parse_args()

    # load chapter JSON
    data = json.loads(Path(args.chapters_json).read_text())
    chap_map = {}
    for chap in data.get("chapters", []):
        idx_match = re.search(r"\d+", chap.get("name", ""))
        if idx_match:
            idx = int(idx_match.group())
            # use full_description for context
            desc = chap.get("full_description", "")
            chap_map[idx] = desc

    # load lessons.csv
    df = pd.read_csv(args.lessons_csv)
    # ensure link column is string to avoid NaN float errors
    df['link'] = df['link'].fillna('').astype(str)
    # only extract name if not already present or empty
    if 'name' not in df.columns:
        df['name'] = df['link'].apply(extract_lesson_name)
    else:
        df['name'] = df['name'].fillna(df['link'].apply(extract_lesson_name))

    # parse optional range
    allowed = None
    if args.range:
        m = re.match(r"^(\d+)-(\d+)$", args.range)
        if not m:
            raise ValueError("Range must be in format N-M")
        start, end = map(int, m.groups())
        allowed = set(range(start, end + 1))

    # generate descriptions
    descriptions = []
    for _, row in df.iterrows():
        # safely parse chapter_index, skip if invalid
        raw_idx = row.get('chapter_index')
        try:
            chap_idx = int(raw_idx)
        except (ValueError, TypeError):
            descriptions.append("")
            continue
        chap_idx = int(row['chapter_index'])
        if chap_idx is not None and (allowed is None or chap_idx in allowed):
            chapter_desc = chap_map.get(chap_idx, "")
            lesson_name = row['name']
            descriptions.append(
                generate_lesson_description(chapter_desc, lesson_name)
            )
        else:
            descriptions.append("")

    # save output
    df['description'] = descriptions
    df[['name', 'description', 'link']].to_csv(args.output, index=False)
    print(f"Saved {len(df)} lessons to {args.output}")

