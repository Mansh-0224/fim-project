
QUICKSTART.md
FIM Quick Start Cheatsheet
🎯 30-Second Setup
bash
# 1. Create folders
mkdir fim-project
cd fim-project
mkdir backend frontend

# 2. Install dependencies
cd backend
pip install flask flask-cors

# 3. Copy all code files to appropriate folders
# (fim_core.py, app.py → backend/)
# (index.html, style.css, script.js → frontend/)

# 4. Terminal 1 - Start backend
python app.py

# 5. Terminal 2 - Open frontend
cd ../frontend
# Double-click index.html OR:
python -m http.server 8000
🚀 Quick Usage
Step	Action	Example
1	Enter folder path in Step 1	C:\Users\You\Documents
2	Click "Initialize Baseline"	✅ Success
3	Modify/add/delete files	Add test.txt
4	Enter same path in Step 2	C:\Users\You\Documents
5	Click "Check Integrity"	See results
📋 File Descriptions
File	Purpose
fim_core.py	Hashing logic + baseline management
app.py	Flask API server
index.html	Frontend UI structure
style.css	Beautiful styling
script.js	Frontend-backend communication
baseline.json	Generated baseline (auto-created)
🔧 Key Functions
Backend (fim_core.py):

python
compute_file_hash(path)        # → SHA-256 hash
build_baseline(folder)          # → Create baseline
check_integrity(folder)         # → Compare & report
Frontend (script.js):

javascript
initializeBaseline()            # → Initialize button
checkIntegrity()                # → Check button
displayResults(data)            # → Show results
API Endpoints (app.py):

text
POST /api/init-baseline         # Request: {folder: path}
POST /api/check                 # Request: {folder: path}
GET  /api/health                # Health check
⚡ Common Commands
bash
# Start Flask
python app.py

# Install Flask
pip install flask flask-cors

# Run Python HTTP server
python -m http.server 8000

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (macOS/Linux)
source venv/bin/activate
✅ Success Checklist
 All 5 code files copied to correct folders

 Flask installed: pip install flask flask-cors

 Backend running: python app.py (shows port 5000)

 Frontend loaded: index.html displays

 Input folder path works: No "Invalid folder" error

 Initialize creates baseline.json

 Check Integrity shows results

🐛 Quick Fixes
Problem	Fix
Backend won't start	pip install flask flask-cors
Connection refused	Start Flask in another terminal
Folder not found	Use absolute path: C:\full\path\here
No results shown	Check browser console (F12)
baseline.json missing	Run initialize first
📊 Result Colors
🟢 Green = Unchanged files ✓

🟠 Yellow = Modified files ⚠️

🔵 Blue = Added files ➕

🔴 Red = Deleted files ➖

💡 Pro Tips
Test Folder: Use a small folder with 5-10 files first

Two Terminals: Keep backend and frontend in separate terminal windows

Path Format: Use full paths from root (e.g., C:\Users\... not ~)

Refresh: Browser refresh (F5) won't affect backend

Multiple Folders: Run separate instances for different folders

🎓 Learning Path
Phase 1 - Basic (Day 1)

 Understand SHA-256 hashing concept

 Setup and run the project

 Test with sample folder

Phase 2 - Intermediate (Day 2-3)

 Read through fim_core.py

 Understand Flask endpoints

 Modify UI styling

Phase 3 - Advanced (Day 4+)

 Add new features (multiple folders, CSV export)

 Learn about watchdog for real-time monitoring

 Deploy to web server

📚 Resources
hashlib docs: https://docs.python.org/3/library/hashlib.html

Flask docs: https://flask.palletsprojects.com/

JavaScript Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API

Ready? Start with: python app.py 🚀