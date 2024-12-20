import sqlite3

# Connect to the database (creates the file if it doesn't exist)
db_path = 'experts.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Debug: Check connection
print(f"Connected to database: {db_path}")

# Create the `experts` table
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
print("Table `experts` created or already exists.")

# Insert sample data
cursor.execute("SELECT COUNT(*) FROM experts;")
if cursor.fetchone()[0] == 0:
    print("Inserting sample data into `experts` table...")
    sample_data = [
        ('Jane Doe', 'Senior Compliance Consultant', 'FinTech', 10, 'fraud detection,CRM integration,compliance consulting', 'Acme Consulting', 'CAMS', 'English,Spanish', 1),
        ('John Smith', 'AI Solutions Architect', 'FinTech', 6, 'fraud detection,AI-driven analysis,compliance', 'ProNexus', 'AWS Certified', 'English', 1),
        ('Sarah Lee', 'CRM Specialist', 'SaaS', 4, 'CRM integration,Customer onboarding', 'GlobalTech', '', 'English,French', 0)
    ]
    cursor.executemany("""
    INSERT INTO experts (name, title, industry, years_experience, skills, company_affiliation, certifications, languages, availability)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, sample_data)
    print("Sample data inserted.")
else:
    print("Sample data already exists. Skipping insertion.")

# Commit and close
conn.commit()
conn.close()
print("Database creation complete.")
