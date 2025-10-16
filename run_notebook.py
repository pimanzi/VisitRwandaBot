#!/usr/bin/env python3
"""
Simple launcher - notebook approach
"""

import subprocess
import os

def main():
    print("🇷🇼 Visit Rwanda Tourism Chatbot - Notebook Style")
    print("=" * 50)
    
    # Check if model exists
    if not os.path.exists("models/conservative_FIXED"):
        print("❌ Model not found: models/conservative_FIXED")
        return
    
    print("✅ Model found!")
    print("🚀 Launching app with notebook approach...")
    print("📱 Opening at: http://localhost:8501")
    
    subprocess.run(["streamlit", "run", "app_notebook.py"])

if __name__ == "__main__":
    main()