# Multi-Model Conversational AI Workflow Lab

LLM workflows using OpenAI GPT, Llama (Groq) and Mistral through OpenRouter, with prompt-engineering
A/B tests, LangChain pipelines, a tool-using agent and a Streamlit chat UI.

## Setup
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # add your OpenRouter key
```

## Run (from project root)
```bash
python -m src.compare "What is 17% of 2340?" cot   # side-by-side models
python -m src.evaluate --n 30                      # A/B test -> results.csv
python -m src.chains                               # draft -> critique -> revise
python -m src.agent                                # tool-use agent
streamlit run app.py                               # chat UI
```

## Results
Paste your measured accuracy table and relative improvement from `python -m src.evaluate` here.

| model | baseline | role | few_shot | cot |
|---|---|---|---|---|
| gpt | | | | |
| groq_llama | | | | |
| mistral | | | | |

## Architecture
`clients.py` (retry + fallback) -> `prompts.py` (techniques) -> `evaluate.py` (A/B scoring);
`chains.py` (LangChain pipeline) -> `agent.py` (tools); `app.py` (UI).

## Method
30 math word problems with numeric ground truth; each prompt style run on each model at temperature 0;
answers parsed from the final `Answer:` line and compared with tolerance 0.01.
