import os
import random
from typing import Dict, Any, List
from backend.services.groq_service import query_groq_json

class CodingInterviewAgent:
    """
    Agent 5: Coding Interview Agent
    Responsibilities:
    - Generate DSA, SQL, Python, React, and FastAPI coding problems
    - Deliver starter code snippets & input/output constraints
    """
    def __init__(self):
        prompt_path = os.path.join("backend", "prompts", "coding_prompt.txt")
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                self.system_prompt = f.read()
        else:
            self.system_prompt = "You are a Coding Interviewer AI. Generate algorithmic, DSA, or system coding challenges. Return JSON."

    def generate_coding_question(self, domain: str = "Python & DSA", seed: str = "", previous_questions: List[str] = None) -> Dict[str, Any]:
        prev_q_str = ""
        if previous_questions:
            recent_prev = [q.strip() for q in previous_questions[-15:] if q.strip()]
            if recent_prev:
                prev_q_str = "\nCRITICAL: DO NOT repeat or generate variations of any of these previously asked coding questions:\n" + "\n".join([f"- {q}" for q in recent_prev]) + "\n"

        prompt = f"""
DOMAIN: {domain}
SESSION VARIATION SEED: {seed}
{prev_q_str}
Generate 1 algorithmic, DSA, or system coding challenge in {domain}.
Ensure the problem is UNIQUE, challenging, and tests core problem-solving capabilities.

Return ONLY JSON:
{{
  "questions": [
    {{
      "question_text": "Detailed coding problem statement here...",
      "difficulty": "medium",
      "type": "coding",
      "starter_code": "# starter code here",
      "constraints": "Time: O(N), Space: O(N)"
    }}
  ]
}}
"""
        result = query_groq_json(self.system_prompt, prompt)
        questions = result.get("questions", [])
        
        prev_set = set(q.lower().strip() for q in (previous_questions or []))
        
        if questions:
            q = questions[0]
            if q.get("question_text", "").strip().lower() not in prev_set:
                return q

        # Varied coding fallback pool
        coding_pool = [
            {
                "question_text": "Write a function `two_sum(nums: List[int], target: int) -> List[int]` that returns the indices of the two numbers that add up to target in O(N) time.",
                "difficulty": "medium",
                "type": "coding",
                "starter_code": "def two_sum(nums: list[int], target: int) -> list[int]:\n    # Implement hash table approach\n    pass",
                "constraints": "O(N) Time Complexity, O(N) Space Complexity"
            },
            {
                "question_text": "Implement a LRU (Least Recently Used) Cache class with `get(key)` and `put(key, value)` methods operating in O(1) time.",
                "difficulty": "hard",
                "type": "coding",
                "starter_code": "class LRUCache:\n    def __init__(self, capacity: int):\n        pass\n    def get(self, key: int) -> int:\n        pass\n    def put(self, key: int, value: int) -> None:\n        pass",
                "constraints": "O(1) Time complexity for get and put"
            },
            {
                "question_text": "Write a Python function `group_anagrams(words: List[str]) -> List[List[str]]` that groups words that are anagrams of each other.",
                "difficulty": "medium",
                "type": "coding",
                "starter_code": "def group_anagrams(words: list[str]) -> list[list[str]]:\n    # Write solution\n    pass",
                "constraints": "O(N * K log K) where N is number of words and K is max length of a word"
            },
            {
                "question_text": "Write a function `max_subarray_sum(nums: List[int]) -> int` that finds the contiguous subarray with the largest sum (Kadane's Algorithm).",
                "difficulty": "medium",
                "type": "coding",
                "starter_code": "def max_subarray_sum(nums: list[int]) -> int:\n    # Write Kadane's Algorithm\n    pass",
                "constraints": "O(N) Time Complexity, O(1) Space Complexity"
            },
            {
                "question_text": "Write a function `isValidBST(root: Optional[TreeNode]) -> bool` to validate whether a given Binary Tree is a valid Binary Search Tree.",
                "difficulty": "medium",
                "type": "coding",
                "starter_code": "def isValidBST(root) -> bool:\n    # Validate BST constraints\n    pass",
                "constraints": "O(N) Time Complexity, O(H) Space Complexity"
            },
            {
                "question_text": "Implement a function `merge_k_sorted_lists(lists: List[ListNode]) -> ListNode` using a min-heap.",
                "difficulty": "hard",
                "type": "coding",
                "starter_code": "def merge_k_sorted_lists(lists):\n    # Min heap implementation\n    pass",
                "constraints": "O(N log K) Time Complexity, O(K) Space Complexity"
            },
            {
                "question_text": "Write a function `find_median_from_data_stream()` that supports adding numbers and finding the current median in O(log N) time.",
                "difficulty": "hard",
                "type": "coding",
                "starter_code": "class MedianFinder:\n    def __init__(self):\n        pass\n    def addNum(self, num: int) -> None:\n        pass\n    def findMedian(self) -> float:\n        pass",
                "constraints": "O(log N) addNum, O(1) findMedian"
            },
            {
                "question_text": "Write a function `longest_substring_without_repeating_characters(s: str) -> int` using sliding window.",
                "difficulty": "medium",
                "type": "coding",
                "starter_code": "def length_of_longest_substring(s: str) -> int:\n    # Sliding window\n    pass",
                "constraints": "O(N) Time Complexity, O(K) Space Complexity"
            }
        ]
        random.shuffle(coding_pool)
        for item in coding_pool:
            if item["question_text"].strip().lower() not in prev_set:
                return item

        # Dynamic fallback coding challenge for domain
        count = 1
        while True:
            dyn_text = f"Write an efficient implementation in {domain} to process stream data or optimize algorithmic complexity (Problem Variant #{count})."
            if dyn_text.lower() not in prev_set:
                return {
                    "question_text": dyn_text,
                    "difficulty": "medium",
                    "type": "coding",
                    "starter_code": f"# Implementation for {domain}\ndef solve():\n    pass",
                    "constraints": "O(N) Time Complexity, O(N) Space Complexity"
                }
            count += 1

coding_agent = CodingInterviewAgent()
