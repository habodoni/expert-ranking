import sqlite3
import streamlit as st
from src.utils.data_loader import DataLoader
from src.embeddings.embedding_engine import EmbeddingEngine
from src.ranking.ranking_module import RankingModule
from src.utils.explainability import ExplanationEngine

# Ensure database exists
db_path = 'src/data/experts.db'  # Use the pre-built database
conn = sqlite3.connect(db_path)
conn.close()

# Initialize components
loader = DataLoader(db_path)
experts = loader.load_experts()
embedding_engine = EmbeddingEngine()
ranking_module = RankingModule(embedding_engine)
explanation_engine = ExplanationEngine()


# Streamlit UI
st.title("Dynamic Expert Ranking System")
st.write("Provide a description of what you're looking for, and we'll rank the most relevant experts!")

# User input for candidate description
candidate_description = st.text_area(
    "Describe what you're looking for:",
    placeholder="E.g., 'Looking for a FinTech expert with over 5 years of experience specializing in compliance and fraud detection.'"
)

# Optional filters
st.write("Optional Filters:")
industry = st.selectbox("Select Industry:", options=["Any", "FinTech", "SaaS", "Other"])
min_experience = st.slider("Minimum Years of Experience:", 0, 20, 5)
required_skills = st.text_input("Required Skills (comma-separated):", placeholder="E.g., compliance, fraud detection")
availability = st.checkbox("Only show available experts", value=True)

if st.button("Find Experts"):
    if candidate_description.strip():
        # Extract keywords dynamically
        extracted_keywords = explanation_engine.extract_keywords(candidate_description, max_features=10)
        st.write(f"**Extracted Keywords:** {', '.join(extracted_keywords)}")

        # Query database with filters
        filters = {
            "industry": industry,
            "min_experience": min_experience,
            "required_skills": required_skills,
            "availability": availability
        }
        filtered_experts = loader.load_experts(filters=filters)

        if not filtered_experts:
            st.warning("No experts match your criteria. Try adjusting the filters.")
        else:
            # Rank filtered experts and limit to top 10
            ranked_experts = ranking_module.rank_experts(
                candidate_desc=candidate_description,
                experts=filtered_experts,
                extracted_keywords=extracted_keywords,
                min_experience=min_experience,
                limit=10  # Limit results to the top 10 experts
            )

            # Display results
            st.write("### Ranked Experts:")
            for i, entry in enumerate(ranked_experts, start=1):
                explanation = explanation_engine.generate_explanation(entry, candidate_description, rank=i)
                st.write(f"#### Rank {i}: {entry['expert']['name']}")
                st.text(explanation)
    else:
        st.error("Please enter a valid description.")



