"""Quick side-by-side: python -m src.compare "Your question" [prompt_name]"""
import sys
from src.clients import MODELS, chat
from src.prompts import PROMPTS

if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "What is 17% of 2340?"
    style = sys.argv[2] if len(sys.argv) > 2 else "cot"
    for key in MODELS:
        print(f"\n=== {key} ({style}) ===")
        print(chat(key, PROMPTS[style](q)))
