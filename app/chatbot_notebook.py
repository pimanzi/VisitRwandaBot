"""
Rwanda Tourism Chatbot - Exactly like your notebook
Uses proper context retrieval system
"""

import os
import pandas as pd
from typing import Dict, Optional, List
from transformers import pipeline
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer, util
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import torch
import numpy as np

# Download NLTK data (one time only)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
    
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

class ContextRetrievalSystem:
    """Hybrid BM25 + Semantic search - EXACTLY from your notebook"""

    def __init__(self, retrieval_method: str = "hybrid"):
        self.retrieval_method = retrieval_method
        self.bm25 = None
        self.sentence_model = None
        self.context_embeddings = None
        self.contexts = []
        self.stop_words = set(stopwords.words('english'))

    def build_retrieval_index(self, contexts: List[str]):
        """Build retrieval index - EXACTLY from your notebook"""
        self.contexts = contexts

        if self.retrieval_method in ["bm25", "hybrid"]:
            tokenized = [self._tokenize_text(ctx) for ctx in contexts]
            self.bm25 = BM25Okapi(tokenized)
            print(f" Built BM25 index with {len(contexts)} contexts")

        if self.retrieval_method in ["semantic", "hybrid"]:
            print(" Building semantic index...")
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            self.context_embeddings = self.sentence_model.encode(
                contexts, convert_to_tensor=True, show_progress_bar=False
            )
            print(f" Built semantic index with {len(contexts)} contexts")

    def _tokenize_text(self, text: str) -> List[str]:
        """Tokenize and clean text - EXACTLY from your notebook"""
        text = text.lower()
        tokens = word_tokenize(text)
        tokens = [t for t in tokens if t not in self.stop_words and len(t) > 2]
        return tokens

    def retrieve_contexts(self, query: str, top_k: int = 3) -> List[str]:
        """Retrieve top-k contexts - EXACTLY from your notebook"""
        if self.retrieval_method == "bm25":
            return self._bm25_retrieval(query, top_k)
        elif self.retrieval_method == "semantic":
            return self._semantic_retrieval(query, top_k)
        else:
            return self._hybrid_retrieval(query, top_k)

    def _bm25_retrieval(self, query: str, top_k: int) -> List[str]:
        """BM25 retrieval - EXACTLY from your notebook"""
        tokenized_query = self._tokenize_text(query)
        scores = self.bm25.get_scores(tokenized_query)
        top_indices = np.argsort(scores)[::-1][:top_k]
        return [self.contexts[i] for i in top_indices if scores[i] > 0]

    def _semantic_retrieval(self, query: str, top_k: int) -> List[str]:
        """Semantic retrieval - EXACTLY from your notebook"""
        query_embedding = self.sentence_model.encode(query, convert_to_tensor=True)
        cos_scores = util.cos_sim(query_embedding, self.context_embeddings)[0]
        top_results = torch.topk(cos_scores, k=min(top_k, len(self.contexts)))
        return [self.contexts[idx] for idx in top_results.indices]

    def _hybrid_retrieval(self, query: str, top_k: int) -> List[str]:
        """Hybrid retrieval - EXACTLY from your notebook"""
        bm25_results = self._bm25_retrieval(query, top_k * 2)
        semantic_results = self._semantic_retrieval(query, top_k * 2)

        # Combine with scoring
        combined = {}
        for ctx in bm25_results:
            combined[ctx] = combined.get(ctx, 0) + 1
        for ctx in semantic_results:
            combined[ctx] = combined.get(ctx, 0) + 1

        sorted_results = sorted(combined.items(), key=lambda x: x[1], reverse=True)
        return [ctx for ctx, _ in sorted_results[:top_k]]


class NonTourismQuestionHandler:
    """Handle non-tourism questions - EXACTLY from your notebook"""

    def __init__(self):
        self.tourism_keywords = {
            'national_parks': [
                'park', 'gorilla', 'chimpanzee', 'wildlife', 'safari',
                'akagera', 'volcanoes', 'nyungwe', 'gishwati', 'mukura',
                'trekking', 'hiking', 'animals', 'birds'
            ],
            'cultural_heritage': [
                'museum', 'culture', 'dance', 'traditional', 'heritage',
                'palace', 'history', 'intore', 'art', 'monument',
                'ethnographic', 'genocide', 'memorial'
            ],
            'general_tourism': [
                'rwanda', 'visit', 'tourism', 'travel', 'tourist',
                'attraction', 'destination', 'kigali'
            ]
        }

    def is_tourism_related(self, question: str) -> tuple[bool, str]:
        """Check if question is tourism-related - EXACTLY from your notebook"""
        question_lower = question.lower()

        # Check each category
        for category, keywords in self.tourism_keywords.items():
            if any(keyword in question_lower for keyword in keywords):
                return True, category

        return False, "non_tourism"

    def get_fallback_response(self, question: str) -> str:
        """Generate fallback response - EXACTLY from your notebook"""
        return (
            "I apologize, but I'm specifically designed to answer questions "
            "about Rwanda's tourism, including national parks and cultural heritage. "
            "Your question doesn't seem to be related to these topics. "
            "Please ask me about Rwanda's national parks (Volcanoes, Akagera, "
            "Nyungwe, Gishwati-Mukura) or cultural heritage sites (museums, "
            "traditional dances, monuments, etc.)."
        )


class RwandaChatbot:
    """Rwanda Tourism Chatbot - EXACTLY like your notebook AdvancedTester"""

    def __init__(self):
        """Initialize chatbot - EXACTLY like your notebook"""
        print(" Loading your conservative_FIXED model...")
        
        # Load QA pipeline - EXACTLY like your notebook
        self.qa_pipeline = pipeline(
            "question-answering",
            model="models/conservative_FIXED",
            tokenizer="models/conservative_FIXED",
            device=0 if torch.cuda.is_available() else -1
        )
        print(" Model loaded successfully!")
        
        # Initialize retrieval system - EXACTLY like your notebook
        self.retrieval_system = ContextRetrievalSystem("hybrid")
        self.non_tourism_handler = NonTourismQuestionHandler()
        
        # Load knowledge base - EXACTLY like your notebook
        self.load_knowledge_base()

    def load_knowledge_base(self):
        """Load knowledge base from dataset - EXACTLY like your notebook"""
        try:
            # Try multiple possible paths
            possible_paths = [
                'Data/visitRwanda_qa.csv',
                'visitRwanda_qa.csv',
                'rwanda_tourism_balanced_FIXED.csv'
            ]
            
            df = None
            for path in possible_paths:
                if os.path.exists(path):
                    df = pd.read_csv(path)
                    print(f" Loaded knowledge base from: {path}")
                    break
            
            if df is not None:
                self.knowledge_base = df['answer'].dropna().unique().tolist()
                self.retrieval_system.build_retrieval_index(self.knowledge_base)
                print(f" Loaded knowledge base with {len(self.knowledge_base)} tourism facts")
            else:
                print(" Could not find knowledge base file")
                self.knowledge_base = []
                
        except Exception as e:
            print(f" Could not load knowledge base: {e}")
            self.knowledge_base = []

    def answer_question(self, question: str, provide_context: bool = True) -> Optional[Dict]:
        """Answer a question - EXACTLY like your notebook"""
        
        # Check if tourism-related - EXACTLY like your notebook
        is_tourism, category = self.non_tourism_handler.is_tourism_related(question)

        if not is_tourism:
            return {
                "answer": self.non_tourism_handler.get_fallback_response(question),
                "category": "non_tourism"
            }

        try:
            if provide_context and self.knowledge_base:
                # Retrieve relevant contexts - EXACTLY like your notebook
                contexts = self.retrieval_system.retrieve_contexts(question, top_k=3)
                combined_context = " ".join(contexts)
            else:
                # Generic context - EXACTLY like your notebook
                combined_context = (
                    "Rwanda has four national parks: Volcanoes National Park for mountain gorillas, "
                    "Akagera National Park for safari wildlife, Nyungwe National Park for chimpanzees, "
                    "and Gishwati-Mukura National Park. Rwanda also has cultural heritage sites like "
                    "museums, traditional dance performances, and historical monuments."
                )

            # Get answer - EXACTLY like your notebook
            result = self.qa_pipeline(
                question=question,
                context=combined_context,
                max_answer_len=200,
                handle_impossible_answer=False
            )

            return {
                "answer": result['answer'].strip(),
                "category": category
            }

        except Exception as e:
            return {
                "answer": f"I apologize, but I encountered an error processing your question about Rwanda tourism: {str(e)}",
                "error": str(e)
            }