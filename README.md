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

30 math word problems, temperature 0, one run per configuration (accuracy):

| model                       | baseline | role | few_shot | cot  |
| --------------------------- | -------- | ---- | -------- | ---- |
| gpt (gpt-4o-mini)           | 86.7%    | 100% | 73.3%    | 100% |
| groq_llama (Llama 3.3 70B)  | 100%     | 100% | 96.7%    | 100% |
| mistral (Mistral Small 3.1) | 83.3%    | 90%  | 86.7%    | 100% |

**Key findings**

- Chain-of-thought reached 100% on all three models, lifting the average from 90% (baseline) to 100%.
- Largest relative gain: Mistral, +20% (83.3% to 100%). GPT: +15.4%.
- Few-shot prompting lowered accuracy on GPT and Llama.

**Limitations**: small benchmark (30 questions), a single run per configuration, and ceiling effects for the strongest model.

## Architecture

`clients.py` (retry + fallback) -> `prompts.py` (techniques) -> `evaluate.py` (A/B scoring);
`chains.py` (LangChain pipeline) -> `agent.py` (tools); `app.py` (UI).

## Method

30 math word problems with numeric ground truth; each prompt style run on each model at temperature 0;
answers parsed from the final `Answer:` line and compared with tolerance 0.01.

## Demo

![Chat app](docs/app.png)
