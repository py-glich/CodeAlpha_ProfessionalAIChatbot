import streamlit as st
import random
import time

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="AI ChatBot with Games & Stories",
    page_icon="🤖",
    layout="wide"
)

# ==================== SESSION STATE ====================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

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

After surviving traps and jungle dangers, she found not gold —
but ancient knowledge that changed the world forever.
""",

    "scifi": """
# 🚀 The Last Human Colony on Mars

Year 2347. Earth was gone.

But Mars bloomed with life.
Humanity didn’t just survive —
it evolved.
""",

    "fantasy": """
# 🐉 The Last Dragon Rider

Kira found a glowing dragon egg.

When it hatched, magic returned to the world.

She was no longer alone.
"""
}

# ==================== FUNCTIONS ====================

def bot_response(user_input):
    text = user_input.lower()

    # Story mode trigger
    if "story" in text:
        st.session_state.story_mode = True
        return "Which story would you like?\n\n- adventure\n- scifi\n- fantasy"

    # Start game
    if "game" in text:
        st.session_state.game_active = True
        st.session_state.secret_number = random.randint(1, 20)
        return "🎮 I picked a number between 1 and 20. Try to guess it!"

    # If story mode active
    if st.session_state.story_mode:
        if text in stories:
            st.session_state.story_mode = False
            return stories[text]
        else:
            return "Please choose: adventure, scifi, or fantasy"

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
        else:
            return "Please enter a number!"

    # Default reply
    responses = [
        "That's interesting!",
        "Tell me more!",
        "I like that!",
        "Ask me for a story or game!",
    ]
    return random.choice(responses)


# ==================== TITLE ====================
st.title("🤖 AI ChatBot with Games & Stories")

st.write("Type **story** to read a story.")
st.write("Type **game** to play a guessing game.")

# ==================== DISPLAY CHAT ====================
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# ==================== USER INPUT ====================
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message
    st.session_state.chat_history.append(("user", user_input))

    # Generate bot response
    response = bot_response(user_input)

    # Simulate typing delay
    time.sleep(0.5)

    # Add bot message
    st.session_state.chat_history.append(("assistant", response))

    st.rerun()
