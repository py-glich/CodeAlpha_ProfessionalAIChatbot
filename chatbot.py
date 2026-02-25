import streamlit as st
import random

st.set_page_config(page_title="Smart Chatbot", page_icon="🤖")

# ================= SESSION =================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "mood" not in st.session_state:
    st.session_state.mood = None

# ================= BOT LOGIC =================
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
    if "i am sad" in text:
        st.session_state.mood = "sad"
        return "I'm sorry you're feeling sad. I'm here 💙"

    if "i am happy" in text:
        st.session_state.mood = "happy"
        return "That's great! Keep smiling 😊"

    if "i am tired" in text:
        st.session_state.mood = "tired"
        return "Take rest. Self-care matters 💫"

    # Mood replies
    if st.session_state.mood == "sad":
        return "Things will get better. I'm here to listen 💙"

    if st.session_state.mood == "happy":
        return "I'm happy you're happy! What made your day great?"

    # Movie recommendation
    if "movie" in text or "recommend" in text:
        movies = ["Inception", "Interstellar", "The Matrix", "Avengers: Endgame", "Joker"]
        return f"I recommend watching: {random.choice(movies)} 🎬"

    # Small talk
    if "how are you" in text:
        return "I'm good! Thanks for asking 😊"

    if "bye" in text:
        return "Goodbye! Take care 👋"

    return "I’m a simple chatbot. I can chat, remember your name, and recommend movies."

# ================= UI =================
st.title("🤖 Smart Chatbot")

# Chat history display
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# Chat input
user_input = st.chat_input("Type your message")

if user_input:
    st.session_state.chat_history.append(("user", user_input))

    response = bot_reply(user_input)

    st.session_state.chat_history.append(("assistant", response))

    st.rerun()

# ================= FEATURES INFO =================
st.markdown("---")
st.markdown("### Features")
st.markdown("""
✔ name memory  
✔ mood replies  
✔ movie recommendations  
✔ basic conversation  
✔ no external APIs
""")
