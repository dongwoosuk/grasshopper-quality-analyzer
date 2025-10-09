"""
Grasshopper All-in-One Analyzer - v3.0 (Auto Path + Auto Run)

Complete analysis with multiple modes

Inputs:
- mode: Number (0-4) - Analysis mode (default: 0)
  0 = Quick Check
  1 = Full Analysis  
  2 = Statistics Only
  3 = Find Issues
  4 = Auto-Fix
- auto_fix: Boolean - Enable automatic fixes (default: False)

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
        
        # Get mode (default 0)
        analysis_mode = int(mode) if 'mode' in dir() and mode is not None else 0
        do_auto_fix = auto_fix if 'auto_fix' in dir() and auto_fix else False
        
        analyzer = GHLiveAnalyzer()
        analyzer.scan_document()
        
        if analysis_mode == 0:
            # Quick Check
            analyzer.run_all_checks()
            score = analyzer.calculate_health_score()
            stats = analyzer.get_statistics()
            issues = analyzer.issues
            
            errors = len([i for i in issues if i['severity'] == 'error'])
            warnings = len([i for i in issues if i['severity'] == 'warning'])
            
            if score >= 90:
                status = "✅ Excellent"
            elif score >= 70:
                status = "👍 Good"
            elif score >= 50:
                status = "⚠️  Needs Attention"
            else:
                status = "❌ Critical"
            
            a = f"""
==================================================
QUICK CHECK
==================================================

📊 Score: {score}/100
Status: {status}

🔧 Components: {stats['total_components']}
Issues: {errors} errors, {warnings} warnings

==================================================
"""
        
        elif analysis_mode == 1:
            # Full Analysis
            analyzer.run_all_checks()
            score = analyzer.calculate_health_score()
            stats = analyzer.get_statistics()
            issues = analyzer.issues
            
            errors = [i for i in issues if i['severity'] == 'error']
            warnings = [i for i in issues if i['severity'] == 'warning']
            info = [i for i in issues if i['severity'] == 'info']
            
            report = f"""
==================================================
FULL ANALYSIS
==================================================

📊 Score: {score}/100
🔧 Components: {stats['total_components']}
🔗 Wires: {stats['total_wires']}
📁 Groups: {stats['total_groups']}

"""
            if errors:
                report += "❌ ERRORS:\n"
                for issue in errors:
                    report += f"  [{issue['rule_id']}] {issue['title']}\n"
            
            if warnings:
                report += "\n⚠️  WARNINGS:\n"
                for issue in warnings:
                    report += f"  [{issue['rule_id']}] {issue['title']}\n"
            
            if info:
                report += f"\nℹ️  INFO: {len(info)} items\n"
            
            report += "\n==================================================\n"
            a = report
        
        elif analysis_mode == 2:
            # Statistics Only
            stats = analyzer.get_statistics()
            
            report = f"""
==================================================
STATISTICS
==================================================

📊 Document Overview:
  • Components: {stats['total_components']}
  • Parameters: {stats['total_params']}
  • Wires: {stats['total_wires']}
  • Groups: {stats['total_groups']}

==================================================
"""
            a = report
        
        elif analysis_mode == 3:
            # Find Issues
            analyzer.run_all_checks()
            issues = analyzer.issues
            
            if not issues:
                a = "✅ No issues found!"
            else:
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
        
        elif analysis_mode == 4:
            # Auto-Fix
            fixed = analyzer.auto_name_parameters()
            
            if fixed > 0:
                a = f"""
==================================================
AUTO-FIX COMPLETE
==================================================

✅ Fixed {fixed} unnamed parameters

==================================================
"""
            else:
                a = """
==================================================
AUTO-FIX COMPLETE
==================================================

ℹ️  No fixes needed!

==================================================
"""
        else:
            a = "❌ Invalid mode! Use 0-4"
            
    except Exception as e:
        a = f"❌ ERROR: {str(e)}\n\nPlease check that gh_live_analyzer.py exists in the path folder."
