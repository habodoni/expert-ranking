import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

class ExplanationEngine:
    def extract_keywords(self, description, max_features=10):
        """
        Extract key terms from the candidate description using TF-IDF.
        Args:
            description (str): The candidate's job description.
            max_features (int): The maximum number of keywords to extract.
        Returns:
            list: A list of the most relevant keywords.
        """
        # Define custom stopwords
        domain_stopwords = {"expert", "looking", "need", "experience", "with"}
        custom_stopwords = list(ENGLISH_STOP_WORDS.union(domain_stopwords))  # Convert to list

        # TF-IDF vectorization
        vectorizer = TfidfVectorizer(stop_words=custom_stopwords, max_features=max_features)
        tfidf_matrix = vectorizer.fit_transform([description])

        # Extract keywords based on feature importance
        keywords = vectorizer.get_feature_names_out()
        return list(keywords)


    def generate_explanation(self, entry, candidate_desc, rank):
        expert = entry['expert']
        similarity_percentage = entry['similarity'] * 100
        skills_match_percentage = entry['skill_score'] * 100
        experience_percentage = entry['experience_score'] * 100

        # Construct dynamic summary
        emphasis = []
        if similarity_percentage >= 70:
            emphasis.append(f"strong similarity of {similarity_percentage:.0f}% with the candidate description")
        if skills_match_percentage > 0:
            emphasis.append(f"a skills match of {skills_match_percentage:.0f}%")
        if experience_percentage > 0:
            emphasis.append(f"experience meeting {experience_percentage:.0f}% of the target years")

        if emphasis:
            if rank == 1:
                summary = f"{expert['name']} was ranked 1st due to their " + ", ".join(emphasis) + "."
            elif rank == 2:
                summary = f"{expert['name']} was ranked 2nd, showing " + ", ".join(emphasis) + "."
            elif rank == 3:
                summary = f"{expert['name']} was ranked 3rd because of their " + ", ".join(emphasis) + "."
        else:
            summary = f"{expert['name']} was ranked lower due to insufficient match across key criteria."

        explanation = (
            f"Name: {expert['name']}\n"
            f"Score Breakdown:\n"
            f"  - Similarity to Candidate Description: {similarity_percentage:.0f}%\n"
            f"  - Skills Match: {skills_match_percentage:.0f}% of key requested skills\n"
            f"  - Relevant Experience: {experience_percentage:.0f}% of the minimum required\n"
            f"Summary: {summary}\n"
            f"Matched Skills: {', '.join(entry['matched_skills']) if entry['matched_skills'] else 'None'}\n"
        )
        return explanation

    def visualize_scores(self, entry):
        """
        Visualize the scoring breakdown for a given expert.
        """
        scores = {
            'Similarity': entry['similarity'] * 100,
            'Skill Match': entry['skill_score'] * 100,
            'Experience': entry['experience_score'] * 100
        }
        plt.bar(scores.keys(), scores.values())
        plt.title(f"Score Breakdown for {entry['expert']['name']}")
        plt.ylabel("Percentage (%)")
        plt.show()
