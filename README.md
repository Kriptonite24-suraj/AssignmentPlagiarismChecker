# AssignmentPlagiarismChecker

The Assignment Plagiarism Checker Using AI is an intelligent system developed to detect plagiarism in student assignments. The core objective is to ensure academic integrity by identifying copied or highly similar content among submissions. Built using Python and AI-based text comparison techniques, the system streamlines the process of plagiarism detection and provides accurate results in real-time.

The application supports both text input and file uploads (.txt, .pdf, .doc, .docx), allowing users to submit assignments conveniently. Each input undergoes a normalization process, where punctuation, symbols, case differences, and extra spaces are removed. This ensures that semantic similarity is prioritized over surface-level formatting differences.

Once the text is cleaned, the system uses TF-IDF vectorization and Cosine Similarity to compare the current submission against a growing database of previous assignments. If the similarity score exceeds a defined threshold, the system flags the submission as potentially plagiarized.

The backend is developed in Python, while the project is hosted using Render and version-controlled with GitHub. The system includes an integrated SQLite database to store assignment content, filenames, similarity scores, and timestamps for future reference and auditing.

A user-friendly interface is provided to make it easy for users to upload assignments, view results, and understand similarity reports. The project was built with scalability in mind — as more assignments are submitted, the database grows, thereby improving the system’s comparison accuracy over time.

This project provides a real-world solution to an academic problem using a combination of software engineering, AI, and natural language processing. It is reliable, efficient, and extensible for future improvements such as semantic NLP models, PDF report generation, and user authentication.