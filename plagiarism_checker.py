import sqlite3
from difflib import SequenceMatcher
from datetime import datetime
import re

def normalize_text(text):
    # Keep only letters and join them into words without gaps
    words = re.findall(r'[a-zA-Z]+', text)
    normalized = ' '.join(words).lower()
    return normalized.strip()

def check_plagiarism(input_text, threshold=0.7, top_n=3):
    conn = sqlite3.connect('plagiarism.db')
    c = conn.cursor()

    # Fetch all past submissions
    c.execute("SELECT filename, content, timestamp FROM submissions")
    previous_assignments = c.fetchall()
    conn.close()

    # Normalize input text
    normalized_input = normalize_text(input_text)

    similarity_list = []
    above_threshold_found = False

    for filename, content, timestamp in previous_assignments:
        normalized_db_content = normalize_text(content)
        similarity = SequenceMatcher(None, normalized_input, normalized_db_content).ratio()

        # Format timestamp
        try:
            timestamp_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            timestamp_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        timestamp_str = timestamp_obj.strftime('%b %d, %Y %H:%M')

        snippet = content[:100].replace('\n', ' ').strip() + "..."

        if similarity >= threshold:
            above_threshold_found = True

        similarity_list.append((similarity, filename, timestamp_str, snippet))

    # Sort by similarity descending
    similarity_list.sort(reverse=True, key=lambda x: x[0])
    top_matches = similarity_list[:top_n]

    results = []

    # Add top N match previews
    results.append(f"🔍 Top {top_n} Similar Assignments:")
    for sim, filename, timestamp_str, snippet in top_matches:
        symbol = "⚠️" if sim >= threshold else "ℹ️"
        results.append(f"{symbol} '{filename}' ({sim:.2%}) on {timestamp_str}\nSnippet: {snippet}")

    # Final summary based on threshold
    if not above_threshold_found:
        results.append("\n✅ No significant matches found. Assignment looks original.")
        results.append("📝 Do you want to save this assignment to the database? (yes/no)")
    else:
        results.append("\n❌ Similar assignment(s) detected above the threshold. Not saving automatically.")

    return results
