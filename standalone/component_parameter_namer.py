"""
Grasshopper Parameter Namer - v1.0 (Type-selective naming)

Automatically name parameter components with customizable options

Inputs (from Grasshopper):
- path: Text - Path to standalone folder containing gh_live_analyzer.py
- prefix: Text - Prefix for parameter names (optional, default: 'Param')
- types: Number/Text - Which types to rename (optional, default: all)
         Accepts:
         • Integer Slider: 0, 1, 2, or 3
         • Text Panel: "0", "1,2", "0,1,2,3"
         • Multiple Sliders: List of numbers
         • Empty = all types
         Type codes:
         0 = Panel
         1 = Number Slider
         2 = Boolean Toggle
         3 = Value List
- run_fix: Boolean - Execute naming (connect Button/Toggle)
- reset: Boolean - Reset parameter names (connect Button/Toggle)

Outputs:
- a: Results and preview
"""

import sys
import os

# === PATH INPUT VALIDATION ===
if 'path' not in dir() or not path:  # type: ignore
    a = """❌ PATH REQUIRED!

Please connect 'path' input with your standalone folder location.

Example:
r"C:\\Users\\Soku\\OneDrive - Steinberg Hart\\Desktop\\Source\\RhinoScripts\\src\\gh\\gh_analyzer_release\\standalone"

Optional inputs:
- prefix: Text for parameter naming (default: 'Param')
- types: Which parameter types to rename
  • Integer Slider with value 0-3
  • Text Panel: "0", "1", "1,2", etc.
  • Multiple Sliders as list
  • Empty = All types
  Type codes:
  0 = Panel, 1 = Number Slider, 2 = Boolean Toggle, 3 = Value List
- run_fix: Boolean to execute naming
- reset: Boolean to reset names
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
            
            # Check if reset should run
            should_reset = False
            try:
                if 'reset' in dir() and reset:  # type: ignore
                    should_reset = True
            except:
                pass
            
            # Check if naming should run
            should_run_fix = False
            try:
                if 'run_fix' in dir() and run_fix:  # type: ignore
                    should_run_fix = True
            except:
                pass
            
            # Get prefix for parameter naming
            param_prefix = 'Param'
            try:
                if 'prefix' in dir() and prefix:  # type: ignore
                    param_prefix = str(prefix).strip()  # type: ignore
                    if not param_prefix:
                        param_prefix = 'Param'
            except:
                pass
            
            # Parse types input - support multiple formats
            target_types = None  # None means all types
            type_names_display = "All types"
            try:
                if 'types' in dir() and types is not None:  # type: ignore
                    # Handle different input types
                    parsed_types = []
                    
                    # Case 1: Integer slider (single value)
                    if isinstance(types, int):  # type: ignore
                        if 0 <= types <= 3:  # type: ignore
                            parsed_types = [types]  # type: ignore
                    
                    # Case 2: List from multiple sliders or data tree
                    elif hasattr(types, '__iter__') and not isinstance(types, str):  # type: ignore
                        for item in types:  # type: ignore
                            if isinstance(item, (int, float)):
                                num = int(item)
                                if 0 <= num <= 3:
                                    parsed_types.append(num)
                    
                    # Case 3: String "0,1,2,3" or "0" (text panel)
                    elif isinstance(types, str):  # type: ignore
                        types_str = str(types).strip()  # type: ignore
                        if types_str:
                            for t in types_str.split(','):
                                t = t.strip()
                                if t.replace('.', '').isdigit():  # Handle float strings
                                    num = int(float(t))
                                    if 0 <= num <= 3:
                                        parsed_types.append(num)
                    
                    # Case 4: Single float/number
                    elif isinstance(types, float):  # type: ignore
                        num = int(types)  # type: ignore
                        if 0 <= num <= 3:
                            parsed_types = [num]
                    
                    # Remove duplicates and sort
                    if parsed_types:
                        parsed_types = sorted(list(set(parsed_types)))
                        target_types = parsed_types
                        # Create display names
                        type_map = {
                            0: 'Panel',
                            1: 'Number Slider',
                            2: 'Boolean Toggle',
                            3: 'Value List'
                        }
                        type_names_display = ', '.join([type_map[t] for t in parsed_types])
            except Exception as e:
                # If parsing fails, default to all types
                pass
            
            # Create analyzer
            analyzer = GHLiveAnalyzer()
            
            # RESET MODE (takes priority)
            if should_reset:
                report_lines = []
                report_lines.append("🔄 PARAMETER NAME RESET")
                report_lines.append("=" * 50)
                report_lines.append("")
                
                try:
                    reset_result = analyzer.reset_parameter_names(reset_all=False)
                    
                    report_lines.append("✅ RESET COMPLETE")
                    report_lines.append(f"   {reset_result}")
                    report_lines.append("")
                    report_lines.append("📋 What was reset:")
                    report_lines.append("   • Pattern: [prefix]_[number] (e.g., Param_01, Soku_01)")
                    report_lines.append("   • Number Sliders/Panels → Empty (unnamed)")
                    report_lines.append("   • Boolean Toggles → 'Toggle'")
                    report_lines.append("")
                    report_lines.append("💡 You can now re-run with different settings!")
                    
                except Exception as e:
                    report_lines.append(f"❌ RESET FAILED: {str(e)}")
                
                report_lines.append("")
                report_lines.append("=" * 50)
                
                a = "\\n".join(report_lines)
                
            elif not should_run_fix:
                # PREVIEW MODE
                unnamed_params = analyzer.check_unnamed_parameters()
                
                report_lines = []
                report_lines.append("🏷️ PARAMETER NAMER - PREVIEW")
                report_lines.append("=" * 50)
                report_lines.append("")
                report_lines.append("📝 Current Settings:")
                report_lines.append(f"   • Prefix: '{param_prefix}'")
                report_lines.append(f"   • Target types: {type_names_display}")
                report_lines.append("")
                
                if unnamed_params:
                    valid_params = [p for p in unnamed_params if 'type' in p and p.get('type') != 'ERROR']
                    
                    if valid_params:
                        # Filter by type if specified
                        if target_types is not None:
                            type_map_reverse = {
                                'GH_Panel': 0,
                                'GH_NumberSlider': 1,
                                'GH_BooleanToggle': 2,
                                'GH_ValueList': 3
                            }
                            filtered_params = []
                            for p in valid_params:
                                p_type = p.get('type', '')
                                type_num = type_map_reverse.get(p_type, -1)
                                if type_num in target_types:
                                    filtered_params.append(p)
                            
                            report_lines.append(f"🎯 WILL BE RENAMED ({len(filtered_params)} of {len(valid_params)} found):")
                        else:
                            filtered_params = valid_params
                            report_lines.append(f"🎯 WILL BE RENAMED ({len(filtered_params)} found):")
                        
                        report_lines.append("")
                        
                        if filtered_params:
                            for i, param in enumerate(filtered_params[:10], 1):
                                current_name = param.get('current_name', 'Unknown')
                                param_type = param.get('type', 'Unknown')
                                new_name = f"{param_prefix}_{i:02d}"
                                
                                if not current_name or current_name == param_type:
                                    current_name = f"[{param_type}]"
                                
                                type_display = param_type.replace('GH_', '')
                                report_lines.append(f"   {i:2d}. {type_display}: '{current_name}' → '{new_name}'")
                            
                            if len(filtered_params) > 10:
                                report_lines.append(f"       ... and {len(filtered_params) - 10} more")
                            
                            report_lines.append("")
                            report_lines.append("💡 Naming pattern:")
                            report_lines.append(f"   {param_prefix}_01, {param_prefix}_02, {param_prefix}_03, ...")
                        else:
                            report_lines.append("   ℹ️ No parameters match the selected types")
                            if target_types:
                                report_lines.append(f"   Try different types or leave 'types' empty for all")
                        
                        # Show what will be skipped
                        if target_types and len(filtered_params) < len(valid_params):
                            skipped_count = len(valid_params) - len(filtered_params)
                            report_lines.append("")
                            report_lines.append(f"⏭️ WILL BE SKIPPED ({skipped_count} parameters):")
                            report_lines.append(f"   Other types not in selection")
                    else:
                        report_lines.append("❓ NO PARAMETERS FOUND")
                else:
                    report_lines.append("✅ NO PARAMETERS NEED RENAMING")
                    report_lines.append("   All parameters already have custom names!")
                
                report_lines.append("")
                report_lines.append("🚀 TO EXECUTE:")
                report_lines.append("   Connect Boolean Toggle/Button to 'run_fix' and activate")
                report_lines.append("")
                report_lines.append("🔄 TO RESET:")
                report_lines.append("   Connect Boolean Toggle/Button to 'reset' and activate")
                report_lines.append("")
                report_lines.append("⚙️ TYPE OPTIONS:")
                report_lines.append("   Use Integer Slider (0-3) or Text Panel:")
                report_lines.append("   0 = Panel")
                report_lines.append("   1 = Number Slider")
                report_lines.append("   2 = Boolean Toggle")
                report_lines.append("   3 = Value List")
                report_lines.append("   Examples:")
                report_lines.append("   • Slider set to 1 (sliders only)")
                report_lines.append("   • Text Panel: '0,1' (panels + sliders)")
                report_lines.append("   • Multiple sliders: [0, 1] as list")
                
                a = "\\n".join(report_lines)
                
            else:
                # EXECUTION MODE
                report_lines = []
                report_lines.append("🏷️ PARAMETER NAMER - EXECUTION")
                report_lines.append("=" * 50)
                report_lines.append("")
                report_lines.append("📝 Settings:")
                report_lines.append(f"   • Prefix: '{param_prefix}'")
                report_lines.append(f"   • Target types: {type_names_display}")
                report_lines.append("")
                
                try:
                    # Execute naming
                    rename_result = analyzer.auto_name_parameters(param_prefix, target_types)
                    
                    report_lines.append("✅ NAMING COMPLETE")
                    report_lines.append(f"   {rename_result}")
                    report_lines.append("")
                    
                    # Extract count
                    renamed_count = 0
                    skipped_count = 0
                    if "Named" in rename_result:
                        try:
                            parts = rename_result.split()
                            for i, part in enumerate(parts):
                                if part.isdigit():
                                    if i > 0 and parts[i-1] == "Named":
                                        renamed_count = int(part)
                                    elif "skipped" in rename_result and i > 0 and parts[i-1] == "skipped":
                                        skipped_count = int(part)
                        except:
                            pass
                    
                    if renamed_count > 0:
                        report_lines.append("📊 RESULTS:")
                        report_lines.append(f"   • Successfully renamed: {renamed_count}")
                        if skipped_count > 0:
                            report_lines.append(f"   • Skipped (other types): {skipped_count}")
                        report_lines.append(f"   • Naming pattern: {param_prefix}_01, {param_prefix}_02, ...")
                        report_lines.append("")
                        report_lines.append("🎯 NEXT STEPS:")
                        report_lines.append("   1. Check the renamed parameters")
                        report_lines.append("   2. Run Health Check to see improvement")
                        report_lines.append("   3. Use 'reset' if you want to undo")
                    else:
                        report_lines.append("ℹ️ No parameters were renamed")
                        if target_types:
                            report_lines.append("   • Check if selected types exist in definition")
                            report_lines.append("   • Try different type selection")
                    
                except Exception as e:
                    report_lines.append(f"❌ NAMING FAILED: {str(e)}")
                
                report_lines.append("")
                report_lines.append("=" * 50)
                
                a = "\\n".join(report_lines)
                
        except Exception as e:
            a = f"""❌ PARAMETER NAMER FAILED: {str(e)}

Possible causes:
- Document access issues
- Component modification restrictions
- Invalid type selection

Try:
1. Check if document is open and not locked
2. Verify type input format (e.g., "0,1,2,3")
3. Test with Health Check component first
"""
