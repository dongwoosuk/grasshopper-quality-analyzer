"""
Grasshopper Issue Finder - v3.0 (Auto Path + Auto Run)

Shows detailed list of all issues found

Inputs (from Grasshopper):
- path: Text - Path to standalone folder

Outputs:
- a: Detailed issue report
"""

# Grasshopper inputs (automatically defined by GH Python component)
# pylint: disable=undefined-variable
# type: ignore

import sys
import os

# === PATH INPUT VALIDATION ===
if 'path' not in dir() or not path:  # type: ignore
    a = """❌ PATH REQUIRED!

Please connect 'path' input with your standalone folder location.

Example:
1. Add text panel with: r"C:\\gh_analyzer\\standalone"
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
    if gh_path not in sys.path:
        sys.path.insert(0, gh_path)
    
    try:
        from gh_live_analyzer import GHLiveAnalyzer
        
        analyzer = GHLiveAnalyzer()
        analyzer.scan_document()
        analyzer.run_all_checks()
        
        # Get all issues
        issues = analyzer.issues
        
        if not issues:
            a = "✅ No issues found!"
        else:
            # Group by severity
            errors = [i for i in issues if i['severity'] == 'error']
            warnings = [i for i in issues if i['severity'] == 'warning']
            info = [i for i in issues if i['severity'] == 'info']
            
            report = "=== ISSUES FOUND ===\n\n"
            
            if errors:
                report += "❌ ERRORS:\n"
                for issue in errors:
                    report += f"  [{issue['rule_id']}] {issue['title']}\n"
                    report += f"  → {issue['message']}\n\n"
            
            if warnings:
                report += "⚠️  WARNINGS:\n"
                for issue in warnings:
                    report += f"  [{issue['rule_id']}] {issue['title']}\n"
                    report += f"  → {issue['message']}\n\n"
            
            if info:
                report += "ℹ️  INFO:\n"
                for issue in info:
                    report += f"  [{issue['rule_id']}] {issue['title']}\n"
                    report += f"  → {issue['message']}\n\n"
            
            report += f"\nTotal: {len(errors)} errors, {len(warnings)} warnings, {len(info)} info"
            a = report
            
    except Exception as e:
        a = f"❌ ERROR: {str(e)}\n\nPlease check that gh_live_analyzer.py exists in the path folder."
