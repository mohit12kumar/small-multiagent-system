import os
import random
from typing import Dict, Any, List
from backend.services.groq_service import query_groq_json

class QuestionGeneratorAgent:
    """
    Agent 4: Question Generator Agent
    Responsibilities:
    - Synthesize candidate-tailored technical & scenario questions
    - Ensure fresh, unique, non-repeating questions for every interview session
    """
    def __init__(self):
        prompt_path = os.path.join("backend", "prompts", "question_prompt.txt")
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                self.system_prompt = f.read()
        else:
            self.system_prompt = "You are a Senior Technical Interviewer AI. Synthesize unique, technical conceptual and scenario-based interview questions. Return valid JSON."

    def generate_questions(self, role_title: str, matched_skills: List[str], missing_skills: List[str], seed: str = "", previous_questions: List[str] = None) -> List[Dict[str, Any]]:
        matched_str = ', '.join(matched_skills[:6]) if matched_skills else 'General Software Development, Problem Solving'
        missing_str = ', '.join(missing_skills[:4]) if missing_skills else 'System Design, Optimization, Cloud Security'
        
        prev_q_str = ""
        if previous_questions:
            # Select recent 15 previous questions to keep prompt concise yet prevent repeats
            recent_prev = [q.strip() for q in previous_questions[-15:] if q.strip()]
            if recent_prev:
                prev_q_str = "\nCRITICAL: DO NOT repeat or ask close variations of any of these previously asked questions:\n" + "\n".join([f"- {q}" for q in recent_prev]) + "\n"
        
        prompt = f"""
ROLE: {role_title}
MATCHED SKILLS ON RESUME: {matched_str}
TARGET SKILLS TO EVALUATE: {missing_str}
SESSION ID / VARIATION SEED: {seed}
{prev_q_str}
Instructions:
Generate 3 COMPLETELY FRESH, UNIQUE, and CHALLENGING interview questions tailored to the above candidate profile.
Make sure questions are NOT generic and DO NOT duplicate any previously asked questions. Ask about real-world scenarios, architectural trade-offs, or deep internal mechanics of their skills.

Return ONLY JSON format matching this schema:
{{
  "questions": [
    {{
      "question_text": "Detailed question 1...",
      "difficulty": "medium",
      "type": "technical"
    }},
    {{
      "question_text": "Detailed question 2...",
      "difficulty": "hard",
      "type": "scenario"
    }},
    {{
      "question_text": "Detailed question 3...",
      "difficulty": "medium",
      "type": "technical"
    }}
  ]
}}
"""
        result = query_groq_json(self.system_prompt, prompt)
        raw_questions = result.get("questions", [])
        
        # Deduplicate generated questions against previous_questions
        prev_set = set(q.lower().strip() for q in (previous_questions or []))
        questions = []
        for q in raw_questions:
            q_text = q.get("question_text", "").strip()
            if q_text and q_text.lower() not in prev_set:
                questions.append(q)
                prev_set.add(q_text.lower())
        
        if len(questions) < 3:
            all_skills = (matched_skills or ['Software Engineering']) + (missing_skills or ['Distributed Systems'])
            primary_skill = all_skills[0] if all_skills else 'Software Engineering'
            secondary_skill = all_skills[1] if len(all_skills) > 1 else 'System Architecture'
            
            fallback_templates = [
                f"How do you approach designing high-availability systems using {primary_skill} for {role_title} roles?",
                f"Explain the internal mechanics of memory management and concurrency when working with {secondary_skill}.",
                f"Describe a real-world debugging scenario where a service built with {primary_skill} experienced high latency or memory leaks.",
                f"Compare the architectural trade-offs of monolithic vs microservices patterns for a platform using {secondary_skill}.",
                f"How do you implement robust caching, data indexing, and rate-limiting using {primary_skill}?",
                f"What security practices and authentication patterns do you enforce when developing enterprise solutions with {secondary_skill}?",
                f"How do you write automated test suites and benchmark performance for applications built on {primary_skill}?",
                f"Explain how transaction isolation levels and distributed locks function in systems leveraging {secondary_skill}."
            ]
            
            for tpl in fallback_templates:
                if tpl.lower() not in prev_set:
                    questions.append({
                        "question_text": tpl,
                        "difficulty": "medium",
                        "type": "technical"
                    })
                    prev_set.add(tpl.lower())
                if len(questions) >= 3:
                    break
                    
        # Guaranteed unique dynamic fallback generator if still under 3
        count = 1
        while len(questions) < 3:
            dyn_q = f"For the role of {role_title}, how would you architect and optimize a mission-critical subsystem evaluating {matched_str[:30]} (Scenario #{count})?"
            if dyn_q.lower() not in prev_set:
                questions.append({
                    "question_text": dyn_q,
                    "difficulty": "hard",
                    "type": "scenario"
                })
                prev_set.add(dyn_q.lower())
            count += 1

        return questions[:3]

question_generator_agent = QuestionGeneratorAgent()
