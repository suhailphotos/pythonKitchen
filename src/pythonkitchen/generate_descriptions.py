# generate_descriptions.py

import os
import re
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

# 1) Check any explicitly listed .env paths
for env_path in GLOBAL_ENV_FILE:
    p = Path(env_path)
    if p.is_file():
        load_dotenv(dotenv_path=p)
        _loaded = True
        break

# 2) Fallback to ~/.<package_name>/.env
if not _loaded:
    p = Path.home() / f".{PACKAGE_NAME}" / ".env"
    if p.is_file():
        load_dotenv(dotenv_path=p)
        _loaded = True

# 3) Final fallback: default lookup (cwd & parent dirs)
if not _loaded:
    load_dotenv()

# 4) Read the API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("OPENAI_API_KEY not found in environment or .env file")

# —————————————————————————————
# STATIC CHAPTER (WEEK) DESCRIPTIONS
# —————————————————————————————
chapter_descriptions = {
    1: "Introduction to AI/ML fundamentals, essential tools, hardware, calculus, linear algebra, and basic Python environments.",
    2: "Foundations of production-level code, GPU programming, data structures, tensors, and virtual environments like Houdini.",
    3: "Data pipelines with web scraping, MLOps basics, Pandas, Matplotlib, Seaborn, and exploratory data analysis techniques.",
    4: "Supervised learning foundations, linear regression, evaluation metrics, and machine learning model building in Houdini.",
    5: "Advanced ML with bias-variance tradeoff, supervised and unsupervised learning, feature engineering, and SVM techniques.",
    6: "Unsupervised learning deep dive into clustering, PCA, recommender systems, DBscan, and advanced data visualization.",
    7: "Deep learning introduction covering neural networks, activation functions, backpropagation, and CNNs inside Houdini.",
    8: "Hands-on ML frameworks with TensorFlow, PyTorch, cloud-based training, CUDA acceleration, and production modeling.",
    9: "Advanced MLOps with Docker, system design, transfer learning, model optimization, and hardware acceleration strategies.",
    10: "Exploring NLP architectures, LLMs, generative AI, computer vision, prompt engineering, and ML for Houdini pipelines.",
}

# —————————————————————————————
# HELPER: Extract a clean lesson name from the URL
# —————————————————————————————
def extract_lesson_name(url: str) -> str:
    path     = urlparse(url).path.rstrip('/')
    last     = path.split('/')[-1]
    no_pref  = re.sub(r'^\d+[_-]?', '', last)
    no_suf   = re.sub(r'[-_]\d+$', '', no_pref)
    text     = re.sub(r'[-_]+', ' ', no_suf).strip()
    return text.title()

# —————————————————————————————
# LOAD LESSONS CSV & EXTRACT NAMES
# —————————————————————————————
desktop    = Path.home() / "Desktop"
input_csv  = desktop / "lessons.csv"
output_csv = desktop / "lessons_with_descriptions.csv"

df = pd.read_csv(input_csv)
df['name'] = df['link'].apply(extract_lesson_name)

# —————————————————————————————
# GENERATE TWO-SENTENCE DESCRIPTIONS
# —————————————————————————————
descriptions = []
for _, row in df.iterrows():
    chap_idx     = int(row['chapter_index'])
    chapter_desc = chapter_descriptions.get(chap_idx, "")
    lesson_name  = row['name']

    prompt = (
        f"Chapter description:\n{chapter_desc}\n\n"
        f"Lesson title:\n{lesson_name}\n\n"
        "Provide a concise, two-sentence, marketing-style description for this lesson."
    )

    resp = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful course content writer."},
            {"role": "user",   "content": prompt}
        ],
        temperature=0.7,
        max_tokens=100,
    )
    # The new API still returns .choices with message.content
    descriptions.append(resp.choices[0].message.content.strip())

# —————————————————————————————
# SAVE OUTPUT CSV
# —————————————————————————————
df['description'] = descriptions
df[['name', 'description', 'link']].to_csv(output_csv, index=False)
print(f"Saved {len(df)} lessons to {output_csv}")
