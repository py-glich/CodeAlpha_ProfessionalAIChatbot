import streamlit as st
from groq import Groq

# ================= CONFIG =================
st.set_page_config(
    page_title="AI Multi-Mode Assistant",
    page_icon="🤖",
    layout="wide"
)

# ================= API KEY =================
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = st.sidebar.text_input("Enter Groq API Key", type="password")

if not api_key:
    st.warning("Please enter your Groq API key")
    st.stop()

client = Groq(api_key=api_key)

# ================= SESSION =================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "mode" not in st.session_state:
    st.session_state.mode = "Business"

# ================= SIDEBAR =================
st.sidebar.title("⚙️ Assistant Mode")

st.session_state.mode = st.sidebar.selectbox(
    "Choose Mode",
    ["Business", "Creative", "Fun"]
)

st.sidebar.markdown("""
### Modes

💼 Business → Professional  
🎨 Creative → Storytelling  
🎉 Fun → Casual & witty
""")

# ================= SYSTEM PROMPTS =================
def get_system_prompt(mode):
    if mode == "Business":
        return """
You are a professional business assistant.
Provide structured, analytical responses.
Use bullet points when helpful.
"""
    elif mode == "Creative":
        return """
You are a creative assistant.
Use imaginative and expressive language.
Tell stories when relevant.
"""
    elif mode == "Fun":
        return """
You are a fun AI.
Be casual, humorous, and lighthearted.
"""

# ================= LLM RESPONSE =================
def generate_response(user_input):

    messages = [
        {"role": "system", "content": get_system_prompt(st.session_state.mode)}
    ]

    for role, content in st.session_state.chat_history:
        messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=0.7
    )

    return response.choices[0].message.content

# ================= UI =================
st.title("🤖 Advanced AI Assistant (Cloud Ready)")

# Display chat
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# Input
user_input = st.chat_input("Ask anything...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))

    with st.spinner("Thinking..."):
        response = generate_response(user_input)

    st.session_state.chat_history.append(("assistant", response))

    st.rerun()
