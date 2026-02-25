import streamlit as st
import requests
import random

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

# ================= SESSION =================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "mood" not in st.session_state:
    st.session_state.mood = None

# ================= AI API (HuggingFace) =================
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
HEADERS = {}

# If you have a token (optional)
# HEADERS = {"Authorization": "Bearer YOUR_TOKEN"}

def ai_reply(user_input):
    try:
        payload = {"inputs": user_input}
        response = requests.post(API_URL, headers=HEADERS, json=payload)

        if response.status_code == 200:
            data = response.json()
            return data.get("generated_text", "I couldn't understand that.")
        else:
            return "AI service unavailable. Try again later."
    except:
        return "Something went wrong with AI."

# ================= BOT LOGIC (Features) =================
def bot_reply(user_input):
    text = user_input.lower()

    # Name memory
    if "my name is" in text:
        name = user_input.split("my name is")[-1].strip().title()
        st.session_state.user_name = name
        return f"Nice to meet you, {name}! I'll remember your name 😊"

    # Greetings
    if any(word in text for word in ["hi", "hello", "hey"]):
        if st.session_state.user_name:
            return f"Hello {st.session_state.user_name}! How can I help you?"
        return "Hello! What's your name?"

    # Mood detection
    if "i am sad" in text or "feeling sad" in text:
        st.session_state.mood = "sad"
        return "I'm sorry you're feeling sad. I'm here for you 💙"

    if "i am happy" in text:
        st.session_state.mood = "happy"
        return "That's great! Keep smiling 😊"

    if "i am tired" in text:
        st.session_state.mood = "tired"
        return "Take some rest. Self-care matters 💫"

    # Mood-based replies
    if st.session_state.mood == "sad":
        return "Things will get better. I'm here to listen 💙"

    if st.session_state.mood == "happy":
        return "I'm happy you're happy! What made your day great?"

    # Movie recommendation
    if "movie" in text or "recommend" in text:
        movies = ["Inception", "Interstellar", "The Matrix", "Avengers: Endgame", "Joker"]
        return f"I recommend watching: {random.choice(movies)} 🎬"

    # AI response (fallback)
    return ai_reply(user_input)


# ================= UI =================
st.title("🤖 AI Chatbot (Basic + AI)")

for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

user_input = st.chat_input("Type your message")

if user_input:
    st.session_state.chat_history.append(("user", user_input))

    response = bot_reply(user_input)

    st.session_state.chat_history.append(("assistant", response))

    st.rerun()

# ================= INFO =================
st.markdown("---")
st.markdown("### Features")
st.markdown("""
✔ AI-powered replies  
✔ name memory  
✔ mood detection  
✔ movie recommendations  
✔ basic conversation
""")
