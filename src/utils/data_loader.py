import sqlite3

class DataLoader:
    def __init__(self, db_path='experts.db'):
        self.conn = sqlite3.connect(db_path)

    def load_experts(self, filters=None):
        """
        Load experts from the database, applying filters dynamically.
        """
        cursor = self.conn.cursor()
        query = "SELECT * FROM experts WHERE 1=1"
        params = []

        # Apply filters
        if filters:
            if 'industry' in filters and filters['industry'] != 'Any':
                query += " AND industry = ?"
                params.append(filters['industry'])
            if 'min_experience' in filters:
                query += " AND years_experience >= ?"
                params.append(filters['min_experience'])
            if 'required_skills' in filters and filters['required_skills']:
                required_skills = filters['required_skills'].split(',')
                for skill in required_skills:
                    query += " AND skills LIKE ?"
                    params.append(f"%{skill.strip()}%")

        # Execute query
        cursor.execute(query, params)
        rows = cursor.fetchall()

        # Convert rows to dictionaries
        experts = [
            {
                "id": row[0],
                "name": row[1],
                "title": row[2],
                "industry": row[3],
                "years_experience": row[4],
                "skills": row[5].split(","),
                "company_affiliation": row[6],
                "certifications": row[7].split(",") if row[7] else [],
                "languages": row[8].split(",") if row[8] else [],
                "availability": bool(row[9])
            }
            for row in rows
        ]
        return experts

