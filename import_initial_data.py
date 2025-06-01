import os
import sqlite3
from datetime import datetime

# Path to your assignments folder
ASSIGNMENTS_FOLDER = 'assignments'

# Connect to the database
conn = sqlite3.connect('plagiarism.db')
c = conn.cursor()

# Loop through all .txt files
for filename in os.listdir(ASSIGNMENTS_FOLDER):
    if filename.endswith('.txt'):
        filepath = os.path.join(ASSIGNMENTS_FOLDER, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            c.execute("INSERT INTO submissions (filename, content, result, timestamp) VALUES (?, ?, ?, ?)",
                      (filename, content, 'Baseline dataset', datetime.now()))

conn.commit()
conn.close()

print("✅ Existing assignments imported into the database.")
