import os
from typing import Dict, Any
from backend.services.groq_service import query_groq_json

class FeedbackAgent:
    """
    Agent 7: Feedback Agent
    Responsibilities:
    - Evaluate candidate answer on 5 dimensions:
      1. Technical Accuracy
      2. Grammar & Syntax
      3. Communication Clarity
      4. Confidence Score
      5. Completeness Score
    - Calculate aggregate overall score
    """
    def __init__(self):
        prompt_path = os.path.join("backend", "prompts", "feedback_prompt.txt")
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                self.system_prompt = f.read()
        else:
            self.system_prompt = "You are a Feedback Agent. Evaluate candidate answer across 5 metrics (grammar_score, technical_score, communication_score, confidence_score, completeness_score, overall_score, comments)."

    def evaluate_answer(self, question_text: str, user_answer: str) -> Dict[str, Any]:
        prompt = f"""
QUESTION: {question_text}
CANDIDATE ANSWER: {user_answer}

Evaluate the answer. Return JSON:
{{
  "grammar_score": 90.0,
  "technical_score": 85.0,
  "communication_score": 88.0,
  "confidence_score": 80.0,
  "completeness_score": 82.0,
  "overall_score": 85.0,
  "comments": "Feedback comments..."
}}
"""
        result = query_groq_json(self.system_prompt, prompt)
        
        # Ensure default score bounds
        grammar = float(result.get("grammar_score", 85.0))
        technical = float(result.get("technical_score", 80.0))
        comm = float(result.get("communication_score", 85.0))
        confidence = float(result.get("confidence_score", 80.0))
        completeness = float(result.get("completeness_score", 80.0))
        overall = float(result.get("overall_score", (grammar + technical + comm + confidence + completeness) / 5.0))
        
        return {
            "grammar_score": round(grammar, 1),
            "technical_score": round(technical, 1),
            "communication_score": round(comm, 1),
            "confidence_score": round(confidence, 1),
            "completeness_score": round(completeness, 1),
            "overall_score": round(overall, 1),
            "comments": result.get("comments", "Well structured response. Keep focusing on technical depth.")
        }

feedback_agent = FeedbackAgent()
