"""
Grasshopper Health Check Component - v3.0 (Auto Path + Auto Run)

Quick health check with score

Outputs:
- a: Analysis report
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
        analyzer.run_all_checks()
        
        score = analyzer.calculate_health_score()
        stats = analyzer.get_statistics()
        issues = analyzer.issues
        
        # Count by severity
        errors = len([i for i in issues if i['severity'] == 'error'])
        warnings = len([i for i in issues if i['severity'] == 'warning'])
        info_count = len([i for i in issues if i['severity'] == 'info'])
        
        # Status
        if score >= 90:
            status = "✅ Excellent"
        elif score >= 70:
            status = "👍 Good"
        elif score >= 50:
            status = "⚠️  Needs Attention"
        else:
            status = "❌ Critical"
        
        report = f"""
==================================================
GRASSHOPPER HEALTH CHECK
==================================================

📊 Score: {score}/100
Status: {status}

🔧 Components: {stats['total_components']}
🔗 Connections: {stats['total_wires']}
📁 Groups: {stats['total_groups']}

Issues:
  ❌ Errors: {errors}
  ⚠️  Warnings: {warnings}
  ℹ️  Info: {info_count}

==================================================
"""
        a = report
            
    except Exception as e:
        a = f"❌ ERROR: {str(e)}\n\nPlease check that gh_live_analyzer.py exists in the path folder."
