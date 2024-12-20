from sentence_transformers import util

class RankingModule:
    def __init__(self, embedding_engine):
        self.embedding_engine = embedding_engine

    def compute_score(self, candidate_desc, expert, extracted_keywords=None, min_experience=0):
        # Embed candidate description and expert profile
        candidate_embedding = self.embedding_engine.embed(candidate_desc)
        expert_text = (
            f"{expert['title']} in {expert['industry']} with {expert['years_experience']} years. "
            f"Skills: {', '.join(expert['skills'])}."
        )
        expert_embedding = self.embedding_engine.embed(expert_text)

        # Calculate similarity
        similarity = float(util.cos_sim(candidate_embedding, expert_embedding)[0][0])

        # Match skills dynamically based on extracted keywords
        matched_skills = set()  # Use a set to ensure uniqueness
        if extracted_keywords:
            for keyword in extracted_keywords:
                for skill in expert['skills']:
                    # Match keyword to skill (case-insensitive)
                    if keyword.lower() in skill.lower():
                        matched_skills.add(skill)  # Add skill to set

        # Convert set back to a list for further processing
        matched_skills = list(matched_skills)

        # Calculate skill match score
        skill_score = len(matched_skills) / len(extracted_keywords) if extracted_keywords else 0

        # Calculate experience score based on minimum required experience
        if min_experience > 0:
            experience_score = min(1.0, expert["years_experience"] / min_experience)  # Cap at 100%
        else:
            experience_score = min(1.0, expert["years_experience"] / 10.0)  # Default cap at 10 years

        # Final composite score
        final_score = (0.7 * similarity) + (0.2 * skill_score) + (0.1 * experience_score)
        return final_score, similarity, skill_score, experience_score, matched_skills

    def rank_experts(self, candidate_desc, experts, extracted_keywords=None, min_experience=0, limit=10):
        """
        Rank experts based on relevance to the candidate description.
        Args:
            candidate_desc (str): The input description.
            experts (list): List of expert profiles.
            extracted_keywords (list): Dynamically extracted keywords from the description.
            min_experience (int): Minimum years of experience required.
            limit (int): Maximum number of experts to return.
        Returns:
            list: Top `limit` ranked experts with their scores.
        """
        scored = []
        for expert in experts:
            # Compute score for each expert
            final_score, similarity, skill_score, experience_score, matched_skills = self.compute_score(
                candidate_desc, expert, extracted_keywords, min_experience
            )
            scored.append({
                "expert": expert,
                "final_score": final_score,
                "similarity": similarity,
                "skill_score": skill_score,
                "experience_score": experience_score,
                "matched_skills": matched_skills
            })

        # Sort by final score in descending order
        scored = sorted(scored, key=lambda x: x['final_score'], reverse=True)

        # Return only the top `limit` experts
        return scored[:limit]
