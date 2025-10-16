"""
Context Retrieval System for Rwanda Tourism QA
Combines BM25 and semantic search for optimal context retrieval
"""

import numpy as np
import torch
from typing import List, Tuple
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer, util
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import streamlit as st

# Download NLTK data if not present
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')
    
try:
    word_tokenize("test")
except LookupError:
    nltk.download('punkt')


class ContextRetrievalSystem:
    """Hybrid BM25 + Semantic search for context retrieval"""

    def __init__(self, retrieval_method: str = "hybrid"):
        self.retrieval_method = retrieval_method
        self.bm25 = None
        self.sentence_model = None
        self.context_embeddings = None
        self.contexts = []
        self.stop_words = set(stopwords.words('english'))

    @st.cache_resource
    def build_retrieval_index(_self, contexts: List[str]):
        """Build retrieval index with caching"""
        _self.contexts = contexts

        if _self.retrieval_method in ["bm25", "hybrid"]:
            tokenized = [_self._tokenize_text(ctx) for ctx in contexts]
            _self.bm25 = BM25Okapi(tokenized)

        if _self.retrieval_method in ["semantic", "hybrid"]:
            _self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            _self.context_embeddings = _self.sentence_model.encode(
                contexts, convert_to_tensor=True, show_progress_bar=False
            )

    def _tokenize_text(self, text: str) -> List[str]:
        """Tokenize and clean text"""
        text = text.lower()
        tokens = word_tokenize(text)
        tokens = [t for t in tokens if t not in self.stop_words and len(t) > 2]
        return tokens

    def retrieve_contexts(self, query: str, top_k: int = 3) -> List[str]:
        """Retrieve top-k contexts"""
        if self.retrieval_method == "bm25":
            return self._bm25_retrieval(query, top_k)
        elif self.retrieval_method == "semantic":
            return self._semantic_retrieval(query, top_k)
        else:
            return self._hybrid_retrieval(query, top_k)

    def _bm25_retrieval(self, query: str, top_k: int) -> List[str]:
        """BM25 retrieval"""
        tokenized_query = self._tokenize_text(query)
        scores = self.bm25.get_scores(tokenized_query)
        top_indices = np.argsort(scores)[::-1][:top_k]
        return [self.contexts[i] for i in top_indices if scores[i] > 0]

    def _semantic_retrieval(self, query: str, top_k: int) -> List[str]:
        """Semantic retrieval"""
        query_embedding = self.sentence_model.encode(query, convert_to_tensor=True)
        cos_scores = util.cos_sim(query_embedding, self.context_embeddings)[0]
        top_results = torch.topk(cos_scores, k=min(top_k, len(self.contexts)))
        return [self.contexts[idx] for idx in top_results.indices]

    def _hybrid_retrieval(self, query: str, top_k: int) -> List[str]:
        """Hybrid retrieval combining BM25 and semantic search"""
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