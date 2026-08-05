from typing import Dict, Any, List

class SkillMatchingAgent:
    """
    Agent 3: Skill Matching Agent
    Responsibilities:
    - Compare Resume Skills & JD Required Skills
    - Compute weighted Skill Match %
    - Identify missing skills & generate learning recommendations
    """
    def compare_skills(self, resume_skills: List[str], jd_skills: List[str]) -> Dict[str, Any]:
        if not jd_skills:
            return {
                "match_percentage": 100.0,
                "matched_skills": resume_skills,
                "missing_skills": [],
                "recommendations": ["Great profile alignment!"]
            }
        
        # Normalize skill strings
        res_set = {s.strip().lower() for s in resume_skills if s}
        jd_set = {s.strip().lower() for s in jd_skills if s}
        
        matched_set = res_set.intersection(jd_set)
        missing_set = jd_set - res_set
        
        match_percentage = round((len(matched_set) / len(jd_set)) * 100.0, 1) if jd_set else 100.0
        
        # Original casing map for display
        casing_map = {s.strip().lower(): s for s in jd_skills}
        matched_list = [casing_map.get(m, m.capitalize()) for m in matched_set]
        missing_list = [casing_map.get(m, m.capitalize()) for m in missing_set]
        
        recommendations = [f"Gain practical project exposure in {skill}" for skill in missing_list[:5]]
        if not recommendations:
            recommendations = ["Continue honing core competencies and architecture principles."]
            
        return {
            "match_percentage": match_percentage,
            "matched_skills": matched_list,
            "missing_skills": missing_list,
            "recommendations": recommendations
        }

skill_matching_agent = SkillMatchingAgent()
