"""
Quick Test Script - GH Live Analyzer
Copy this into a Grasshopper Python component to test basic functionality

Inputs:
- x: Button (press to test)

Outputs:
- a: Test result (str)
"""

import sys

# IMPORTANT: Change this path to your actual standalone folder location
gh_path = r"C:\Users\Soku\OneDrive - Steinberg Hart\Desktop\Source\RhinoScripts\src\gh\standalone"

if gh_path not in sys.path:
    sys.path.insert(0, gh_path)

try:
    from gh_live_analyzer import GHLiveAnalyzer
    
    if x:
        # Create analyzer
        analyzer = GHLiveAnalyzer()
        
        # Run quick test
        analyzer.scan_document()
        stats = analyzer.get_statistics()
        analyzer.run_all_checks()
        score = analyzer.calculate_health_score()
        
        # Format result
        result = [
            "=" * 40,
            "✅ GH LIVE ANALYZER TEST",
            "=" * 40,
            "",
            "Connection: SUCCESS ✓",
            "",
            f"Document: {analyzer.doc.DisplayName}",
            f"Components: {stats['total_components']}",
            f"Wires: {stats['total_wires']}",
            f"Groups: {stats['total_groups']}",
            "",
            f"Health Score: {score}/100",
            f"Issues Found: {len(analyzer.issues)}",
            "",
            "=" * 40,
            "Test completed successfully! 🎉",
            "",
            "You can now use:",
            "- component_all_in_one.py",
            "- component_health_check.py",
            "- component_issue_finder.py",
            "- component_auto_fix.py",
            "- component_statistics.py",
            "=" * 40
        ]
        
        a = "\n".join(result)
    else:
        a = "Press button to test GH Live Analyzer"

except ImportError as e:
    a = f"""
ERROR: Cannot import gh_live_analyzer

Problem: {str(e)}

Fix:
1. Check the path in the script:
   gh_path = r"YOUR_ACTUAL_PATH"

2. Make sure gh_live_analyzer.py exists at that location

3. Current path trying:
   {gh_path}
"""

except Exception as e:
    import traceback
    a = f"""
ERROR: {str(e)}

Full traceback:
{traceback.format_exc()}
"""
