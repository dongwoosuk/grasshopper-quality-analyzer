"""
Grasshopper Health Check - v4.0 (Updated for Unified Analyzer)

Quick health overview of your Grasshopper definition

Inputs (from Grasshopper):
- path: Text - Path to standalone folder containing gh_live_analyzer.py

Outputs:
- a: Health check report
"""

import sys
import os

# === PATH INPUT VALIDATION ===
if 'path' not in dir() or not path:  # type: ignore
    a = """❌ PATH REQUIRED!

Please connect 'path' input with your standalone folder location.

Example:
1. Add text panel with: r"C:\\Users\\Soku\\OneDrive - Steinberg Hart\\Desktop\\Source\\RhinoScripts\\src\\gh\\gh_analyzer_release\\standalone"
2. Connect to 'path' input

💡 Use 'r' prefix for Windows paths
"""
elif not os.path.exists(str(path).strip()):  # type: ignore
    a = f"""❌ PATH NOT FOUND: {path}

Please check:
1. Path exists
2. Spelling is correct  
3. Use raw string format: r"C:\\path\\to\\folder"
"""
else:
    gh_path = str(path).strip()  # type: ignore
    analyzer_file = os.path.join(gh_path, 'gh_live_analyzer.py')
    
    if not os.path.exists(analyzer_file):
        a = f"""❌ gh_live_analyzer.py not found in: {gh_path}

Please ensure gh_live_analyzer.py exists in the specified folder.
"""
    else:
        try:
            # Load the analyzer
            with open(analyzer_file, 'r', encoding='utf-8') as f:
                exec(f.read())
            
            # Run health check
            result = quick_check()
            a = result
            
        except Exception as e:
            a = f"""❌ HEALTH CHECK FAILED: {str(e)}

This may be due to:
- Document access issues
- Grasshopper version compatibility
- Component type recognition problems

Try:
1. Ensure Grasshopper document is open
2. Check if definition has circular references
3. Verify all components are functioning properly
"""
