"""Prompt-engineering techniques, each building messages for the same question."""


def baseline(q):
    return [{"role": "user", "content": q}]


def role_based(q):
    return [
        {"role": "system", "content": "You are a meticulous senior analyst. "
         "Give the final result as 'Answer: <number>' with no extra text after it."},
        {"role": "user", "content": q},
    ]


def few_shot(q):
    return [
        {"role": "system", "content": "Reply with the final answer only, in the form 'Answer: <number>'."},
        {"role": "user", "content": "A shirt costs $20 and is 25% off. Price?"},
        {"role": "assistant", "content": "Answer: 15"},
        {"role": "user", "content": "A book costs $40 and is 10% off. Price?"},
        {"role": "assistant", "content": "Answer: 36"},
        {"role": "user", "content": q},
    ]


def chain_of_thought(q):
    return [
        {"role": "system", "content": "Think step by step, showing brief working. "
         "Finish with a last line 'Answer: <number>'."},
        {"role": "user", "content": q},
    ]


PROMPTS = {
    "baseline": baseline,
    "role": role_based,
    "few_shot": few_shot,
    "cot": chain_of_thought,
}
