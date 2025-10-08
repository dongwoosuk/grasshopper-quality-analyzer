"""
Grasshopper Health Check Component - v3.0 (Auto Path + Auto Run)

No inputs needed - runs automatically!

Outputs:
- a: Analysis report
"""

import sys
import os

# === CLEAR CACHE ===
if 'gh_live_analyzer' in sys.modules:
    del sys.modules['gh_live_analyzer']

# === AUTO PATH DETECTION ===
def find_gh_analyzer():
    username = os.environ.get('USERNAME', '')
    
    # Try common paths (most specific first)
    # Support both gh_analyzer and gh_analyzer_release folder names
    common_paths = [
        rf"C:\Users\{username}\OneDrive - Steinberg Hart\Desktop\Source\RhinoScripts\src\gh\gh_analyzer_release\standalone",
        rf"C:\Users\{username}\OneDrive - Steinberg Hart\Desktop\Source\RhinoScripts\src\gh\gh_analyzer\standalone",
        rf"C:\Users\{username}\Desktop\Source\RhinoScripts\src\gh\gh_analyzer_release\standalone",
        rf"C:\Users\{username}\Desktop\Source\RhinoScripts\src\gh\gh_analyzer\standalone",
        rf"C:\Users\{username}\Source\RhinoScripts\src\gh\gh_analyzer_release\standalone",
        rf"C:\Users\{username}\Source\RhinoScripts\src\gh\gh_analyzer\standalone",
        rf"C:\Users\{username}\OneDrive\Desktop\gh_analyzer_release\standalone",
        rf"C:\Users\{username}\OneDrive\Desktop\gh_analyzer\standalone",
        rf"C:\Users\{username}\Desktop\gh_analyzer_release\standalone",
        rf"C:\Users\{username}\Desktop\gh_analyzer\standalone",
        rf"C:\Users\{username}\Documents\gh_analyzer_release\standalone",
        rf"C:\Users\{username}\Documents\gh_analyzer\standalone",
        r"C:\GH_Analyzer\standalone",
        r"C:\gh_analyzer\standalone",
    ]
    
    for path in common_paths:
        if os.path.exists(os.path.join(path, "gh_live_analyzer.py")):
            return path
    
    # Try glob for OneDrive company folders
    try:
        import glob
        patterns = [
            rf"C:\Users\{username}\OneDrive - *\Desktop\Source\RhinoScripts\src\gh\gh_analyzer_release\standalone",
            rf"C:\Users\{username}\OneDrive - *\Desktop\Source\RhinoScripts\src\gh\gh_analyzer\standalone"
        ]
        for pattern in patterns:
            for match in glob.glob(pattern):
                if os.path.exists(os.path.join(match, "gh_live_analyzer.py")):
                    return match
    except:
        pass
    
    return None

gh_path = find_gh_analyzer()

# === MAIN CODE ===
if not gh_path:
    username = os.environ.get('USERNAME', 'Unknown')
    a = f"""ERROR: gh_live_analyzer.py not found!

Current user: {username}

Please place gh_analyzer folder in one of these locations:
  - Desktop\\gh_analyzer\\standalone
  - Documents\\gh_analyzer\\standalone
  - C:\\GH_Analyzer\\standalone

Or use custom path input parameter.
"""
else:
    # Add to path
    if gh_path in sys.path:
        sys.path.remove(gh_path)
    sys.path.insert(0, gh_path)
    
    try:
        from gh_live_analyzer import GHLiveAnalyzer
        
        analyzer = GHLiveAnalyzer()
        analyzer.scan_document()
        analyzer.run_all_checks()
        
        stats = analyzer.get_statistics()
        score = analyzer.calculate_health_score()
        
        # Count issues
        error_count = sum(i['count'] for i in analyzer.issues if i['severity'] == 'error')
        warning_count = sum(i['count'] for i in analyzer.issues if i['severity'] == 'warning')
        info_count = sum(i['count'] for i in analyzer.issues if i['severity'] == 'info')
        
        # Format report
        lines = [
            "=" * 50,
            "🦗 GRASSHOPPER HEALTH CHECK",
            "=" * 50,
            "",
            f"📄 Document: {analyzer.doc.DisplayName}",
            f"📊 Score: {score}/100",
            "",
            "📈 Statistics:",
            f"  Components: {stats['total_components']}",
            f"  Wires: {stats['total_wires']}",
            f"  Groups: {stats['total_groups']}",
            f"  Parameters: {stats.get('total_params', 0)}",
            "",
            "🔍 Issues Found:",
        ]
        
        if error_count > 0:
            lines.append(f"  ❌ Errors: {error_count}")
        if warning_count > 0:
            lines.append(f"  ⚠️  Warnings: {warning_count}")
        if info_count > 0:
            lines.append(f"  ℹ️  Info: {info_count}")
        
        if not analyzer.issues:
            lines.append("  ✅ No issues found!")
        
        lines.extend([
            "",
            "=" * 50,
            f"Status: {'✅ Good' if score >= 80 else '⚠️ Needs Work' if score >= 60 else '❌ Poor'}",
            "=" * 50,
        ])
        
        a = "\n".join(lines)
        
    except Exception as e:
        import traceback
        a = f"ERROR: {str(e)}\n\n{traceback.format_exc()}"
