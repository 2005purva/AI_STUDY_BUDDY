import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RAGEngine:
    """Retrieval-Augmented Generation Engine using vector similarity over document chunks."""

    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        self.chunks = []
        self.tfidf_matrix = None
        self.is_indexed = False

    def index_chunks(self, chunks: list[dict]):
        """Indexes text chunks for vector search."""
        if not chunks:
            self.is_indexed = False
            return
        
        self.chunks = chunks
        raw_texts = [c["text"] for c in chunks]
        self.tfidf_matrix = self.vectorizer.fit_transform(raw_texts)
        self.is_indexed = True

    def retrieve(self, query: str, top_k: int = 3) -> list[dict]:
        """Retrieves top_k most relevant chunks for a user query."""
        if not self.is_indexed or self.tfidf_matrix is None:
            return []

        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            if score > 0.01:
                results.append({
                    "chunk_id": self.chunks[idx]["id"],
                    "text": self.chunks[idx]["text"],
                    "score": round(score, 3)
                })
        
        return results

    def answer_question(self, query: str) -> dict:
        """Answers user question grounded in retrieved context."""
        retrieved_chunks = self.retrieve(query, top_k=3)
        
        if not retrieved_chunks:
            return {
                "answer": "I couldn't find relevant information in the uploaded study material to answer this question. Try rephrasing or checking if the document covers this topic.",
                "sources": []
            }
        
        answer_summary = f"Based on your study notes:\n\n{retrieved_chunks[0]['text']}"
        if len(retrieved_chunks) > 1:
            answer_summary += f"\n\nAdditionally:\n{retrieved_chunks[1]['text']}"

        return {
            "answer": answer_summary,
            "sources": retrieved_chunks
        }
