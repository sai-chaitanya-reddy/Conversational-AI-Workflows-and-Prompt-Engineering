"""A/B test every prompt technique on every model and report accuracy + lift.
Run from project root:  python -m src.evaluate [--n 30]"""
import argparse
import json
import re
import pandas as pd
from src.clients import MODELS, chat
from src.prompts import PROMPTS


def extract_number(text):
    m = re.findall(r"Answer:\s*(.+)", text)
    target = m[-1] if m else text
    nums = re.findall(r"-?\d[\d,]*\.?\d*", target.replace("$", ""))
    if not nums:
        return None
    try:
        return float((nums[0] if m else nums[-1]).replace(",", "").rstrip("."))
    except ValueError:
        return None


def is_correct(output, truth, tol=0.01):
    pred = extract_number(output)
    return pred is not None and abs(pred - float(truth)) <= tol


def main(n):
    data = json.load(open("data/eval_set.json"))[:n]
    rows = []
    for model in MODELS:
        for name, build in PROMPTS.items():
            correct = 0
            for d in data:
                try:
                    out = chat(model, build(d["question"]))
                except RuntimeError as e:
                    print(f"[skip] {e}")
                    continue
                correct += is_correct(out, d["answer"])
            acc = correct / len(data)
            rows.append({"model": model, "prompt": name, "accuracy": acc})
            print(f"{model:12s} {name:9s} {acc:.2%}")

    df = pd.DataFrame(rows)
    table = df.pivot(index="model", columns="prompt", values="accuracy")
    print("\n", table.round(3))

    base = table["baseline"]
    best = table.max(axis=1)
    lift = ((best - base) / base.replace(0, float("nan")) * 100).round(1)
    print("\nRelative improvement of best prompt vs baseline (%):")
    print(lift)
    df.to_csv("results.csv", index=False)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=30)
    main(ap.parse_args().n)
