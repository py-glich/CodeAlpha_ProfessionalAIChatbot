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

# ================= GROQ API =================
API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Put your API key here (from Groq dashboard)
API_KEY = "YOUR_GROQ_API_KEY"

def ai_reply(user_input):
    try:
        payload = {
            "model": "llama3-70b-8192",
            "messages": [
                {"role": "user", "content": user_input}
            ],
            "temperature": 0.7
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            return "AI service error. Check API key or try later."
    except:
        return "Something went wrong with AI."

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
        return f"I recommend: {random.choice(movies)} 🎬"

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
✔ AI-powered replies (Groq)  
✔ name memory  
✔ mood detection  
✔ movie recommendations  
✔ basic conversation
""")
