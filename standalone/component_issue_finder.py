"""
Grasshopper Issue Finder - v3.0 (Auto Path + Auto Run)

Shows detailed list of all issues found

Outputs:
- a: Detailed issue report
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
        
        lines = [
            "=" * 60,
            "🔍 DETAILED ISSUE REPORT",
            "=" * 60,
            ""
        ]
        
        if not analyzer.issues:
            lines.append("✅ No issues found! Perfect definition!")
        else:
            for issue_group in analyzer.issues:
                severity = issue_group['severity']
                icon = "❌" if severity == 'error' else "⚠️" if severity == 'warning' else "ℹ️"
                
                lines.append(f"{icon} [{issue_group['rule_id']}] {issue_group['title']}")
                lines.append(f"   Count: {issue_group['count']} items")
                lines.append("")
                lines.append("   Examples:")
                
                for item in issue_group['items'][:5]:
                    comp_name = item.get('component_name', 'Unknown')
                    lines.append(f"     • {comp_name}")
                    
                    if 'input_name' in item:
                        lines.append(f"       Input: {item['input_name']}")
                    if 'output_name' in item:
                        lines.append(f"       Output: {item['output_name']}")
                    if 'warnings' in item:
                        for w in item['warnings']:
                            lines.append(f"       Warning: {w}")
                    if 'position' in item:
                        pos = item['position']
                        lines.append(f"       Position: ({pos[0]:.0f}, {pos[1]:.0f})")
                
                if issue_group['count'] > 5:
                    lines.append(f"     ... and {issue_group['count'] - 5} more")
                
                lines.append("")
        
        lines.append("=" * 60)
        a = "\n".join(lines)
        
    except Exception as e:
        import traceback
        a = f"ERROR: {str(e)}\n\n{traceback.format_exc()}"
