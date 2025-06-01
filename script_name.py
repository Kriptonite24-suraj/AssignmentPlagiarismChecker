import sqlite3

conn = sqlite3.connect('plagiarism.db')
cursor = conn.cursor()

cursor.execute("SELECT id, filename, content, timestamp FROM assignments")
rows = cursor.fetchall()

for row in rows:
    print(f"ID: {row[0]}, Filename: {row[1]}, Timestamp: {row[3]}")
    print(f"Content:\n{row[2][:500]}...")  # print first 500 chars
    print("="*50)

conn.close()
