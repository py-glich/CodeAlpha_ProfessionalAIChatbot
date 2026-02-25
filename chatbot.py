import streamlit as st
import random
import time

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Advanced AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ================= SESSION STATE =================
def init_state():
    defaults = {
        "chat_history": [],
        "greeted": False,
        "user_name": None,
        "mood": None,
        "game_active": False,
        "secret_number": None,
        "story_mode": False,
        "recommend_mode": False,
        "last_category": None,
        "preferences": []
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

# ================= STORY ENGINE =================
stories = {
    "adventure": "An explorer discovers an ancient civilization hidden beneath the ocean...",
    "scifi": "In 2150, AI governs Earth while humans colonize Titan...",
    "fantasy": "A forgotten kingdom awakens when a young mage discovers forbidden magic..."
}

# ================= RECOMMENDATION ENGINE =================
recommendations = {
    "movies": {
        "Inception": "because you enjoy deep and intelligent storytelling.",
        "Interstellar": "because you seem curious about space and big ideas.",
        "The Matrix": "because you like questioning reality.",
        "Avengers: Endgame": "because you enjoy epic emotional journeys."
    },
    "books": {
        "Atomic Habits": "because you seem growth-oriented.",
        "The Alchemist": "because you might be searching for purpose.",
        "Rich Dad Poor Dad": "because financial intelligence is powerful.",
        "Harry Potter": "because imagination fuels creativity."
    },
    "tech": {
        "Learn Python": "because it opens doors to AI and automation.",
        "Build SaaS": "because scalable ideas build wealth.",
        "AI Projects": "because AI is shaping the future.",
        "Cybersecurity": "because digital protection is critical."
    }
}

# ================= AI ROUTER =================
def detect_mood(text):
    if any(word in text for word in ["sad", "tired", "bad", "upset"]):
        return "low"
    if any(word in text for word in ["happy", "great", "excited"]):
        return "high"
    return None


def advanced_ai(user_input):
    text = user_input.lower()

    # Save mood
    mood = detect_mood(text)
    if mood:
        st.session_state.mood = mood

    # ========= NAME MEMORY =========
    if "my name is" in text:
        name = text.split("my name is")[-1].strip().capitalize()
        st.session_state.user_name = name
        return f"Nice to meet you, {name}! I'll remember that."

    # ========= GREETING =========
    if any(word in text for word in ["hi", "hello", "hey"]):
        if st.session_state.user_name:
            return f"Hello {st.session_state.user_name}! How can I assist you today?"
        return "Hello! What's your name?"

    # ========= MOOD RESPONSE =========
    if st.session_state.mood == "low":
        return "I sense you might be feeling low. Want some motivation or a light story?"

    if st.session_state.mood == "high":
        return "You sound excited! Want to play a game or explore something ambitious?"

    # ========= STORY SYSTEM =========
    if "story" in text:
        st.session_state.story_mode = True
        return "Choose a genre: adventure, scifi, fantasy"

    if st.session_state.story_mode:
        if text in stories:
            st.session_state.story_mode = False
            return stories[text]
        return "Please choose: adventure, scifi, fantasy"

    # ========= GAME SYSTEM =========
    if "game" in text:
        st.session_state.game_active = True
        st.session_state.secret_number = random.randint(1, 50)
        return "I picked a number between 1 and 50. Guess it."

    if st.session_state.game_active:
        if text.isdigit():
            guess = int(text)
            secret = st.session_state.secret_number
            if guess < secret:
                return "Too low."
            elif guess > secret:
                return "Too high."
            else:
                st.session_state.game_active = False
                return "Correct. You think strategically."
        return "Enter a valid number."

    # ========= RECOMMENDATION SYSTEM =========
    if "recommend" in text:
        st.session_state.recommend_mode = True
        return "Category? movies, books, tech"

    if st.session_state.recommend_mode:
        if text in recommendations:
            st.session_state.last_category = text
            item = random.choice(list(recommendations[text].keys()))
            reason = recommendations[text][item]

            st.session_state.preferences.append(text)

            return f"""
🎯 Recommendation: {item}

Why? {reason}

Want another or switch category?
"""
        return "Choose: movies, books, tech"

    # ========= INTELLIGENT DEFAULT =========
    smart_responses = [
        "That’s an interesting thought. Expand on it.",
        "What outcome are you aiming for?",
        "Would you like strategy, creativity, or logic?",
        "We can explore business, technology, psychology, or fun."
    ]

    return random.choice(smart_responses)


# ================= UI =================
st.title("🤖 Advanced Multi-Mode AI Assistant")

# Auto Greeting
if not st.session_state.greeted:
    st.session_state.chat_history.append((
        "assistant",
        """Welcome. I'm your Advanced AI Assistant.

I combine:
- Smart conversation
- Emotional awareness
- Games
- Stories
- Intelligent recommendations
- Memory

Tell me your name to begin.
"""
    ))
    st.session_state.greeted = True

# Display chat
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# Input
user_input = st.chat_input("Enter your message...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))

    response = advanced_ai(user_input)

    time.sleep(0.4)

    st.session_state.chat_history.append(("assistant", response))
    st.rerun()
