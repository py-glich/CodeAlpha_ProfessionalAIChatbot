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
    .main { padding-bottom: 100px; }
    .stChatMessage { border-radius: 12px; padding: 16px; margin: 8px 0; }
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
    .game-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        color: white;
        text-align: center;
    }
    h1, h2, h3 { color: #667eea; font-weight: 700; }
    .score-display {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'game_state' not in st.session_state:
    st.session_state.game_state = {}
if 'story_settings' not in st.session_state:
    st.session_state.story_settings = {'typing_speed': 0.05, 'auto_read': False}

# ==================== CHATBOT FUNCTIONS ====================

def get_bot_response(user_input):
    user_input_lower = user_input.lower()
    
    responses = {
        'greeting': ["Hello! How can I help you today? 😊", "Hi there!", "Hey! I'm here to help."],
        'help': ["I'm here to help! What do you need?", "Sure, I can help with that."],
        'weather': ["I don't have real-time weather data, but weather is fascinating! ☀️"],
        'time': ["Time is precious! ⏰ What else can I help with?"],
        'name': ["I'm your friendly AI chatbot! 🤖", "You can call me ChatBot!"],
        'joke': ["Why did the AI go to therapy? Too many deep learning issues! 😄", "Why do programmers prefer dark mode? Light attracts bugs! 🐛"],
        'thanks': ["You're welcome! Happy to help! 😊", "Anytime!"],
        'goodbye': ["Goodbye! It was great chatting! 👋", "See you later!", "Take care!"],
        'default': ["That's interesting! Tell me more.", "What else is on your mind?", "I'm not sure. Could you elaborate?"]
    }
    
    if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'greetings']): return random.choice(responses['greeting'])
    elif any(word in user_input_lower for word in ['help', 'assist', 'support']): return random.choice(responses['help'])
    elif any(word in user_input_lower for word in ['weather', 'temperature']): return random.choice(responses['weather'])
    elif any(word in user_input_lower for word in ['time', 'clock', 'hour']): return random.choice(responses['time'])
    elif any(word in user_input_lower for word in ['name', 'who are you']): return random.choice(responses['name'])
    elif any(word in user_input_lower for word in ['joke', 'funny', 'laugh']): return random.choice(responses['joke'])
    elif any(word in user_input_lower for word in ['thanks', 'thank you']): return random.choice(responses['thanks'])
    elif any(word in user_input_lower for word in ['bye', 'goodbye', 'later']): return random.choice(responses['goodbye'])
    else: return random.choice(responses['default'])

# ==================== GAMES FUNCTIONS ====================

def init_game_state(game_name):
    if game_name not in st.session_state.game_state:
        st.session_state.game_state[game_name] = {}

def rock_paper_scissors():
    init_game_state('rps')
    st.markdown("<h2 style='text-align:center;'>🪨 Rock Paper Scissors ✂️📄</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    moves = ['🪨 Rock', '✂️ Scissors', '📄 Paper']
    
    for col, move in zip([col1, col2, col3], moves):
        with col:
            if st.button(move, use_container_width=True):
                computer_move = random.choice(moves)
                if move == computer_move:
                    result, color = "🤝 It's a Tie!", "blue"
                elif (move == '🪨 Rock' and computer_move == '✂️ Scissors') or \
                     (move == '✂️ Scissors' and computer_move == '📄 Paper') or \
                     (move == '📄 Paper' and computer_move == '🪨 Rock'):
                    result, color = "🎉 You Win!", "green"
                else:
                    result, color = "😔 You Lose!", "red"
                st.session_state.game_state['rps']['last_result'] = {'user': move, 'computer': computer_move, 'result': result, 'color': color}
    
    if 'last_result' in st.session_state.game_state.get('rps', {}):
        r = st.session_state.game_state['rps']['last_result']
        color_hex = '#38ef7d' if r['color'] == 'green' else '#ef4444' if r['color'] == 'red' else '#fbbf24'
        st.markdown(f"""
        <div style='text-align:center; padding:20px; background:linear-gradient(135deg,#667eea,#764ba2); border-radius:16px; color:white; margin-top:20px;">
            <h3>Your Choice: {r['user']}</h3>
            <h3>Computer's Choice: {r['computer']}</h3>
            <h2 style='color:{color_hex}'>{r['result']}</h2>
        </div>
        """, unsafe_allow_html=True)

def number_guessing_game():
    init_game_state('number_guess')
    if 'target_number' not in st.session_state.game_state['number_guess']:
        st.session_state.game_state['number_guess'] = {
            'target_number': random.randint(1, 100),
            'attempts': 0,
            'game_over': False
        }
    
    st.markdown("<h2 style='text-align:center;'>🎯 Number Guessing Game</h2>", unsafe_allow_html=True)
    
    if st.session_state.game_state['number_guess']['game_over']:
        st.markdown(f"""
        <div style='text-align:center; padding:20px; background:linear-gradient(135deg,#11998e,#38ef7d); border-radius:16px; color:white;'>
            <h2>🎉 Congratulations!</h2>
            <p>Number: <strong>{st.session_state.game_state['number_guess']['target_number']}</strong></p>
            <p>Attempts: <strong>{st.session_state.game_state['number_guess']['attempts']}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 Play Again"):
            del st.session_state.game_state['number_guess']
            st.rerun()
    else:
        col1, col2 = st.columns([2, 1])
        with col1:
            guess = st.number_input("Enter guess (1-100):", 1, 100, 50)
        with col2:
            if st.button("Submit"):
                target = st.session_state.game_state['number_guess']['target_number']
                st.session_state.game_state['number_guess']['attempts'] += 1
                if guess == target:
                    st.session_state.game_state['number_guess']['game_over'] = True
                    st.balloons()
                elif guess < target: st.error("📈 Too low!")
                else: st.error("📉 Too high!")
        st.info(f"📊 Attempts: {st.session_state.game_state['number_guess']['attempts']}")

def tic_tac_toe():
    init_game_state('tictactoe')
    if 'board' not in st.session_state.game_state['tictactoe']:
        st.session_state.game_state['tictactoe'] = {
            'board': [''] * 9,
            'game_over': False,
            'winner': None
        }
    
    st.markdown("<h2 style='text-align:center;'>❌⭕ Tic Tac Toe</h2>", unsafe_allow_html=True)
    board = st.session_state.game_state['tictactoe']['board']
    
    def check_winner(b, p):
        patterns = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        return any(all(b[i] == p for i in pat) for pat in patterns)
    
    def is_full(b): return all(c != '' for c in b)
    
    cols = st.columns(3)
    for i in range(9):
        with cols[i % 3]:
            if board[i] == '' and not st.session_state.game_state['tictactoe']['game_over']:
                if st.button(' ', key=f'ttt_{i}', use_container_width=True):
                    board[i] = 'X'
                    if check_winner(board, 'X'):
                        st.session_state.game_state['tictactoe']['game_over'] = True
                        st.session_state.game_state['tictactoe']['winner'] = 'You'
                    elif is_full(board):
                        st.session_state.game_state['tictactoe']['game_over'] = True
                        st.session_state.game_state['tictactoe']['winner'] = 'Draw'
                    else:
                        # Computer's turn
                        empty = [j for j, c in enumerate(board) if c == '']
                        if empty:
                            board[random.choice(empty)] = 'O'
                            if check_winner(board, 'O'):
                                st.session_state.game_state['tictactoe']['game_over'] = True
                                st.session_state.game_state['tictactoe']['winner'] = 'Computer'
            
            # Display cell
            emoji = '❌' if board[i] == 'X' else '⭕' if board[i] == 'O' else ''
            bg = '#e8f5e9' if board[i] == 'X' else '#ffebee' if board[i] == 'O' else '#f5f5f5'
            st.markdown(f"<div style='padding:20px; background:{bg}; border-radius:12px; text-align:center; font-size:32px;'>{emoji}</div>", unsafe_allow_html=True)
    
    if st.session_state.game_state['tictactoe']['game_over']:
        winner = st.session_state.game_state['tictactoe']['winner']
        if winner == 'Draw':
            st.warning("🤝 It's a Draw!")
        else:
            st.success(f"🎉 {winner} Wins!")
        if st.button("🔄 Play Again"):
            del st.session_state.game_state['tictactoe']
            st.rerun()

# ==================== MAIN APP ====================

def main():
    st.title("🤖 AI ChatBot & Games")
    st.markdown("Welcome! Choose a tab below to chat or play games.")
    
    tab1, tab2, tab3, tab4 = st.tabs(["💬 ChatBot", "🪨 Rock Paper Scissors", "🎯 Number Guessing", "❌⭕ Tic Tac Toe"])
    
    with tab1:
        # Chat display
        for msg in st.session_state.chat_history:
            with st.chat_message(msg['role']):
                st.markdown(msg['content'])
        
        # Chat input
        if prompt := st.chat_input("Type a message..."):
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.chat_history.append({'role': 'user', 'content': prompt})
            
            response = get_bot_response(prompt)
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.chat_history.append({'role': 'assistant', 'content': response})
        
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    with tab2:
        rock_paper_scissors()
    
    with tab3:
        number_guessing_game()
    
    with tab4:
        tic_tac_toe()

if __name__ == "__main__":
    main()
