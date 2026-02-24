import streamlit as st
import random
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI ChatBot & Games",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding-bottom: 100px;
    }
    
    /* Chat message styling */
    .stChatMessage {
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
    }
    
    /* User message styling */
    .stChatMessageContent {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        padding: 12px 16px;
    }
    
    /* Bot message styling */
    .stChatMessageContent {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        color: #333;
        border-radius: 12px;
        padding: 12px 16px;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        padding: 20px;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 10px 20px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: scale(1.02);
    }
    
    /* Game cards styling */
    .game-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        color: white;
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .game-card:hover {
        transform: translateY(-5px);
    }
    
    /* Story container */
    .story-container {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 16px;
        padding: 32px;
        color: #f0f0f0;
        line-height: 1.8;
        font-size: 18px;
        margin: 20px 0;
    }
    
    /* Info box styling */
    .info-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 12px;
        padding: 16px;
        margin: 16px 0;
    }
    
    /* Section headers */
    h1, h2, h3 {
        color: #667eea;
        font-weight: 700;
    }
    
    /* Game button styling */
    .game-btn {
        width: 100%;
        margin: 8px 0;
        padding: 16px;
        font-size: 16px;
    }
    
    /* Score display */
    .score-display {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: bold;
    }
    
    /* Navigation tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 8px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'typing_complete' not in st.session_state:
    st.session_state.typing_complete = True

if 'game_state' not in st.session_state:
    st.session_state.game_state = {}

if 'story_settings' not in st.session_state:
    st.session_state.story_settings = {
        'typing_speed': 0.05,
        'auto_read': False
    }

# ==================== CHATBOT FUNCTIONS ====================

def get_bot_response(user_input):
    """Generate bot response based on user input keywords"""
    user_input_lower = user_input.lower()
    
    responses = {
        'greeting': [
            "Hello! How can I help you today? 😊",
            "Hi there! What would you like to know?",
            "Hey! I'm here to help. What's on your mind?",
            "Greetings! How may I assist you?"
        ],
        'help': [
            "I'm here to help! What do you need assistance with?",
            "Sure, I can help with that. Please tell me more.",
            "I'd be happy to help. What would you like to know?",
            "Help is my middle name! What do you need?"
        ],
        'weather': [
            "I don't have real-time weather data, but I can tell you that weather is a fascinating topic! ☀️",
            "While I can't check the current weather, I can discuss weather patterns and climate if you're interested.",
            "Weather prediction requires real-time data, which I don't have access to. Is there something else I can help with?"
        ],
        'time': [
            "I don't have access to real-time data, but I can tell you that time is a precious resource! ⏰",
            "Time flies when you're having fun chatting with me! What else can I help you with?"
        ],
        'name': [
            "I'm your friendly AI chatbot! You can call me whatever you like. 🤖",
            "My name is ChatBot, but you can think of me as your digital assistant.",
            "I'm just a simple chatbot, but I'm here to help! What should I call you?"
        ],
        'joke': [
            "Why did the AI go to therapy? Because it had too many deep learning issues! 😄",
            "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
            "What do you call a computer that sings? A-Dell! 🎤",
            "Why did the computer go to the doctor? It had a bad virus! 🦠"
        ],
        'thanks': [
            "You're welcome! Happy to help! 😊",
            "Anytime! That's what I'm here for.",
            "My pleasure! Is there anything else I can assist you with?",
            "You're very welcome! Don't hesitate to ask more questions."
        ],
        'goodbye': [
            "Goodbye! It was great chatting with you! 👋",
            "See you later! Don't be a stranger!",
            "Bye for now! Take care and stay safe!",
            "Until next time! Have a wonderful day!"
        ],
        'default': [
            "That's interesting! Tell me more about that.",
            "I appreciate you sharing that. What else is on your mind?",
            "I'm not sure I understand completely. Could you elaborate?",
            "That's a great point! What would you like to explore next?",
            "I hear you! Is there something specific I can help you with?",
            "Thanks for sharing! What else would you like to discuss?"
        ]
    }
    
    if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return random.choice(responses['greeting'])
    elif any(word in user_input_lower for word in ['help', 'assist', 'support']):
        return random.choice(responses['help'])
    elif any(word in user_input_lower for word in ['weather', 'temperature', 'forecast']):
        return random.choice(responses['weather'])
    elif any(word in user_input_lower for word in ['time', 'clock', 'hour']):
        return random.choice(responses['time'])
    elif any(word in user_input_lower for word in ['name', 'who are you', 'what are you']):
        return random.choice(responses['name'])
    elif any(word in user_input_lower for word in ['joke', 'funny', 'laugh']):
        return random.choice(responses['joke'])
    elif any(word in user_input_lower for word in ['thanks', 'thank you', 'appreciate']):
        return random.choice(responses['thanks'])
    elif any(word in user_input_lower for word in ['bye', 'goodbye', 'see you', 'later']):
        return random.choice(responses['goodbye'])
    else:
        return random.choice(responses['default'])

def typing_effect(text, speed=0.03):
    """Create typing effect for bot response"""
    message_placeholder = st.empty()
    displayed_text = ""
    
    for char in text:
        displayed_text += char
        message_placeholder.markdown(displayed_text)
        time.sleep(speed)
    
    return displayed_text

# ==================== GAMES FUNCTIONS ====================

def init_game_state(game_name):
    """Initialize game state if not exists"""
    if game_name not in st.session_state.game_state:
        st.session_state.game_state[game_name] = {}

def rock_paper_scissors():
    """Rock Paper Scissors game"""
    init_game_state('rps')
    
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h2>🪨 Rock Paper Scissors ✂️📄</h2>
        <p>Choose your move and see if you can beat the computer!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    moves = ['🪨 Rock', '✂️ Scissors', '📄 Paper']
    
    with col1:
        if st.button("🪨 Rock", use_container_width=True):
            computer_move = random.choice(moves)
            user_move = "🪨 Rock"
            
            if "Scissors" in computer_move:
                result = "🎉 You Win!"
                color = "green"
            elif "Paper" in computer_move:
                result = "😔 You Lose!"
                color = "red"
            else:
                result = "🤝 It's a Tie!"
                color = "blue"
            
            st.session_state.game_state['rps']['last_result'] = {
                'user': user_move,
                'computer': computer_move,
                'result': result,
                'color': color
            }
    
    with col2:
        if st.button("✂️ Scissors", use_container_width=True):
            computer_move = random.choice(moves)
            user_move = "✂️ Scissors"
            
            if "Paper" in computer_move:
                result = "🎉 You Win!"
                color = "green"
            elif "Rock" in computer_move:
                result = "😔 You Lose!"
                color = "red"
            else:
                result = "🤝 It's a Tie!"
                color = "blue"
            
            st.session_state.game_state['rps']['last_result'] = {
                'user': user_move,
                'computer': computer_move,
                'result': result,
                'color': color
            }
    
    with col3:
        if st.button("📄 Paper", use_container_width=True):
            computer_move = random.choice(moves)
            user_move = "📄 Paper"
            
            if "Rock" in computer_move:
                result = "🎉 You Win!"
                color = "green"
            elif "Scissors" in computer_move:
                result = "😔 You Lose!"
                color = "red"
            else:
                result = "🤝 It's a Tie!"
                color = "blue"
            
            st.session_state.game_state['rps']['last_result'] = {
                'user': user_move,
                'computer': computer_move,
                'result': result,
                'color': color
            }
    
    # Display result
    if 'last_result' in st.session_state.game_state.get('rps', {}):
        result = st.session_state.game_state['rps']['last_result']
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 16px; color: white; margin-top: 20px;">
            <h3>Your Choice: {result['user']}</h3>
            <h3>Computer's Choice: {result['computer']}</h3>
            <h2 style="color: {'#38ef7d' if result['color'] == 'green' else '#ef4444' if result['color'] == 'red' else '#fbbf24'};">{result['result']}</h2>
        </div>
        """, unsafe_allow_html=True)

def number_guessing_game():
    """Number Guessing Game"""
    init_game_state('number_guess')
    
    if 'target_number' not in st.session_state.game_state['number_guess']:
        st.session_state.game_state['number_guess']['target_number'] = random.randint(1, 100)
        st.session_state.game_state['number_guess']['attempts'] = 0
        st.session_state.game_state['number_guess']['game_over'] = False
    
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h2>🎯 Number Guessing Game</h2>
        <p>I'm thinking of a number between 1 and 100. Can you guess it?</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.game_state['number_guess']['game_over']:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); border-radius: 16px; color: white;">
            <h2>🎉 Congratulations!</h2>
            <p>You guessed the number <strong>{st.session_state.game_state['number_guess']['target_number']}</strong> correctly!</p>
            <p>Total attempts: <strong>{st.session_state.game_state['number_guess']['attempts']}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Play Again", use_container_width=True):
            del st.session_state.game_state['number_guess']
            st.rerun()
    else:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            guess = st.number_input("Enter your guess (1-100):", min_value=1, max_value=100, value=50)
        
        with col2:
            if st.button("Submit Guess", use_container_width=True):
                target = st.session_state.game_state['number_guess']['target_number']
                st.session_state.game_state['number_guess']['attempts'] += 1
                
                if guess == target:
                    st.session_state.game_state['number_guess']['game_over'] = True
                    st.balloons()
                elif guess < target:
                    st.error("📈 Too low! Try a higher number.")
                else:
                    st.error("📉 Too high! Try a lower number.")
        
        st.info(f"📊 Attempts: {st.session_state.game_state['number_guess']['attempts']}")

def tic_tac_toe():
    """Tic Tac Toe Game"""
    init_game_state('tictactoe')
    
    if 'board' not in st.session_state.game_state['tictactoe']:
        st.session_state.game_state['tictactoe']['board'] = [''] * 9
        st.session_state.game_state['tictactoe']['current_player'] = 'X'
        st.session_state.game_state['tictactoe']['game_over'] = False
        st.session_state.game_state['tictactoe']['winner'] = None
    
    board = st.session_state.game_state['tictactoe']['board']
    
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h2>❌⭕ Tic Tac Toe</h2>
        <p>You play as X, Computer plays as O</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check for winner
    def check_winner(b, player):
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        for pattern in win_patterns:
            if all(b[i] == player for i in pattern):
                return True
        return False
    
    def is_board_full(b):
        return all(cell != '' for cell in b)
    
    # Display board
    cols = st.columns(3)
    for i in range(9):
        row = i // 3
        col = i % 3
        
        with cols[col]:
            button_style = """
            <style>
            .stButton > button[kind="secondary"] {
                width: 80px;
                height: 80px;
                font-size: 32px;
                font-weight: bold;
                border-radius: 12px;
                border: 2px solid #667eea;
            }
            </style>
            """
            st.markdown(button_style, unsafe_allow_html=True)
            
            if board[i] == '' and not st.session_state.game_state['tictactoe']['game_over']:
                if st.button(board[i] if board[i] else ' ', key=f'ttt_{i}', type="secondary"):
                    board[i] = 'X'
                    if check_winner(board, 'X'):
                        st.session_state.game_state['tictactoe']['game_over'] = True
                        st.session_state.game_state['tictactoe']['winner'] = 'You'
                    elif is_board_full(board):
                        st.session_state.game
