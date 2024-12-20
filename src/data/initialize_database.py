import sqlite3
import os

def initialize_database():
    # Use the current working directory to locate the database
    db_path = os.path.join(os.getcwd(), 'experts.db')

    print(f"Database Path: {db_path}")  # Debugging: Ensure this path is correct in deployment
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS experts (
        id INTEGER PRIMARY KEY,
        name TEXT,
        title TEXT,
        industry TEXT,
        years_experience INTEGER,
        skills TEXT,
        company_affiliation TEXT,
        certifications TEXT,
        languages TEXT,
        availability BOOLEAN
    );
    """)

    # Insert sample data if table is empty
    cursor.execute("SELECT COUNT(*) FROM experts;")
    if cursor.fetchone()[0] == 0:
        sample_data = [
            ('Jane Doe', 'Senior Compliance Consultant', 'FinTech', 10, 'fraud detection,CRM integration,compliance consulting', 'Acme Consulting', 'CAMS', 'English,Spanish', 1),
            ('John Smith', 'AI Solutions Architect', 'FinTech', 6, 'fraud detection,AI-driven analysis,compliance', 'ProNexus', 'AWS Certified', 'English', 1),
            ('Sarah Lee', 'CRM Specialist', 'SaaS', 4, 'CRM integration,Customer onboarding', 'GlobalTech', '', 'English,French', 0)
        ]
        cursor.executemany("""
        INSERT INTO experts (name, title, industry, years_experience, skills, company_affiliation, certifications, languages, availability)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_data)

    conn.commit()
    conn.close()
