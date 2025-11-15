"""
Grasshopper Preview Control - v1.0

Simple preview enable/disable control for all components with exclusion support

@input: path, enable_preview, use_exclusions, exclude_names, trigger
@output: report

Inputs:
- path (str): Path to standalone folder containing gh_live_analyzer.py
- enable_preview (bool): True=Enable all previews, False=Disable all previews
- use_exclusions (bool): True=Apply exclusions, False=Ignore exclusions (optional)
- exclude_names (str): Comma-separated list of component names to exclude (optional)
- trigger (bool): Execute when True

Outputs:
- report (str): Execution report

How It Works:
- Controls each component's individual 'Hidden' property (component-level preview setting)
- When enable_preview=False: Sets Hidden=True for all components (disables preview)
- When enable_preview=True: Sets Hidden=False for all components (enables preview)
- Excluded components maintain their current Hidden state (no changes applied)

Exclusion Feature:
- Excluded components keep their individual preview settings unchanged
- Name matching is case-insensitive (e.g., "unit_boxes" matches "Unit_Boxes")
- Matches both custom names (NickName) and component type names (Name)
- Multiple exclusions: Separate with commas, e.g., "unit_boxes, panel_data, floor_slabs"

Example Usage:
1. Disable all previews EXCEPT "unit_boxes":
   - enable_preview: False
   - use_exclusions: True
   - exclude_names: "unit_boxes"

2. Enable all previews EXCEPT specific components:
   - enable_preview: True
   - use_exclusions: True
   - exclude_names: "unit_boxes, filler_boxes"

Note: For this to work correctly, excluded components should have their individual
preview enabled (right-click component > Preview > Show). The script will skip
changing their Hidden property, so they remain visible regardless of the global setting.
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
- enable_preview (Boolean): True=Enable all, False=Disable all
- trigger (Boolean): Set to True to execute

💡 Use toggle for enable_preview and button for trigger
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
            enable_val = None
            try:
                if 'enable_preview' in dir():
                    enable_val = enable_preview  # type: ignore
            except:
                pass

            use_exclusions_val = False
            try:
                if 'use_exclusions' in dir():
                    use_exclusions_val = bool(use_exclusions)  # type: ignore
            except:
                pass

            exclude_list = []
            try:
                if 'exclude_names' in dir() and exclude_names:  # type: ignore
                    # Handle both string and list inputs
                    if isinstance(exclude_names, list):  # type: ignore
                        exclude_list = [str(name).strip() for name in exclude_names if name]  # type: ignore
                    else:
                        exclude_str = str(exclude_names).strip()  # type: ignore
                        # Remove list brackets if present
                        if exclude_str.startswith('[') and exclude_str.endswith(']'):
                            exclude_str = exclude_str[1:-1]
                        # Remove quotes
                        exclude_str = exclude_str.replace("'", "").replace('"', '')
                        if exclude_str:
                            exclude_list = [name.strip() for name in exclude_str.split(',') if name.strip()]
            except:
                pass

            trigger_val = False
            try:
                if 'trigger' in dir():
                    trigger_val = trigger  # type: ignore
            except:
                pass

            # Execute if triggered
            if trigger_val:
                report_lines = []
                report_lines.append("=" * 60)
                report_lines.append("PREVIEW CONTROL")
                report_lines.append("=" * 60)
                report_lines.append("")

                if enable_val is None:
                    report_lines.append("⚠️ ENABLE_PREVIEW NOT SET")
                    report_lines.append("")
                    report_lines.append("Please connect a Boolean toggle to 'enable_preview' input:")
                    report_lines.append("  • True = Enable all previews")
                    report_lines.append("  • False = Disable all previews")

                else:
                    if enable_val:
                        report_lines.append("🔆 ENABLING ALL PREVIEWS...")
                    else:
                        report_lines.append("🔅 DISABLING ALL PREVIEWS...")

                    # Show exclusion status
                    if use_exclusions_val and exclude_list:
                        report_lines.append(f"   Exclusions: ON - {', '.join(exclude_list)}")
                    elif exclude_list:
                        report_lines.append(f"   Exclusions: OFF (defined but disabled)")
                    report_lines.append("")

                    # Apply preview changes with exclusions
                    affected = 0
                    excluded = 0

                    for comp in analyzer.components:
                        # Get both NickName (user-set) and Name (default type)
                        nick_name = comp.NickName if hasattr(comp, 'NickName') and comp.NickName else ""
                        type_name = comp.Name if hasattr(comp, 'Name') and comp.Name else ""

                        # Check if component should be excluded
                        is_excluded = False
                        if use_exclusions_val and exclude_list:
                            # Case-insensitive comparison with whitespace stripped
                            nick_lower = nick_name.strip().lower()
                            type_lower = type_name.strip().lower()
                            exclude_lower = [e.strip().lower() for e in exclude_list]

                            if nick_lower in exclude_lower or type_lower in exclude_lower:
                                excluded += 1
                                is_excluded = True

                        if not is_excluded:
                            # Apply preview change
                            try:
                                if hasattr(comp, 'Hidden'):
                                    comp.Hidden = not enable_val
                                    affected += 1
                            except:
                                pass

                    report_lines.append(f"✓ Affected: {affected} components")
                    if use_exclusions_val and excluded > 0:
                        report_lines.append(f"○ Excluded: {excluded} components")

                report_lines.append("")
                report_lines.append("=" * 60)
                report = '\n'.join(report_lines)

            else:
                # Show status
                report_lines = []
                report_lines.append("=" * 60)
                report_lines.append("PREVIEW CONTROL v1.0")
                report_lines.append("=" * 60)
                report_lines.append("")
                report_lines.append("📊 STATUS:")
                report_lines.append(f"   Total components: {len(analyzer.components)}")
                report_lines.append("")
                report_lines.append("📋 CURRENT SETTINGS:")

                if enable_val is None:
                    report_lines.append("   Preview: Not configured")
                else:
                    action = "ENABLE ALL" if enable_val else "DISABLE ALL"
                    report_lines.append(f"   Preview: Ready to {action}")

                # Show exclusion configuration
                if use_exclusions_val and exclude_list:
                    report_lines.append(f"   Exclusions: ON - {', '.join(exclude_list)}")
                elif exclude_list:
                    report_lines.append(f"   Exclusions: OFF (defined: {', '.join(exclude_list)})")
                else:
                    report_lines.append("   Exclusions: None defined")

                report_lines.append("")
                report_lines.append("💡 USAGE:")
                report_lines.append("   1. Connect Boolean toggle to 'enable_preview'")
                report_lines.append("   2. Set enable_preview: True (enable) or False (disable)")
                report_lines.append("   3. (Optional) Set use_exclusions: True to enable exclusions")
                report_lines.append("   4. (Optional) Add exclude_names: 'Panel, Slider'")
                report_lines.append("   5. Set trigger to True to execute")
                report_lines.append("")
                report_lines.append("=" * 60)
                report = '\n'.join(report_lines)

        except Exception as e:
            import traceback
            report = f"""❌ PREVIEW CONTROL FAILED: {str(e)}

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
"""

# Ensure report is always set and output
if 'report' not in dir():
    report = "❌ Error: Report variable not initialized"

print(report)
