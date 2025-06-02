from flask import Flask, request, render_template, redirect, url_for, session
from plagiarism_checker import check_plagiarism
import sqlite3
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
import docx

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session handling

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_content(file_path, extension):
    try:
        if extension == 'txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        elif extension == 'pdf':
            reader = PdfReader(file_path)
            return "\n".join([page.extract_text() or "" for page in reader.pages])
        elif extension == 'docx':
            doc = docx.Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print("Error extracting content:", e)
        return ""
    return ""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    input_text = ""

    if request.method == 'POST':
        # File upload
        file = request.files.get('file')
        filename = "Pasted Text"

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_ext = filename.rsplit('.', 1)[1].lower()
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            input_text = extract_content(save_path, file_ext)
        else:
            # Fallback to pasted content
            input_text = request.form.get('assignment', '')

        if input_text.strip():  # Ensure content isn't blank
            result = check_plagiarism(input_text)

            # ✅ FIXED LOGIC: Search all result lines for originality confirmation
            if result and any("No significant matches found" in line for line in result):
                session['pending_data'] = {
                    'filename': filename,
                    'content': input_text,
                    'result': result[0]
                }
                return render_template('index.html', result=result, ask_to_save=True)

        else:
            result = ["No valid content extracted from file or paste. Please try again."]

    return render_template('index.html', result=result)

@app.route('/save', methods=['POST'])
def save():
    data = session.pop('pending_data', None)
    if data:
        conn = sqlite3.connect('plagiarism.db')
        c = conn.cursor()
        c.execute("INSERT INTO submissions (filename, content, result, timestamp) VALUES (?, ?, ?, ?)",
                  (data['filename'], data['content'], data['result'], datetime.now()))
        conn.commit()
        conn.close()
        return render_template('index.html', result=["✅ Assignment saved successfully."], ask_to_save=False)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
