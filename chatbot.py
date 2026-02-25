import streamlit as st
import requests
import json

# ================= PAGE =================
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ================= LOAD API KEY =================
try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.error("API key not found in secrets. Please add your Groq API key to the secrets.toml file.")
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
    ["Business", "Creative", "Fun"],
    index=["Business", "Creative", "Fun"].index(st.session_state.mode)
)

# ================= SYSTEM PROMPT =================
def get_system_prompt(mode):
    if mode == "Business":
        return "You are a professional business assistant. Be structured, concise, and focus on productivity and efficiency."
    elif mode == "Creative":
        return "You are a creative assistant. Be imaginative, inspiring, and help with creative projects."
    else:  # Fun
        return "You are a fun and friendly assistant. Be casual, witty, and make conversations enjoyable."

# ================= CALL GROQ API =================
def generate_response(user_input):
    messages = [
        {"role": "system", "content": get_system_prompt(st.session_state.mode)}
    ]
    
    # Add chat history
    for role, content in st.session_state.chat_history:
        messages.append({"role": role, "content": content})
    
    # Add current user message
    messages.append({"role": "user", "content": user_input})
    
    payload = {
        "model": "llama-3.3-70b-versatile",  # Updated model
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            return f"API Error: {response.status_code} - {response.text}"
        
        data = response.json()
        return data["choices"][0]["message"]["content"]
        
    except requests.exceptions.Timeout:
        return "Error: Request timed out. Please try again."
    except Exception as e:
        return f"Error: {str(e)}"

# ================= UI =================
st.title("🤖 AI Assistant")
st.markdown(f"**Current Mode:** {st.session_state.mode}")

# Display chat history
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# Chat input
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Add user message to history
    st.session_state.chat_history.append(("user", user_input))
    
    # Generate and display response
    with st.spinner("Thinking..."):
        response = generate_response(user_input)
    
    # Add assistant response to history
    st.session_state.chat_history.append(("assistant", response))
    
    # Rerun to display new messages
    st.rerun()
