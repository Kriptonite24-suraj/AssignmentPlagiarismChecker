import sqlite3

def init_db():
    conn = sqlite3.connect('plagiarism.db')
    c = conn.cursor()

    # Drop old table if exists (optional safety)
    c.execute('DROP TABLE IF EXISTS submissions')

    # Create new table with 'content' column
    c.execute('''
        CREATE TABLE submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            content TEXT,
            result TEXT,
            timestamp TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database initialized with required columns.")

if __name__ == '__main__':
    init_db()
