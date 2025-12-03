File Integrity Monitoring System - Setup & Usage Guide
Project Overview
A beginner-intermediate FIM system that monitors folder changes using SHA-256 hashing. It detects added, modified, and deleted files in real-time.

Tech Stack:

Backend: Python + Flask + hashlib

Frontend: HTML + CSS + JavaScript

Database: JSON baseline file

📂 Project Structure
text
fim-project/
│
├── backend/
│   ├── app.py              # Flask API server
│   ├── fim_core.py         # Core hashing logic
│   └── baseline.json       # Generated baseline (created after init)
│
├── frontend/
│   ├── index.html          # Main UI
│   ├── style.css           # Styling
│   └── script.js           # Frontend logic
│
└── requirements.txt        # Python dependencies
⚙️ Installation & Setup
Step 1: Create Project Folder
bash
# On Windows
mkdir fim-project
cd fim-project

# Create backend and frontend folders
mkdir backend
mkdir frontend
Step 2: Install Python Dependencies
bash
# Navigate to backend folder
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Flask and CORS
pip install flask flask-cors
Step 3: Copy Backend Files
Place these files in the backend/ folder:

fim_core.py (the hashing logic file)

app.py (the Flask API server)

Step 4: Copy Frontend Files
Place these files in the frontend/ folder:

index.html (main UI)

style.css (styling)

script.js (JavaScript logic)

🚀 Running the Project
Terminal 1 - Start Backend
bash
cd backend
python app.py
You should see output like:

text
Starting File Integrity Monitoring Backend...
Frontend should call: http://localhost:5000/api/...
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:5000
Terminal 2 - Open Frontend
bash
cd frontend

# Option A: Open index.html directly in browser
# Just double-click index.html

# Option B: Serve with Python (recommended)
python -m http.server 8000
# Then open: http://localhost:8000
📖 How to Use
Step 1: Initialize Baseline
Open the frontend in your browser.

Enter a folder path in the "Folder Path" field (e.g., C:\Users\YourName\Documents)

Click "Initialize Baseline" button.

Wait for success message showing file count scanned.

A baseline.json file is created in the backend folder.

Example paths:

Windows: C:\Users\YourName\Documents

macOS: /Users/yourname/Documents

Linux: /home/username/documents

Step 2: Modify Your Test Folder
After creating baseline, test the system by:

Adding a new file to the folder

Modifying an existing file (change content)

Deleting an existing file

Step 3: Check Integrity
Enter the same folder path in the "Check Integrity" section.

Click "Check Integrity" button.

The system will display:

✅ Unchanged Files (green)

⚠️ Modified Files (yellow)

➕ Added Files (blue)

➖ Deleted Files (red)

🔍 Understanding the System
How Hashing Works
The system uses SHA-256 algorithm:

Reads each file in the folder

Computes a unique 64-character hash (fingerprint)

Stores all hashes in baseline.json

Later, recalculates hashes and compares with baseline

Any change in file = different hash = detected modification

Example baseline.json
json
{
  "document.txt": {
    "hash": "a1b2c3d4e5f6...",
    "size": 1024,
    "last_modified": 1701325086.123
  },
  "image.png": {
    "hash": "f6e5d4c3b2a1...",
    "size": 2048,
    "last_modified": 1701325090.456
  }
}
🐛 Troubleshooting
"Connection refused" or "Could not connect to backend"
Solution: Make sure Flask is running in another terminal

Run: cd backend && python app.py

"Folder not found"
Solution: Use absolute path (full path from root)

Windows example: C:\Users\John\Desktop\test-folder

Linux example: /home/john/Desktop/test-folder

"Permission denied" error
Solution: Make sure the folder is readable

Avoid system folders like Windows\System32

Use a regular user folder like Documents

Baseline.json not created
Solution: Check backend console for errors

Ensure the folder path is correct

Try a folder with fewer files first

Frontend shows "Backend not reachable"
Solution: Flask must be running

Check that port 5000 is not blocked by firewall

Try: python app.py --port 5001

📚 Code Explanation
fim_core.py - Key Functions
compute_file_hash(file_path)

Reads file in 64KB chunks (efficient for large files)

Returns SHA-256 hash as hex string

build_baseline(folder_path)

Walks directory recursively using os.walk()

Creates dictionary: {file_path: {hash, size, modified_time}}

Saves to baseline.json

check_integrity(folder_path)

Compares current scan with baseline

Returns 4 lists: added, modified, deleted, unchanged

app.py - API Endpoints
POST /api/init-baseline

text
Request: {"folder": "/path/to/folder"}
Response: {"status": "success", "files_scanned": 25}
POST /api/check

text
Request: {"folder": "/path/to/folder"}
Response: {
  "status": "success",
  "added": [...],
  "modified": [...],
  "deleted": [...],
  "unchanged_count": 20
}
script.js - Frontend Functions
initializeBaseline()

Reads folder path from input

Sends POST to /api/init-baseline

Displays success/error message

checkIntegrity()

Sends POST to /api/check

Calls displayResults() to show results in UI

displayResults(data, container)

Updates summary stats

Populates file lists dynamically

Shows results container

✨ Features Implemented
✅ SHA-256 file hashing
✅ Recursive directory scanning
✅ JSON baseline storage
✅ Detect added files
✅ Detect modified files
✅ Detect deleted files
✅ Beautiful responsive UI
✅ Error handling & validation
✅ CORS enabled for frontend-backend communication
✅ Loading states & status messages
✅ Portable folder monitoring (relative paths)

🎯 Next Steps (Optional Improvements)
Level 1: Easy
 Add "Clear Baseline" button to reset monitoring

 Display file modification time in results

 Add keyboard shortcuts (Enter to submit)

Level 2: Intermediate
 Auto-refresh: check integrity every 30 seconds

 Support multiple folders (different baselines)

 Choose between MD5, SHA-1, SHA-256 algorithms

 Export results to CSV file

Level 3: Advanced
 Real-time file monitoring using watchdog library

 Database backend (SQLite) instead of JSON

 File content comparison for modified files

 Scheduling periodic checks using APScheduler

 Web dashboard with graphs and statistics

📝 Example Walkthrough
Scenario: Monitor a Documents folder

Initialize:

Input: C:\Users\John\Documents

System scans 50 files

Creates baseline with all 50 file hashes

Make Changes:

Add newfile.txt

Edit report.docx (content changed)

Delete old_notes.txt

Check Integrity:

Modified: report.docx (hash mismatch)

Added: newfile.txt

Deleted: old_notes.txt

Unchanged: 47 files

🔒 Security Notes
SHA-256 is cryptographically secure

Can detect accidental file changes or corruption

Cannot detect intentional attacks with forged files

For production use, consider adding digital signatures

📞 Support
If you encounter issues:

Check the terminal output for error messages

Verify folder paths are correct and accessible

Ensure Flask backend is running

Check browser console (F12 → Console tab) for JavaScript errors

Happy monitoring! 🔐

