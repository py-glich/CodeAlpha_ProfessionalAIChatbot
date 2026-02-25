import streamlit as st
from openai import OpenAI

# ================= PAGE =================
st.set_page_config(page_title="OpenAI Chatbot", page_icon="🤖")

# ================= API KEY =================
api_key = st.secrets.get("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")

if not api_key:
    st.error("OpenAI API key not found in secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

# ================= SESSION =================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "mood" not in st.session_state:
    st.session_state.mood = None

# ================= SYSTEM PROMPT =================
def system_prompt():
    return """
You are a helpful and friendly chatbot.
Remember basic conversation.
If user tells their name, remember it.
Be polite and concise.
"""

# ================= GENERATE RESPONSE =================
def generate_response():

    messages = [{"role": "system", "content": system_prompt()}]

    for role, content in st.session_state.chat_history:
        messages.append({"role": role, "content": content})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )

    return response.choices[0].message.content

# ================= UI =================
st.title("🤖 OpenAI Chatbot")

for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

user_input = st.chat_input("Type your message")

if user_input:
    st.session_state.chat_history.append(("user", user_input))

    with st.spinner("Thinking..."):
        reply = generate_response()

    st.session_state.chat_history.append(("assistant", reply))

    st.rerun()
