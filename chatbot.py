import streamlit as st
import random
import time

# Page configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered",
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
    .stChatMessage[data-testid="stChatMessageContent"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        padding: 12px 16px;
    }
    
    /* Bot message styling */
    .stChatMessage[data-testid="stChatMessageContent"]:has(div:contains("assistant")) {
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
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: scale(1.02);
    }
    
    /* Input field styling */
    .stChatInput > div {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
    }
    
    /* Title styling */
    h1 {
        color: #667eea;
        font-weight: 700;
        margin-bottom: 20px;
    }
    
    /* Info box styling */
    .info-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 12px;
        padding: 16px;
        margin: 16px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'typing_complete' not in st.session_state:
    st.session_state.typing_complete = True

# Keyword-based response system
def get_bot_response(user_input):
    """Generate bot response based on user input keywords"""
    user_input_lower = user_input.lower()
    
    # Define keywords and responses
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
            "What do you call a computer that sings? A-Dell! 🎤"
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
    
    # Check for keywords in user input
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

def main():
    """Main application function"""
    
    # Sidebar with options
    with st.sidebar:
        st.title("🤖 ChatBot Settings")
        st.markdown("---")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")
            st.rerun()
        
        st.markdown("---")
        
        # Information section
        st.subheader("ℹ️ About")
        st.info("""
        **ChatBot Features:**
        - 💬 Natural conversation
        - 🎯 Keyword-based responses
        - 🎨 Modern UI design
        - 🌙 Dark mode support
        - 🔒 Session-based memory
        
        **Capabilities:**
        - General conversation
        - Simple Q&A
        - Jokes and fun facts
        - Helpful responses
        """)
        
        st.markdown("---")
        
        # Tips section
        st.subheader("💡 Tips")
        st.markdown("""
        - Try asking about **weather** or **time**
        - Ask for a **joke** to lighten the mood
        - Say **hello** or **goodbye**
        - Ask for **help** anytime
        """)
    
    # Main chat interface
    st.title("🤖 AI ChatBot")
    st.markdown("Welcome! I'm your friendly AI assistant. How can I help you today?")
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate bot response
        with st.chat_message("assistant"):
            # Show typing indicator
            with st.spinner("🤔 Thinking..."):
                time.sleep(0.5)  # Simulate thinking time
                bot_response = get_bot_response(prompt)
            
            # Apply typing effect
            final_response = typing_effect(bot_response)
        
        # Add bot response to chat history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": final_response
        })

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #666; padding: 20px;">
            Made with ❤️ using Streamlit | AI ChatBot v1.0
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
