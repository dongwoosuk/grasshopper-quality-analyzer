"""
Grasshopper Issue Finder - v4.0 (Updated for Unified Analyzer)

Find and highlight components with issues in your definition

Inputs (from Grasshopper):
- path: Text - Path to standalone folder containing gh_live_analyzer.py
- highlight: Boolean - Whether to highlight problematic components (optional)

Outputs:
- a: Detailed issue report with highlighting
"""

import sys
import os

# === PATH INPUT VALIDATION ===
if 'path' not in dir() or not path:  # type: ignore
    a = """❌ PATH REQUIRED!

Please connect 'path' input with your standalone folder location.

Example:
1. Add text panel with: r"C:\\Users\\Soku\\OneDrive - Steinberg Hart\\Desktop\\Source\\RhinoScripts\\src\\gh\\gh_analyzer_release\\standalone"
2. Connect to 'path' input

Optional:
- Connect Boolean Toggle to 'highlight' input to auto-highlight issues
"""
elif not os.path.exists(str(path).strip()):  # type: ignore
    a = f"""❌ PATH NOT FOUND: {path}

Please check:
1. Path exists
2. Spelling is correct  
3. Use raw string format: r"C:\\path\\to\\folder"
"""
else:
    gh_path = str(path).strip()  # type: ignore
    analyzer_file = os.path.join(gh_path, 'gh_live_analyzer.py')
    
    if not os.path.exists(analyzer_file):
        a = f"""❌ gh_live_analyzer.py not found in: {gh_path}

Please ensure gh_live_analyzer.py exists in the specified folder.
"""
    else:
        try:
            # Load the analyzer
            with open(analyzer_file, 'r', encoding='utf-8') as f:
                exec(f.read())
            
            # Create analyzer and run checks
            analyzer = GHLiveAnalyzer()
            analyzer.run_all_checks()
            
            # Build detailed report
            report_lines = ["=== ISSUE FINDER RESULTS ===", ""]
            
            if not analyzer.issues:
                report_lines.append("✅ No issues found! Your definition is clean!")
            else:
                # Group by severity
                errors = [i for i in analyzer.issues if i['severity'] == 'error']
                warnings = [i for i in analyzer.issues if i['severity'] == 'warning']
                info_issues = [i for i in analyzer.issues if i['severity'] == 'info']
                
                # Summary first
                error_count = sum(i['count'] for i in errors)
                warning_count = sum(i['count'] for i in warnings)
                info_count = sum(i['count'] for i in info_issues)
                
                report_lines.append(f"📊 SUMMARY:")
                report_lines.append(f"   ❌ Errors: {error_count}")
                report_lines.append(f"   ⚠️ Warnings: {warning_count}")
                report_lines.append(f"   ℹ️ Info: {info_count}")
                report_lines.append("")
                
                # Detailed breakdown
                if errors:
                    report_lines.append("❌ ERRORS (Fix immediately!):")
                    for issue in errors:
                        report_lines.append(f"  [{issue['rule_id']}] {issue['title']}: {issue['count']} found")
                        for i, item in enumerate(issue['items'][:3], 1):
                            if 'component_name' in item and item['component_name'] != 'ERROR':
                                name = item.get('component_name', 'Unknown')
                                if 'input_name' in item:
                                    report_lines.append(f"    {i}. {name} -> missing input '{item['input_name']}'")
                                elif 'errors' in item:
                                    report_lines.append(f"    {i}. {name}")
                                    for error in item['errors'][:1]:  # Show first error only
                                        report_lines.append(f"       -> {error}")
                                else:
                                    report_lines.append(f"    {i}. {name}")
                            elif 'error' in item:
                                report_lines.append(f"    {i}. Error: {item['error']}")
                        
                        if issue['count'] > 3:
                            report_lines.append(f"    ... and {issue['count'] - 3} more")
                        report_lines.append("")
                
                if warnings:
                    report_lines.append("⚠️ WARNINGS (Should be fixed):")
                    for issue in warnings:
                        report_lines.append(f"  [{issue['rule_id']}] {issue['title']}: {issue['count']} found")
                        for i, item in enumerate(issue['items'][:2], 1):
                            if 'component_name' in item and item['component_name'] != 'ERROR':
                                name = item.get('component_name', 'Unknown')
                                if 'output_name' in item:
                                    report_lines.append(f"    {i}. {name} -> unused output '{item['output_name']}'")
                                elif 'type' in item:
                                    report_lines.append(f"    {i}. {item['type']} ('{item.get('current_name', '')}')")
                                else:
                                    report_lines.append(f"    {i}. {name}")
                        
                        if issue['count'] > 2:
                            report_lines.append(f"    ... and {issue['count'] - 2} more")
                        report_lines.append("")
                
                if info_issues:
                    report_lines.append("ℹ️ INFO (Consider improving):")
                    for issue in info_issues:
                        report_lines.append(f"  [{issue['rule_id']}] {issue['title']}: {issue['count']} found")
                        if 'items' in issue and issue['items']:
                            for item in issue['items'][:1]:
                                if 'message' in item:
                                    report_lines.append(f"    -> {item['message']}")
                        report_lines.append("")
            
            # Check if highlighting is requested
            should_highlight = False
            try:
                if 'highlight' in dir() and highlight:  # type: ignore
                    should_highlight = True
            except:
                pass
            
            if should_highlight and analyzer.issues:
                report_lines.append("🎯 HIGHLIGHTING:")
                
                # Highlight errors first
                error_highlighted = 0
                for issue in analyzer.issues:
                    if issue['severity'] == 'error':
                        try:
                            result = analyzer.highlight_issues(issue['rule_id'])
                            error_highlighted += issue['count']
                        except:
                            pass
                
                if error_highlighted > 0:
                    report_lines.append(f"   ✅ Highlighted {error_highlighted} error components")
                else:
                    report_lines.append("   ⚠️ Could not highlight components")
            
            report_lines.append("")
            report_lines.append("=" * 50)
            
            a = "\n".join(report_lines)
            
        except Exception as e:
            a = f"""❌ ISSUE FINDER FAILED: {str(e)}

This may be due to:
- Document access issues
- Grasshopper version compatibility
- Component analysis problems

Try:
1. Ensure Grasshopper document is open and active
2. Check if definition has circular references
3. Verify gh_live_analyzer.py is not corrupted
"""
