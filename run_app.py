#!/usr/bin/env python3
"""
Optimized launcher for Visit Rwanda Tourism Chatbot
Pre-downloads all data to avoid delays during user interaction
"""

import sys
import os
import subprocess

def check_requirements():
    """Check if required packages are installed"""
    try:
        import streamlit
        import transformers
        import torch
        import pandas
        import nltk
        import sentence_transformers
        print("✅ All required packages are installed!")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("📦 Run: pip install -r requirements.txt")
        return False

def preload_all_models():
    """Pre-download and cache all models to avoid delays during user interaction"""
    print("🔄 Pre-loading models and data (one-time setup)...")
    
    try:
        # Download NLTK data
        import nltk
        print("  📚 Downloading NLTK data...")
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('punkt_tab', quiet=True)
        
        # Pre-load sentence transformer model
        print("  🧠 Loading sentence transformer model...")
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("  ✅ Sentence transformer cached!")
        
        # Test tokenizer loading
        print("  🔤 Testing tokenizer...")
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained("models/conservative_FIXED")
        print("  ✅ Tokenizer ready!")
        
        print("✅ All models pre-loaded successfully!")
        return True
        
    except Exception as e:
        print(f"⚠️ Warning during pre-loading: {e}")
        return True  # Continue anyway

def check_model_files():
    """Check if trained model files exist"""
    model_path = "models/conservative_FIXED"
    if os.path.exists(model_path):
        print(f"✅ Found trained model: {model_path}")
        return True
    else:
        print(f"❌ Trained model not found: {model_path}")
        return False

def check_data_files():
    """Check if required data files exist"""
    # Check for any of these data files
    possible_files = [
        "Data/visitRwanda_qa.csv",
        "visitRwanda_qa.csv", 
        "data/visitRwanda_qa.csv"
    ]
    
    for data_file in possible_files:
        if os.path.exists(data_file):
            print(f"✅ Found data file: {data_file}")
            return True
    
    print(f"⚠️ Data file not found, using default contexts")
    return True  # Continue without data file

def main():
    """Main function to test and launch the app"""
    print("🇷🇼 Visit Rwanda Tourism Chatbot - Optimized Launcher")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check model files
    if not check_model_files():
        print("\n❌ Cannot run without trained model!")
        sys.exit(1)
    
    # Check data files
    check_data_files()
    
    # Pre-load everything
    print("\n🚀 Preparing for fast user experience...")
    preload_all_models()
    
    # Launch the app
    print("\n✨ Launching Rwanda Tourism Chatbot...")
    print("📱 App will open at: http://localhost:8501")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 60)
    
    try:
        subprocess.run([
            "streamlit", "run", "app.py",
            "--server.port=8501",
            "--server.address=localhost",
            "--server.headless=false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Thank you for using Visit Rwanda Chatbot!")
    except FileNotFoundError:
        print("❌ Streamlit not found. Install with: pip install streamlit")

if __name__ == "__main__":
    main()