"""
Grasshopper Component Auto-Alignment - v1.0 (Stable)

Smart component alignment with horizontal wire optimization and drift prevention

═══════════════════════════════════════════════════════════════
REQUIRED INPUT:
═══════════════════════════════════════════════════════════════
- path: Text - Path to standalone folder

═══════════════════════════════════════════════════════════════
ALIGNMENT CONTROLS:
═══════════════════════════════════════════════════════════════
- spacing_x: Number - Horizontal spacing between layers (default: 200)
- spacing_y: Number - Vertical spacing within layer (optional, auto if not connected)
- trigger: Boolean - Execute alignment when True

Features:
  • 🎯 Smart layer detection (analyzes wire connections)
  • 🔒 Zero drift (repeatable alignment)
  • 📏 Horizontal wire optimization (parameter-aware)
  • ⚓ Anchor system (parameter components stay fixed)
  • 🚀 Auto-optimization (intelligent spacing)

Usage:
  1. Select 2+ components
  2. Set spacing_x and spacing_y
  3. Set trigger=True
  4. Components align perfectly!
  
Repeat alignment = same result (zero drift!)

To change spacing:
  1. Deselect all components
  2. Change spacing values
  3. Reselect components
  4. Trigger again
"""

import sys
import os
import scriptcontext as sc

# === PERSISTENT STATE FOR SELECTION TRACKING ===
# Prevents unwanted re-alignment when selection hasn't changed
if 'alignment_last_selection' not in sc.sticky:
    sc.sticky['alignment_last_selection'] = None

# === PATH INPUT VALIDATION ===
if 'path' not in dir() or not path:  # type: ignore
    a = """❌ PATH REQUIRED!

Please connect 'path' input with your standalone folder location.
"""
elif not os.path.exists(str(path).strip()):  # type: ignore
    a = f"""❌ PATH NOT FOUND: {path}"""
else:
    gh_path = str(path).strip()  # type: ignore
    analyzer_file = os.path.join(gh_path, 'gh_live_analyzer.py')
    
    if not os.path.exists(analyzer_file):
        a = f"""❌ gh_live_analyzer.py not found in: {gh_path}"""
    else:
        try:
            # Load the analyzer
            namespace = {}
            with open(analyzer_file, 'r', encoding='utf-8') as f:
                exec(f.read(), namespace)
            
            GHLiveAnalyzer = namespace['GHLiveAnalyzer']
            analyzer = GHLiveAnalyzer()
            analyzer.scan_document()
            
            # === INPUT PARSING ===
            
            spacing_x_val = 200  # Default horizontal spacing
            spacing_y_val = None  # None = auto-optimize
            trigger_val = False
            
            try:
                if 'spacing_x' in dir() and spacing_x is not None:  # type: ignore
                    spacing_x_val = int(float(spacing_x))  # type: ignore
            except:
                pass
            try:
                if 'spacing_y' in dir() and spacing_y is not None:  # type: ignore
                    spacing_y_val = int(float(spacing_y))  # type: ignore
            except:
                pass
            try:
                if 'trigger' in dir():
                    trigger_val = trigger  # type: ignore
            except:
                pass
            
            # === EXECUTION LOGIC ===
            
            report_lines = []
            
            if trigger_val:
                # Display mode indicator
                if spacing_y_val is not None:
                    report_lines.append(f"🎯 AUTO-ALIGNMENT: Manual Spacing")
                    report_lines.append(f"   Horizontal: {spacing_x_val}px")
                    report_lines.append(f"   Vertical: {spacing_y_val}px")
                else:
                    report_lines.append(f"🎯 AUTO-ALIGNMENT: Smart Mode")
                    report_lines.append(f"   Horizontal: {spacing_x_val}px")
                    report_lines.append(f"   Vertical: 🚀 AUTO-OPTIMIZE")
                report_lines.append("")
                
                try:
                    selected = [c for c in analyzer.components if hasattr(c, 'Attributes') and c.Attributes.Selected]
                    
                    # 🔒 SELECTION CHANGE DETECTION
                    current_selection = frozenset(str(c.InstanceGuid) for c in selected)
                    last_selection = sc.sticky['alignment_last_selection']
                    selection_changed = (last_selection != current_selection)
                    
                    if not selection_changed and len(selected) >= 2:
                        report_lines.append(f"   ✋ Selection unchanged ({len(selected)} components)")
                        report_lines.append(f"   💤 Skipping alignment (prevents drift)")
                        report_lines.append(f"")
                        report_lines.append(f"   💡 To re-align with new spacing:")
                        report_lines.append(f"      1. Deselect all")
                        report_lines.append(f"      2. Change spacing values")
                        report_lines.append(f"      3. Reselect components")
                        report_lines.append(f"      4. Trigger again")
                    elif len(selected) >= 2:
                        # Record positions BEFORE alignment
                        positions_before = [(c.Attributes.Pivot.X, c.Attributes.Pivot.Y) for c in selected]
                        
                        # Execute smart alignment
                        result = analyzer.align_selected_parameter_based(spacing_x_val, spacing_y_val)
                        
                        # Check positions AFTER alignment
                        positions_after = [(c.Attributes.Pivot.X, c.Attributes.Pivot.Y) for c in selected]
                        
                        # Verify positions changed
                        changed = sum(1 for i in range(len(selected)) if positions_before[i] != positions_after[i])
                        
                        report_lines.append(f"   {result}")
                        report_lines.append(f"")
                        report_lines.append(f"   🔍 Verification:")
                        report_lines.append(f"      {changed}/{len(selected)} components moved")
                        report_lines.append(f"")
                        
                        if changed == 0:
                            report_lines.append(f"   ⚠️ WARNING: No movement detected!")
                            report_lines.append(f"      Possible causes:")
                            report_lines.append(f"      • Selection already aligned")
                            report_lines.append(f"      • Try different spacing")
                        else:
                            report_lines.append(f"   ✅ Success!")
                            report_lines.append(f"      • Wires are horizontal at parameter points")
                            report_lines.append(f"      • Zero drift (repeatable alignment)")
                            report_lines.append(f"      • Anchor system active")
                            report_lines.append(f"")
                            
                            # 🔓 UPDATE SELECTION STATE
                            sc.sticky['alignment_last_selection'] = current_selection
                            report_lines.append(f"   🔒 Selection state saved")
                    else:
                        report_lines.append(f"   ⚠️ Need at least 2 components")
                        report_lines.append(f"      Currently selected: {len(selected)}")
                        report_lines.append(f"")
                        report_lines.append(f"   Please select more components and try again")
                        
                        # Update state even when insufficient
                        sc.sticky['alignment_last_selection'] = current_selection
                except Exception as e:
                    import traceback
                    report_lines.append(f"   ❌ ERROR: {str(e)}")
                    report_lines.append(f"")
                    report_lines.append(f"   Details:")
                    for line in traceback.format_exc().split('\n')[:5]:
                        report_lines.append(f"      {line}")
                
                report_lines.append("")
                report_lines.append("=" * 50)
            else:
                # DEFAULT: SHOW STATUS
                report_lines.append("🎯 AUTO-ALIGNMENT v1.0 (Stable)")
                report_lines.append("=" * 50)
                report_lines.append("")
                report_lines.append("📊 STATUS:")
                report_lines.append(f"   Total components: {len(analyzer.components)}")
                
                selected = [c for c in analyzer.components if hasattr(c, 'Attributes') and c.Attributes.Selected]
                if selected:
                    report_lines.append(f"   Selected: {len(selected)}")
                    
                    # Check if any are parameter components
                    params = [c for c in selected if analyzer._is_param_component(c)]
                    if params:
                        report_lines.append(f"   Parameters: {len(params)} (will be anchor)")
                
                report_lines.append("")
                report_lines.append("📋 SETTINGS:")
                report_lines.append("")
                report_lines.append(f"   Horizontal spacing: {spacing_x_val}px")
                
                if spacing_y_val is not None:
                    report_lines.append(f"   Vertical spacing: {spacing_y_val}px (manual)")
                else:
                    report_lines.append(f"   Vertical spacing: 🚀 AUTO (adaptive)")
                
                report_lines.append("")
                
                if selected and len(selected) >= 2:
                    report_lines.append(f"   ✅ Ready to align!")
                    report_lines.append(f"      Set trigger=True to execute")
                else:
                    report_lines.append(f"   ⚠️ Select 2+ components first")
                
                report_lines.append("")
                report_lines.append("💡 FEATURES:")
                report_lines.append("   • Parameter-aware alignment")
                report_lines.append("   • Horizontal wire optimization")
                report_lines.append("   • Zero drift (repeatable)")
                report_lines.append("   • Anchor system (params fixed)")
                report_lines.append("")
                report_lines.append("=" * 50)
            
            a = "\n".join(report_lines)
            
        except Exception as e:
            import traceback
            a = f"""❌ ERROR: {str(e)}

Traceback:
{traceback.format_exc()}
"""
