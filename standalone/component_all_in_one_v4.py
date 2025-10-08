"""
Grasshopper All-in-One Analyzer - v4.0 (Universal Path Detection)

🌍 WORKS ANYWHERE - No hardcoded paths!

Inputs (ALL OPTIONAL):
- mode: Number (0-4) - Analysis mode (default: 0)
  0 = Quick Check
  1 = Full Analysis  
  2 = Statistics Only
  3 = Find Issues
  4 = Auto-Fix
- auto_fix: Boolean - Enable automatic fixes (default: False)
- lib_path: Text - Custom path to gh_live_analyzer.py folder (optional)

Outputs:
- a: Main report
"""

import sys
import os
from pathlib import Path

# === CLEAR CACHE ===
if 'gh_live_analyzer' in sys.modules:
    del sys.modules['gh_live_analyzer']

# === UNIVERSAL PATH DETECTION ===
def find_gh_analyzer_universal():
    """
    Try multiple methods to find gh_live_analyzer.py
    Returns: Path to the folder containing gh_live_analyzer.py, or None
    """
    
    # Method 1: Check if lib_path was provided by user
    if 'lib_path' in dir() and lib_path:
        user_path = Path(lib_path)
        if (user_path / "gh_live_analyzer.py").exists():
            return user_path
    
    # Method 2: Check config file (if previously set up)
    try:
        config_file = Path.home() / ".gh_analyzer_config"
        if config_file.exists():
            saved_path = Path(config_file.read_text().strip())
            if (saved_path / "gh_live_analyzer.py").exists():
                return saved_path
    except:
        pass
    
    # Method 3: Search from common user locations
    username = os.environ.get('USERNAME', '')
    
    # Search patterns (more flexible)
    search_roots = []
    
    if username:
        user_home = Path.home()
        search_roots.extend([
            user_home / "Desktop",
            user_home / "Documents", 
            user_home / "OneDrive",
        ])
        
        # Check all OneDrive folders (OneDrive - Company Name)
        try:
            for onedrive_folder in user_home.glob("OneDrive*"):
                if onedrive_folder.is_dir():
                    search_roots.append(onedrive_folder / "Desktop")
                    search_roots.append(onedrive_folder / "Documents")
        except:
            pass
    
    # Add system-wide locations
    search_roots.extend([
        Path("C:/GH_Analyzer"),
        Path("C:/gh_analyzer"),
    ])
    
    # Search for the file in all roots
    for root in search_roots:
        if not root.exists():
            continue
        
        # Try direct path first
        direct_path = root / "gh_analyzer" / "standalone"
        if (direct_path / "gh_live_analyzer.py").exists():
            return direct_path
        
        # Try Source/RhinoScripts structure
        source_path = root / "Source" / "RhinoScripts" / "src" / "gh" / "gh_analyzer" / "standalone"
        if (source_path / "gh_live_analyzer.py").exists():
            return source_path
        
        # Try recursive search (up to 3 levels deep)
        try:
            for py_file in root.rglob("gh_live_analyzer.py"):
                if "standalone" in str(py_file.parent):
                    return py_file.parent
        except:
            pass
    
    return None

# === MAIN CODE ===
gh_path = find_gh_analyzer_universal()

if not gh_path:
    a = """❌ ERROR: gh_live_analyzer.py not found!

🔍 Search Methods Tried:
  1. Custom lib_path input
  2. Saved config file
  3. Common user folders
  4. Recursive search

💡 Solutions:
  A. Provide lib_path input with folder containing gh_live_analyzer.py
  B. Place gh_live_analyzer.py in one of these locations:
     - Desktop/gh_analyzer/standalone/
     - Documents/gh_analyzer/standalone/
     - C:/gh_analyzer/standalone/
  C. Use the standalone version (copy entire gh_live_analyzer.py code)

📁 Current search included:
  - Desktop folders
  - OneDrive folders  
  - Documents folders
  - C:/ root folders
"""
else:
    # Save path to config for next time
    try:
        config_file = Path.home() / ".gh_analyzer_config"
        config_file.write_text(str(gh_path))
    except:
        pass
    
    # Add to Python path
    if str(gh_path) in sys.path:
        sys.path.remove(str(gh_path))
    sys.path.insert(0, str(gh_path))
    
    try:
        from gh_live_analyzer import GHLiveAnalyzer
        
        # Get mode (default 0 if not provided)
        analysis_mode = int(mode) if 'mode' in dir() and mode is not None else 0
        do_autofix = auto_fix if 'auto_fix' in dir() and auto_fix else False
        
        analyzer = GHLiveAnalyzer()
        analyzer.scan_document()
        
        # === ANALYSIS MODES (same as v3) ===
        
        # Mode 0: Quick Check
        if analysis_mode == 0:
            analyzer.run_all_checks()
            score = analyzer.calculate_health_score()
            stats = analyzer.get_statistics()
            
            error_count = sum(i['count'] for i in analyzer.issues if i['severity'] == 'error')
            warning_count = sum(i['count'] for i in analyzer.issues if i['severity'] == 'warning')
            
            status_emoji = '✅' if score >= 80 else '⚠️' if score >= 60 else '❌'
            
            a = f"""=== QUICK CHECK ===
{status_emoji} Score: {score}/100
📦 Components: {stats['total_components']}
🔗 Wires: {stats['total_wires']}
📁 Groups: {stats['total_groups']}

🔍 Issues: {error_count} errors, {warning_count} warnings

📍 Library: {gh_path.name}/
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
                f"  Wires: {stats['total_wires']}",
                f"  Groups: {stats['total_groups']}",
                "",
                "🔧 Component Categories:",
            ]
            
            by_category = stats.get('by_category', {})
            for cat, count in sorted(by_category.items(), key=lambda x: x[1], reverse=True)[:5]:
                lines.append(f"  • {cat}: {count}")
            
            lines.append("")
            lines.append("🔍 Issues Found:")
            
            if analyzer.issues:
                for issue_group in analyzer.issues:
                    severity = issue_group['severity']
                    icon = "❌" if severity == 'error' else "⚠️" if severity == 'warning' else "ℹ️"
                    lines.append(f"  {icon} {issue_group['title']}: {issue_group['count']}")
            else:
                lines.append("  ✅ No issues found!")
            
            lines.append("")
            lines.append(f"📍 Library: {gh_path}")
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
                f"📦 Components: {stats['total_components']}",
                f"🔗 Wires: {stats['total_wires']}",
                f"📁 Groups: {stats['total_groups']}",
                "",
                "🔧 Top Categories:",
            ]
            
            by_category = stats.get('by_category', {})
            for cat, count in sorted(by_category.items(), key=lambda x: x[1], reverse=True)[:10]:
                lines.append(f"  {cat}: {count}")
            
            lines.append("")
            
            param_types = stats.get('param_types', {})
            if param_types:
                lines.append("🎛️ Parameters:")
                for ptype, count in sorted(param_types.items(), key=lambda x: x[1], reverse=True):
                    lines.append(f"  {ptype}: {count}")
            
            a = "\n".join(lines)
        
        # Mode 3: Find Issues
        elif analysis_mode == 3:
            analyzer.run_all_checks()
            
            lines = ["=" * 50, "🔍 ISSUES FOUND", "=" * 50, ""]
            
            if not analyzer.issues:
                lines.append("✅ No issues found!")
            else:
                for issue_group in analyzer.issues:
                    severity = issue_group['severity']
                    icon = "❌" if severity == 'error' else "⚠️" if severity == 'warning' else "ℹ️"
                    lines.append(f"{icon} [{issue_group['rule_id']}] {issue_group['title']}")
                    lines.append(f"   Count: {issue_group['count']}")
                    lines.append("")
            
            a = "\n".join(lines)
        
        # Mode 4: Auto-Fix
        elif analysis_mode == 4:
            analyzer.run_all_checks()
            before_score = analyzer.calculate_health_score()
            
            lines = [
                "=" * 50,
                "🔧 AUTO-FIX",
                "=" * 50,
                f"📊 Before Score: {before_score}/100",
                ""
            ]
            
            if do_autofix:
                # Auto-fix unnamed parameters
                result = analyzer.auto_name_parameters()
                lines.append(f"✅ {result}")
                
                # Re-analyze
                analyzer.scan_document()
                analyzer.run_all_checks()
                after_score = analyzer.calculate_health_score()
                
                lines.append(f"📊 After Score: {after_score}/100")
                improvement = after_score - before_score
                lines.append(f"📈 Improvement: {'+' if improvement >= 0 else ''}{improvement} points")
            else:
                lines.append("⚠️  auto_fix is set to False")
                lines.append("")
                lines.append("To enable fixes:")
                lines.append("  1. Set auto_fix input to True")
                lines.append("  2. Re-run component")
            
            a = "\n".join(lines)
        
        else:
            a = f"❌ Invalid mode: {analysis_mode}\n\nValid modes: 0-4"
        
    except Exception as e:
        import traceback
        a = f"""❌ ERROR:
{str(e)}

Stack Trace:
{traceback.format_exc()}

📍 Library Path: {gh_path}
"""
