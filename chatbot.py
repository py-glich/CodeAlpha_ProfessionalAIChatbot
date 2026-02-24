import streamlit as st
import random
import time
import re
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI ChatBot & Companion",
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
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 18px;
        padding: 16px 20px;
        margin: 8px 0;
    }
    
    /* Bot message styling */
    .bot-message {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        color: #333;
        border-radius: 18px;
        padding: 16px 20px;
        margin: 8px 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        padding: 20px;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 12px;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Game cards styling */
    .game-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 28px;
        margin: 20px 0;
        color: white;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }
    
    .game-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
    }
    
    /* Story container */
    .story-container {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 20px;
        padding: 40px;
        color: #f0f0f0;
        line-height: 2;
        font-size: 18px;
        margin: 24px 0;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }
    
    /* Info box styling */
    .info-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 16px;
        padding: 20px;
        margin: 20px 0;
    }
    
    /* Section headers */
    h1, h2, h3 {
        color: #667eea;
        font-weight: 700;
    }
    
    /* Game button styling */
    .game-btn {
        width: 100%;
        margin: 10px 0;
        padding: 20px;
        font-size: 18px;
    }
    
    /* Score display */
    .score-display {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        color: white;
        font-size: 28px;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Navigation tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 56px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 12px;
        font-weight: 600;
        font-size: 14px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Quick reply buttons */
    .quick-reply {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        margin: 4px;
        font-size: 14px;
        cursor: pointer;
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: inline-block;
        padding: 12px 20px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 18px;
    }
    
    .typing-indicator span {
        height: 8px;
        width: 8px;
        background-color: #667eea;
        border-radius: 50%;
        display: inline-block;
        margin: 0 2px;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .typing-indicator span:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-indicator span:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes typing {
        0%, 60%, 100% {
            transform: translateY(0);
        }
        30% {
            transform: translateY(-10px);
        }
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border-left: 4px solid #667eea;
    }
    
    .feature-card:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'conversation_context' not in st.session_state:
    st.session_state.conversation_context = {
        'last_topic': None,
        'user_name': None,
        'mood': None,
        'conversation_count': 0
    }

if 'game_state' not in st.session_state:
    st.session_state.game_state = {}

if 'story_settings' not in st.session_state:
    st.session_state.story_settings = {
        'typing_speed': 0.04,
        'auto_read': False
    }

# ==================== ADVANCED CHATBOT ENGINE ====================

class SmartChatbot:
    """Advanced chatbot with intelligent understanding and responses"""
    
    def __init__(self):
        self.responses = self._build_response_database()
        self.synonyms = self._build_synonyms()
        self.context_patterns = self._build_context_patterns()
    
    def _build_synonyms(self):
        """Build synonym mappings for better understanding"""
        return {
            'greeting': ['hello', 'hi', 'hey', 'hii', 'hlo', 'hola', 'greetings', 'good morning', 'good afternoon', 'good evening', 'yo', 'sup', "what's up", 'howdy'],
            'goodbye': ['bye', 'goodbye', 'see you', 'later', 'ciao', 'farewell', 'tata', 'byebye', 'gotta go', 'have to go'],
            'thanks': ['thanks', 'thank you', 'thankyou', 'thx', 'ty', 'appreciate', 'grateful', 'cheers', 'many thanks'],
            'help': ['help', 'assist', 'support', 'guide', 'how to', 'instructions', 'what can you do', 'capabilities'],
            'name': ['name', 'who are you', 'what are you', 'your name', 'call you', 'identify yourself'],
            'joke': ['joke', 'funny', 'laugh', 'humor', 'make me laugh', 'tell me a joke', 'jokes'],
            'weather': ['weather', 'temperature', 'forecast', 'rain', 'sunny', 'cold', 'hot', 'climate'],
            'time': ['time', 'clock', 'hour', 'what time', 'current time', 'now'],
            'date': ['date', 'today', 'day', 'what day', 'calendar'],
            'age': ['age', 'old', 'how old', 'created', 'birthday', 'when created'],
            'location': ['where', 'location', 'place', 'where are you', 'where do you live'],
            'feeling': ['how are you', 'how do you feel', 'feeling', 'mood', 'are you okay', 'whats up'],
            'happy': ['happy', 'good', 'great', 'awesome', 'excellent', 'wonderful', 'amazing', 'fantastic'],
            'sad': ['sad', 'bad', 'terrible', 'awful', 'depressed', 'unhappy', 'upset', 'lonely'],
            'angry': ['angry', 'mad', 'frustrated', 'annoyed', 'irritated', 'furious'],
            'tired': ['tired', 'sleepy', 'exhausted', 'fatigue', 'drowsy', 'weary'],
            'bored': ['bored', 'boring', 'nothing to do', 'bore', 'entertain me'],
            'excited': ['excited', 'exciting', 'thrilled', 'pumped', 'enthusiastic'],
            'worried': ['worried', 'anxious', 'nervous', 'scared', 'afraid', 'fear', 'stress', 'stressed'],
            'love': ['love', 'like', 'adore', 'care', 'affection', 'heart'],
            'hate': ['hate', 'dislike', 'loathe', 'despise', 'annoying'],
            'food': ['food', 'eat', 'hungry', 'meal', 'breakfast', 'lunch', 'dinner', 'snack', 'cooking', 'recipe'],
            'music': ['music', 'song', 'singer', 'band', 'listen', 'play music', 'playlist'],
            'movie': ['movie', 'film', 'watch', 'cinema', 'netflix', 'series', 'show', 'tv'],
            'book': ['book', 'read', 'reading', 'novel', 'story', 'author'],
            'sports': ['sports', 'game', 'match', 'football', 'cricket', 'basketball', 'tennis', 'player', 'team'],
            'coding': ['code', 'coding', 'program', 'programming', 'developer', 'software', 'computer', 'python', 'javascript'],
            'math': ['math', 'mathematics', 'calculate', 'calculation', 'sum', 'add', 'subtract', 'multiply', 'divide', 'equation'],
            'science': ['science', 'science', 'physics', 'chemistry', 'biology', 'experiment', 'discovery'],
            'history': ['history', 'historical', 'past', 'ancient', 'war', 'civilization', 'century'],
            'travel': ['travel', 'trip', 'vacation', 'holiday', 'tourism', 'visit', 'destination', 'flight', 'hotel'],
            'health': ['health', 'fitness', 'exercise', 'workout', 'gym', 'diet', 'nutrition', 'wellness', 'doctor'],
            'relationship': ['relationship', 'friend', 'family', 'boyfriend', 'girlfriend', 'marriage', 'love life'],
            'work': ['work', 'job', 'career', 'office', 'boss', 'colleague', 'professional', 'business'],
            'study': ['study', 'learning', 'education', 'school', 'college', 'university', 'exam', 'homework'],
            'motivation': ['motivation', 'inspire', 'inspired', 'motivated', 'encourage', 'encouragement', 'quote'],
            'advice': ['advice', 'suggestion', 'recommend', 'tip', 'guidance', 'opinion', 'think'],
            'question': ['question', 'ask', 'query', 'wonder', 'curious', 'curiosity', 'know'],
            'yes': ['yes', 'yeah', 'yep', 'sure', 'okay', 'ok', 'alright'],
            'no': ['no', 'nope', 'nah', 'not', 'never'],
            'sorry': ['sorry', 'apologize', 'apology', 'excuse', 'forgive'],
            'please': ['please', 'kindly', 'would you'],
            'game': ['game', 'play', 'gaming', 'fun', 'entertainment'],
            'story': ['story', 'tale', 'bedtime', 'fairy tale', 'adventure', 'fiction'],
            'fact': ['fact', 'interesting', 'did you know', 'trivia', 'information', 'tell me'],
            'opinion': ['opinion', 'think', 'believe', 'feel about', 'view'],
        }
    
    def _build_response_database(self):
        """Build comprehensive response database"""
        return {
            'greeting': {
                'responses': [
                    "Hello! 👋 Great to see you! How can I assist you today?",
                    "Hi there! 😊 I'm happy you're here. What's on your mind?",
                    "Hey! ✨ How's your day going? Let me know if you need any help!",
                    "Greetings! 🎉 Welcome! How may I help you?",
                    "Hi! 🌟 It's wonderful to chat with you. What would you like to talk about?",
                ],
                'follow_up': ['How are you feeling today?', 'Is there anything specific you need help with?', 'What would you like to do?']
            },
            'goodbye': {
                'responses': [
                    "Goodbye! 👋 It was great chatting with you. Take care!",
                    "See you later! 🌙 Don't be a stranger. Bye!",
                    "Bye for now! 💫 Have an amazing day ahead!",
                    "Until next time! 🎯 Stay safe and stay awesome!",
                    "Farewell! 🎉 Hope to chat with you again soon!",
                ],
                'follow_up': []
            },
            'thanks': {
                'responses': [
                    "You're very welcome! 😊 Happy to help!",
                    "My pleasure! 🙏 Is there anything else I can do for you?",
                    "Anytime! 💪 That's what I'm here for!",
                    "You're welcome! 🌟 Don't hesitate to ask more questions!",
                    "Glad I could help! 🎉 What else can I assist you with?",
                ],
                'follow_up': ['Is there anything else you need?', 'Can I help you with something else?', 'Let me know if you have more questions!']
            },
            'help': {
                'responses': [
                    "I'd be happy to help! 🤝 Here's what I can do:\n\n• Answer your questions\n• Have friendly conversations\n• Play games with you\n• Tell you bedtime stories\n• Provide information and facts\n• Give advice and suggestions\n• And much more!\n\nWhat would you like to explore?",
                    "Great question! 🌟 I can assist you with:\n\n💬 General conversation\n🎮 Fun games (Rock Paper Scissors, Number Guessing, Tic Tac Toe)\n📖 Bedtime stories\n💡 Advice and motivation\n📚 Information on various topics\n\nJust let me know what you need!",
                    "I'm here to help! 🎯 How can I assist you today? Feel free to ask anything!",
                ],
                'follow_up': ['What interests you?', 'Is there a specific topic you want to discuss?', 'Would you like to play a game or hear a story?']
            },
            'name': {
                'responses': [
                    "I'm your friendly AI companion! 🤖 You can call me 'ChatBot' or any name you like!",
                    "I'm ChatBot, your AI friend! 💫 I'm here to chat, help, and entertain you!",
                    "I'm your virtual assistant! 😊 Think of me as a helpful friend who's always here for you!",
                    "I'm called ChatBot! 🎉 I'm designed to assist you with conversations, games, stories, and more!",
                ],
                'follow_up': ['What should I call you?', 'Would you like to tell me your name?']
            },
            'feeling': {
                'responses': [
                    "I'm doing great, thank you for asking! 😊 As an AI,
