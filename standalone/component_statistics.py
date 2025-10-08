"""
Grasshopper Statistics - v3.0 (Auto Path + Auto Run)

Shows document statistics only

Outputs:
- a: Statistics report
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
        stats = analyzer.get_statistics()
        
        lines = [
            "=" * 50,
            "📊 GRASSHOPPER STATISTICS",
            "=" * 50,
            "",
            "Overview:",
            f"  Components: {stats['total_components']}",
            f"  Wires: {stats['total_wires']}",
            f"  Groups: {stats['total_groups']}",
            f"  Parameters: {stats.get('total_params', 0)}",
            "",
            "Top 10 Categories:",
        ]
        
        by_category = stats.get('by_category', {})
        for cat, count in sorted(by_category.items(), key=lambda x: x[1], reverse=True)[:10]:
            lines.append(f"  {cat}: {count}")
        
        lines.append("")
        lines.append("=" * 50)
        
        a = "\n".join(lines)
        
    except Exception as e:
        import traceback
        a = f"ERROR: {str(e)}\n\n{traceback.format_exc()}"
