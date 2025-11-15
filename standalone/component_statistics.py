"""
Grasshopper Statistics - v4.0 (Updated for Unified Analyzer)

Get detailed statistics about your Grasshopper definition

Inputs (from Grasshopper):
- path: Text - Path to standalone folder containing gh_live_analyzer.py

Outputs:
- a: Statistics report
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

💡 Use 'r' prefix for Windows paths
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
            
            # Create analyzer and get statistics
            analyzer = GHLiveAnalyzer()
            stats = analyzer.get_statistics()
            
            # Build statistics report
            report_lines = []
            report_lines.append("=" * 50)
            report_lines.append("GRASSHOPPER DEFINITION STATISTICS")
            report_lines.append("=" * 50)
            report_lines.append("")
            
            # Basic counts
            report_lines.append("📊 BASIC COUNTS:")
            report_lines.append(f"   Total Components: {stats['total_components']}")
            report_lines.append(f"   Total Connections: {stats['total_wires']}")
            report_lines.append(f"   Total Groups: {stats['total_groups']}")
            report_lines.append("")
            
            # Component breakdown by category
            if stats['by_category']:
                report_lines.append("🔧 COMPONENTS BY CATEGORY:")
                sorted_categories = sorted(stats['by_category'].items(), key=lambda x: x[1], reverse=True)
                for category, count in sorted_categories:
                    if category and category != 'Unknown':
                        percentage = (count / stats['total_components']) * 100 if stats['total_components'] > 0 else 0
                        report_lines.append(f"   {category}: {count} ({percentage:.1f}%)")
                
                if 'Unknown' in stats['by_category']:
                    count = stats['by_category']['Unknown']
                    percentage = (count / stats['total_components']) * 100 if stats['total_components'] > 0 else 0
                    report_lines.append(f"   Unknown: {count} ({percentage:.1f}%)")
                report_lines.append("")
            
            # Parameter types
            if stats['param_types']:
                report_lines.append("🎛️ PARAMETER TYPES:")
                sorted_params = sorted(stats['param_types'].items(), key=lambda x: x[1], reverse=True)
                for param_type, count in sorted_params:
                    report_lines.append(f"   {param_type}: {count}")
                report_lines.append("")
            
            # Component exposure levels
            if stats['by_exposure']:
                report_lines.append("👁️ COMPONENT EXPOSURE:")
                exposure_order = ['primary', 'secondary', 'tertiary', 'quarternary', 'quinary', 'senary', 'septenary', 'obscure', 'hidden']
                
                for exposure in exposure_order:
                    if exposure in stats['by_exposure']:
                        count = stats['by_exposure'][exposure]
                        report_lines.append(f"   {exposure.title()}: {count}")
                
                # Add any other exposure levels not in the standard order
                for exposure, count in stats['by_exposure'].items():
                    if exposure.lower() not in exposure_order and exposure != 'Unknown':
                        report_lines.append(f"   {exposure}: {count}")
                
                if 'Unknown' in stats['by_exposure']:
                    report_lines.append(f"   Unknown: {stats['by_exposure']['Unknown']}")
                report_lines.append("")
            
            # Calculate some ratios and insights
            report_lines.append("🔍 INSIGHTS:")
            
            if stats['total_components'] > 0:
                wires_per_component = stats['total_wires'] / stats['total_components']
                report_lines.append(f"   Connections per Component: {wires_per_component:.1f}")
                
                if stats['total_groups'] > 0:
                    components_per_group = stats['total_components'] / stats['total_groups']
                    report_lines.append(f"   Components per Group: {components_per_group:.1f}")
                else:
                    report_lines.append("   Components per Group: No groups found")
                
                # Definition complexity assessment
                if stats['total_components'] < 10:
                    complexity = "Simple"
                elif stats['total_components'] < 50:
                    complexity = "Medium"
                elif stats['total_components'] < 150:
                    complexity = "Complex"
                else:
                    complexity = "Very Complex"
                
                report_lines.append(f"   Definition Complexity: {complexity}")
                
                # Organization assessment
                if stats['total_groups'] == 0 and stats['total_components'] > 20:
                    organization = "Poor (No groups)"
                elif stats['total_groups'] > 0:
                    if components_per_group < 15:
                        organization = "Good"
                    else:
                        organization = "Could be improved"
                else:
                    organization = "Good"
                
                report_lines.append(f"   Organization: {organization}")
            
            report_lines.append("")
            
            # Scan errors if any
            if stats.get('scan_error'):
                report_lines.append("⚠️ SCAN WARNINGS:")
                report_lines.append(f"   {stats['scan_error']}")
                report_lines.append("")
            
            report_lines.append("=" * 50)
            
            a = "\n".join(report_lines)
            
        except Exception as e:
            a = f"""❌ STATISTICS FAILED: {str(e)}

This may be due to:
- Document access issues
- Grasshopper version compatibility
- Component scanning problems

Try:
1. Ensure Grasshopper document is open and active
2. Test with Health Check component first
3. Check if definition has circular references
4. Verify all components are functioning properly
"""
