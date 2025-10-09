"""
Grasshopper Auto-Fix - v3.0 (Auto Path + Auto Run)

Automatically fixes common issues

Outputs:
- a: Fix report
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
        
        analyzer = GHLiveAnalyzer()
        analyzer.scan_document()
        
        # Auto-fix unnamed parameters
        fixed = analyzer.auto_name_parameters()
        
        if fixed > 0:
            report = f"""
==================================================
AUTO-FIX COMPLETE
==================================================

✅ Fixed {fixed} unnamed parameters

All unnamed sliders and panels now have descriptive names.

==================================================
"""
        else:
            report = """
==================================================
AUTO-FIX COMPLETE
==================================================

ℹ️  No fixes needed - all parameters already named!

==================================================
"""
        
        a = report
            
    except Exception as e:
        a = f"❌ ERROR: {str(e)}\n\nPlease check that gh_live_analyzer.py exists in the path folder."
