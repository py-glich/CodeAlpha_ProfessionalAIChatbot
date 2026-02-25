import streamlit as st
import requests
import json

# ================= PAGE =================
st.set_page_config(
    page_title="AI Assistant",
    page_icon="AI",
    layout="wide"
)

# ================= LOAD API KEY =================
try:
    API_KEY = st.secrets["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"]
except:
    st.error("API key not found in secrets.")
    st.stop()

API_URL = "https://api.groq.com/openai/v1/chat/completions"

# ================= SESSION =================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "mode" not in st.session_state:
    st.session_state.mode = "Business"

# ================= MODE =================
st.sidebar.title("Mode")
st.session_state.mode = st.sidebar.selectbox(
    "Assistant Mode",
    ["Business", "Creative", "Fun"]
)

# ================= SYSTEM PROMPT =================
def get_system_prompt(mode):
    if mode == "Business":
        return "You are a professional business assistant. Be structured."
    if mode == "Creative":
        return "You are a creative assistant. Be imaginative."
    return "You are a fun assistant. Be casual."

# ================= CALL GROQ (RAW HTTP) =================
def generate_response(user_input):

    messages = [
        {"role": "system", "content": get_system_prompt(st.session_state.mode)}
    ]

    for role, content in st.session_state.chat_history:
        messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": user_input})

    payload = {
        "model": "llama3-70b-8192",
        "messages": messages,
        "temperature": 0.7
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return f"API Error: {response.text}"

    data = response.json()
    return data["choices"][0]["message"]["content"]

# ================= UI =================
st.title("AI Assistant")

for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

user_input = st.chat_input("Ask anything")

if user_input:
    st.session_state.chat_history.append(("user", user_input))

    with st.spinner("Thinking"):
        response = generate_response(user_input)

    st.session_state.chat_history.append(("assistant", response))

    st.rerun()
