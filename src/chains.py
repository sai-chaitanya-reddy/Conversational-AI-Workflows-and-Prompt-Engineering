"""Multi-step LangChain pipeline: draft -> critique -> revise."""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.3,
)
parse = StrOutputParser()

draft = ChatPromptTemplate.from_template("Write a concise answer to: {q}") | llm | parse
critique = ChatPromptTemplate.from_template(
    "Question: {q}\nDraft: {draft}\nList the draft's weaknesses briefly.") | llm | parse
revise = ChatPromptTemplate.from_template(
    "Question: {q}\nDraft: {draft}\nCritique: {critique}\n"
    "Write an improved final answer.") | llm | parse


def pipeline(q):
    d = draft.invoke({"q": q})
    c = critique.invoke({"q": q, "draft": d})
    return {"draft": d, "critique": c, "final": revise.invoke({"q": q, "draft": d, "critique": c})}


if __name__ == "__main__":
    print(pipeline("Explain why the sky is blue to a 10 year old.")["final"])
