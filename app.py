"""
Visit Rwanda Tourism Chatbot - Streamlit Interface
Clean, single-page design optimized for user experience
"""

import streamlit as st
import time
from app.chatbot import RwandaTourismChatbot

# Page configuration - REMOVE white space at top
st.set_page_config(
    page_title="Visit Rwanda Chatbot",
    page_icon="🇷🇼",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar completely
)

# Custom CSS to remove white space and improve design
st.markdown("""
<style>
    /* Remove top padding and margins */
    .main > div {
        padding-top: 0.5rem;
    }
    
    /* Hide sidebar completely */
    .css-1d391kg, [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Remove header space and menu */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    
    /* Hide Streamlit menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .css-14xtw13.e8zbici0 {display: none;}
    
    /* Ensure black text on white background */
    .main, .stApp {
        background-color: white;
        color: black;
    }
    
    /* Custom chat container */
    .chat-container {
        background: linear-gradient(135deg, #f8fff8 0%, #ffffff 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border-left: 5px solid #2E8B57;
        color: black;
    }
    
    /* Question examples styling */
    .stButton > button {
        background: #2E8B57;
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        margin: 5px;
        border: none;
        cursor: pointer;
        font-size: 14px;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: #228B50;
        color: white;
    }
    
    /* Main title styling */
    .main-title {
        text-align: center;
        color: #2E8B57;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: bold;
    }
    
    /* Subtitle styling */
    .subtitle {
        text-align: center;
        color: #333;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Chat input styling */
    .stChatInput > div > div > input {
        border-radius: 20px;
        border: 2px solid #2E8B57;
        padding: 10px 15px;
        color: black;
        background-color: white;
    }
    
    /* Chat messages styling */
    .stChatMessage {
        background-color: white;
        color: black;
    }
    
    /* Ensure all text is black */
    p, div, span, h1, h2, h3, h4, h5, h6 {
        color: black !important;
    }
    
    /* Example questions section */
    .example-section {
        background: #f8fff8;
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        border: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize chatbot (cached to avoid reloading)
@st.cache_resource
def load_chatbot():
    """Load chatbot once and cache it"""
    try:
        return RwandaTourismChatbot()
    except Exception as e:
        st.error(f"Failed to load chatbot: {e}")
        return None

def main():
    """Main application"""
    
    # Header Section
    st.markdown('<h1 class="main-title">🇷🇼 Visit Rwanda Tourism Chatbot</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your AI guide to the Land of a Thousand Hills 🏔️</p>', unsafe_allow_html=True)
    
    # Load chatbot
    chatbot = load_chatbot()
    if not chatbot:
        st.error("❌ Unable to load the chatbot. Please check your model files.")
        return
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Welcome message
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Hello! 👋 I'm your Rwanda Tourism guide. Ask me about national parks, wildlife, cultural sites, or any tourism information about Rwanda!",
            "confidence": 1.0
        })
    
    # Example questions section
    st.markdown('<div class="example-section">', unsafe_allow_html=True)
    st.markdown("### 💡 Try these questions:")
    
    # Create columns for example questions
    col1, col2, col3 = st.columns(3)
    
    example_questions = [
        "How many national parks are in Rwanda?",
        "Where can I see mountain gorillas?", 
        "What animals are in Akagera National Park?",
        "What museums can I visit in Rwanda?",
        "Tell me about Rwanda's cultural heritage",
        "What is the best time to visit Rwanda?"
    ]
    
    # Display example questions as buttons
    for i, question in enumerate(example_questions):
        col = [col1, col2, col3][i % 3]
        with col:
            if st.button(question, key=f"example_{i}", help="Click to ask this question"):
                st.session_state.user_input = question
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Chat interface
    st.markdown("### 💬 Chat with Rwanda Tourism Bot")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                st.write(message["content"])
                if "confidence" in message and message["confidence"] < 1.0:
                    confidence_color = "🟢" if message["confidence"] > 0.7 else "🟡" if message["confidence"] > 0.4 else "🔴"
                    st.caption(f"{confidence_color} Confidence: {message['confidence']:.1%}")
            else:
                st.write(message["content"])
    
    # Chat input
    user_input = st.chat_input("Ask me anything about Rwanda tourism...")
    
    # Handle user input from chat or example buttons
    if user_input or (hasattr(st.session_state, 'user_input') and st.session_state.user_input):
        
        # Get the question
        question = user_input if user_input else st.session_state.user_input
        
        # Clear the session state input
        if hasattr(st.session_state, 'user_input'):
            del st.session_state.user_input
        
        # Add user message
        st.session_state.messages.append({
            "role": "user", 
            "content": question
        })
        
        # Display user message
        with st.chat_message("user"):
            st.write(question)
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    response = chatbot.answer_question(question)
                    
                    if response:
                        st.write(response["answer"])
                        
                        # Add to session state
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response["answer"],
                            "confidence": response.get("confidence", 0.0)
                        })
                        
                        # Show confidence
                        confidence = response.get("confidence", 0.0)
                        if confidence > 0:
                            confidence_color = "🟢" if confidence > 0.7 else "🟡" if confidence > 0.4 else "🔴"
                            st.caption(f"{confidence_color} Confidence: {confidence:.1%}")
                    
                    else:
                        error_msg = "I apologize, but I couldn't process your question. Please try asking about Rwanda's national parks or cultural heritage."
                        st.write(error_msg)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": error_msg,
                            "confidence": 0.0
                        })
                        
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": error_msg,
                        "confidence": 0.0
                    })
    
    # Footer information
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <small>
        🌟 Powered by AI trained on Rwanda Tourism data<br>
        🏔️ Discover Rwanda's national parks, wildlife, and cultural heritage<br>
        🤖 Built with Streamlit and Transformers
        </small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()