"""Multi-model API layer. OpenRouter exposes an OpenAI-compatible API,
so one client reaches GPT, Llama (served via Groq) and Mistral models."""
import os
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    timeout=60,
)

# Verify current slugs at https://openrouter.ai/models -- they change often.
MODELS = {
    "gpt": "openai/gpt-4o-mini",
    "groq_llama": "meta-llama/llama-3.3-70b-instruct",
    "mistral": "mistralai/mistral-small-3.1-24b-instruct",
}
FALLBACK_ORDER = ["gpt", "groq_llama", "mistral"]


def chat(model_key, messages, temperature=0.0, retries=3, max_tokens=512):
    """Call one model with retry + exponential backoff."""
    last_err = None
    for attempt in range(retries):
        try:
            r = client.chat.completions.create(
                model=MODELS[model_key],
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return r.choices[0].message.content or ""
        except Exception as e:  # rate limits, timeouts, 5xx
            last_err = e
            if "402" in str(e):  # out of credits: retrying won't help
                break
            time.sleep(2 ** attempt)
    raise RuntimeError(f"{model_key} failed after {retries} tries: {last_err}")


def chat_with_fallback(model_key, messages, **kw):
    """Try the requested model first, then fall back to the others."""
    order = [model_key] + [m for m in FALLBACK_ORDER if m != model_key]
    for m in order:
        try:
            return m, chat(m, messages, **kw)
        except RuntimeError as e:
            print(f"[warn] {e}")
    raise RuntimeError("All models failed")