import streamlit as st
import google.generativeai as genai
import time

# =======================================
# CONFIGURATION
# =======================================

# Replace with your Gemini API key
API_KEY = "YOUR_GEMINI_API_KEY"

genai.configure(api_key=API_KEY)

# Model setup (Gemini Pro)
model = genai.GenerativeModel("gemini-pro")

# Page config (professional UI)
st.set_page_config(page_title="AI Chatbot | CodeAlpha", page_icon="🤖")

st.title("🤖 Professional AI Chatbot")
st.write("Powered by Google Gemini AI")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# =======================================
# RESPONSE GENERATION
# =======================================

def generate_response(user_input):
    try:
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        return "Sorry, I couldn't process that request."

# =======================================
# STREAMLIT CHAT INTERFACE
# =======================================

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Type your message..."):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI response with typing effect
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response = generate_response(prompt)

        # Typing animation
        full_response = ""
        for char in response:
            full_response += char
            message_placeholder.markdown(full_response)
            time.sleep(0.01)

    # Save response
    st.session_state.messages.append({"role": "assistant", "content": response})
