import streamlit as st
import openai
from core.config import config

client = openai.OpenAI(api_key=config.OPENAI_API_KEY)


if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm a chatbot. How can I help you today?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

for i, m in enumerate(st.session_state.messages):
    print(f"Message {i}: role={m.get('role')}, content={type(m.get('content'))} {m.get('content')}")

if prompt := st.chat_input("Hello! I'm a chatbot. How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        output = client.chat.completions.create(
            model="gpt-4o-mini",
        messages=[
            {"role": str(m.get("role", "")), "content": str(m.get("content", ""))}
            for m in st.session_state.messages
            if m.get("role") and m.get("content") is not None
        ],
            max_tokens=500,
        )

        st.write(output.choices[0].message.content)

#    st.session_state.messages.append({"role": "assistant", "content": output.choices[0].message.content})
                