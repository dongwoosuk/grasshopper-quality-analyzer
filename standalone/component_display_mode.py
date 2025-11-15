"""
Grasshopper Display Mode Control - v1.0

Control component display mode (Icon/Name/Both)

@input: path, component_name, display_mode, trigger
@output: report

Inputs:
- path (str): Path to standalone folder containing gh_live_analyzer.py
- component_name (str): Name of component to modify
- display_mode (int): 0=Icon only, 1=Name only, 2=Icon+Name (default: 2)
- trigger (bool): Execute when True

Outputs:
- report (str): Execution report
"""

import sys
import os

# === PATH INPUT VALIDATION ===
if 'path' not in dir() or not path:  # type: ignore
    report = """❌ PATH REQUIRED!

Please connect 'path' input with your standalone folder location.

Example:
1. Add text panel with: r"C:\\Users\\Soku\\OneDrive - Steinberg Hart\\Desktop\\Source\\RhinoScripts\\src\\gh\\gh_analyzer_release\\standalone"
2. Connect to 'path' input

Inputs:
- component_name (Text): Name of component (e.g., "Addition", "Python Script")
- display_mode (Integer): 0=Icon, 1=Name, 2=Both (default: 2)
- trigger (Boolean): Set to True to execute

💡 Use text panel for component_name and number slider for display_mode
"""

elif not os.path.exists(str(path).strip()):  # type: ignore
    report = f"""❌ PATH NOT FOUND: {path}

Please check:
1. Path exists
2. Spelling is correct
3. Use raw string format: r"C:\\path\\to\\folder"
"""

else:
    gh_path = str(path).strip()  # type: ignore
    analyzer_file = os.path.join(gh_path, 'gh_live_analyzer.py')

    if not os.path.exists(analyzer_file):
        report = f"""❌ gh_live_analyzer.py not found in: {gh_path}

Please ensure gh_live_analyzer.py exists in the specified folder.
"""

    else:
        try:
            # Load the analyzer
            with open(analyzer_file, 'r', encoding='utf-8') as f:
                exec(f.read())

            # Create analyzer
            analyzer = GHLiveAnalyzer()
            analyzer.scan_document()

            # Get inputs
            comp_name = ""
            try:
                if 'component_name' in dir() and component_name:  # type: ignore
                    comp_name = str(component_name).strip()  # type: ignore
            except:
                pass

            mode_val = 2  # Default: Both
            try:
                if 'display_mode' in dir() and display_mode is not None:  # type: ignore
                    mode_val = int(float(display_mode))  # type: ignore
                    mode_val = max(0, min(2, mode_val))  # Clamp to 0-2
            except:
                pass

            trigger_val = False
            try:
                if 'trigger' in dir():
                    trigger_val = trigger  # type: ignore
            except:
                pass

            mode_names = {
                0: 'Icon only',
                1: 'Name only',
                2: 'Icon + Name'
            }

            # Execute if triggered
            if trigger_val:
                report_lines = []
                report_lines.append("=" * 60)
                report_lines.append("DISPLAY MODE CONTROL")
                report_lines.append("=" * 60)
                report_lines.append("")

                if not comp_name:
                    report_lines.append("⚠️ COMPONENT_NAME NOT SET")
                    report_lines.append("")
                    report_lines.append("Please connect a Text panel to 'component_name' input")
                    report_lines.append("")
                    report_lines.append("Examples:")
                    report_lines.append("  • 'Addition'")
                    report_lines.append("  • 'Python Script'")
                    report_lines.append("  • 'Number Slider'")
                    report_lines.append("")
                    report_lines.append("💡 Use exact component name as it appears in GH")

                else:
                    report_lines.append(f"🎨 SETTING DISPLAY MODE")
                    report_lines.append(f"   Component: '{comp_name}'")
                    report_lines.append(f"   Mode: {mode_val} ({mode_names[mode_val]})")
                    report_lines.append("")

                    try:
                        result = analyzer.set_icon_display_by_name(comp_name, mode_val)
                        report_lines.append(f"Result: {result}")
                    except Exception as e:
                        report_lines.append(f"❌ ERROR: {str(e)}")
                        report_lines.append("")
                        report_lines.append("Possible issues:")
                        report_lines.append("  • Component name not found")
                        report_lines.append("  • Spelling/capitalization mismatch")
                        report_lines.append("  • Component not in current document")

                report_lines.append("")
                report_lines.append("=" * 60)
                report = '\n'.join(report_lines)

            else:
                # Show status
                report_lines = []
                report_lines.append("=" * 60)
                report_lines.append("DISPLAY MODE CONTROL v1.0")
                report_lines.append("=" * 60)
                report_lines.append("")
                report_lines.append("📊 STATUS:")
                report_lines.append(f"   Total components: {len(analyzer.components)}")
                report_lines.append("")
                report_lines.append("📋 CURRENT SETTINGS:")

                if comp_name:
                    report_lines.append(f"   Target: '{comp_name}'")
                    report_lines.append(f"   Mode: {mode_val} ({mode_names[mode_val]})")
                else:
                    report_lines.append("   Target: Not configured")
                    report_lines.append(f"   Mode: {mode_val} ({mode_names[mode_val]})")

                report_lines.append("")
                report_lines.append("💡 USAGE:")
                report_lines.append("   1. Connect Text panel to 'component_name'")
                report_lines.append("   2. Enter exact component name (e.g., 'Addition')")
                report_lines.append("   3. Set display_mode:")
                report_lines.append("      • 0 = Icon only")
                report_lines.append("      • 1 = Name only")
                report_lines.append("      • 2 = Icon + Name (default)")
                report_lines.append("   4. Set trigger to True to execute")
                report_lines.append("")
                report_lines.append("📝 DISPLAY MODES:")
                report_lines.append("   0 (Icon):    Compact, shows only icon")
                report_lines.append("   1 (Name):    Text-only, no icon")
                report_lines.append("   2 (Both):    Full display with icon + name")
                report_lines.append("")
                report_lines.append("=" * 60)
                report = '\n'.join(report_lines)

        except Exception as e:
            import traceback
            report = f"""❌ DISPLAY MODE CONTROL FAILED: {str(e)}

This may be due to:
- Document access issues
- Grasshopper version compatibility
- Component access problems

Traceback:
{traceback.format_exc()}

Try:
1. Ensure Grasshopper document is open and active
2. Check if gh_live_analyzer.py is up to date
3. Verify component has proper permissions
4. Check component name spelling and capitalization
"""

# Ensure report is always set and output
if 'report' not in dir():
    report = "❌ Error: Report variable not initialized"

print(report)
