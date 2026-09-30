import streamlit as st
from src.clients import MODELS, chat_with_fallback
from src.prompts import PROMPTS

st.set_page_config(page_title="Multi-Model Chat")
st.title("Multi-Model Chat")

model = st.sidebar.selectbox("Model", list(MODELS))
style = st.sidebar.selectbox("Prompt style", ["none"] + list(PROMPTS))
if st.sidebar.button("Clear chat"):
    st.session_state.history = []

st.session_state.setdefault("history", [])
for m in st.session_state.history:
    st.chat_message(m["role"]).write(m["content"])

if q := st.chat_input("Ask something"):
    st.session_state.history.append({"role": "user", "content": q})
    st.chat_message("user").write(q)
    msgs = list(st.session_state.history)
    if style in ("role", "cot"):
        msgs = PROMPTS[style]("")[:1] + msgs          # system prompt only
    elif style == "few_shot":
        msgs = PROMPTS["few_shot"]("")[:-1] + msgs    # system + examples
    with st.spinner("Thinking..."):
        used, answer = chat_with_fallback(model, msgs, temperature=0.3)
    st.session_state.history.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer + (f"\n\n_(fell back to {used})_" if used != model else ""))
