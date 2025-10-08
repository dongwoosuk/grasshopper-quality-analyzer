"""
Grasshopper Auto-Fix - v3.0 (Auto Path + Auto Run)

Automatically fixes common issues

Outputs:
- a: Fix report
"""

import sys
import os

# === CLEAR CACHE ===
if 'gh_live_analyzer' in sys.modules:
    del sys.modules['gh_live_analyzer']

# === AUTO PATH DETECTION ===
def find_gh_analyzer():
    username = os.environ.get('USERNAME', '')
    
    common_paths = [
        rf"C:\Users\{username}\OneDrive - Steinberg Hart\Desktop\Source\RhinoScripts\src\gh\gh_analyzer\standalone",
        rf"C:\Users\{username}\Desktop\Source\RhinoScripts\src\gh\gh_analyzer\standalone",
        rf"C:\Users\{username}\Source\RhinoScripts\src\gh\gh_analyzer\standalone",
        rf"C:\Users\{username}\OneDrive\Desktop\gh_analyzer\standalone",
        rf"C:\Users\{username}\Desktop\gh_analyzer\standalone",
        rf"C:\Users\{username}\Documents\gh_analyzer\standalone",
        r"C:\GH_Analyzer\standalone",
        r"C:\gh_analyzer\standalone",
    ]
    
    for path in common_paths:
        if os.path.exists(os.path.join(path, "gh_live_analyzer.py")):
            return path
    
    try:
        import glob
        pattern = rf"C:\Users\{username}\OneDrive - *\Desktop\Source\RhinoScripts\src\gh\gh_analyzer\standalone"
        for match in glob.glob(pattern):
            if os.path.exists(os.path.join(match, "gh_live_analyzer.py")):
                return match
    except:
        pass
    
    return None

gh_path = find_gh_analyzer()

# === MAIN CODE ===
if not gh_path:
    a = "ERROR: gh_live_analyzer.py not found!\n\nPlease check installation."
else:
    if gh_path in sys.path:
        sys.path.remove(gh_path)
    sys.path.insert(0, gh_path)
    
    try:
        from gh_live_analyzer import GHLiveAnalyzer
        
        analyzer = GHLiveAnalyzer()
        analyzer.scan_document()
        analyzer.run_all_checks()
        
        before_score = analyzer.calculate_health_score()
        before_issues = len(analyzer.issues)
        
        lines = [
            "=" * 50,
            "🔧 AUTO-FIX",
            "=" * 50,
            "",
            f"Before Score: {before_score}/100",
            f"Issues: {before_issues}",
            "",
            "Applying fixes...",
            ""
        ]
        
        # Auto-name unnamed parameters
        fixed_params = analyzer.auto_name_parameters()
        lines.append(f"✓ Named {fixed_params} parameters")
        
        # Re-analyze
        analyzer.scan_document()
        analyzer.run_all_checks()
        after_score = analyzer.calculate_health_score()
        after_issues = len(analyzer.issues)
        
        lines.extend([
            "",
            "=" * 50,
            f"After Score: {after_score}/100",
            f"Issues: {after_issues}",
            f"Improvement: +{after_score - before_score} points",
            "=" * 50,
        ])
        
        a = "\n".join(lines)
        
    except Exception as e:
        import traceback
        a = f"ERROR: {str(e)}\n\n{traceback.format_exc()}"
