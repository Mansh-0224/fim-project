# fim_core.py - File Integrity Monitoring Core Logic
import os
import hashlib
import json
from pathlib import Path
from datetime import datetime

class FileIntegrityMonitor:
    """Core FIM functionality using SHA-256 hashing"""
    
    def __init__(self, baseline_file="baseline.json"):
        self.baseline_file = baseline_file
        self.baseline = {}
    
    def get_all_files(self, folder_path):
        """
        Recursively get all files in a folder.
        Returns list of (relative_path, full_path) tuples
        """
        files = []
        try:
            for root, dirs, filenames in os.walk(folder_path):
                for filename in filenames:
                    full_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(full_path, folder_path)
                    files.append((relative_path, full_path))
        except Exception as e:
            print(f"Error scanning folder: {e}")
        return files
    
    def compute_file_hash(self, file_path):
        """
        Compute SHA-256 hash of a file.
        Reads file in chunks to handle large files efficiently.
        """
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                # Read file in 64kb chunks
                for chunk in iter(lambda: f.read(65536), b""):
                    sha256_hash.update(chunk)
            return sha256_hash.hexdigest()
        except Exception as e:
            print(f"Error computing hash for {file_path}: {e}")
            return None
    
    def build_baseline(self, folder_path):
        """
        Scan all files in folder and create baseline (dictionary of hashes).
        Save to baseline.json file.
        Returns count of files scanned.
        """
        self.baseline = {}
        files = self.get_all_files(folder_path)
        
        for relative_path, full_path in files:
            file_hash = self.compute_file_hash(full_path)
            if file_hash:
                self.baseline[relative_path] = {
                    "hash": file_hash,
                    "size": os.path.getsize(full_path),
                    "last_modified": os.path.getmtime(full_path)
                }
        
        # Save baseline to JSON
        self._save_baseline()
        return len(self.baseline)
    
    def _save_baseline(self):
        """Save baseline dictionary to JSON file"""
        try:
            with open(self.baseline_file, "w") as f:
                json.dump(self.baseline, f, indent=2)
        except Exception as e:
            print(f"Error saving baseline: {e}")
    
    def load_baseline(self):
        """Load baseline from JSON file"""
        try:
            if os.path.exists(self.baseline_file):
                with open(self.baseline_file, "r") as f:
                    self.baseline = json.load(f)
                return True
            else:
                print(f"Baseline file not found: {self.baseline_file}")
                return False
        except Exception as e:
            print(f"Error loading baseline: {e}")
            return False
    
    def check_integrity(self, folder_path):
        """
        Compare current state with baseline.
        Returns dict with added, modified, deleted, and unchanged files.
        """
        if not self.load_baseline():
            return {
                "status": "error",
                "message": "No baseline found. Please initialize first."
            }
        
        # Current state
        current_files = {}
        files = self.get_all_files(folder_path)
        
        for relative_path, full_path in files:
            file_hash = self.compute_file_hash(full_path)
            if file_hash:
                current_files[relative_path] = {
                    "hash": file_hash,
                    "size": os.path.getsize(full_path),
                    "last_modified": os.path.getmtime(full_path)
                }
        
        # Compare
        added = []
        modified = []
        deleted = []
        unchanged = []
        
        # Check baseline files
        for file_path, baseline_info in self.baseline.items():
            if file_path not in current_files:
                deleted.append(file_path)
            elif current_files[file_path]["hash"] != baseline_info["hash"]:
                modified.append(file_path)
            else:
                unchanged.append(file_path)
        
        # Check for new files
        for file_path in current_files:
            if file_path not in self.baseline:
                added.append(file_path)
        
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "added": added,
            "modified": modified,
            "deleted": deleted,
            "unchanged_count": len(unchanged),
            "total_files": len(current_files)
        }
