import sqlite3

def create_database():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    # Drop old table if exists (safe for learning)
    cursor.execute("DROP TABLE IF EXISTS students")

    # Create new table with subject-wise marks
    cursor.execute("""
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            roll INTEGER,
            maths INTEGER,
            physics INTEGER,
            chemistry INTEGER,
            english INTEGER,
            computer INTEGER,
            total INTEGER,
            percentage REAL,
            result TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("Database updated with subject-wise marks table.")

if __name__ == "__main__":
    create_database()
