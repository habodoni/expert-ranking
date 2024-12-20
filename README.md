# Expert Ranking System

An interactive tool to rank experts based on user-provided criteria, leveraging NLP embeddings, SQLite databases, and a Streamlit-based interface.

## Prerequisites

Before running the project, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package manager)

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/habodoni/expert-ranking.git
   cd expert-ranking
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the Database**:
   ```bash
   python src/data/initialize_database.py
   ```

4. **Run the Streamlit App**:
   ```bash
   streamlit run app.py
   ```

5. **Access the App**:
   Open the URL provided in the terminal (e.g., `http://localhost:8501`) to interact with the app.

## Troubleshooting

- **Missing Database**: If `experts.db` is missing, ensure step 3 is completed successfully.
- **Dependency Issues**: Ensure you're using the correct Python version (`python --version`).

## Sample Input and Output

### Example Input:
```
Looking for a FinTech expert with experience in compliance and fraud detection, CRM (5 years of experience).
```

### Example Output:
```yaml
Extracted Keywords: compliance, crm, detection, fintech, fraud

Ranked Experts:

Rank 1: Jane Doe
Name: Jane Doe
Score Breakdown:
- Similarity to Candidate Description: 78%
- Skills Match: 60% of key requested skills
- Relevant Experience: 100% of the minimum required
Summary: Jane Doe was ranked 1st due to their strong similarity of 78% with the candidate description, a skills match of 60%, experience meeting 100% of the target years.
Matched Skills: compliance consulting, CRM integration, fraud detection

Rank 2: John Smith
Name: John Smith
Score Breakdown:
- Similarity to Candidate Description: 66%
- Skills Match: 40% of key requested skills
- Relevant Experience: 100% of the minimum required
Summary: John Smith was ranked 2nd, showing a skills match of 40%, experience meeting 100% of the target years.
Matched Skills: compliance, fraud detection
```

## Additional Notes

For questions or issues, please contact Hazem Abo-Donia or create an issue in the repository.
