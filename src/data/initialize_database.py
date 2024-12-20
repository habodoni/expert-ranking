import sqlite3

def initialize_database():
    # Connect to the database (creates file if it doesn't exist)
    conn = sqlite3.connect('../experts.db')
    cursor = conn.cursor()

    # Create table
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

    # Sample data to insert
    data = [
        ('Jane Doe', 'Senior Compliance Consultant', 'FinTech', 10, 'fraud detection,CRM integration,compliance consulting', 'Acme Consulting', 'CAMS', 'English,Spanish', 1),
        ('John Smith', 'AI Solutions Architect', 'FinTech', 6, 'fraud detection,AI-driven analysis,compliance', 'ProNexus', 'AWS Certified', 'English', 1),
        ('Sarah Lee', 'CRM Specialist', 'SaaS', 4, 'CRM integration,Customer onboarding', 'GlobalTech', '', 'English,French', 0)
    ]

    # Insert sample data if table is empty
    cursor.execute("SELECT COUNT(*) FROM experts;")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
        INSERT INTO experts (name, title, industry, years_experience, skills, company_affiliation, certifications, languages, availability)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data)

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
