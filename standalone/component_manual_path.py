"""
Grasshopper All-in-One Analyzer - Manual Path Version

Simple version with manual path input - Most reliable for any computer

Inputs (REQUIRED):
- path: String - Path to gh_live_analyzer.py folder
  Example: r"C:\gh_analyzer\standalone"
  
Inputs (OPTIONAL):
- mode: Number (0-4) - Analysis mode (default: 0)
- auto_fix: Boolean - Enable automatic fixes (default: False)

Outputs:
- a: Main report
"""

import sys
import os

# === CLEAR CACHE ===
if 'gh_live_analyzer' in sys.modules:
    del sys.modules['gh_live_analyzer']

# === PATH VALIDATION ===
if 'path' not in dir() or not path:
    a = """❌ PATH REQUIRED!

Please connect 'path' input:

1. Add text panel with your path
2. Connect to 'path' input
3. Examples:
   r"C:\\gh_analyzer\\standalone"
   r"C:\\Users\\YourName\\Desktop\\gh_analyzer\\standalone"

💡 TIP: Use 'r' before quotes for raw string
"""
else:
    gh_path = str(path).strip()
    
    # Validate path
    if not os.path.exists(gh_path):
        a = f"""❌ PATH NOT FOUND: {gh_path}

Please check:
1. Path exists
2. Spelling is correct
3. Use double backslashes \\\\ or r"..." format

Example:
r"C:\\gh_analyzer\\standalone"
"""
    elif not os.path.exists(os.path.join(gh_path, "gh_live_analyzer.py")):
        a = f"""❌ gh_live_analyzer.py NOT FOUND in: {gh_path}

Please check:
1. gh_live_analyzer.py exists in folder
2. Path points to 'standalone' folder
3. All files are extracted

Expected structure:
{gh_path}\\
  ├── gh_live_analyzer.py ✓
  └── component_*.py
"""
    else:
        # Path is valid, proceed with analysis
        if gh_path in sys.path:
            sys.path.remove(gh_path)
        sys.path.insert(0, gh_path)
        
        try:
            from gh_live_analyzer import GHLiveAnalyzer
            
            # Get mode (default 0 if not provided)
            analysis_mode = int(mode) if 'mode' in dir() and mode is not None else 0
            do_autofix = auto_fix if 'auto_fix' in dir() and auto_fix else False
            
            analyzer = GHLiveAnalyzer()
            analyzer.scan_document()
            
            # Mode 0: Quick Check
            if analysis_mode == 0:
                analyzer.run_all_checks()
                score = analyzer.calculate_health_score()
                stats = analyzer.get_statistics()
                
                error_count = sum(i['count'] for i in analyzer.issues if i['severity'] == 'error')
                warning_count = sum(i['count'] for i in analyzer.issues if i['severity'] == 'warning')
                
                a = f"""{'='*50}
🦗 GRASSHOPPER HEALTH CHECK
{'='*50}

📊 Score: {score}/100
🔧 Components: {stats['total_components']}
🔗 Connections: {stats['total_wires']}

⚠️ Issues: {error_count} errors, {warning_count} warnings
Status: {'✅ Good' if score >= 80 else '⚠️ Needs Work' if score >= 60 else '❌ Poor'}
{'='*50}
"""
            
            # Mode 1: Full Analysis
            elif analysis_mode == 1:
                analyzer.run_all_checks()
                score = analyzer.calculate_health_score()
                stats = analyzer.get_statistics()
                
                lines = [
                    "=" * 60,
                    "🦗 FULL ANALYSIS",
                    "=" * 60,
                    "",
                    f"📊 Health Score: {score}/100",
                    "",
                    "📈 Statistics:",
                    f"  Components: {stats['total_components']}",
                    f"  Parameters: {stats['total_params']}",
                    f"  Wires: {stats['total_wires']}",
                    f"  Groups: {stats['total_groups']}",
                    "",
                    "⚠️ Issues Found:",
                ]
                
                if analyzer.issues:
                    for issue in analyzer.issues:
                        severity = issue['severity']
                        icon = "❌" if severity == "error" else "⚠️" if severity == "warning" else "ℹ️"
                        lines.append(f"{icon} {issue['rule']}: {issue['count']}")
                else:
                    lines.append("✅ No issues found!")
                
                lines.append("")
                lines.append("=" * 60)
                a = "\n".join(lines)
            
            # Mode 2: Statistics Only
            elif analysis_mode == 2:
                stats = analyzer.get_statistics()
                
                a = f"""STATISTICS:
Components: {stats['total_components']}
Parameters: {stats['total_params']}
Wires: {stats['total_wires']}
Groups: {stats['total_groups']}
"""
            
            # Mode 3: Find Issues
            elif analysis_mode == 3:
                analyzer.run_all_checks()
                
                lines = ["=== ISSUES FOUND ===", ""]
                
                if analyzer.issues:
                    for issue in analyzer.issues:
                        icon = "❌" if issue['severity'] == "error" else "⚠️"
                        lines.append(f"{icon} {issue['rule']} ({issue['count']})")
                        lines.append(f"   {issue['description']}")
                        if issue.get('examples'):
                            for ex in issue['examples'][:3]:
                                lines.append(f"   • {ex}")
                        lines.append("")
                else:
                    lines.append("✅ No issues found!")
                
                a = "\n".join(lines)
            
            # Mode 4: Auto-Fix
            elif analysis_mode == 4:
                if do_autofix:
                    result = analyzer.auto_fix_parameters()
                    a = f"""AUTO-FIX COMPLETE:
Fixed: {result['fixed']} parameters
Failed: {result['failed']} parameters

Details:
{chr(10).join(result['details'])}
"""
                else:
                    a = "⚠️ Set 'auto_fix' to True to enable auto-fix"
            
            else:
                a = f"❌ Invalid mode: {analysis_mode}. Use 0-4."
        
        except Exception as e:
            a = f"""❌ ERROR:
{str(e)}

Path: {gh_path}

Try:
1. Restart Grasshopper
2. Check file permissions
3. Verify Python compatibility
"""
