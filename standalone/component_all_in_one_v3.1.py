"""
Grasshopper All-in-One Analyzer - v3.1 (Universal Path Detection)

Complete analysis tool with multiple modes and manual path override

Inputs (ALL OPTIONAL):
- mode: Number (0-4) - Analysis mode (default: 0)
  0 = Quick Check
  1 = Full Analysis
  2 = Statistics Only
  3 = Find Issues
  4 = Auto-Fix
- auto_fix: Boolean - Enable automatic fixes (default: False)
- custom_path: String - Manual path override (optional)
  Example: r"C:\MyFolder\gh_analyzer\standalone"

Outputs:
- a: Main report
- path: Path used (for debugging)
"""

import sys
import os

# === CLEAR CACHE ===
if 'gh_live_analyzer' in sys.modules:
    del sys.modules['gh_live_analyzer']

# === ENHANCED AUTO PATH DETECTION ===
def find_gh_analyzer():
    """
    Searches for gh_live_analyzer.py in common locations
    Priority order:
    1. Script's own directory
    2. Common user paths
    3. System paths
    4. OneDrive pattern search
    """
    username = os.environ.get('USERNAME', '')
    
    # Try script's directory first (if user puts files together)
    try:
        script_dir = os.path.dirname(__file__) if '__file__' in dir() else None
        if script_dir and os.path.exists(os.path.join(script_dir, "gh_live_analyzer.py")):
            return script_dir
    except:
        pass
    
    # Common installation paths (no company-specific paths)
    common_paths = [
        rf"C:\Users\{username}\Desktop\gh_analyzer\standalone",
        rf"C:\Users\{username}\Documents\gh_analyzer\standalone",
        rf"C:\Users\{username}\Downloads\gh_analyzer\standalone",
        rf"C:\Users\{username}\gh_analyzer\standalone",
        r"C:\gh_analyzer\standalone",
        r"C:\GH_Analyzer\standalone",
        r"C:\Tools\gh_analyzer\standalone",
    ]
    
    for path in common_paths:
        if os.path.exists(os.path.join(path, "gh_live_analyzer.py")):
            return path
    
    # OneDrive pattern search (any organization)
    try:
        import glob
        patterns = [
            rf"C:\Users\{username}\OneDrive\Desktop\gh_analyzer\standalone",
            rf"C:\Users\{username}\OneDrive - *\Desktop\gh_analyzer\standalone",
        ]
        for pattern in patterns:
            for match in glob.glob(pattern):
                if os.path.exists(os.path.join(match, "gh_live_analyzer.py")):
                    return match
    except:
        pass
    
    return None

# === PATH RESOLUTION ===
# Check if user provided custom path
if 'custom_path' in dir() and custom_path:
    gh_path = str(custom_path).strip()
    if not os.path.exists(os.path.join(gh_path, "gh_live_analyzer.py")):
        gh_path = None
        error_msg = f"Custom path not found: {custom_path}"
else:
    gh_path = find_gh_analyzer()
    error_msg = None

# Output path for debugging
path = gh_path if gh_path else "NOT FOUND"

# === MAIN CODE ===
if not gh_path:
    error_details = error_msg if error_msg else """
Auto-detection failed. Please provide custom_path input:
1. Add 'custom_path' input to component
2. Connect text panel with your path
3. Example: r"C:\\MyFolder\\gh_analyzer\\standalone"

Or move files to a common location:
- C:\\gh_analyzer\\standalone\\
- C:\\Users\\[YOU]\\Desktop\\gh_analyzer\\standalone\\
"""
    
    a = f"""❌ ERROR: gh_live_analyzer.py not found!

{error_details}

📍 Searched in:
- Desktop
- Documents  
- Downloads
- OneDrive folders

💡 TIP: Use 'custom_path' input for manual override
"""
else:
    # Remove from path if already there
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
📁 Groups: {stats['total_groups']}

⚠️ Issues: {error_count} errors, {warning_count} warnings
Status: {'✅ Excellent' if score >= 90 else '✅ Good' if score >= 80 else '⚠️ Needs Work' if score >= 60 else '❌ Poor'}
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
                    if issue.get('examples'):
                        for ex in issue['examples'][:2]:
                            lines.append(f"    • {ex}")
            else:
                lines.append("✅ No issues found!")
            
            lines.append("")
            lines.append("=" * 60)
            a = "\n".join(lines)
        
        # Mode 2: Statistics Only
        elif analysis_mode == 2:
            stats = analyzer.get_statistics()
            
            a = f"""STATISTICS:
Total Components: {stats['total_components']}
Total Parameters: {stats['total_params']}
Total Wires: {stats['total_wires']}
Total Groups: {stats['total_groups']}
"""
        
        # Mode 3: Find Issues
        elif analysis_mode == 3:
            analyzer.run_all_checks()
            
            lines = ["=== ISSUES FOUND ===", ""]
            
            if analyzer.issues:
                for issue in analyzer.issues:
                    severity = issue['severity']
                    icon = "❌" if severity == "error" else "⚠️" if severity == "warning" else "ℹ️"
                    lines.append(f"{icon} {issue['rule']} ({issue['count']})")
                    lines.append(f"   {issue['description']}")
                    if issue.get('examples'):
                        lines.append("   Examples:")
                        for ex in issue['examples']:
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
                a = "⚠️ Auto-fix disabled. Set 'auto_fix' input to True to enable."
        
        else:
            a = f"❌ Invalid mode: {analysis_mode}. Use 0-4."
    
    except Exception as e:
        a = f"""❌ ERROR:
{str(e)}

Path used: {gh_path}

Try:
1. Check if gh_live_analyzer.py exists
2. Verify Python version compatibility
3. Restart Grasshopper
"""
