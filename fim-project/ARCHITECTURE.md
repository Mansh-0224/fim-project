FIM System Architecture & Complete Guide
🏗️ System Architecture
text
┌─────────────────────────────────────────────────────────────┐
│                       FRONTEND (Browser)                     │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  index.html (UI Structure)                              │  │
│  │  ├─ Folder input field                                  │  │
│  │  ├─ Initialize Baseline button                          │  │
│  │  ├─ Check Integrity button                              │  │
│  │  └─ Results display (Added/Modified/Deleted/Unchanged)  │  │
│  └────────────────────────────────────────────────────────┘  │
│           ▼                                                    │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  script.js (JavaScript Logic)                           │  │
│  │  ├─ Fetch API calls to backend                          │  │
│  │  ├─ Display results dynamically                         │  │
│  │  └─ Handle user interactions                            │  │
│  └────────────────────────────────────────────────────────┘  │
│           ▼                                                    │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  style.css (Styling)                                    │  │
│  │  ├─ Beautiful gradient background                       │  │
│  │  ├─ Color-coded status messages                         │  │
│  │  └─ Responsive mobile-friendly design                   │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
        ▲                                         ▼
        │  HTTP Requests (POST/GET)              │ HTTP Responses (JSON)
        │  http://localhost:5000/api/...         │
        │                                         │
┌───────┴────────────────────────────────────────┴───────────────┐
│                   FLASK API (Backend)                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  app.py (Flask Server - Port 5000)                       │  │
│  │  ├─ POST /api/init-baseline (Initialize)                 │  │
│  │  ├─ POST /api/check (Check Integrity)                    │  │
│  │  └─ GET /api/health (Health Check)                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│           ▼                                                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  fim_core.py (Core Logic)                               │  │
│  │  ├─ FileIntegrityMonitor class                           │  │
│  │  ├─ get_all_files() - Scan directory recursively         │  │
│  │  ├─ compute_file_hash() - SHA-256 hashing                │  │
│  │  ├─ build_baseline() - Create snapshot                   │  │
│  │  ├─ load_baseline() - Read stored hashes                 │  │
│  │  └─ check_integrity() - Compare & detect changes         │  │
│  └──────────────────────────────────────────────────────────┘  │
│           ▼                                                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  File System Access                                      │  │
│  │  └─ os.walk(), os.path, file I/O (rb mode)              │  │
│  └──────────────────────────────────────────────────────────┘  │
│           ▼                                                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  baseline.json (Persistent Storage)                      │  │
│  │  ├─ Stores: relative_path, hash, size, modified_time     │  │
│  │  └─ Auto-created by build_baseline()                     │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
📊 Data Flow Diagram
Initialize Baseline Flow
text
User Input (folder path)
    ↓
validate folder exists?
    ├─ NO → Show error
    └─ YES → Continue
    ↓
os.walk() → Get all files recursively
    ↓
For each file:
    ├─ Open in binary read mode
    ├─ SHA-256.update(file_chunks)
    └─ Get hash digest (64 hex chars)
    ↓
Build dict: {relative_path: {hash, size, last_modified}}
    ↓
json.dump() → baseline.json
    ↓
Return: {"status": "success", "files_scanned": N}
    ↓
Display: "✅ Baseline created for N files"
Check Integrity Flow
text
User Input (folder path)
    ↓
Load baseline.json
    ↓
Current scan:
    ├─ os.walk() → Get all files
    ├─ Compute SHA-256 for each
    └─ Build current_dict
    ↓
Compare baseline vs current:
    ├─ File in baseline but not current → DELETED
    ├─ File in current but not baseline → ADDED
    ├─ File in both:
    │   ├─ Hash different → MODIFIED
    │   └─ Hash same → UNCHANGED
    └─ (repeat for all files)
    ↓
Return: {added: [...], modified: [...], deleted: [...], unchanged_count: N}
    ↓
Display results with color coding:
    ├─ 🟢 Green = Unchanged
    ├─ 🟠 Yellow = Modified
    ├─ 🔵 Blue = Added
    └─ 🔴 Red = Deleted
🔐 How SHA-256 Hashing Works
text
Original File: "Hello, World!"

┌─────────────────────────────────────┐
│   hashlib.sha256()                   │
│   sha256_hash = hashlib.sha256()     │
│   sha256_hash.update(b"Hello, World!")│
│   result = sha256_hash.hexdigest()  │
└─────────────────────────────────────┘
                ↓
Result: "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"
        (64 character hexadecimal string = unique fingerprint)

Key Property:
• Same file = Same hash
• Any byte changes = Completely different hash
• One-way function (cannot reverse hash to get file)
🔄 API Communication Example
Initialize Baseline Request
text
POST /api/init-baseline
Content-Type: application/json

{
  "folder": "C:\\Users\\John\\Documents"
}

---

Response (200 OK):
{
  "status": "success",
  "message": "Baseline created successfully!",
  "files_scanned": 35,
  "baseline_file": "baseline.json"
}
Check Integrity Request
text
POST /api/check
Content-Type: application/json

{
  "folder": "C:\\Users\\John\\Documents"
}

---

Response (200 OK):
{
  "status": "success",
  "timestamp": "2025-11-30T19:18:45.123456",
  "added": [
    "new_document.docx",
    "screenshot.png"
  ],
  "modified": [
    "report.xlsx",
    "notes.txt"
  ],
  "deleted": [
    "old_backup.zip"
  ],
  "unchanged_count": 32,
  "total_files": 35
}
🛠️ Configuration & Customization
Change Hash Algorithm
In fim_core.py, modify compute_file_hash():

python
# Current (SHA-256):
sha256_hash = hashlib.sha256()

# Alternative options:
md5_hash = hashlib.md5()           # Faster but less secure
sha1_hash = hashlib.sha1()         # Medium security
sha512_hash = hashlib.sha512()     # More secure, larger output
Change Flask Port
In app.py, modify the last line:

python
app.run(debug=True, port=5000)  # Change 5000 to your port
Change Chunk Size (for large files)
In fim_core.py, modify compute_file_hash():

python
for chunk in iter(lambda: f.read(65536), b""):  # 65KB chunks
# Change 65536 to:
# 1048576 = 1MB (faster, more memory)
# 8192 = 8KB (slower, less memory)
Change Baseline Filename
In app.py, modify initialization:

python
fim = FileIntegrityMonitor("baseline.json")
# Change to:
fim = FileIntegrityMonitor("fim_backup.json")
📈 Performance Considerations
Factor	Impact	Note
File Count	Linear time	1000 files ≈ 1-2 seconds
File Size	Linear time	Large files slow down hash computation
Chunk Size	Memory vs Speed	Larger chunks = faster but more RAM
Hash Algorithm	Security vs Speed	SHA-256 is balanced choice
Directory Depth	Linear time	os.walk handles recursion efficiently
🔒 Security & Integrity
Capabilities ✅
Detect accidental file modifications

Detect file corruption

Verify data integrity

Track changes over time

Limitations ⚠️
Cannot detect forged files if attacker modifies both file AND hash

No digital signatures (cannot verify who made changes)

No encryption (baseline.json is readable)

Cannot detect access without modification

Production Hardening
For real-world use, consider:

Digital signatures on baseline using private key

Store baseline in immutable location

Use tamper-proof storage (blockchain, HSM)

Add access control & audit logging

Combine with real-time monitoring tools

📝 Code Statistics
Component	Lines	Complexity
fim_core.py	~150	Medium
app.py	~80	Low
index.html	~120	Low
style.css	~250	Low
script.js	~180	Low
Total	~780	Beginner-Intermediate
🎓 Learning Outcomes
After completing this project, you'll understand:

✅ Python Concepts

File I/O and binary reading

Dictionary/JSON operations

Exception handling

Function design patterns

✅ Backend Concepts

Flask framework basics

RESTful API design

HTTP methods (POST/GET)

CORS and cross-origin requests

✅ Frontend Concepts

HTML structure and forms

CSS styling and responsive design

JavaScript ES6+ (fetch, async/await)

DOM manipulation

✅ Security Concepts

Cryptographic hashing (SHA-256)

File integrity checking

Baseline snapshots

Change detection

✅ Full-Stack Integration

Frontend-backend communication

JSON data exchange

Error handling across layers

Testing and debugging

🚀 Deployment Options
Local Development
Run python app.py + open index.html

Best for learning and testing

Single Machine
Keep frontend and backend on same computer

Access via http://localhost:5000

Local Network
Host Flask on network IP: 0.0.0.0:5000

Access from other computers: http://your-ip:5000

Cloud Deployment
Docker containerization

AWS/Azure/Google Cloud

Heroku for simple hosting

With database instead of JSON

🐍 Python Version Requirements
Minimum: Python 3.7

Recommended: Python 3.9+

Tested with: Python 3.10, 3.11

📚 Further Reading
Python hashlib: https://docs.python.org/3/library/hashlib.html

Flask documentation: https://flask.palletsprojects.com/

SHA-256 explanation: https://en.wikipedia.org/wiki/SHA-2

REST API design: https://restfulapi.net/

File integrity monitoring best practices: https://www.cisecurity.org/

You now have a complete, working File Integrity Monitoring System! 🎉