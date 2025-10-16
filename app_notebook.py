"""
Visit Rwanda Tourism Chatbot - Using notebook's exact approach
Clean UI with proper button visibility
"""

import streamlit as st
from app.chatbot_notebook import RwandaChatbot

# Page config
st.set_page_config(
    page_title="Visit Rwanda Chatbot",
    page_icon="🇷🇼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Clean CSS styling - white background, green accents, black text
st.markdown("""
<style>
    /* Clean white background for entire app */
    .main > div { 
        padding-top: 1rem; 
        background-color: white;
    }
    .css-1d391kg, [data-testid="stSidebar"] { display: none; }
    .block-container { 
        padding-top: 2rem; 
        background-color: white;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main title styling - green accent */
    .main-title {
        text-align: center;
        color: #2E8B57;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: bold;
    }
    
    /* Subtitle styling - black text */
    .subtitle {
        text-align: center;
        color: #000;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Clean button styling - white background, green border, black text */
    .stButton > button {
        background-color: white !important;
        color: black !important;
        border: 1px solid #2E8B57 !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        margin: 4px !important;
        width: 100% !important;
        font-size: 14px !important;
        transition: none !important;
    }
    
    /* Simple hover effect - just green background */
    .stButton > button:hover {
        background-color: #2E8B57 !important;
        color: white !important;
        border: 1px solid #2E8B57 !important;
    }
    
    /* Clean text styling - black throughout */
    .stMarkdown, .stText, .stCaption, p, div, span {
        color: #000 !important;
    }
    
    /* Chat input styling */
    .stChatInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #2E8B57;
        padding: 10px 15px;
        color: black;
        background-color: white;
    }
    
    /* Chat messages styling */
    .stChatMessage {
        background-color: white;
        color: black;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_chatbot():
    """Load chatbot with notebook's exact approach"""
    return RwandaChatbot()

def main():
    # Header
    st.markdown('<h1 class="main-title">🇷🇼 Visit Rwanda Tourism Chatbot</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your AI guide to the Land of a Thousand Hills 🏔️</p>', unsafe_allow_html=True)
    
    # Load chatbot
    chatbot = load_chatbot()
    
    # Initialize chat
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Hello! 👋 I'm your Rwanda Tourism guide using your trained conservative_FIXED model with proper context retrieval. Ask me about national parks, wildlife, cultural sites, or any tourism information!"
        })
    
    # Example questions section - clean and simple
    st.markdown("### 💡 Try these questions:")
    
    col1, col2, col3 = st.columns(3)
    
    examples = [
        "How many national parks are in Rwanda?",
        "Where can I see mountain gorillas?", 
        "What animals are in Akagera National Park?",
        "What museums can I visit in Rwanda?",
        "What is the best time to visit Rwanda?",
        "What are traditional Rwandan ceremonial dances?"
    ]
    
    for i, question in enumerate(examples):
        col = [col1, col2, col3][i % 3]
        with col:
            if st.button(question, key=f"ex_{i}"):
                st.session_state.user_input = question
                st.rerun()
    
    st.markdown("---")
    
    # Chat interface
    st.markdown("### 💬 Chat")
    
    # Display messages (NO CONFIDENCE)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    user_input = st.chat_input("Ask about Rwanda tourism...")
    
    if user_input or (hasattr(st.session_state, 'user_input') and st.session_state.user_input):
        question = user_input if user_input else st.session_state.user_input
        
        if hasattr(st.session_state, 'user_input'):
            del st.session_state.user_input
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": question})
        
        with st.chat_message("user"):
            st.write(question)
        
        # Get response using notebook's exact method
        with st.chat_message("assistant"):
            with st.spinner("🤔 Retrieving context and generating answer..."):
                response = chatbot.answer_question(question, provide_context=True)
                
                if response:
                    st.write(response["answer"])
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response["answer"]
                    })
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <small>
        🌟 Powered by your trained conservative_FIXED model<br>
        🏔️ Discover Rwanda's national parks, wildlife, and cultural heritage<br>
        🤖 Built with exact notebook approach
        </small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()