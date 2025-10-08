"""
Grasshopper All-in-One Analyzer - v3.0 (Auto Path + Flexible)

Complete analysis tool with multiple modes

Inputs (ALL OPTIONAL):
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
            
            a = f"""=== QUICK CHECK ===
Score: {score}/100
Components: {stats['total_components']}
Issues: {error_count} errors, {warning_count} warnings
Status: {'✅ Good' if score >= 80 else '⚠️ Needs Work' if score >= 60 else '❌ Poor'}
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
                f"📊 Score: {score}/100",
                "",
                "📈 Statistics:",
                f"  Components: {stats['total_components']}",
                f"  Wires: {stats['total_wires']}",
                f"  Groups: {stats['total_groups']}",
                "",
                "🔍 Issues:",
            ]
            
            if analyzer.issues:
                for issue_group in analyzer.issues:
                    severity = issue_group['severity']
                    icon = "❌" if severity == 'error' else "⚠️" if severity == 'warning' else "ℹ️"
                    lines.append(f"  {icon} {issue_group['title']}: {issue_group['count']}")
            else:
                lines.append("  ✅ No issues found!")
            
            lines.append("")
            lines.append("=" * 60)
            a = "\n".join(lines)
        
        # Mode 2: Statistics
        elif analysis_mode == 2:
            stats = analyzer.get_statistics()
            
            lines = [
                "=" * 50,
                "📊 STATISTICS",
                "=" * 50,
                "",
                f"Components: {stats['total_components']}",
                f"Wires: {stats['total_wires']}",
                f"Groups: {stats['total_groups']}",
                "",
                "Top Categories:",
            ]
            
            by_category = stats.get('by_category', {})
            for cat, count in sorted(by_category.items(), key=lambda x: x[1], reverse=True)[:10]:
                lines.append(f"  {cat}: {count}")
            
            a = "\n".join(lines)
        
        # Mode 3: Find Issues
        elif analysis_mode == 3:
            analyzer.run_all_checks()
            
            lines = ["=== ISSUES ===", ""]
            
            if not analyzer.issues:
                lines.append("✅ No issues found!")
            else:
                for issue_group in analyzer.issues:
                    severity = issue_group['severity']
                    icon = "❌" if severity == 'error' else "⚠️" if severity == 'warning' else "ℹ️"
                    lines.append(f"{icon} [{issue_group['rule_id']}] {issue_group['title']}: {issue_group['count']}")
            
            a = "\n".join(lines)
        
        # Mode 4: Auto-Fix
        elif analysis_mode == 4:
            analyzer.run_all_checks()
            before_score = analyzer.calculate_health_score()
            
            lines = [
                "=== AUTO-FIX ===",
                f"Before Score: {before_score}/100",
                ""
            ]
            
            if do_autofix:
                # Auto-fix unnamed parameters
                fixed = analyzer.auto_name_parameters()
                lines.append(f"Fixed: {fixed} unnamed parameters")
                
                # Re-analyze
                analyzer.scan_document()
                analyzer.run_all_checks()
                after_score = analyzer.calculate_health_score()
                
                lines.append(f"After Score: {after_score}/100")
                lines.append(f"Improvement: +{after_score - before_score}")
            else:
                lines.append("⚠️ auto_fix is False")
                lines.append("Set auto_fix = True to enable fixes")
            
            a = "\n".join(lines)
        
        else:
            a = f"Invalid mode: {analysis_mode}\nUse 0-4"
        
    except Exception as e:
        import traceback
        a = f"ERROR: {str(e)}\n\n{traceback.format_exc()}"
