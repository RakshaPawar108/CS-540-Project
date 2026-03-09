"""Download PubMedQA labeled split to data/raw/pubmedqa/."""
from datasets import load_dataset
import json, pathlib

OUTPUT_DIR = pathlib.Path("data/raw/pubmedqa")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ds = load_dataset("qiaojin/PubMedQA", "pqa_labeled", split="train")
# Save as line-delimited JSON for easy inspection
out_path = OUTPUT_DIR / "pqa_labeled.jsonl"
with open(out_path, "w") as f:
    for row in ds:
        f.write(json.dumps(row) + "\n")
print(f"Saved {len(ds)} records to {out_path}")
