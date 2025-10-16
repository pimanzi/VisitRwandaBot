"""
Rwanda Tourism Chatbot - Optimized for fast responses
Pre-loads models to avoid user delays
"""

import os
import pandas as pd
from typing import Dict, Optional
from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering
from app.config.settings import MODEL_CONFIG, DATASET_CONFIG
from app.utils.context_retrieval import ContextRetrievalSystem
from app.utils.question_handler import NonTourismQuestionHandler

class RwandaTourismChatbot:
    """Rwanda Tourism Chatbot with optimized loading"""

    def __init__(self):
        """Initialize chatbot with pre-loaded models"""
        self.qa_pipeline = None
        self.retrieval_system = None
        self.non_tourism_handler = NonTourismQuestionHandler()
        self.knowledge_base = []
        self.is_initialized = False
        
        # Load everything immediately
        self._load_models()
        self._load_knowledge_base()
        self.is_initialized = True

    def _load_models(self):
        """Load QA model (should be fast since it's cached)"""
        try:
            model_path = MODEL_CONFIG["model_path"]
            
            # Load model and tokenizer
            tokenizer = AutoTokenizer.from_pretrained(model_path)
            model = AutoModelForQuestionAnswering.from_pretrained(model_path)
            
            # Create pipeline with optimized parameters
            self.qa_pipeline = pipeline(
                "question-answering",
                model=model,
                tokenizer=tokenizer,
                device=-1,  # Use CPU for stability
                max_answer_len=MODEL_CONFIG["max_answer_length"],
                handle_impossible_answer=True,
                return_tensors=True,
                top_k=1,
                doc_stride=128,
                max_question_len=64,
                max_seq_len=512
            )
            
            print(" QA model loaded successfully")
            
        except Exception as e:
            print(f" Failed to load QA model: {e}")
            raise

    def _load_knowledge_base(self):
        """Load knowledge base for context retrieval"""
        try:
            # Try to find the data file
            possible_paths = [
                "Data/visitRwanda_qa.csv",
                "visitRwanda_qa.csv",
                "data/visitRwanda_qa.csv",
                "Data/QA.txt"
            ]
            
            contexts_loaded = False
            for path in possible_paths:
                if os.path.exists(path):
                    if path.endswith('.csv'):
                        df = pd.read_csv(path)
                        if 'answer' in df.columns:
                            self.knowledge_base = df['answer'].dropna().unique().tolist()
                            contexts_loaded = True
                            print(f" Loaded {len(self.knowledge_base)} contexts from: {path}")
                            break
                    elif path.endswith('.txt'):
                        with open(path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Split by questions or double newlines
                            contexts = [ctx.strip() for ctx in content.split('\n\n') if ctx.strip()]
                            self.knowledge_base = contexts
                            contexts_loaded = True
                            print(f" Loaded {len(self.knowledge_base)} contexts from: {path}")
                            break
            
            if not contexts_loaded:
                print(" Using default Rwanda tourism contexts")
                self._create_default_contexts()
            
            # Initialize retrieval system
            self.retrieval_system = ContextRetrievalSystem("hybrid")
            self.retrieval_system.build_retrieval_index(self.knowledge_base)
            print(f" Context retrieval ready")
                
        except Exception as e:
            print(f" Knowledge base loading failed: {e}")
            self._create_default_contexts()

    def _create_default_contexts(self):
        """Create default contexts if data file not available"""
        self.knowledge_base = [
            "Rwanda has four national parks: Volcanoes National Park for mountain gorillas, Akagera National Park for safari wildlife, Nyungwe National Park for chimpanzees and forest biodiversity, and Gishwati-Mukura National Park for conservation.",
            "Volcanoes National Park is famous for mountain gorilla trekking experiences with permits costing $1,500 per person.",
            "Akagera National Park offers classic African safari experiences with the Big Five animals: lions, elephants, leopards, rhinoceros, and buffalo.",
            "Nyungwe National Park features ancient rainforest with chimpanzee tracking, canopy walks, and over 300 bird species.",
            "Rwanda has several important museums: King's Palace Museum in Nyanza, Ethnographic Museum in Huye, Kigali Genocide Memorial, Rwanda Art Museum, and Kandt House Museum.",
            "Traditional Rwandan dances include Intore warrior dances performed at cultural centers and special events.",
            "Lake Kivu is one of Africa's great lakes offering beautiful beaches, water sports, and scenic boat trips.",
            "Kigali, the capital city, is known for being one of the cleanest cities in Africa with modern infrastructure.",
            "Rwanda is famous for its high-quality coffee grown in volcanic soil at high altitudes.",
            "The best time to visit Rwanda is during the dry seasons: June to September and December to February."
        ]
        
        # Initialize retrieval system with defaults
        self.retrieval_system = ContextRetrievalSystem("hybrid") 
        self.retrieval_system.build_retrieval_index(self.knowledge_base)

    def answer_question(self, question: str) -> Optional[Dict]:
        """Answer user question quickly"""
        try:
            # Check if tourism-related
            is_tourism, category = self.non_tourism_handler.is_tourism_related(question)
            
            if not is_tourism:
                return {
                    "answer": self.non_tourism_handler.get_fallback_response(question),
                    "confidence": 0.0,
                    "category": "non_tourism"
                }
            
            # Get context (should be fast since models are pre-loaded)
            if self.retrieval_system:
                contexts = self.retrieval_system.retrieve_contexts(question, top_k=3)
                combined_context = " ".join(contexts)
            else:
                combined_context = " ".join(self.knowledge_base[:3])
            
            # Get answer from QA model
            result = self.qa_pipeline(
                question=question,
                context=combined_context
            )
            
            return {
                "answer": result['answer'].strip(),
                "confidence": result['score'],
                "category": category,
                "context_used": len(combined_context)
            }
            
        except Exception as e:
            return {
                "answer": f"I apologize, but I encountered an error processing your question about Rwanda tourism. Please try rephrasing your question.",
                "confidence": 0.0,
                "error": str(e)
            }

    def is_model_ready(self) -> bool:
        """Check if the model is ready for inference"""
        return self.qa_pipeline is not None and self.is_initialized