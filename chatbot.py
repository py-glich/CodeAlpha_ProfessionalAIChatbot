import streamlit as st
import random
import time

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Smart AI ChatBot",
    page_icon="🤖",
    layout="wide"
)

# ==================== SESSION STATE ====================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "greeted" not in st.session_state:
    st.session_state.greeted = False

if "game_active" not in st.session_state:
    st.session_state.game_active = False

if "secret_number" not in st.session_state:
    st.session_state.secret_number = None

if "story_mode" not in st.session_state:
    st.session_state.story_mode = False


# ==================== STORIES ====================
stories = {
    "adventure": """
# 🗺️ The Lost Treasure of Emerald Island
Captain Maya searched for years...
The real treasure was knowledge, not gold.
""",

    "scifi": """
# 🚀 The Last Human Colony on Mars
Humanity transformed Mars into a new Earth.
""",

    "fantasy": """
# 🐉 The Last Dragon Rider
Kira awakened dragons and restored magic to the world.
"""
}

# ==================== RECOMMENDATIONS ====================
recommendations = {
    "movies": [
        "Inception",
        "Interstellar",
        "The Matrix",
        "Avengers: Endgame"
    ],
    "books": [
        "Atomic Habits",
        "Harry Potter",
        "The Alchemist",
        "Rich Dad Poor Dad"
    ],
    "tech": [
        "Learn Python",
        "Build a Website",
        "Create a Mobile App",
        "Start AI Projects"
    ]
}


# ==================== BOT LOGIC ====================
def bot_response(user_input):
    text = user_input.lower()

    # Greeting responses
    if any(word in text for word in ["hi", "hello", "hey"]):
        return "Hello there! 😊 How can I help you today?\n\nYou can ask for:\n- story\n- game\n- recommendations\n- general questions"

    # Ask about user
    if "how are you" in text:
        return "I'm doing great! 🤖 Thanks for asking. How about you?"

    # Ask name
    if "your name" in text:
        return "I'm your Smart AI ChatBot! 🤖"

    # Story trigger
    if "story" in text:
        st.session_state.story_mode = True
        return "Which story would you like?\n- adventure\n- scifi\n- fantasy"

    # If story mode active
    if st.session_state.story_mode:
        if text in stories:
            st.session_state.story_mode = False
            return stories[text]
        return "Please choose: adventure, scifi, or fantasy"

    # Game trigger
    if "game" in text:
        st.session_state.game_active = True
        st.session_state.secret_number = random.randint(1, 20)
        return "🎮 I picked a number between 1 and 20. Try to guess it!"

    # If game active
    if st.session_state.game_active:
        if text.isdigit():
            guess = int(text)
            secret = st.session_state.secret_number

            if guess < secret:
                return "Too low! Try again."
            elif guess > secret:
                return "Too high! Try again."
            else:
                st.session_state.game_active = False
                return "🎉 Correct! You win!"
        return "Please enter a valid number!"

    # Recommendations trigger
    if "recommend" in text:
        return "What would you like recommendations for?\n- movies\n- books\n- tech"

    if text in recommendations:
        item = random.choice(recommendations[text])
        return f"I recommend: **{item}** 🎯\n\nWant another one?"

    # General questions suggestions
    if "what can i ask" in text:
        return """Here are some things you can ask me:

- Tell me a motivational quote
- Recommend a movie
- Play a game
- Tell me a story
- Ask me tech advice
- Ask general knowledge questions
"""

    # Motivation
    if "motivate" in text:
        return "🔥 Success doesn't come from what you do occasionally, but what you do consistently."

    # Default smart reply
    default_responses = [
        "That's interesting! Tell me more.",
        "Hmm 🤔 Can you explain more?",
        "I like that question!",
        "Would you like a recommendation or play a game?",
    ]
    return random.choice(default_responses)


# ==================== TITLE ====================
st.title("🤖 Smart AI ChatBot")

# Auto Greeting (Only Once)
if not st.session_state.greeted:
    welcome_message = """Hello! 👋 I'm your Smart AI ChatBot.

I can:
- 💬 Chat with you
- 📖 Tell stories
- 🎮 Play games
- 🎬 Recommend movies/books/tech
- 💡 Motivate you

What would you like to do today?
"""
    st.session_state.chat_history.append(("assistant", welcome_message))
    st.session_state.greeted = True

# ==================== DISPLAY CHAT ====================
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# ==================== USER INPUT ====================
user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))

    response = bot_response(user_input)

    time.sleep(0.5)

    st.session_state.chat_history.append(("assistant", response))

    st.rerun()
