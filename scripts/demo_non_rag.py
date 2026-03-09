"""Non-RAG baseline demo: send PubMedQA questions directly to local Ollama model."""
import sys, json, time, pathlib, datetime

sys.path.insert(0, ".")

from langchain_core.messages import SystemMessage, HumanMessage
from src.models.model_factory import ModelFactory

DATASET_PATH = "data/raw/pubmedqa/pqa_labeled.jsonl"
N_SAMPLES = 5

SYSTEM_PROMPT = (
    "You are a medical question-answering assistant. "
    "Answer only with 'yes', 'no', or 'maybe'. "
    "Do not explain."
)


def load_samples(path: str, n: int) -> list[dict]:
    rows = []
    with open(path) as f:
        for line in f:
            if len(rows) >= n:
                break
            rows.append(json.loads(line))
    return rows


def format_prompt(row: dict) -> str:
    # Non-RAG baseline: no context provided
    return f"Question: {row['question']}"


def run_demo():
    dataset_path = pathlib.Path(DATASET_PATH)
    if not dataset_path.exists():
        print(f"Dataset not found at {DATASET_PATH}")
        print("Run: python scripts/download_pubmedqa.py")
        sys.exit(1)

    samples = load_samples(DATASET_PATH, N_SAMPLES)
    print(f"Loaded {len(samples)} samples from PubMedQA\n")

    model = ModelFactory.get_model("llama3.1-local")

    correct = 0
    sample_results = []
    run_date = datetime.datetime.now().isoformat()

    for i, row in enumerate(samples, 1):
        question = row["question"]
        expected = row["final_decision"].lower()

        print(f"--- Sample {i}/{N_SAMPLES} ---")
        print(f"Question : {question}")
        print(f"Expected : {expected}")

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=format_prompt(row)),
        ]

        start = time.perf_counter()
        try:
            response = model.invoke(messages)
            elapsed = time.perf_counter() - start
            answer = response.content.strip()
        except Exception as e:
            print(f"ERROR    : {e}")
            print("Make sure Ollama is running: ollama serve")
            print()
            continue

        is_correct = expected in answer.lower()
        if is_correct:
            correct += 1

        sample_results.append({
            "question": question,
            "expected": expected,
            "response": answer,
            "latency_s": round(elapsed, 2),
            "correct": is_correct,
        })

        print(f"Response : {answer}")
        print(f"Latency  : {elapsed:.2f}s")
        print(f"Correct  : {is_correct}")
        print()

    print(f"=== Summary: {correct}/{len(samples)} correct ===")

    results_dict = {
        "run_date": run_date,
        "model": "llama3.1-local",
        "dataset": "PubMedQA pqa_labeled",
        "n_samples": len(samples),
        "accuracy": round(correct / len(samples), 4) if samples else 0.0,
        "correct": correct,
        "samples": sample_results,
    }
    save_results(results_dict, pathlib.Path("results"))


def save_results(results_dict: dict, out_dir: pathlib.Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"non_rag_{timestamp}.json"
    with open(out_path, "w") as f:
        json.dump(results_dict, f, indent=2)
    print(f"Results saved to {out_path}")


if __name__ == "__main__":
    run_demo()
