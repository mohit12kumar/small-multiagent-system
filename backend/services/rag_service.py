import os
import re
from typing import List, Dict, Any
from backend.schemas.agent_schemas import CompanyMode

class RAGKnowledgeEngine:
    """
    RAG (Retrieval-Augmented Generation) Engine with Company-Specific Interview Modes:
    - Amazon: 16 Leadership Principles (Customer Obsession, Ownership, Bias for Action, Dive Deep).
    - Google: Distributed Systems, Scalability, Algorithmic Complexity, Googlyness.
    - Microsoft: System Resilience, Cloud Microservices, Growth Mindset.
    - Meta: High-Concurrency Coding, System Design at Billion-User Scale.
    """
    def __init__(self):
        self.company_knowledge_banks: Dict[str, List[Dict[str, Any]]] = {
            CompanyMode.AMAZON.value: [
                {
                    "text": "Describe a STAR scenario demonstrating Customer Obsession where you made a technical tradeoff to protect customer experience.",
                    "principle": "Customer Obsession",
                    "type": "behavioral"
                },
                {
                    "text": "How have you demonstrated Ownership when inheriting a legacy service with zero test coverage?",
                    "principle": "Ownership",
                    "type": "behavioral"
                },
                {
                    "text": "Explain a situation demonstrating Bias for Action where you had 70% data and had to make an immediate architectural decision.",
                    "principle": "Bias for Action",
                    "type": "behavioral"
                }
            ],
            CompanyMode.GOOGLE.value: [
                {
                    "text": "Design a globally distributed Rate Limiter operating across multi-region Google Cloud nodes with sub-10ms latency.",
                    "domain": "System Design",
                    "type": "technical"
                },
                {
                    "text": "Optimize a Graph Search algorithm for finding shortest paths in a massive social network graph with 1B+ nodes.",
                    "domain": "Graph Algorithms",
                    "type": "coding"
                }
            ],
            CompanyMode.MICROSOFT.value: [
                {
                    "text": "How do you ensure zero-downtime deployments for Azure microservices using Canary rollouts and blue-green environments?",
                    "domain": "Cloud Systems",
                    "type": "system_design"
                }
            ],
            CompanyMode.META.value: [
                {
                    "text": "Design a Real-Time Live Stream Comments Engine handling 100K comments/sec with low-latency pub/sub queues.",
                    "domain": "High-Throughput Systems",
                    "type": "system_design"
                }
            ]
        }

        self.general_knowledge_base: List[Dict[str, Any]] = [
            {
                "text": "Explain how database indexing operates (B-Trees vs Hash Indexes) and how you optimize slow queries using EXPLAIN execution plans.",
                "domain": "SQL & DBMS"
            },
            {
                "text": "How do you handle microservices distributed transaction consistency using Sagas or 2-Phase Commit protocols?",
                "domain": "System Architecture"
            },
            {
                "text": "Write an efficient Python function implementing LRU Cache with O(1) get and put time complexity using a doubly linked list and hash map.",
                "domain": "DSA & Algorithms"
            }
        ]

    def _tokenize(self, text: str) -> set:
        return set(re.findall(r'\w+', text.lower()))

    def retrieve_relevant_knowledge(self, query: str, company: str = "general", top_k: int = 3) -> List[Dict[str, Any]]:
        bank = self.company_knowledge_banks.get(company.lower(), self.general_knowledge_base)
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return bank[:top_k]

        scored_items = []
        for item in bank:
            item_tokens = self._tokenize(item["text"] + " " + item.get("domain", "") + " " + item.get("principle", ""))
            intersection = query_tokens.intersection(item_tokens)
            score = len(intersection) / max(len(query_tokens), 1)
            scored_items.append((score, item))

        scored_items.sort(key=lambda x: x[0], reverse=True)
        return [item for score, item in scored_items[:top_k]]

rag_engine = RAGKnowledgeEngine()
