import os
import random
from typing import Dict, Any, List
from backend.services.groq_service import query_groq_json

class HRInterviewAgent:
    """
    Agent 6: HR Interview Agent
    Responsibilities:
    - Generate behavioral STAR questions
    - Evaluate leadership, teamwork, communication, and situational handling
    """
    def __init__(self):
        prompt_path = os.path.join("backend", "prompts", "hr_prompt.txt")
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                self.system_prompt = f.read()
        else:
            self.system_prompt = "You are an HR Director & Behavioral Interviewer AI. Generate STAR behavioral questions. Return JSON."

    def generate_hr_questions(self, seed: str = "", previous_questions: List[str] = None) -> List[Dict[str, Any]]:
        prev_q_str = ""
        if previous_questions:
            recent_prev = [q.strip() for q in previous_questions[-15:] if q.strip()]
            if recent_prev:
                prev_q_str = "\nCRITICAL: DO NOT repeat or ask variations of any of these previously asked behavioral questions:\n" + "\n".join([f"- {q}" for q in recent_prev]) + "\n"

        prompt = f"""
SESSION VARIATION SEED: {seed}
{prev_q_str}
Generate 2 COMPLETELY UNIQUE behavioral STAR (Situation, Task, Action, Result) interview questions.
Focus on conflict resolution, leadership under pressure, cross-functional collaboration, or managing technical debt.

Return ONLY JSON:
{{
  "questions": [
    {{
      "question_text": "Describe a situation where...",
      "difficulty": "medium",
      "type": "hr"
    }},
    {{
      "question_text": "Tell me about a time when...",
      "difficulty": "medium",
      "type": "hr"
    }}
  ]
}}
"""
        result = query_groq_json(self.system_prompt, prompt)
        raw_questions = result.get("questions", [])
        
        prev_set = set(q.lower().strip() for q in (previous_questions or []))
        questions = []
        for q in raw_questions:
            q_text = q.get("question_text", "").strip()
            if q_text and q_text.lower() not in prev_set:
                questions.append(q)
                prev_set.add(q_text.lower())
                
        if len(questions) >= 2:
            return questions[:2]
            
        hr_pool = [
            {
                "question_text": "Tell me about a challenging project deadline where requirements changed midway. How did you re-prioritize your deliverables?",
                "difficulty": "medium",
                "type": "hr"
            },
            {
                "question_text": "Describe a situation where you had a technical disagreement with a senior teammate or architect. How did you resolve it?",
                "difficulty": "medium",
                "type": "hr"
            },
            {
                "question_text": "Give an example of a time when a system bug or outage occurred under your responsibility. What steps did you take to resolve and prevent recurrence?",
                "difficulty": "hard",
                "type": "hr"
            },
            {
                "question_text": "How do you handle managing technical debt versus delivering new features requested by stakeholders?",
                "difficulty": "medium",
                "type": "hr"
            },
            {
                "question_text": "Describe a scenario where you had to mentor a struggling team member or onboard someone to a complex codebase.",
                "difficulty": "medium",
                "type": "hr"
            },
            {
                "question_text": "Tell me about a time when you received constructive feedback on your code or architecture that you initially disagreed with. How did you respond?",
                "difficulty": "medium",
                "type": "hr"
            }
        ]
        random.shuffle(hr_pool)
        for fb in hr_pool:
            fb_text = fb["question_text"].strip()
            if fb_text.lower() not in prev_set:
                questions.append(fb)
                prev_set.add(fb_text.lower())
            if len(questions) >= 2:
                break

        # Dynamic fallback generator for HR questions
        count = 1
        while len(questions) < 2:
            dyn_hr = f"Describe a workplace scenario (STAR format) where you demonstrated leadership, accountability, and problem-solving under strict constraints (Scenario #{count})."
            if dyn_hr.lower() not in prev_set:
                questions.append({
                    "question_text": dyn_hr,
                    "difficulty": "medium",
                    "type": "hr"
                })
                prev_set.add(dyn_hr.lower())
            count += 1

        return questions[:2]

hr_agent = HRInterviewAgent()
