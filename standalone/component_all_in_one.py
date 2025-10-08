"""
Grasshopper All-in-One Analyzer - v4.0 (Universal Path Detection)

🌍 WORKS ANYWHERE - No hardcoded paths!

Inputs (ALL OPTIONAL):
- mode: Number (0-4) - Analysis mode (default: 0)
  0 = Quick Check
  1 = Full Analysis  
  2 = Statistics Only
  3 = Find Issues
  4 = Auto-Fix
- auto_fix: Boolean - Enable automatic fixes (default: False)
- lib_path: Text - Custom path to gh_live_analyzer.py folder (optional)

Outputs:
- a: Main report
"""

import sys
import os

# === PATH INPUT VALIDATION ===
if 'path' not in dir() or not path:
    a = """❌ PATH REQUIRED!

Please connect 'path' input with your standalone folder location.

Example:
1. Add text panel with: r"C:\\gh_analyzer\\standalone"
2. Connect to 'path' input

💡 Use 'r' prefix for Windows paths
"""
elif not os.path.exists(str(path).strip()):
    a = f"""❌ PATH NOT FOUND: {path}

Please check:
1. Path exists
2. Spelling is correct  
3. Use raw string format: r"C:\\path\\to\\folder"
"""
else:
    gh_path = str(path).strip()
    if gh_path not in sys.path:
        sys.path.insert(0, gh_path)
    
    try:
        from gh_live_analyzer import GHLiveAnalyzer

from gh_live_analyzer import GHLiveAnalyzer