# app.py - Flask Backend API
from flask import Flask, request, jsonify
from flask_cors import CORS
from fim_core import FileIntegrityMonitor
import os

app = Flask(__name__)
CORS(app)  # Enable CORS so frontend can call backend

# Initialize FIM with baseline file in backend folder
fim = FileIntegrityMonitor("baseline.json")

@app.route("/api/init-baseline", methods=["POST"])
def init_baseline():
    """
    Initialize baseline for a folder.
    Expected JSON: { "folder": "/path/to/folder" }
    """
    try:
        data = request.json
        folder_path = data.get("folder", "").strip()
        
        # Validate folder exists
        if not folder_path or not os.path.isdir(folder_path):
            return jsonify({
                "status": "error",
                "message": f"Invalid folder path: {folder_path}"
            }), 400
        
        # Build baseline
        file_count = fim.build_baseline(folder_path)
        
        return jsonify({
            "status": "success",
            "message": f"Baseline created successfully!",
            "files_scanned": file_count,
            "baseline_file": "baseline.json"
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error: {str(e)}"
        }), 500

@app.route("/api/check", methods=["POST"])
def check_integrity():
    """
    Check file integrity against baseline.
    Expected JSON: { "folder": "/path/to/folder" }
    """
    try:
        data = request.json
        folder_path = data.get("folder", "").strip()
        
        # Validate folder exists
        if not folder_path or not os.path.isdir(folder_path):
            return jsonify({
                "status": "error",
                "message": f"Invalid folder path: {folder_path}"
            }), 400
        
        # Check integrity
        result = fim.check_integrity(folder_path)
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error: {str(e)}"
        }), 500

@app.route("/api/health", methods=["GET"])
def health():
    """Simple health check endpoint"""
    return jsonify({
        "status": "ok",
        "message": "FIM Backend is running"
    }), 200

if __name__ == "__main__":
    print("Starting File Integrity Monitoring Backend...")
    print("Frontend should call: http://localhost:5000/api/...")
    app.run(debug=True, port=5000)