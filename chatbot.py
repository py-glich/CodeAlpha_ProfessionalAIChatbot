import streamlit as st
import ollama

# ================= CONFIG =================
st.set_page_config(
    page_title="Advanced Local AI (Windows)",
    page_icon="🤖",
    layout="wide"
)

# ================= SESSION =================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "mode" not in st.session_state:
    st.session_state.mode = "Business"

if "model" not in st.session_state:
    st.session_state.model = "llama3:8b"  # Change to "phi3" if low RAM

# ================= SIDEBAR =================
st.sidebar.title("⚙️ AI Settings")

st.session_state.mode = st.sidebar.selectbox(
    "Assistant Mode",
    ["Business", "Creative", "Fun"]
)

st.session_state.model = st.sidebar.selectbox(
    "Model (Performance)",
    ["llama3:8b", "phi3"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### Mode Behavior

💼 Business → Professional, structured  
🎨 Creative → Imaginative, expressive  
🎉 Fun → Casual, humorous  
""")

# ================= SYSTEM PROMPT =================
def get_system_prompt(mode):
    if mode == "Business":
        return """
You are a strategic business consultant.
Be professional, structured, and analytical.
Use bullet points when helpful.
"""
    elif mode == "Creative":
        return """
You are a highly creative assistant.
Use vivid language and imaginative responses.
"""
    elif mode == "Fun":
        return """
You are a fun and witty AI.
Be energetic and humorous.
"""

# ================= GENERATE RESPONSE =================
def generate_response(user_input):

    messages = [
        {"role": "system", "content": get_system_prompt(st.session_state.mode)}
    ]

    # Limit memory for performance (last 10 messages)
    for role, content in st.session_state.chat_history[-10:]:
        messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": user_input})

    stream = ollama.chat(
        model=st.session_state.model,
        messages=messages,
        stream=True
    )

    full_response = ""
    for chunk in stream:
        full_response += chunk["message"]["content"]
        yield full_response


# ================= UI =================
st.title("🤖 Advanced Local AI Assistant (Windows)")

st.markdown(f"**Mode:** {st.session_state.mode} | **Model:** {st.session_state.model}")

# Display chat
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# Input
user_input = st.chat_input("Ask anything...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        response_generator = generate_response(user_input)

        for partial in response_generator:
            message_placeholder.markdown(partial)

        final_response = partial

    st.session_state.chat_history.append(("assistant", final_response))
