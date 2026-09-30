"""Tool-using agent with a safe calculator, a file reader and a word counter."""
import ast
import operator as op
from pathlib import Path
from langchain_core.tools import tool
from src.chains import llm

try:
    from langchain.agents import create_agent  # LangChain 1.x
except ImportError:  # older versions
    from langgraph.prebuilt import create_react_agent as create_agent

_OPS = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv,
        ast.Pow: op.pow, ast.USub: op.neg, ast.Mod: op.mod}


def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.operand))
    raise ValueError("Unsupported expression")


@tool
def calculator(expression: str) -> str:
    """Evaluate an arithmetic expression such as '0.17 * 2340'."""
    return str(_eval(ast.parse(expression, mode="eval").body))


@tool
def read_text_file(filename: str) -> str:
    """Read a text file from the data/ folder (e.g. 'notes.txt')."""
    p = (Path("data") / filename).resolve()
    if Path("data").resolve() not in p.parents or not p.exists():
        return "File not found or not allowed."
    return p.read_text()[:4000]


@tool
def word_count(text: str) -> str:
    """Count the words in a piece of text."""
    return str(len(text.split()))


agent = create_agent(llm, tools=[calculator, read_text_file, word_count])

if __name__ == "__main__":
    res = agent.invoke({"messages": [("user", "What is 17% of 2340, and how many words are in 'the quick brown fox'?")]})
    print(res["messages"][-1].content)
