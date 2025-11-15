"""
Test Script with Force Reload - v3.0

Tests GH Live Analyzer with automatic path detection

Outputs:
- a: Test result
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

# === MAIN TEST ===
if not gh_path:
    username = os.environ.get('USERNAME', 'Unknown')
    a = f"""❌ ERROR: gh_live_analyzer.py not found!

Current user: {username}

Please place gh_analyzer in one of these locations:
  - Desktop\\gh_analyzer\\standalone
  - Documents\\gh_analyzer\\standalone
  - C:\\GH_Analyzer\\standalone
"""
else:
    if gh_path in sys.path:
        sys.path.remove(gh_path)
    sys.path.insert(0, gh_path)
    
    try:
        from gh_live_analyzer import GHLiveAnalyzer
        
        analyzer = GHLiveAnalyzer()
        analyzer.scan_document()
        stats = analyzer.get_statistics()
        analyzer.run_all_checks()
        score = analyzer.calculate_health_score()
        
        lines = [
            "=" * 50,
            "✅ GH LIVE ANALYZER TEST",
            "=" * 50,
            "",
            "Connection: SUCCESS ✓",
            "Module: Loaded ✓",
            "Cache: Cleared ✓",
            "",
            f"Path: {gh_path}",
            f"User: {os.environ.get('USERNAME')}",
            "",
            f"Document: {analyzer.doc.DisplayName}",
            f"Components: {stats['total_components']}",
            f"Wires: {stats['total_wires']}",
            f"Groups: {stats['total_groups']}",
            "",
            f"Health Score: {score}/100",
            f"Issues Found: {len(analyzer.issues)}",
            "",
            "=" * 50,
            "✅ Test completed successfully! 🎉",
            "",
            "Ready to use all components!",
            "=" * 50
        ]
        
        a = "\n".join(lines)
        
    except Exception as e:
        import traceback
        a = f"ERROR: {str(e)}\n\nPath: {gh_path}\n\n{traceback.format_exc()}"
