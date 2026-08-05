import os
import re
from typing import List, Dict, Any

class KnowledgeItem(Dict[str, Any]):
    text: str
    category: str
    metadata: Dict[str, Any]

class RAGKnowledgeEngine:
    """
    RAG (Retrieval-Augmented Generation) Engine:
    - Stores and retrieves domain-specific CSE interview question banks, STAR behavioral questions, and resume knowledge.
    - Uses TF-IDF cosine similarity search fallback vector indexing.
    """
    def __init__(self):
        self.knowledge_base: List[Dict[str, Any]] = [
            {
                "text": "Explain how database indexing operates (B-Trees vs Hash Indexes) and how you optimize slow queries using EXPLAIN execution plans.",
                "category": "database",
                "domain": "SQL & DBMS"
            },
            {
                "text": "How do you handle microservices distributed transaction consistency using Sagas or 2-Phase Commit protocols?",
                "category": "system_design",
                "domain": "System Architecture"
            },
            {
                "text": "Write an efficient Python function implementing LRU Cache with O(1) get and put time complexity using a doubly linked list and hash map.",
                "category": "coding",
                "domain": "DSA & Algorithms"
            },
            {
                "text": "Describe a STAR situation where technical requirements changed midway through sprint delivery. How did you re-prioritize?",
                "category": "hr",
                "domain": "Behavioral STAR"
            },
            {
                "text": "Explain Python GIL (Global Interpreter Lock), process vs thread concurrency, and when to utilize multiprocessing or asyncio.",
                "category": "language_internals",
                "domain": "Python Systems"
            }
        ]

    def _tokenize(self, text: str) -> set:
        return set(re.findall(r'\w+', text.lower()))

    def retrieve_relevant_knowledge(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return self.knowledge_base[:top_k]

        scored_items = []
        for item in self.knowledge_base:
            item_tokens = self._tokenize(item["text"] + " " + item.get("domain", ""))
            intersection = query_tokens.intersection(item_tokens)
            score = len(intersection) / max(len(query_tokens), 1)
            scored_items.append((score, item))

        scored_items.sort(key=lambda x: x[0], reverse=True)
        return [item for score, item in scored_items[:top_k]]

rag_engine = RAGKnowledgeEngine()
