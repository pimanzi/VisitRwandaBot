"""
Configuration settings for Rwanda Tourism Chatbot
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "Data"
MODELS_DIR = BASE_DIR / "models"

# Model configurations - Optimized for your DistilBERT conservative_FIXED model
MODEL_CONFIG = {
    "model_name": "conservative_FIXED",  # Your trained model
    "model_path": MODELS_DIR / "conservative_FIXED",
    "max_answer_length": 200,  # Matches your training configuration
    "max_context_length": 512,  # Matches model's max_position_embeddings
    "confidence_threshold": 0.2,  # Optimized for DistilBERT QA performance
    "model_type": "distilbert",  # Specific model architecture
    "tokenizer_max_length": 512,  # Matches model configuration
}

# Dataset configuration
DATASET_CONFIG = {
    "knowledge_base_path": DATA_DIR / "visitRwanda_qa.csv",
    "fallback_contexts": {
        "national_parks": (
            "Rwanda has four national parks: Volcanoes National Park famous for mountain gorilla trekking, "
            "Akagera National Park offering Big Five safari experiences, Nyungwe National Park known for "
            "chimpanzee tracking and canopy walks, and Gishwati-Mukura National Park focusing on forest conservation."
        ),
        "cultural_heritage": (
            "Rwanda's cultural heritage includes the King's Palace Museum in Nyanza, Ethnographic Museum in Huye, "
            "Kigali Genocide Memorial, Rwanda Art Museum, and traditional Intore dance performances. "
            "These sites showcase Rwanda's rich history, culture, and traditions."
        ),
        "general": (
            "Rwanda is known as the Land of a Thousand Hills, offering incredible wildlife experiences in national parks "
            "and rich cultural heritage sites. The country is famous for mountain gorilla trekking, safari adventures, "
            "and welcoming culture."
        )
    }
}

# UI Configuration
UI_CONFIG = {
    "page_title": "Visit Rwanda Chatbot",
    "page_icon": "🇷🇼",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Colors (Tourism theme - green and white)
COLORS = {
    "primary": "#2E8B57",      # Sea Green
    "secondary": "#90EE90",    # Light Green
    "accent": "#228B22",       # Forest Green
    "background": "#F0FFF0",   # Honeydew
    "text": "#2F4F4F",         # Dark Slate Gray
    "white": "#FFFFFF"
}

# Chat configuration
CHAT_CONFIG = {
    "max_messages": 50,
    "welcome_message": (
        "🇷🇼 **Muraho!** Welcome to Visit Rwanda! I'm your personal tourism guide.\n\n"
        "I can help you with:\n"
        "🦍 National Parks (Volcanoes, Akagera, Nyungwe, Gishwati-Mukura)\n"
        "🏛️ Cultural Heritage (Museums, Traditional Dances, Historical Sites)\n"
        "🎯 Tourism Planning (Best times to visit, permits, activities)\n\n"
        "**What would you like to know about Rwanda?**"
    ),
    "example_questions": [
        "How many national parks are in Rwanda?",
        "Where can I see mountain gorillas?",
        "What museums can I visit in Rwanda?",
        "What is the best time to visit Rwanda?",
        "How much does gorilla trekking cost?",
        "What animals are in Akagera National Park?"
    ]
}