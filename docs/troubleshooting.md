# Troubleshooting Log
Record every issue you hit while building. Template:

## Issue: <short title>
- **Symptom:**
- **Cause:**
- **Fix:**
- **Commit:**

## Common ones to expect
- 404 / "model not found": OpenRouter slugs change; check openrouter.ai/models and update `MODELS`.
- 429 rate limits: handled by retry with backoff in `clients.chat`; lower request rate or use a fallback.
- LangChain ImportError: APIs move between versions; check current docs (`create_agent` vs `create_react_agent`).
- Answer parsing failures: models ignore the "Answer:" format; tighten the system prompt or use an LLM judge.
