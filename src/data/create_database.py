import sqlite3

# Connect to the database (this will create experts.db)
conn = sqlite3.connect('experts.db')
cursor = conn.cursor()

# Create the experts table
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

# Insert sample data if the table is empty
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

print("Database created and populated as experts.db")
