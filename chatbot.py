import streamlit as st
import google.generativeai as genai
import os
import time

API_KEY = os.getenv("AIzaSyBI767obYsPgqsy-XbM4AgHoNtPR6YJbJo")

if not API_KEY:
    st.error("API key not found. Set GEMINI_API_KEY environment variable.")
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-pro")

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("Professional AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

def generate_response(user_input):
    try:
        response = model.generate_content(user_input)
        return response.text
    except Exception:
        return "Sorry, I couldn't process that request."

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response = generate_response(prompt)

        full_response = ""
        for char in response:
            full_response += char
            message_placeholder.markdown(full_response)
            time.sleep(0.01)

    st.session_state.messages.append({"role": "assistant", "content": response})
