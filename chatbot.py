import streamlit as st
from groq import Groq

# ================= PAGE =================
st.set_page_config(
    page_title="AI Assistant",
    page_icon="AI",
    layout="wide"
)

# ================= LOAD API FROM SECRETS =================
try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("""
API key not found.

Add it in Streamlit secrets:
Settings → Secrets → add:

GROQ_API_KEY = "your_api_key"
""")
    st.stop()

client = Groq(api_key=api_key)

# ================= SESSION =================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "mode" not in st.session_state:
    st.session_state.mode = "Business"

# ================= MODE SELECT =================
st.sidebar.title("Mode")

st.session_state.mode = st.sidebar.selectbox(
    "Assistant Mode",
    ["Business", "Creative", "Fun"]
)

# ================= SYSTEM PROMPT (ASCII SAFE) =================
def get_system_prompt(mode):
    if mode == "Business":
        return """
You are a professional business assistant.
Be structured and analytical.
"""
    elif mode == "Creative":
        return """
You are a creative assistant.
Be imaginative and expressive.
"""
    elif mode == "Fun":
        return """
You are a fun assistant.
Be casual and lighthearted.
"""

# ================= RESPONSE =================
def generate_response(user_input):

    messages = [
        {"role": "system", "content": get_system_prompt(st.session_state.mode)}
    ]

    for role, content in st.session_state.chat_history:
        messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        temperature=0.7
    )

    return response.choices[0].message.content

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
