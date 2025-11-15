"""
Grasshopper Live Analyzer - Standalone Version (v1.1.0 - ZERO DRIFT!)
Analyzes the current open GH definition without requiring external tools
For use directly in Grasshopper Python components

Author: Soku
Version: 1.1.0 - TRUE Idempotency! Real-time offset calculation (no stored positions)
"""

import Grasshopper as gh
import Grasshopper.Kernel as ghk
import scriptcontext as sc
import System
from System import Guid


class GHLiveAnalyzer:
    """
    Real-time analyzer for Grasshopper definitions
    Works with the currently active document
    """
    
    def __init__(self, gh_doc=None):
        """Initialize with optional GH document"""
        try:
            if gh_doc:
                self.doc = gh_doc
            else:
                # Use ActiveCanvas (we know this works now)
                if hasattr(gh.Instances, 'ActiveCanvas') and gh.Instances.ActiveCanvas:
                    self.doc = gh.Instances.ActiveCanvas.Document
                else:
                    raise Exception("No Grasshopper document found")
            
            if not self.doc:
                raise Exception("No active Grasshopper document found!")
            
            self.components = []
            self.wires = []
            self.groups = []
            self.issues = []
            
        except Exception as e:
            raise Exception("Failed to initialize analyzer: " + str(e))
        
    def scan_document(self):
        """Scan the current document and collect all objects (CORRECTED SCANNING)"""
        try:
            self.components = []
            self.wires = []
            self.groups = []
            
            # Use the WORKING approach from debugging
            if self.doc and hasattr(self.doc, 'Objects'):
                for obj in self.doc.Objects:
                    try:
                        # Get the actual type name (this is the key fix!)
                        full_type = obj.GetType().FullName
                        
                        # All objects with InstanceGuid are components
                        if hasattr(obj, 'InstanceGuid'):
                            self.components.append(obj)
                        
                        # Check for groups
                        if 'Group' in full_type:
                            self.groups.append(obj)
                            
                    except Exception as e:
                        continue
            
            # Count wires safely
            wire_count = 0
            try:
                for comp in self.components:
                    if hasattr(comp, 'Params') and hasattr(comp.Params, 'Output'):
                        for param in comp.Params.Output:
                            if hasattr(param, 'Recipients'):
                                wire_count += param.Recipients.Count
            except:
                pass
            
            return {
                'components': len(self.components),
                'wires': wire_count,
                'groups': len(self.groups)
            }
            
        except Exception as e:
            return {
                'components': 0,
                'wires': 0,
                'groups': 0,
                'error': str(e)
            }
    
    def get_statistics(self):
        """Get document statistics"""
        # Ensure document is scanned
        if not self.components:
            self.scan_document()
        stats = self.scan_document()
        
        # Count by category
        by_category = {}
        by_exposure = {}
        param_types = {}
        
        try:
            for comp in self.components:
                # Category (safer approach)
                try:
                    cat = str(comp.Category) if hasattr(comp, 'Category') else 'Unknown'
                    by_category[cat] = by_category.get(cat, 0) + 1
                except:
                    by_category['Unknown'] = by_category.get('Unknown', 0) + 1
                
                # Exposure (safer approach)
                try:
                    exp = str(comp.Exposure) if hasattr(comp, 'Exposure') else 'Unknown'
                    by_exposure[exp] = by_exposure.get(exp, 0) + 1
                except:
                    by_exposure['Unknown'] = by_exposure.get('Unknown', 0) + 1
                
                # Parameter types (safer approach)
                try:
                    if self._is_param_component(comp):
                        type_name = comp.GetType().Name
                        param_types[type_name] = param_types.get(type_name, 0) + 1
                except:
                    continue
        except:
            pass
        
        return {
            'total_components': stats.get('components', 0),
            'total_wires': stats.get('wires', 0),
            'total_groups': stats.get('groups', 0),
            'by_category': by_category,
            'by_exposure': by_exposure,
            'param_types': param_types,
            'scan_error': stats.get('error')
        }
    
    def _is_param_component(self, comp):
        """Check if component is a parameter (WORKING method from debug)"""
        try:
            # Use the same approach that worked in debugging
            full_type = comp.GetType().FullName
            
            # Check for parameter component patterns
            param_patterns = [
                'NumberSlider', 'Panel', 'BooleanToggle', 'ValueList',
                'GH_NumberSlider', 'GH_Panel', 'GH_BooleanToggle', 'GH_ValueList'
            ]
            
            for pattern in param_patterns:
                if pattern in full_type:
                    return True
                    
            return False
        except:
            return False
    
    # ==================== LINT CHECKS ====================
    
    def check_dangling_inputs(self):
        """GH001: Find inputs that are not connected"""
        issues = []
        
        try:
            for comp in self.components:
                try:
                    if hasattr(comp, 'Params') and hasattr(comp.Params, 'Input'):
                        for param in comp.Params.Input:
                            try:
                                if hasattr(param, 'SourceCount') and hasattr(param, 'Optional'):
                                    if param.SourceCount == 0 and not param.Optional:
                                        pos = [0, 0]
                                        try:
                                            if hasattr(comp, 'Attributes') and hasattr(comp.Attributes, 'Pivot'):
                                                pos = [comp.Attributes.Pivot.X, comp.Attributes.Pivot.Y]
                                        except:
                                            pass
                                        
                                        issues.append({
                                            'component_name': getattr(comp, 'Name', 'Unknown'),
                                            'component_guid': str(getattr(comp, 'InstanceGuid', Guid.Empty)),
                                            'input_name': getattr(param, 'Name', 'Unknown'),
                                            'position': pos,
                                            'component': comp
                                        })
                            except:
                                continue
                except:
                    continue
        except Exception as e:
            issues.append({
                'component_name': 'ERROR',
                'error': "Failed to check dangling inputs: " + str(e)
            })
        
        return issues
    
    def check_dangling_outputs(self):
        """GH002: Find outputs that are not connected"""
        issues = []
        
        try:
            for comp in self.components:
                try:
                    if hasattr(comp, 'Params') and hasattr(comp.Params, 'Output'):
                        for param in comp.Params.Output:
                            try:
                                if hasattr(param, 'Recipients') and param.Recipients.Count == 0:
                                    pos = [0, 0]
                                    try:
                                        if hasattr(comp, 'Attributes') and hasattr(comp.Attributes, 'Pivot'):
                                            pos = [comp.Attributes.Pivot.X, comp.Attributes.Pivot.Y]
                                    except:
                                        pass
                                    
                                    issues.append({
                                        'component_name': getattr(comp, 'Name', 'Unknown'),
                                        'component_guid': str(getattr(comp, 'InstanceGuid', Guid.Empty)),
                                        'output_name': getattr(param, 'Name', 'Unknown'),
                                        'position': pos,
                                        'component': comp
                                    })
                            except:
                                continue
                except:
                    continue
        except Exception as e:
            issues.append({
                'component_name': 'ERROR', 
                'error': "Failed to check dangling outputs: " + str(e)
            })
        
        return issues
    
    def check_unnamed_parameters(self):
        """GH003: Find parameters without custom names (WORKING VERSION)"""
        issues = []
        default_names = ['Number Slider', 'Panel', 'Boolean Toggle', 'Value List', 'Slider', 'Toggle']
        
        try:
            for comp in self.components:
                try:
                    if self._is_param_component(comp):
                        nickname = getattr(comp, 'NickName', '')
                        name = getattr(comp, 'Name', '')
                        
                        # Use the WORKING logic from debugging
                        needs_rename = (
                            not nickname or           # Empty string or None
                            nickname == '' or         # Explicitly empty
                            nickname == name or       # Same as default name
                            nickname in default_names or  # In default list
                            nickname.startswith('Number Slider') or
                            nickname.startswith('Panel') or
                            nickname.startswith('Boolean Toggle') or
                            nickname.startswith('Value List')
                        )
                        
                        if needs_rename:
                            pos = [0, 0]
                            try:
                                if hasattr(comp, 'Attributes') and hasattr(comp.Attributes, 'Pivot'):
                                    pos = [comp.Attributes.Pivot.X, comp.Attributes.Pivot.Y]
                            except:
                                pass
                            
                            issues.append({
                                'type': comp.GetType().Name,
                                'current_name': nickname if nickname else '[Empty]',
                                'guid': str(getattr(comp, 'InstanceGuid', Guid.Empty)),
                                'position': pos,
                                'component': comp
                            })
                except:
                    continue
        except Exception as e:
            issues.append({
                'type': 'ERROR',
                'error': "Failed to check unnamed parameters: " + str(e)
            })
        
        return issues
    
    def check_disabled_components(self):
        """Find components that are disabled"""
        issues = []
        
        try:
            for comp in self.components:
                try:
                    if hasattr(comp, 'Locked') and comp.Locked:
                        pos = [0, 0]
                        try:
                            if hasattr(comp, 'Attributes') and hasattr(comp.Attributes, 'Pivot'):
                                pos = [comp.Attributes.Pivot.X, comp.Attributes.Pivot.Y]
                        except:
                            pass
                        
                        issues.append({
                            'component_name': getattr(comp, 'Name', 'Unknown'),
                            'guid': str(getattr(comp, 'InstanceGuid', Guid.Empty)),
                            'position': pos,
                            'component': comp
                        })
                except:
                    continue
        except Exception as e:
            issues.append({
                'component_name': 'ERROR',
                'error': "Failed to check disabled components: " + str(e)
            })
        
        return issues
    
    def check_components_with_errors(self):
        """Find components with runtime errors"""
        issues = []
        
        try:
            for comp in self.components:
                try:
                    if hasattr(comp, 'RuntimeMessageLevel'):
                        if str(comp.RuntimeMessageLevel) == 'Error':
                            messages = []
                            try:
                                if hasattr(comp, 'RuntimeMessages'):
                                    for msg in comp.RuntimeMessages(ghk.GH_RuntimeMessageLevel.Error):
                                        messages.append(str(msg))
                            except:
                                messages = ['Error detected but message unavailable']
                            
                            pos = [0, 0]
                            try:
                                if hasattr(comp, 'Attributes') and hasattr(comp.Attributes, 'Pivot'):
                                    pos = [comp.Attributes.Pivot.X, comp.Attributes.Pivot.Y]
                            except:
                                pass
                            
                            issues.append({
                                'component_name': getattr(comp, 'Name', 'Unknown'),
                                'guid': str(getattr(comp, 'InstanceGuid', Guid.Empty)),
                                'errors': messages,
                                'position': pos,
                                'component': comp
                            })
                except:
                    continue
        except Exception as e:
            issues.append({
                'component_name': 'ERROR',
                'error': "Failed to check component errors: " + str(e)
            })
        
        return issues
    
    def check_components_with_warnings(self):
        """Find components with runtime warnings"""
        issues = []
        
        try:
            for comp in self.components:
                try:
                    if hasattr(comp, 'RuntimeMessageLevel'):
                        if str(comp.RuntimeMessageLevel) == 'Warning':
                            messages = []
                            try:
                                if hasattr(comp, 'RuntimeMessages'):
                                    for msg in comp.RuntimeMessages(ghk.GH_RuntimeMessageLevel.Warning):
                                        messages.append(str(msg))
                            except:
                                messages = ['Warning detected but message unavailable']
                            
                            pos = [0, 0]
                            try:
                                if hasattr(comp, 'Attributes') and hasattr(comp.Attributes, 'Pivot'):
                                    pos = [comp.Attributes.Pivot.X, comp.Attributes.Pivot.Y]
                            except:
                                pass
                            
                            issues.append({
                                'component_name': getattr(comp, 'Name', 'Unknown'),
                                'guid': str(getattr(comp, 'InstanceGuid', Guid.Empty)),
                                'warnings': messages,
                                'position': pos,
                                'component': comp
                            })
                except:
                    continue
        except Exception as e:
            issues.append({
                'component_name': 'ERROR',
                'error': "Failed to check component warnings: " + str(e)
            })
        
        return issues
    
    def check_missing_groups(self):
        """GH004: Check if definition needs organization"""
        try:
            if len(self.components) > 10 and len(self.groups) == 0:
                return [{
                    'message': "Definition has " + str(len(self.components)) + " components but no groups",
                    'recommendation': "Consider organizing into logical groups"
                }]
        except:
            return [{
                'message': "Could not check group organization",
                'recommendation': "Manual check required"
            }]
        return []
    
    def check_preview_disabled(self):
        """GH012: Find components with preview disabled"""
        issues = []
        
        try:
            for comp in self.components:
                try:
                    if hasattr(comp, 'Hidden') and comp.Hidden:
                        pos = [0, 0]
                        try:
                            if hasattr(comp, 'Attributes') and hasattr(comp.Attributes, 'Pivot'):
                                pos = [comp.Attributes.Pivot.X, comp.Attributes.Pivot.Y]
                        except:
                            pass
                        
                        issues.append({
                            'component_name': getattr(comp, 'Name', 'Unknown'),
                            'guid': str(getattr(comp, 'InstanceGuid', Guid.Empty)),
                            'position': pos,
                            'component': comp
                        })
                except:
                    continue
        except Exception as e:
            issues.append({
                'component_name': 'ERROR',
                'error': "Failed to check preview disabled: " + str(e)
            })
        
        return issues
    
    def run_all_checks(self):
        """Run all lint checks and return results"""
        # CRITICAL: Scan document first!
        self.scan_document()
        self.issues = []
        
        checks = [
            ('GH001', 'error', 'Dangling Inputs', self.check_dangling_inputs),
            ('GH002', 'warning', 'Dangling Outputs', self.check_dangling_outputs),
            ('GH003', 'warning', 'Unnamed Parameters', self.check_unnamed_parameters),
            ('GH004', 'info', 'Missing Groups', self.check_missing_groups),
            ('GHRT1', 'error', 'Runtime Errors', self.check_components_with_errors),
            ('GHRT2', 'warning', 'Runtime Warnings', self.check_components_with_warnings),
            ('GH012', 'info', 'Preview Disabled', self.check_preview_disabled),
        ]
        
        for rule_id, severity, title, check_func in checks:
            try:
                results = check_func()
                if results:
                    self.issues.append({
                        'rule_id': rule_id,
                        'severity': severity,
                        'title': title,
                        'count': len(results),
                        'items': results
                    })
            except Exception as e:
                self.issues.append({
                    'rule_id': rule_id,
                    'severity': 'error',
                    'title': title + " (Check Failed)",
                    'count': 1,
                    'items': [{'error': str(e)}]
                })
        
        return self.issues
    
    def calculate_health_score(self):
        """Calculate definition health score (0-100)"""
        try:
            if not self.issues:
                self.run_all_checks()
            
            score = 100
            
            for issue in self.issues:
                if issue['severity'] == 'error':
                    score -= issue['count'] * 10
                elif issue['severity'] == 'warning':
                    score -= issue['count'] * 5
                elif issue['severity'] == 'info':
                    score -= issue['count'] * 2
            
            return max(0, score)
        except:
            return 50  # Default score if calculation fails
    
    def format_report(self, style='full'):
        """
        Format analysis report
        style: 'full', 'compact', 'simple'
        """
        try:
            if not self.issues:
                self.run_all_checks()
            
            if style == 'simple':
                return self._format_simple_report()
            elif style == 'compact':
                return self._format_compact_report()
            else:
                return self._format_full_report()
        except Exception as e:
            return "Report generation failed: " + str(e)
    
    def _format_simple_report(self):
        """Simple one-liner report"""
        try:
            stats = self.get_statistics()
            score = self.calculate_health_score()
            
            error_count = sum(1 for i in self.issues if i['severity'] == 'error')
            warning_count = sum(1 for i in self.issues if i['severity'] == 'warning')
            
            if score >= 90:
                status = "Excellent"
            elif score >= 70:
                status = "Good"
            elif score >= 50:
                status = "Needs Attention"
            else:
                status = "Critical"
            
            return status + " | Score: " + str(score) + "/100 | Components: " + str(stats['total_components']) + " | Errors: " + str(error_count) + " | Warnings: " + str(warning_count)
        except Exception as e:
            return "Simple report failed: " + str(e)
    
    def _format_compact_report(self):
        """Compact report for panel display"""
        lines = []
        try:
            stats = self.get_statistics()
            score = self.calculate_health_score()
            
            lines.append("=" * 50)
            lines.append("GRASSHOPPER HEALTH CHECK")
            lines.append("=" * 50)
            lines.append("")
            lines.append("Score: " + str(score) + "/100")
            lines.append("Components: " + str(stats['total_components']))
            lines.append("Connections: " + str(stats['total_wires']))
            lines.append("Groups: " + str(stats['total_groups']))
            
            if stats.get('scan_error'):
                lines.append("Scan Warning: " + str(stats['scan_error']))
            
            lines.append("")
            
            if not self.issues:
                lines.append("No issues found!")
            else:
                lines.append("Found " + str(len(self.issues)) + " issue types:")
                lines.append("")
                
                for issue in self.issues:
                    icon = {'error': 'ERROR', 'warning': 'WARNING', 'info': 'INFO'}.get(issue['severity'], '•')
                    lines.append(icon + " " + issue['title'] + ": " + str(issue['count']))
            
            lines.append("")
            lines.append("=" * 50)
            
        except Exception as e:
            lines = ["Compact report failed: " + str(e)]
        
        return "\n".join(lines)
    
    def _format_full_report(self):
        """Full detailed report"""
        lines = []
        
        try:
            stats = self.get_statistics()
            score = self.calculate_health_score()
            
            lines.append("=" * 60)
            lines.append("GRASSHOPPER DEFINITION ANALYSIS")
            lines.append("=" * 60)
            lines.append("")
            
            # Header
            doc_name = "Unknown"
            try:
                doc_name = self.doc.DisplayName if hasattr(self.doc, 'DisplayName') else "Unknown"
            except:
                pass
            
            lines.append("Document: " + doc_name)
            lines.append("Health Score: " + str(score) + "/100")
            lines.append("")
            
            # Statistics
            lines.append("Statistics:")
            lines.append("   Components: " + str(stats['total_components']))
            lines.append("   Connections: " + str(stats['total_wires']))
            lines.append("   Groups: " + str(stats['total_groups']))
            
            if stats.get('scan_error'):
                lines.append("   Scan Warning: " + str(stats['scan_error']))
            
            lines.append("")
            
            # Component breakdown
            if stats['by_category']:
                lines.append("Components by Category:")
                for cat, count in sorted(stats['by_category'].items(), key=lambda x: x[1], reverse=True)[:5]:
                    lines.append("   " + cat + ": " + str(count))
                lines.append("")
            
            # Issues
            if not self.issues:
                lines.append("No issues found! Great work!")
            else:
                lines.append("Found " + str(len(self.issues)) + " issue types:")
                lines.append("")
                
                for issue in self.issues:
                    icon = {'error': 'ERROR', 'warning': 'WARNING', 'info': 'INFO'}.get(issue['severity'], '•')
                    
                    lines.append(icon + " " + issue['rule_id'] + ": " + issue['title'] + " [" + issue['severity'].upper() + "]")
                    lines.append("   Count: " + str(issue['count']))
                    
                    # Show examples
                    for item in issue['items'][:3]:
                        try:
                            if 'component_name' in item and item['component_name'] != 'ERROR':
                                name = item.get('component_name', 'Unknown')
                                if 'input_name' in item:
                                    lines.append("   • " + name + " -> input '" + item['input_name'] + "'")
                                elif 'output_name' in item:
                                    lines.append("   • " + name + " -> output '" + item['output_name'] + "'")
                                else:
                                    lines.append("   • " + name)
                            elif 'type' in item:
                                lines.append("   • " + item['type'] + " ('" + item.get('current_name', '') + "')")
                            elif 'message' in item:
                                lines.append("   • " + item['message'])
                            elif 'error' in item:
                                lines.append("   • Error: " + item['error'])
                        except:
                            lines.append("   • [Display error]")
                    
                    if issue['count'] > 3:
                        lines.append("   ... and " + str(issue['count'] - 3) + " more")
                    
                    lines.append("")
            
            # Summary
            error_count = sum(1 for i in self.issues if i['severity'] == 'error')
            warning_count = sum(1 for i in self.issues if i['severity'] == 'warning')
            info_count = sum(1 for i in self.issues if i['severity'] == 'info')
            
            lines.append("Summary:")
            lines.append("   Errors: " + str(error_count))
            lines.append("   Warnings: " + str(warning_count))
            lines.append("   Info: " + str(info_count))
            lines.append("")
            lines.append("=" * 60)
            
        except Exception as e:
            lines = [
                "=" * 60,
                "GRASSHOPPER DEFINITION ANALYSIS - ERROR",
                "=" * 60,
                "",
                "Analysis failed: " + str(e),
                "",
                "This may be due to:",
                "- Document access issues",
                "- Grasshopper version compatibility",
                "- Component type recognition problems",
                "",
                "Try using the Health Check component instead.",
                "=" * 60
            ]
        
        return "\n".join(lines)
    
    # ==================== AUTO-FIX FUNCTIONS ====================
    
    def highlight_issues(self, issue_type=None):
        """Select components with issues in the canvas"""
        try:
            # Ensure document is scanned and checked
            if not self.components:
                self.scan_document()
            if not self.issues:
                self.run_all_checks()
            
            # Deselect all first
            if hasattr(self.doc, 'DeselectAll'):
                self.doc.DeselectAll()
            
            count = 0
            # Select components with issues
            for issue in self.issues:
                if issue_type and issue['rule_id'] != issue_type:
                    continue
                
                for item in issue['items']:
                    try:
                        if 'component' in item and hasattr(item['component'], 'Attributes'):
                            comp = item['component']
                            comp.Attributes.Selected = True
                            count += 1
                    except:
                        continue
            
            if hasattr(self.doc, 'Canvas') and hasattr(self.doc.Canvas, 'Refresh'):
                self.doc.Canvas.Refresh()
            
            return "Highlighted " + str(count) + " components with issues"
        except Exception as e:
            return "Highlight failed: " + str(e)
    
    def auto_name_parameters(self, prefix="Param", target_types=None):
        """Automatically name unnamed parameters
        
        Args:
            prefix: Prefix for naming (default: 'Param')
            target_types: List of types to rename. Options:
                         - None or empty: rename all types
                         - List of integers: [0]=Panel, [1]=NumberSlider, [2]=BooleanToggle, [3]=ValueList
                         - Example: [0, 1] = only Panel and NumberSlider
        """
        try:
            # Ensure document is scanned
            if not self.components:
                self.scan_document()
            
            # Type mapping
            type_map = {
                0: 'Panel',
                1: 'NumberSlider',
                2: 'BooleanToggle',
                3: 'ValueList'
            }
            
            # Get target type names
            target_type_names = None
            if target_types is not None and len(target_types) > 0:
                target_type_names = [type_map.get(t) for t in target_types if t in type_map]
            
            unnamed = self.check_unnamed_parameters()
            
            counter = 1
            renamed = 0
            skipped = 0
            
            for item in unnamed:
                try:
                    if 'component' in item and hasattr(item['component'], 'NickName'):
                        comp = item['component']
                        
                        # Check if this component type should be renamed
                        if target_type_names is not None:
                            comp_type = comp.GetType().FullName
                            should_rename = False
                            
                            for type_name in target_type_names:
                                if type_name in comp_type:
                                    should_rename = True
                                    break
                            
                            if not should_rename:
                                skipped += 1
                                continue
                        
                        new_name = prefix + "_" + str(counter).zfill(2)
                        comp.NickName = new_name
                        counter += 1
                        renamed += 1
                except:
                    continue
            
            if renamed > 0:
                try:
                    if hasattr(self.doc, 'NewSolution'):
                        self.doc.NewSolution(False)
                except:
                    pass
            
            result = "Named " + str(renamed) + " parameters"
            if skipped > 0:
                result += " (skipped " + str(skipped) + " other types)"
            
            return result
        except Exception as e:
            return "Auto-naming failed: " + str(e)
    
    def reset_parameter_names(self, reset_all=False):
        """Reset parameter names to empty (unnamed state)
        
        Args:
            reset_all: If True, reset ALL parameters. If False, only reset those with prefix pattern (e.g., 'Param_01')
        """
        try:
            # Ensure document is scanned
            if not self.components:
                self.scan_document()
            
            reset_count = 0
            
            for comp in self.components:
                try:
                    if self._is_param_component(comp):
                        nickname = getattr(comp, 'NickName', '')
                        
                        # Decide whether to reset this parameter
                        should_reset = False
                        
                        if reset_all:
                            # Reset all parameters except those already empty
                            should_reset = nickname and nickname != ''
                        else:
                            # Only reset parameters that look like auto-generated names
                            # Pattern: [prefix]_[number] like "Param_01", "Soku_01", etc.
                            if nickname and '_' in nickname:
                                parts = nickname.rsplit('_', 1)
                                if len(parts) == 2:
                                    prefix_part, num_part = parts
                                    # Check if number part is all digits
                                    if num_part.isdigit():
                                        should_reset = True
                        
                        if should_reset:
                            # Special handling for Boolean Toggle - reset to "Toggle"
                            comp_type = comp.GetType().FullName
                            if 'BooleanToggle' in comp_type or 'Toggle' in comp_type:
                                comp.NickName = 'Toggle'  # Reset Toggle to default name
                            else:
                                comp.NickName = ''  # Reset others to empty string
                            reset_count += 1
                            
                except:
                    continue
            
            if reset_count > 0:
                try:
                    if hasattr(self.doc, 'NewSolution'):
                        self.doc.NewSolution(False)
                except:
                    pass
            
            return "Reset " + str(reset_count) + " parameters to unnamed state"
        except Exception as e:
            return "Reset failed: " + str(e)
    
    def create_suggested_groups(self):
        """Suggest and create logical groups based on component proximity"""
        return "Group creation requires manual selection. Select related components and press Ctrl+G"
    
    # ==================== COMPONENT ORGANIZER FUNCTIONS ====================
    
    def enable_all_previews(self):
        """Enable preview for all components"""
        try:
            if not self.components:
                self.scan_document()
            
            count = 0
            for comp in self.components:
                try:
                    if hasattr(comp, 'Hidden') and comp.Hidden:
                        comp.Hidden = False
                        count += 1
                except:
                    continue
            
            if count > 0 and hasattr(self.doc, 'NewSolution'):
                try:
                    self.doc.NewSolution(False)
                except:
                    pass
            
            return f"Enabled preview for {count} components"
        except Exception as e:
            return f"Enable preview failed: {str(e)}"
    
    def disable_all_previews(self):
        """Disable preview for all components"""
        try:
            if not self.components:
                self.scan_document()
            
            count = 0
            for comp in self.components:
                try:
                    if hasattr(comp, 'Hidden') and not comp.Hidden:
                        comp.Hidden = True
                        count += 1
                except:
                    continue
            
            if count > 0 and hasattr(self.doc, 'NewSolution'):
                try:
                    self.doc.NewSolution(False)
                except:
                    pass
            
            return f"Disabled preview for {count} components"
        except Exception as e:
            return f"Disable preview failed: {str(e)}"
    
    def color_by_category(self):
        """Color components by their category"""
        try:
            if not self.components:
                self.scan_document()
            
            # Category color mapping
            category_colors = {
                'Maths': (255, 100, 100),      # Red
                'Vector': (100, 150, 255),     # Blue
                'Curve': (100, 255, 100),      # Green
                'Surface': (255, 200, 100),    # Orange
                'Mesh': (200, 100, 255),       # Purple
                'Intersect': (255, 150, 200),  # Pink
                'Transform': (150, 255, 200),  # Cyan
                'Params': (200, 200, 200),     # Gray
                'Display': (255, 255, 150),    # Yellow
            }
            
            count = 0
            colored_categories = {}
            
            for comp in self.components:
                try:
                    if hasattr(comp, 'Category') and hasattr(comp, 'Attributes'):
                        category = str(comp.Category)
                        
                        # Get color for this category
                        color = category_colors.get(category, (150, 150, 150))
                        
                        # Set color
                        if hasattr(comp.Attributes, 'Selected'):
                            comp.Attributes.Selected = False
                        
                        try:
                            from System.Drawing import Color
                            comp.Attributes.Selected = False
                            # Note: Direct color setting might not work in all GH versions
                            # This is a best-effort approach
                        except:
                            pass
                        
                        count += 1
                        colored_categories[category] = colored_categories.get(category, 0) + 1
                except:
                    continue
            
            result = f"Attempted to color {count} components by category\n"
            result += "Categories found: " + ", ".join([f"{k}({v})" for k, v in colored_categories.items()])
            result += "\n\nNote: Manual coloring may be needed (right-click component → Display → Color)"
            
            return result
        except Exception as e:
            return f"Color by category failed: {str(e)}"
    
    def color_by_severity(self):
        """Color components by issue severity"""
        try:
            if not self.components:
                self.scan_document()
            if not self.issues:
                self.run_all_checks()
            
            # Create component to severity map
            comp_severity = {}  # guid -> severity
            
            for issue in self.issues:
                for item in issue['items']:
                    if 'component' in item:
                        try:
                            guid = str(item['component'].InstanceGuid)
                            current_severity = comp_severity.get(guid, 'none')
                            
                            # Priority: error > warning > info
                            if issue['severity'] == 'error':
                                comp_severity[guid] = 'error'
                            elif issue['severity'] == 'warning' and current_severity != 'error':
                                comp_severity[guid] = 'warning'
                            elif issue['severity'] == 'info' and current_severity == 'none':
                                comp_severity[guid] = 'info'
                        except:
                            continue
            
            # Color mapping
            severity_colors = {
                'error': (255, 100, 100),    # Red
                'warning': (255, 200, 100),  # Orange/Yellow
                'info': (150, 200, 255),     # Light Blue
            }
            
            count = 0
            severity_counts = {'error': 0, 'warning': 0, 'info': 0}
            
            for comp in self.components:
                try:
                    guid = str(comp.InstanceGuid)
                    if guid in comp_severity:
                        severity = comp_severity[guid]
                        # Deselect component
                        if hasattr(comp, 'Attributes'):
                            comp.Attributes.Selected = False
                        count += 1
                        severity_counts[severity] += 1
                except:
                    continue
            
            result = f"Attempted to color {count} components by issue severity\n"
            result += f"Errors: {severity_counts['error']}, "
            result += f"Warnings: {severity_counts['warning']}, "
            result += f"Info: {severity_counts['info']}\n"
            result += "\nNote: Manual coloring may be needed (right-click component → Display → Color)"
            
            return result
        except Exception as e:
            return f"Color by severity failed: {str(e)}"
    
    def reset_all_colors(self):
        """Reset all component colors to default"""
        try:
            if not self.components:
                self.scan_document()
            
            count = 0
            for comp in self.components:
                try:
                    if hasattr(comp, 'Attributes'):
                        comp.Attributes.Selected = False
                        count += 1
                except:
                    continue
            
            return f"Reset colors for {count} components\n\nNote: Manual color reset may be needed (select all → right-click → Display → Remove Custom Color)"
        except Exception as e:
            return f"Reset colors failed: {str(e)}"
    
    def align_components_grid(self, spacing=100):
        """Align selected components in a grid (requires manual selection)"""
        return "Grid alignment requires manual selection.\n\nSteps:\n1. Select components to align\n2. Right-click → Align → Distribute Horizontal/Vertical\n3. Or use Grasshopper's built-in alignment tools"
    
    def select_by_category(self, category_name):
        """Select all components of a specific category"""
        try:
            if not self.components:
                self.scan_document()
            
            # Deselect all first
            if hasattr(self.doc, 'DeselectAll'):
                self.doc.DeselectAll()
            
            count = 0
            for comp in self.components:
                try:
                    if hasattr(comp, 'Category'):
                        category = str(comp.Category)
                        if category_name.lower() in category.lower():
                            if hasattr(comp, 'Attributes'):
                                comp.Attributes.Selected = True
                                count += 1
                except:
                    continue
            
            if count > 0 and hasattr(self.doc, 'Canvas'):
                try:
                    self.doc.Canvas.Refresh()
                except:
                    pass
            
            return f"Selected {count} components in category '{category_name}'"
        except Exception as e:
            return f"Selection failed: {str(e)}"
    
    def set_icon_display_by_name(self, component_name, display_mode=0):
        """Set icon display mode for specific component by name
        
        Args:
            component_name: Component name to match (e.g., 'EF Data Description')
            display_mode: 0=Icon only, 1=Name only, 2=Icon+Name
        """
        try:
            if not self.components:
                self.scan_document()
            
            # Import the enum
            from Grasshopper.Kernel import GH_IconDisplayMode
            
            # Map integer to enum
            mode_map = {
                0: GH_IconDisplayMode.icon,
                1: GH_IconDisplayMode.name,
                2: GH_IconDisplayMode.application
            }
            
            enum_mode = mode_map.get(display_mode, GH_IconDisplayMode.application)
            
            count = 0
            matched_types = set()
            
            for comp in self.components:
                try:
                    name = getattr(comp, 'Name', '')
                    
                    # Match component name (partial match)
                    if component_name.lower() in name.lower():
                        if hasattr(comp, 'Attributes'):
                            try:
                                # Access the DocObject and set IconDisplayMode
                                top_level = comp.Attributes.GetTopLevel
                                if hasattr(top_level, 'DocObject'):
                                    top_level.DocObject.IconDisplayMode = enum_mode
                                    count += 1
                                    matched_types.add(comp.GetType().Name)
                            except Exception as e:
                                # Fallback: try direct attribute access
                                try:
                                    comp.Attributes.GetTopLevel.DocObject.IconDisplayMode = enum_mode
                                    count += 1
                                    matched_types.add(comp.GetType().Name)
                                except:
                                    continue
                except:
                    continue
            
            # Refresh canvas to show changes
            if count > 0:
                try:
                    if hasattr(self.doc, 'Canvas') and hasattr(self.doc.Canvas, 'Refresh'):
                        self.doc.Canvas.Refresh()
                except:
                    pass
            
            mode_names = {0: 'Icon only', 1: 'Name only', 2: 'Icon + Name'}
            mode_name = mode_names.get(display_mode, 'Unknown')
            
            result = f"Changed display mode to '{mode_name}' for {count} components\n"
            if matched_types:
                result += f"Component types: {', '.join(matched_types)}"
            
            return result
        except Exception as e:
            return f"Display mode change failed: {str(e)}"
    
    def set_icon_display_by_type(self, type_pattern, display_mode=0):
        """Set icon display mode for components by type pattern
        
        Args:
            type_pattern: Type name pattern to match (e.g., 'Parameter_EF_Generic')
            display_mode: 0=Icon only, 1=Name only, 2=Icon+Name
        """
        try:
            if not self.components:
                self.scan_document()
            
            # Import the enum
            from Grasshopper.Kernel import GH_IconDisplayMode
            
            # Map integer to enum
            mode_map = {
                0: GH_IconDisplayMode.icon,
                1: GH_IconDisplayMode.name,
                2: GH_IconDisplayMode.application
            }
            
            enum_mode = mode_map.get(display_mode, GH_IconDisplayMode.application)
            
            count = 0
            matched_names = set()
            
            for comp in self.components:
                try:
                    full_type = comp.GetType().FullName
                    
                    # Match type pattern
                    if type_pattern.lower() in full_type.lower():
                        if hasattr(comp, 'Attributes'):
                            try:
                                top_level = comp.Attributes.GetTopLevel
                                if hasattr(top_level, 'DocObject'):
                                    top_level.DocObject.IconDisplayMode = enum_mode
                                    count += 1
                                    matched_names.add(getattr(comp, 'Name', 'Unknown'))
                            except:
                                continue
                except:
                    continue
            
            # Refresh canvas
            if count > 0:
                try:
                    if hasattr(self.doc, 'Canvas') and hasattr(self.doc.Canvas, 'Refresh'):
                        self.doc.Canvas.Refresh()
                except:
                    pass
            
            mode_names = {0: 'Icon only', 1: 'Name only', 2: 'Icon + Name'}
            mode_name = mode_names.get(display_mode, 'Unknown')
            
            result = f"Changed display mode to '{mode_name}' for {count} components\n"
            if matched_names and len(matched_names) <= 5:
                result += f"Component names: {', '.join(list(matched_names)[:5])}"
            elif matched_names:
                result += f"Component names: {', '.join(list(matched_names)[:3])} ... and {len(matched_names)-3} more"
            
            return result
        except Exception as e:
            return f"Display mode change failed: {str(e)}"
    
    # ==================== ALIGNMENT FUNCTIONS ====================
    
    def align_selected_horizontal(self, spacing=100):
        """Align selected components horizontally with spacing"""
        try:
            selected = []
            
            for comp in self.components:
                try:
                    if hasattr(comp, 'Attributes') and comp.Attributes.Selected:
                        selected.append(comp)
                except:
                    continue
            
            if len(selected) < 2:
                return "Please select at least 2 components first"
            
            # Sort by X position
            selected.sort(key=lambda c: c.Attributes.Pivot.X)
            
            # Align horizontally
            start_x = selected[0].Attributes.Pivot.X
            current_x = start_x
            
            for comp in selected:
                try:
                    pivot = comp.Attributes.Pivot
                    comp.Attributes.Pivot = System.Drawing.PointF(current_x, pivot.Y)
                    
                    # CRITICAL: Force layout update
                    if hasattr(comp.Attributes, 'ExpireLayout'):
                        comp.Attributes.ExpireLayout()
                    if hasattr(comp.Attributes, 'PerformLayout'):
                        comp.Attributes.PerformLayout()
                    
                    # Add spacing plus component width
                    if hasattr(comp.Attributes, 'Bounds'):
                        current_x += comp.Attributes.Bounds.Width + spacing
                    else:
                        current_x += spacing
                except:
                    current_x += spacing
            
            # Refresh (ENHANCED)
            if hasattr(self.doc, 'Canvas'):
                try:
                    # Force update all component positions
                    for comp in selected:
                        try:
                            comp.ExpireSolution(False)
                            # Force bounds recalculation
                            if hasattr(comp.Attributes, 'ExpireLayout'):
                                comp.Attributes.ExpireLayout()
                        except:
                            pass
                    
                    # Invalidate canvas to force redraw
                    if hasattr(self.doc.Canvas, 'Invalidate'):
                        self.doc.Canvas.Invalidate()
                    
                    # Multiple refresh attempts
                    self.doc.Canvas.Refresh()
                    
                    # Force document update
                    if hasattr(self.doc, 'NewSolution'):
                        self.doc.NewSolution(False)
                        
                    # Final canvas refresh
                    self.doc.Canvas.Refresh()
                except:
                    pass
            
            return f"Aligned {len(selected)} components horizontally with {spacing}px spacing"
        except Exception as e:
            return f"Horizontal alignment failed: {str(e)}"
    
    def align_selected_vertical(self, spacing=100):
        """Align selected components vertically with spacing"""
        try:
            selected = []
            
            for comp in self.components:
                try:
                    if hasattr(comp, 'Attributes') and comp.Attributes.Selected:
                        selected.append(comp)
                except:
                    continue
            
            if len(selected) < 2:
                return "Please select at least 2 components first"
            
            # Sort by Y position
            selected.sort(key=lambda c: c.Attributes.Pivot.Y)
            
            # Align vertically
            start_y = selected[0].Attributes.Pivot.Y
            current_y = start_y
            
            for comp in selected:
                try:
                    pivot = comp.Attributes.Pivot
                    comp.Attributes.Pivot = System.Drawing.PointF(pivot.X, current_y)
                    
                    # CRITICAL: Force layout update
                    if hasattr(comp.Attributes, 'ExpireLayout'):
                        comp.Attributes.ExpireLayout()
                    if hasattr(comp.Attributes, 'PerformLayout'):
                        comp.Attributes.PerformLayout()
                    
                    # Add spacing plus component height
                    if hasattr(comp.Attributes, 'Bounds'):
                        current_y += comp.Attributes.Bounds.Height + spacing
                    else:
                        current_y += spacing
                except:
                    current_y += spacing
            
            # Refresh (ENHANCED)
            if hasattr(self.doc, 'Canvas'):
                try:
                    # Force update all component positions
                    for comp in selected:
                        try:
                            comp.ExpireSolution(False)
                            # Force bounds recalculation
                            if hasattr(comp.Attributes, 'ExpireLayout'):
                                comp.Attributes.ExpireLayout()
                        except:
                            pass
                    
                    # Invalidate canvas to force redraw
                    if hasattr(self.doc.Canvas, 'Invalidate'):
                        self.doc.Canvas.Invalidate()
                    
                    # Multiple refresh attempts
                    self.doc.Canvas.Refresh()
                    
                    # Force document update
                    if hasattr(self.doc, 'NewSolution'):
                        self.doc.NewSolution(False)
                        
                    # Final canvas refresh
                    self.doc.Canvas.Refresh()
                except:
                    pass
            
            return f"Aligned {len(selected)} components vertically with {spacing}px spacing"
        except Exception as e:
            return f"Vertical alignment failed: {str(e)}"
    
    def align_selected_grid(self, spacing=100, columns=5):
        """Align selected components in a grid layout
        
        Args:
            spacing: Space between components (pixels)
            columns: Number of columns in grid
        """
        try:
            selected = []
            
            for comp in self.components:
                try:
                    if hasattr(comp, 'Attributes') and comp.Attributes.Selected:
                        selected.append(comp)
                except:
                    continue
            
            if len(selected) < 2:
                return "Please select at least 2 components first"
            
            # Sort by position (left to right, top to bottom)
            selected.sort(key=lambda c: (c.Attributes.Pivot.Y, c.Attributes.Pivot.X))
            
            # Start position
            start_x = selected[0].Attributes.Pivot.X
            start_y = selected[0].Attributes.Pivot.Y
            
            current_x = start_x
            current_y = start_y
            row_height = 0
            
            for i, comp in enumerate(selected):
                try:
                    # Place component
                    comp.Attributes.Pivot = System.Drawing.PointF(current_x, current_y)
                    
                    # CRITICAL: Force layout update
                    if hasattr(comp.Attributes, 'ExpireLayout'):
                        comp.Attributes.ExpireLayout()
                    if hasattr(comp.Attributes, 'PerformLayout'):
                        comp.Attributes.PerformLayout()
                    
                    # Track row height
                    if hasattr(comp.Attributes, 'Bounds'):
                        row_height = max(row_height, comp.Attributes.Bounds.Height)
                        comp_width = comp.Attributes.Bounds.Width
                    else:
                        row_height = max(row_height, 40)  # Default height
                        comp_width = 100  # Default width
                    
                    # Move to next position
                    if (i + 1) % columns == 0:
                        # New row
                        current_x = start_x
                        current_y += row_height + spacing
                        row_height = 0
                    else:
                        # Next column
                        current_x += comp_width + spacing
                except:
                    continue
            
            # Refresh (ENHANCED)
            if hasattr(self.doc, 'Canvas'):
                try:
                    # Force update all component positions
                    for comp in selected:
                        try:
                            comp.ExpireSolution(False)
                            # Force bounds recalculation
                            if hasattr(comp.Attributes, 'ExpireLayout'):
                                comp.Attributes.ExpireLayout()
                        except:
                            pass
                    
                    # Invalidate canvas to force redraw
                    if hasattr(self.doc.Canvas, 'Invalidate'):
                        self.doc.Canvas.Invalidate()
                    
                    # Multiple refresh attempts
                    self.doc.Canvas.Refresh()
                    
                    # Force document update
                    if hasattr(self.doc, 'NewSolution'):
                        self.doc.NewSolution(False)
                        
                    # Final canvas refresh
                    self.doc.Canvas.Refresh()
                except:
                    pass
            
            rows = (len(selected) + columns - 1) // columns
            return f"Aligned {len(selected)} components in {rows}x{columns} grid with {spacing}px spacing"
        except Exception as e:
            return f"Grid alignment failed: {str(e)}"
    
    def align_selected_flow(self, spacing_x=200, spacing_y=100):
        """Smart alignment based on data flow with horizontal wire optimization
        
        Analyzes wire connections and arranges components in layers with
        optimal vertical positioning to minimize wire crossing and maximize
        horizontal wire alignment.
        
        Args:
            spacing_x: Horizontal spacing between layers (pixels)
            spacing_y: Minimum vertical spacing within layer (pixels)
        """
        try:
            selected = []
            
            for comp in self.components:
                try:
                    if hasattr(comp, 'Attributes') and comp.Attributes.Selected:
                        selected.append(comp)
                except:
                    continue
            
            if len(selected) < 2:
                return "Please select at least 2 components first"
            
            # Build connection graph
            comp_to_layer = {}
            comp_inputs = {}  # component -> set of input components
            has_external_input = {}  # component -> has inputs from outside selection
            
            # Analyze connections for selected components
            # Method 1: Check inputs (standard way)
            for comp in selected:
                comp_inputs[comp] = set()
                has_external_input[comp] = False
                try:
                    if hasattr(comp, 'Params') and hasattr(comp.Params, 'Input'):
                        for param in comp.Params.Input:
                            if hasattr(param, 'Sources') and param.Sources:
                                for source in param.Sources:
                                    try:
                                        if hasattr(source, 'Attributes'):
                                            # Get the owner component of this parameter
                                            source_obj = source.Attributes.GetTopLevel.DocObject
                                            if source_obj in selected:
                                                comp_inputs[comp].add(source_obj)
                                            else:
                                                # Has input from outside selection
                                                has_external_input[comp] = True
                                    except:
                                        # If we can't get the source, assume external
                                        has_external_input[comp] = True
                except:
                    pass
            
            # Method 2: Check outputs (reverse direction)
            # This catches connections that Method 1 might miss (e.g., Panel components)
            for comp in selected:
                try:
                    if hasattr(comp, 'Params') and hasattr(comp.Params, 'Output'):
                        for param in comp.Params.Output:
                            if hasattr(param, 'Recipients') and param.Recipients:
                                for recipient in param.Recipients:
                                    try:
                                        if hasattr(recipient, 'Attributes'):
                                            # Get the owner component of this recipient parameter
                                            recipient_obj = recipient.Attributes.GetTopLevel.DocObject
                                            if recipient_obj in selected:
                                                # recipient receives from comp, so comp is input to recipient
                                                if recipient_obj not in comp_inputs:
                                                    comp_inputs[recipient_obj] = set()
                                                comp_inputs[recipient_obj].add(comp)
                                    except:
                                        pass
                except:
                    pass
            
            # Assign layers using topological sort
            assigned = set()
            current_layer = 0
            
            while len(assigned) < len(selected):
                # Find components for current layer
                layer_comps = []
                
                for comp in selected:
                    if comp in assigned:
                        continue
                    
                    # Check if all inputs are already assigned
                    if len(comp_inputs[comp]) == 0 and not has_external_input[comp]:
                        # No inputs at all - true source component (e.g., parameters)
                        layer_comps.append(comp)
                    elif len(comp_inputs[comp]) == 0 and has_external_input[comp]:
                        # Has external input but not from selected components
                        # Treat as if it has inputs (place in later layer)
                        if current_layer > 0:  # Only add after first layer
                            layer_comps.append(comp)
                    else:
                        # Check if all input components are assigned
                        all_inputs_assigned = all(inp in assigned for inp in comp_inputs[comp])
                        if all_inputs_assigned:
                            layer_comps.append(comp)
                
                if not layer_comps:
                    # Handle cycles or disconnected components
                    # Just assign remaining to current layer
                    layer_comps = [c for c in selected if c not in assigned]
                
                # Assign layer
                for comp in layer_comps:
                    comp_to_layer[comp] = current_layer
                    assigned.add(comp)
                
                current_layer += 1
            
            # Group by layer and sort vertically within layer
            layers = {}
            for comp, layer in comp_to_layer.items():
                if layer not in layers:
                    layers[layer] = []
                layers[layer].append(comp)
            
            # Sort each layer by current Y position (initial)
            for layer in layers.values():
                layer.sort(key=lambda c: c.Attributes.Pivot.Y)
            
            # Optimize Y positions based on connections (minimize wire angles)
            # For each component, calculate ideal Y position based on connected components in next layer
            optimized_y = {}
            
            for layer_num in sorted(layers.keys()):
                if layer_num + 1 in layers:
                    next_layer = layers[layer_num + 1]
                    
                    # For each component in next layer, find its input components in current layer
                    for next_comp in next_layer:
                        connected_in_current = [c for c in comp_inputs[next_comp] if c in layers[layer_num]]
                        
                        if connected_in_current:
                            # Calculate average Y of inputs (or use existing if already optimized)
                            avg_y = sum(optimized_y.get(c, c.Attributes.Pivot.Y) for c in connected_in_current) / len(connected_in_current)
                            optimized_y[next_comp] = avg_y
            
            # Re-sort layers based on optimized Y positions
            for layer_num in sorted(layers.keys()):
                layers[layer_num].sort(key=lambda c: optimized_y.get(c, c.Attributes.Pivot.Y))
            
            # Calculate starting position
            # Center vertically based on the tallest layer
            max_layer_height = 0
            for layer_comps in layers.values():
                layer_height = sum(60 if not hasattr(c.Attributes, 'Bounds') else c.Attributes.Bounds.Height for c in layer_comps)
                layer_height += spacing_y * (len(layer_comps) - 1)
                max_layer_height = max(max_layer_height, layer_height)
            
            # Use average Y position of all selected components as center
            avg_y = sum(c.Attributes.Pivot.Y for c in selected) / len(selected)
            start_y = avg_y - (max_layer_height / 2)
            
            min_x = min(c.Attributes.Pivot.X for c in selected)
            
            # Place components
            current_x = min_x
            
            # First pass: calculate ideal Y positions maintaining spacing
            ideal_positions = {}
            
            for layer_num in sorted(layers.keys()):
                layer_comps = layers[layer_num]
                
                if layer_num == 0:
                    # First layer: use optimized Y or default spacing
                    current_y = start_y
                    for comp in layer_comps:
                        ideal_positions[comp] = (current_x, current_y)
                        if hasattr(comp.Attributes, 'Bounds'):
                            current_y += comp.Attributes.Bounds.Height + spacing_y
                        else:
                            current_y += 60 + spacing_y
                else:
                    # Later layers: align with average of input components
                    for comp in layer_comps:
                        connected_inputs = [c for c in comp_inputs[comp] if c in ideal_positions]
                        
                        if connected_inputs:
                            # Use average Y of connected inputs
                            avg_y = sum(ideal_positions[c][1] for c in connected_inputs) / len(connected_inputs)
                            ideal_positions[comp] = (current_x, avg_y)
                        else:
                            # No connections in previous layer, use next available Y
                            if not ideal_positions or layer_num not in [k for k, v in ideal_positions.items()]:
                                current_y = start_y
                            else:
                                # Find max Y in this layer so far
                                layer_ys = [v[1] for k, v in ideal_positions.items() if k in layer_comps]
                                current_y = max(layer_ys) + 100 if layer_ys else start_y
                            ideal_positions[comp] = (current_x, current_y)
                
                # Move to next layer X position
                current_x += spacing_x
            
            # Second pass: actually place components
            for comp, (x, y) in ideal_positions.items():
                try:
                    comp.Attributes.Pivot = System.Drawing.PointF(x, y)
                    
                    # CRITICAL: Force layout update
                    if hasattr(comp.Attributes, 'ExpireLayout'):
                        comp.Attributes.ExpireLayout()
                    if hasattr(comp.Attributes, 'PerformLayout'):
                        comp.Attributes.PerformLayout()
                except:
                    pass
            
            # Refresh (ENHANCED)
            if hasattr(self.doc, 'Canvas'):
                try:
                    for comp in selected:
                        try:
                            comp.ExpireSolution(False)
                            if hasattr(comp.Attributes, 'ExpireLayout'):
                                comp.Attributes.ExpireLayout()
                        except:
                            pass
                    
                    if hasattr(self.doc.Canvas, 'Invalidate'):
                        self.doc.Canvas.Invalidate()
                    
                    self.doc.Canvas.Refresh()
                    
                    if hasattr(self.doc, 'NewSolution'):
                        self.doc.NewSolution(False)
                    
                    self.doc.Canvas.Refresh()
                except:
                    pass
            
            num_layers = len(layers)
            
            # Debug info: show layer assignments with connection details
            debug_info = []
            for layer_num in sorted(layers.keys()):
                layer_comps = layers[layer_num]
                debug_info.append(f"Layer {layer_num}:")
                for comp in layer_comps[:5]:  # Show up to 5 components per layer
                    name = getattr(comp, 'Name', 'Unknown')[:20]
                    num_inputs = len(comp_inputs[comp])
                    external = "(ext)" if has_external_input[comp] else ""
                    if num_inputs > 0:
                        input_names = [getattr(c, 'Name', '?')[:10] for c in list(comp_inputs[comp])[:2]]
                        debug_info.append(f"  • {name} ← {', '.join(input_names)} {external}")
                    else:
                        debug_info.append(f"  • {name} {external}")
                if len(layer_comps) > 5:
                    debug_info.append(f"  ... and {len(layer_comps)-5} more")
            
            result = f"Smart flow aligned {len(selected)} components into {num_layers} layers (left→right)\n"
            result += "\n".join(debug_info)
            return result
        except Exception as e:
            return f"Flow alignment failed: {str(e)}"
    
    def align_selected_parameter_based(self, spacing_x=200, spacing_y=None):
        """Align components based on parameter connections for horizontal wires
        
        Smart alignment that positions components so wires between parameter
        connection points are perfectly horizontal.
        
        🚀 AUTO-OPTIMIZATION: If spacing_y is None (default), the algorithm
        automatically calculates the optimal spacing for each layer based on:
        - Component heights and types (parameters need more space)
        - Connection offset patterns
        - Parameter density in each layer
        
        Example:
            Number Slider ───→ Addition (Input A)
            Number Slider ───→ Addition (Input B)
        
        Args:
            spacing_x: Horizontal spacing between layers (pixels)
            spacing_y: Vertical spacing within layer (pixels)
                      - None (default): Auto-calculate optimal spacing
                      - Integer: Use manual spacing value
        """
        try:
            selected = []
            for comp in self.components:
                try:
                    if hasattr(comp, 'Attributes') and comp.Attributes.Selected:
                        selected.append(comp)
                except:
                    continue
            
            if len(selected) < 2:
                return "Please select at least 2 components first"
            
            # 🔒 CRITICAL FIX: Calculate offsets in REAL-TIME (no stored positions!)
            # This ensures TRUE idempotency: running align 100x gives same result
            # No need to store "original" positions - we calculate relative offsets from current positions
            
            # Debug: Show actual parameter positions before processing
            debug_param_positions = []
            debug_param_positions.append(f"\n   🔍 Raw parameter positions:")
            
            # First, show all selected components
            debug_param_positions.append("   Selected components:")
            for comp in selected:
                comp_name = getattr(comp, 'Name', 'Unknown')[:20]
                comp_type = type(comp).__name__
                comp_y = comp.Attributes.Pivot.Y
                
                # Check if this is a parameter component (Panel, Slider, etc)
                is_param = self._is_param_component(comp)
                
                # For parameters, they ARE the output, no Params.Output
                if is_param:
                    has_output = True  # Parameters always have output
                    has_input = False  # Parameters don't have inputs
                else:
                    has_output = hasattr(comp, 'Params') and hasattr(comp.Params, 'Output')
                    has_input = hasattr(comp, 'Params') and hasattr(comp.Params, 'Input')
                
                debug_param_positions.append("   - {}: Y={:.1f}, Type={}, Out={}, In={}, Param={}".format(
                    comp_name, comp_y, comp_type[:20], has_output, has_input, is_param))
            
            debug_param_positions.append("")
            debug_param_positions.append("   Parameter details:")
            
            for comp in selected:
                comp_name = getattr(comp, 'Name', 'Unknown')[:20]
                comp_y = comp.Attributes.Pivot.Y
                
                # Check outputs
                try:
                    if hasattr(comp, 'Params') and hasattr(comp.Params, 'Output'):
                        for param_idx, param in enumerate(comp.Params.Output):
                            param_y = None
                            method_used = "None"
                            
                            # Try multiple methods
                            try:
                                # Method 1: Pivot
                                if hasattr(param, 'Attributes'):
                                    if hasattr(param.Attributes, 'Pivot'):
                                        param_y = param.Attributes.Pivot.Y
                                        method_used = "Pivot"
                                    # Method 2: Bounds center
                                    elif hasattr(param.Attributes, 'Bounds'):
                                        bounds = param.Attributes.Bounds
                                        param_y = bounds.Y + (bounds.Height / 2)
                                        method_used = "Bounds"
                                    # Method 3: OutputGrip
                                    elif hasattr(param.Attributes, 'OutputGrip'):
                                        param_y = param.Attributes.OutputGrip.Y
                                        method_used = "OutputGrip"
                            except Exception as e:
                                method_used = "Error: " + str(e)[:20]
                            
                            offset = (param_y - comp_y) if param_y else 0.0
                            y_str = "{:.1f}".format(param_y) if param_y else "N/A"
                            off_str = "{:.1f}".format(offset)
                            debug_param_positions.append("   {} Out[{}]: y={}, off={}, [{}]".format(comp_name, param_idx, y_str, off_str, method_used))
                except Exception as e:
                    debug_param_positions.append("   {} outputs failed: {}".format(comp_name, str(e)[:30]))
                
                # Check inputs
                try:
                    if hasattr(comp, 'Params') and hasattr(comp.Params, 'Input'):
                        for param_idx, param in enumerate(comp.Params.Input):
                            param_y = None
                            method_used = "None"
                            
                            try:
                                if hasattr(param, 'Attributes'):
                                    if hasattr(param.Attributes, 'Pivot'):
                                        param_y = param.Attributes.Pivot.Y
                                        method_used = "Pivot"
                                    elif hasattr(param.Attributes, 'Bounds'):
                                        bounds = param.Attributes.Bounds
                                        param_y = bounds.Y + (bounds.Height / 2)
                                        method_used = "Bounds"
                                    elif hasattr(param.Attributes, 'InputGrip'):
                                        param_y = param.Attributes.InputGrip.Y
                                        method_used = "InputGrip"
                            except Exception as e:
                                method_used = "Error: " + str(e)[:20]
                            
                            offset = (param_y - comp_y) if param_y else 0.0
                            y_str = "{:.1f}".format(param_y) if param_y else "N/A"
                            off_str = "{:.1f}".format(offset)
                            debug_param_positions.append("   {} In[{}]: y={}, off={}, [{}]".format(comp_name, param_idx, y_str, off_str, method_used))
                except Exception as e:
                    debug_param_positions.append("   {} inputs failed: {}".format(comp_name, str(e)[:30]))
            
            # Build connection graph with parameter RELATIVE positions (offset from component pivot)
            # This ensures idempotency - same connections = same result regardless of current positions
            comp_connections = {}  # component -> [(source_comp, source_param_rel_offset, target_param_rel_offset)]
            
            # PASS 1: Check Input parameters (component receives from source)
            for comp in selected:
                comp_connections[comp] = []
                try:
                    if hasattr(comp, 'Params') and hasattr(comp.Params, 'Input'):
                        for param_idx, param in enumerate(comp.Params.Input):
                            if hasattr(param, 'Sources') and param.Sources:
                                # Get ACTUAL param Y position (absolute coordinate)
                                target_param_y = None
                                try:
                                    # Method 1: Try Pivot directly
                                    if hasattr(param, 'Attributes') and hasattr(param.Attributes, 'Pivot'):
                                        target_param_y = param.Attributes.Pivot.Y
                                    # Method 2: Try InputGrip
                                    elif hasattr(param, 'Attributes') and hasattr(param.Attributes, 'InputGrip'):
                                        target_param_y = param.Attributes.InputGrip.Y
                                    # Method 3: Estimate from component bounds and parameter index
                                    elif hasattr(comp.Attributes, 'Bounds'):
                                        comp_y = comp.Attributes.Pivot.Y
                                        bounds = comp.Attributes.Bounds
                                        # Estimate: parameters are evenly distributed vertically
                                        num_inputs = comp.Params.Input.Count if hasattr(comp.Params.Input, 'Count') else len(list(comp.Params.Input))
                                        if num_inputs > 1:
                                            # Spread from top to bottom of component
                                            param_spacing = bounds.Height / (num_inputs + 1)
                                            offset = (param_idx + 1) * param_spacing - (bounds.Height / 2)
                                            target_param_y = comp_y + offset
                                        else:
                                            # Single parameter, use center
                                            target_param_y = comp_y
                                except Exception as e:
                                    pass
                                
                                # If we still can't get param position, skip this connection
                                if target_param_y is None:
                                    continue
                                
                                # ✅ Calculate target param offset from CURRENT position (real-time)
                                # Offset is always same regardless of where component is positioned
                                target_param_rel_offset = target_param_y - comp.Attributes.Pivot.Y
                                
                                for source in param.Sources:
                                    try:
                                        if hasattr(source, 'Attributes'):
                                            source_comp = source.Attributes.GetTopLevel.DocObject
                                            if source_comp in selected:
                                                # Get ACTUAL source param Y position
                                                source_param_y = None
                                                try:
                                                    # Method 1: Try Pivot
                                                    if hasattr(source.Attributes, 'Pivot'):
                                                        source_param_y = source.Attributes.Pivot.Y
                                                    # Method 2: Try OutputGrip
                                                    elif hasattr(source.Attributes, 'OutputGrip'):
                                                        source_param_y = source.Attributes.OutputGrip.Y
                                                    # Method 3: Use source component center (for simple params like Number Slider)
                                                    else:
                                                        source_param_y = source_comp.Attributes.Pivot.Y
                                                except:
                                                    source_param_y = source_comp.Attributes.Pivot.Y
                                                
                                                # Only add if we have both positions
                                                if source_param_y is not None:
                                                    # ✅ Calculate source param offset from CURRENT position (real-time)
                                                    source_param_rel_offset = source_param_y - source_comp.Attributes.Pivot.Y
                                                    
                                                    comp_connections[comp].append((
                                                        source_comp,
                                                        source_param_rel_offset,
                                                        target_param_rel_offset
                                                    ))
                                    except:
                                        pass
                except:
                    pass
            
                        # PASS 2: Also check Output parameters to catch all connections
            # 🔑 KEY FIX: Handle parameter components (Panel, Number Slider) differently!
            for comp in selected:
                # Check if this is a parameter component first
                is_param_comp = self._is_param_component(comp)
                
                try:
                    # 🎯 PARAMETER COMPONENT HANDLING
                    if is_param_comp:
                        # Parameter components (Panel, Number Slider, etc.) ARE the output
                        # They don't have separate Params.Output positions - use component Pivot directly
                        source_param_y = comp.Attributes.Pivot.Y
                        source_param_rel_offset = 0.0  # No offset - component IS the parameter
                        
                        # Find all recipients of this parameter component
                        recipients_found = []
                        try:
                            # Parameters might have Recipients directly or through Params
                            if hasattr(comp, 'Recipients') and comp.Recipients:
                                recipients_found = list(comp.Recipients)
                            elif hasattr(comp, 'Params') and hasattr(comp.Params, 'Output'):
                                for param in comp.Params.Output:
                                    if hasattr(param, 'Recipients') and param.Recipients:
                                        recipients_found.extend(list(param.Recipients))
                        except:
                            pass
                        
                        # Process all recipients
                        for recipient in recipients_found:
                            try:
                                if hasattr(recipient, 'Attributes'):
                                    target_comp = recipient.Attributes.GetTopLevel.DocObject
                                    if target_comp in selected:
                                        # Get target param Y
                                        target_param_y = None
                                        try:
                                            if hasattr(recipient.Attributes, 'Pivot'):
                                                target_param_y = recipient.Attributes.Pivot.Y
                                            elif hasattr(recipient.Attributes, 'InputGrip'):
                                                target_param_y = recipient.Attributes.InputGrip.Y
                                            else:
                                                target_param_y = target_comp.Attributes.Pivot.Y
                                        except:
                                            target_param_y = target_comp.Attributes.Pivot.Y
                                        
                                        if target_param_y is not None:
                                            target_param_rel_offset = target_param_y - target_comp.Attributes.Pivot.Y
                                            
                                            if target_comp not in comp_connections:
                                                comp_connections[target_comp] = []
                                            
                                            conn = (comp, source_param_rel_offset, target_param_rel_offset)
                                            if conn not in comp_connections[target_comp]:
                                                comp_connections[target_comp].append(conn)
                            except:
                                pass
                    
                    # 🔧 REGULAR COMPONENT HANDLING (not a parameter)
                    elif hasattr(comp, 'Params') and hasattr(comp.Params, 'Output'):
                        for param_idx, param in enumerate(comp.Params.Output):
                            if hasattr(param, 'Recipients') and param.Recipients:
                                # Get source param Y
                                source_param_y = None
                                try:
                                    # Method 1: Try Pivot
                                    if hasattr(param, 'Attributes') and hasattr(param.Attributes, 'Pivot'):
                                        source_param_y = param.Attributes.Pivot.Y
                                    # Method 2: Try OutputGrip
                                    elif hasattr(param, 'Attributes') and hasattr(param.Attributes, 'OutputGrip'):
                                        source_param_y = param.Attributes.OutputGrip.Y
                                    # Method 3: Estimate from component bounds
                                    elif hasattr(comp.Attributes, 'Bounds'):
                                        comp_y = comp.Attributes.Pivot.Y
                                        bounds = comp.Attributes.Bounds
                                        num_outputs = comp.Params.Output.Count if hasattr(comp.Params.Output, 'Count') else len(list(comp.Params.Output))
                                        if num_outputs > 1:
                                            param_spacing = bounds.Height / (num_outputs + 1)
                                            offset = (param_idx + 1) * param_spacing - (bounds.Height / 2)
                                            source_param_y = comp_y + offset
                                        else:
                                            source_param_y = comp_y
                                    # Method 4: Fallback to component center
                                    else:
                                        source_param_y = comp.Attributes.Pivot.Y
                                except:
                                    source_param_y = comp.Attributes.Pivot.Y
                                
                                if source_param_y is None:
                                    continue
                                
                                # ✅ Calculate source param offset from CURRENT position (real-time)
                                source_param_rel_offset = source_param_y - comp.Attributes.Pivot.Y
                                
                                for recipient in param.Recipients:
                                    try:
                                        if hasattr(recipient, 'Attributes'):
                                            target_comp = recipient.Attributes.GetTopLevel.DocObject
                                            if target_comp in selected:
                                                # Get target param Y
                                                target_param_y = None
                                                try:
                                                    # Method 1: Try Pivot
                                                    if hasattr(recipient.Attributes, 'Pivot'):
                                                        target_param_y = recipient.Attributes.Pivot.Y
                                                    # Method 2: Try InputGrip
                                                    elif hasattr(recipient.Attributes, 'InputGrip'):
                                                        target_param_y = recipient.Attributes.InputGrip.Y
                                                    # Method 3: Fallback to target component center
                                                    else:
                                                        target_param_y = target_comp.Attributes.Pivot.Y
                                                except:
                                                    target_param_y = target_comp.Attributes.Pivot.Y
                                                
                                                if target_param_y is not None:
                                                    # ✅ Calculate target param offset from CURRENT position (real-time)
                                                    target_param_rel_offset = target_param_y - target_comp.Attributes.Pivot.Y
                                                    
                                                    # Check if this connection already exists
                                                    if target_comp not in comp_connections:
                                                        comp_connections[target_comp] = []
                                                    
                                                    conn = (comp, source_param_rel_offset, target_param_rel_offset)
                                                    if conn not in comp_connections[target_comp]:
                                                        comp_connections[target_comp].append(conn)
                                    except:
                                        pass
                except:
                    pass

            
            # 🔒 CRITICAL FIX v2: Use RELATIVE offsets (already calculated above)
            # This ensures idempotency - running align multiple times gives same result
            # Offsets are stored relative to component pivots, so they're always the same
            # regardless of where components are currently positioned
            
            # comp_connections already contains relative offsets, so we can use them directly
            comp_param_offsets = {}  # component -> [(source_comp, source_offset, target_offset)]
            
            for comp in selected:
                comp_param_offsets[comp] = []
                for source_comp, source_rel_offset, target_rel_offset in comp_connections[comp]:
                    # ✅ Offsets are already relative to component pivots - no additional calculation needed!
                    # This makes the algorithm deterministic: same connections = same result
                    comp_param_offsets[comp].append((source_comp, source_rel_offset, target_rel_offset))
            
            # Count connections for debug
            total_connections_found = sum(len(comp_param_offsets[c]) for c in selected)
            connections_per_comp = {}
            for comp in selected:
                comp_name = getattr(comp, 'Name', 'Unknown')[:20]
                num_conns = len(comp_param_offsets[comp])
                if num_conns > 0:
                    connections_per_comp[comp_name] = num_conns
            
            # Determine layers using accurate longest-path algorithm
            # This ensures components are placed at the correct depth even with complex connections
            layer_assignments = {}
            
            # Initialize all components to layer 0
            for comp in selected:
                layer_assignments[comp] = 0
            
            # Find root components (no inputs)
            roots = [c for c in selected if len(comp_param_offsets[c]) == 0]
            if not roots:
                # No roots (circular), use first component
                roots = [selected[0]]
            
            # Keep updating layers until no changes (longest path algorithm)
            max_iterations = len(selected) * 2  # Prevent infinite loops
            iteration = 0
            changed = True
            
            while changed and iteration < max_iterations:
                changed = False
                iteration += 1
                
                for comp in selected:
                    # Calculate this component's layer based on ALL its inputs
                    if len(comp_param_offsets[comp]) > 0:
                        # Find maximum layer of all input components
                        max_input_layer = -1
                        for source_comp, _, _ in comp_param_offsets[comp]:
                            if source_comp in layer_assignments:
                                max_input_layer = max(max_input_layer, layer_assignments[source_comp])
                        
                        # This component should be at max_input_layer + 1
                        new_layer = max_input_layer + 1 if max_input_layer >= 0 else 0
                        
                        if new_layer > layer_assignments[comp]:
                            layer_assignments[comp] = new_layer
                            changed = True
            
            # Group by layer
            layers = {}
            for comp, layer in layer_assignments.items():
                if layer not in layers:
                    layers[layer] = []
                layers[layer].append(comp)
            
            # AUTO-OPTIMIZE spacing if not provided by user
            auto_spacing_mode = (spacing_y is None)
            spacing_analysis = {}
            
            if auto_spacing_mode:
                # 🚀 AUTOMATIC OPTIMAL SPACING CALCULATION
                spacing_analysis['mode'] = 'auto'
                spacing_analysis['details'] = []
                
                # Analyze each layer to find optimal spacing
                layer_optimal_spacings = {}
                
                for layer_num in sorted(layers.keys()):
                    layer_comps = layers[layer_num]
                    
                    # Calculate statistics for this layer
                    heights = []
                    param_count = 0
                    max_offset = 0
                    
                    for comp in layer_comps:
                        # Get component height
                        height = 40  # default
                        if hasattr(comp.Attributes, 'Bounds'):
                            height = comp.Attributes.Bounds.Height
                        heights.append(height)
                        
                        # Check if parameter
                        if self._is_param_component(comp):
                            param_count += 1
                        
                        # Analyze connection offsets
                        for src, src_off, tgt_off in comp_param_offsets.get(comp, []):
                            offset_distance = abs(tgt_off - src_off)
                            max_offset = max(max_offset, offset_distance)
                    
                    # Calculate optimal spacing for this layer
                    avg_height = sum(heights) / len(heights) if heights else 40
                    max_height = max(heights) if heights else 40
                    
                    # Base spacing on component characteristics
                    if param_count > len(layer_comps) / 2:
                        # Mostly parameters - need more space
                        base_spacing = max(60, avg_height * 0.5)
                    else:
                        # Regular components - can be tighter
                        base_spacing = max(40, avg_height * 0.3)
                    
                    # Add buffer for connection offsets
                    offset_buffer = min(max_offset * 0.5, 30) if max_offset > 0 else 0
                    
                    optimal = base_spacing + offset_buffer
                    layer_optimal_spacings[layer_num] = optimal
                    
                    spacing_analysis['details'].append({
                        'layer': layer_num,
                        'comps': len(layer_comps),
                        'avg_height': avg_height,
                        'max_height': max_height,
                        'param_ratio': param_count / len(layer_comps) if layer_comps else 0,
                        'max_offset': max_offset,
                        'optimal_spacing': optimal
                    })
                
                # Use the average optimal spacing across all layers
                if layer_optimal_spacings:
                    spacing_y = sum(layer_optimal_spacings.values()) / len(layer_optimal_spacings)
                    spacing_y = max(50, min(spacing_y, 150))  # Clamp between 50-150px
                else:
                    spacing_y = 70  # Safe default
                
                spacing_analysis['final_spacing_y'] = spacing_y
            else:
                spacing_analysis['mode'] = 'manual'
                spacing_analysis['final_spacing_y'] = spacing_y
            
            # 🔒 ANCHOR-BASED POSITIONING (v1.2.0 - TRUE ZERO DRIFT!)
            # Select an anchor component that will NEVER move
            # All other components are positioned relative to this anchor
            # This ensures perfect idempotency: anchor stays put = no drift!
            
            min_x = min(c.Attributes.Pivot.X for c in selected)
            
            # 🎯 SELECT ANCHOR: First parameter component in Layer 0, or first component
            anchor_comp = None
            anchor_y = None
            
            # Try to find a parameter in Layer 0 first (Panel, Slider, etc.)
            if 0 in layers:
                for comp in layers[0]:
                    if self._is_param_component(comp):
                        anchor_comp = comp
                        anchor_y = comp.Attributes.Pivot.Y
                        break
            
            # If no parameter in Layer 0, use first component in Layer 0
            if anchor_comp is None and 0 in layers and len(layers[0]) > 0:
                anchor_comp = layers[0][0]
                anchor_y = anchor_comp.Attributes.Pivot.Y
            
            # Fallback: use first component overall
            if anchor_comp is None:
                anchor_comp = selected[0]
                anchor_y = anchor_comp.Attributes.Pivot.Y
            
            # Calculate layer widths (maximum component width in each layer)
            layer_widths = {}
            for layer_num in sorted(layers.keys()):
                max_width = 0
                for comp in layers[layer_num]:
                    try:
                        if hasattr(comp.Attributes, 'Bounds'):
                            width = comp.Attributes.Bounds.Width
                            max_width = max(max_width, width)
                        else:
                            max_width = max(max_width, 100)  # Default width
                    except:
                        max_width = max(max_width, 100)
                layer_widths[layer_num] = max_width
            
            # Calculate X positions for each layer (cumulative with minimal margins)
            layer_x_positions = {}
            current_x = min_x
            
            if auto_spacing_mode:
                # AUTO MODE: Use actual component widths + small margin
                base_margin = 50  # Minimal margin between layers
                
                for layer_num in sorted(layers.keys()):
                    layer_x_positions[layer_num] = current_x
                    if layer_num in layer_widths:
                        # Move X by this layer's width + minimal margin
                        current_x += layer_widths[layer_num] + base_margin
                
                # Store for debug output
                spacing_analysis['spacing_x_mode'] = 'auto'
                spacing_analysis['layer_widths'] = layer_widths
                spacing_analysis['base_margin'] = base_margin
            else:
                # MANUAL MODE: Use spacing_x uniformly
                for layer_num in sorted(layers.keys()):
                    layer_x_positions[layer_num] = current_x
                    current_x += spacing_x
                
                spacing_analysis['spacing_x_mode'] = 'manual'
                spacing_analysis['spacing_x'] = spacing_x
            
            # IMPROVED: Position components with REVERSE approach
            # Start from the LAST layer and work backwards for better alignment
            positioned = {}
            spacing_debug = []  # Track spacing decisions for debug output
            
            # 🔒 CRITICAL: Lock anchor position FIRST (prevents drift!)
            # Anchor component will NOT move - all others positioned relative to it
            anchor_layer = layer_assignments[anchor_comp]
            anchor_x = layer_x_positions[anchor_layer]
            positioned[anchor_comp] = (anchor_x, anchor_y)  # Anchor stays at original Y!
            
            # Position layers in REVERSE order (right to left)
            for layer_num in sorted(layers.keys(), reverse=True):
                layer_comps = layers[layer_num]
                current_x = layer_x_positions[layer_num]  # Use pre-calculated X position
                
                if layer_num == max(layers.keys()):
                    # Last layer (outputs): simple vertical stacking relative to anchor
                    current_y = anchor_y - (len(layer_comps) * 30)
                    for comp in layer_comps:
                        # Skip anchor - already positioned!
                        if comp == anchor_comp:
                            continue
                        positioned[comp] = (current_x, current_y)
                        current_y += spacing_y
                        if hasattr(comp.Attributes, 'Bounds'):
                            current_y += comp.Attributes.Bounds.Height
                else:
                    # Earlier layers: align based on WHERE their outputs connect
                    # This is the KEY change - align inputs to match output positions
                    comp_ideal_y = {}
                    
                    for comp in layer_comps:
                        # Skip anchor - already positioned!
                        if comp == anchor_comp:
                            continue
                        # Find all components in NEXT layers that use this comp as input
                        connected_targets = []
                        for target_comp in selected:
                            if target_comp in positioned:  # Already positioned (in later layer)
                                for src, src_off, tgt_off in comp_param_offsets[target_comp]:
                                    if src == comp:
                                        # This comp connects to target_comp
                                        # For horizontal wire: comp.Y + src_off = target_comp.Y + tgt_off
                                        # Therefore: comp.Y = target_comp.Y + tgt_off - src_off
                                        target_y = positioned[target_comp][1]
                                        ideal_comp_y = target_y + tgt_off - src_off
                                        connected_targets.append(ideal_comp_y)
                        
                        if connected_targets:
                            # Average if multiple targets
                            comp_ideal_y[comp] = sum(connected_targets) / len(connected_targets)
                        else:
                            # No connections found - position relative to anchor
                            # Calculate offset from anchor and maintain it
                            current_offset = comp.Attributes.Pivot.Y - anchor_y
                            comp_ideal_y[comp] = anchor_y + current_offset
                    
                    # Sort by ideal Y and assign positions with minimum spacing
                    # Exclude anchor from sorting - it's already positioned!
                    layer_comps_to_sort = [c for c in layer_comps if c != anchor_comp]
                    layer_comps_sorted = sorted(layer_comps_to_sort, key=lambda c: comp_ideal_y[c])
                    
                    for i, comp in enumerate(layer_comps_sorted):
                        ideal_y = comp_ideal_y[comp]
                        
                        # Apply minimum spacing constraint to prevent overlap
                        if i > 0:
                            prev_comp = layer_comps_sorted[i-1]
                            prev_y = positioned[prev_comp][1]
                            prev_height = 40
                            if hasattr(prev_comp.Attributes, 'Bounds'):
                                prev_height = prev_comp.Attributes.Bounds.Height
                            
                            # IMPROVED: Use ADAPTIVE spacing based on component types
                            # Parameters (like Panel) need MORE space, regular components less
                            comp_is_param = self._is_param_component(comp)
                            prev_is_param = self._is_param_component(prev_comp)
                            
                            # Get actual component heights
                            comp_height = 40
                            if hasattr(comp.Attributes, 'Bounds'):
                                comp_height = comp.Attributes.Bounds.Height
                            
                            # Determine spacing type
                            spacing_type = "regular"
                            if comp_is_param or prev_is_param:
                                # At least one is a parameter - use FULL spacing to avoid overlap
                                effective_spacing = max(spacing_y, 60)  # Minimum 60px for parameters
                                spacing_type = "param"
                            else:
                                # Both are regular components - can reduce spacing for wire alignment
                                effective_spacing = max(40, int(spacing_y * 0.6))  # Use 60% spacing, minimum 40px
                                spacing_type = "reduced"
                            
                            min_y = prev_y + prev_height + effective_spacing
                            
                            # Reduce overlap tolerance to prevent components from overlapping
                            overlap_tolerance = 5  # Only 5px overlap allowed (was 20px)
                            adjustment = ""
                            if ideal_y < (prev_y + prev_height - overlap_tolerance):
                                adjustment = " (adjusted from {:.1f})".format(ideal_y)
                                ideal_y = min_y
                            
                            # Record spacing decision for debug
                            comp_name = getattr(comp, 'Name', 'Unknown')[:15]
                            prev_name = getattr(prev_comp, 'Name', 'Unknown')[:15]
                            spacing_debug.append({
                                'layer': layer_num,
                                'prev': prev_name,
                                'comp': comp_name,
                                'prev_is_param': prev_is_param,
                                'comp_is_param': comp_is_param,
                                'spacing': effective_spacing,
                                'type': spacing_type,
                                'adjustment': adjustment
                            })
                        
                        positioned[comp] = (current_x, ideal_y)
            
            # Apply positions
            move_failures = []
            for comp, (x, y) in positioned.items():
                try:
                    # Get the actual component (not just the interface)
                    actual_comp = comp
                    if hasattr(comp, 'Attributes') and hasattr(comp.Attributes, 'GetTopLevel'):
                        try:
                            actual_comp = comp.Attributes.GetTopLevel.DocObject
                        except:
                            pass
                    
                    # Record BEFORE position
                    before_x = actual_comp.Attributes.Pivot.X
                    before_y = actual_comp.Attributes.Pivot.Y
                    comp_name = getattr(actual_comp, 'Name', 'Unknown')[:20]
                    comp_type = type(actual_comp).__name__
                    
                    # Try multiple methods to move the component
                    moved = False
                    
                    # Round to nearest pixel for cleaner alignment
                    x_rounded = round(x)
                    y_rounded = round(y)
                    
                    # Method 1: Direct Pivot assignment
                    try:
                        actual_comp.Attributes.Pivot = System.Drawing.PointF(x_rounded, y_rounded)
                        moved = True
                    except Exception as e1:
                        pass
                    
                    # Method 2: MoveTo (if available)
                    if not moved and hasattr(actual_comp.Attributes, 'MoveTo'):
                        try:
                            actual_comp.Attributes.MoveTo(System.Drawing.PointF(x_rounded, y_rounded))
                            moved = True
                        except Exception as e2:
                            pass
                    
                    # Method 3: Set Bounds location
                    if not moved and hasattr(actual_comp.Attributes, 'Bounds'):
                        try:
                            bounds = actual_comp.Attributes.Bounds
                            new_bounds = System.Drawing.RectangleF(x_rounded, y_rounded, bounds.Width, bounds.Height)
                            actual_comp.Attributes.Bounds = new_bounds
                            moved = True
                        except Exception as e3:
                            pass
                    
                    # Force layout updates
                    if hasattr(actual_comp.Attributes, 'ExpireLayout'):
                        actual_comp.Attributes.ExpireLayout()
                    if hasattr(actual_comp.Attributes, 'PerformLayout'):
                        actual_comp.Attributes.PerformLayout()
                    
                    # Record AFTER position
                    after_x = actual_comp.Attributes.Pivot.X
                    after_y = actual_comp.Attributes.Pivot.Y
                    
                    # Debug: Track if position actually changed
                    delta_y = abs(after_y - y_rounded)
                    if delta_y > 0.5:
                        move_failures.append("   [FAIL] {} ({}): target Y={:.1f}, actual Y={:.1f}, delta={:.1f}".format(
                            comp_name, comp_type[:15], y_rounded, after_y, delta_y))
                    elif delta_y > 0.1:
                        debug_param_positions.append("   [OK] {}: Y diff={:.1f} (acceptable)".format(comp_name, delta_y))
                except Exception as e:
                    comp_name = getattr(comp, 'Name', 'Unknown')[:20] if hasattr(comp, 'Name') else 'Unknown'
                    move_failures.append("   [ERROR] {}: {}".format(comp_name, str(e)[:40]))
            
            # Add failures to debug output
            if move_failures:
                debug_param_positions.append("")
                debug_param_positions.append("   Movement issues:")
                debug_param_positions.extend(move_failures)
            
            # Refresh canvas (ENHANCED - Multiple attempts)
            if hasattr(self.doc, 'Canvas'):
                try:
                    # Force multiple refresh cycles
                    for refresh_cycle in range(3):
                        for comp in selected:
                            try:
                                comp.ExpireSolution(False)
                                if hasattr(comp.Attributes, 'ExpireLayout'):
                                    comp.Attributes.ExpireLayout()
                                if hasattr(comp.Attributes, 'PerformLayout'):
                                    comp.Attributes.PerformLayout()
                            except:
                                pass
                        
                        if hasattr(self.doc.Canvas, 'Invalidate'):
                            self.doc.Canvas.Invalidate()
                        
                        self.doc.Canvas.Refresh()
                    
                    # Force document solution
                    if hasattr(self.doc, 'NewSolution'):
                        self.doc.NewSolution(False)
                    
                    # Final refresh
                    if hasattr(self.doc.Canvas, 'Invalidate'):
                        self.doc.Canvas.Invalidate()
                    self.doc.Canvas.Refresh()
                except:
                    pass
            
            num_layers = len(layers)
            
            # Debug info: show layer assignments and connections
            debug_lines = []
            
            # Add raw parameter positions first
            debug_lines.extend(debug_param_positions)
            
            debug_lines.append(f"\n   📖 Alignment Details:")
            debug_lines.append(f"   Total connections found: {total_connections_found}")
            
            if connections_per_comp:
                debug_lines.append(f"\n   Connections per component:")
                for comp_name, num in connections_per_comp.items():
                    debug_lines.append(f"      • {comp_name}: {num}")
            
            # Show actual parameter offsets for debugging
            debug_lines.append(f"\n   Parameter offsets (for horizontal wires):")
            for comp in selected:
                comp_name = getattr(comp, 'Name', 'Unknown')[:20]
                if len(comp_param_offsets[comp]) > 0:
                    debug_lines.append(f"   {comp_name}:")
                    for src_comp, src_off, tgt_off in comp_param_offsets[comp][:3]:  # Show first 3
                        src_name = getattr(src_comp, 'Name', 'Unknown')[:15]
                        debug_lines.append(f"      ← {src_name}: src_off={src_off:.1f}, tgt_off={tgt_off:.1f}")
            
            debug_lines.append(f"\n   Layer assignments:")
            for layer_num in sorted(layers.keys()):
                layer_comps = layers[layer_num]
                comp_names = [getattr(c, 'Name', 'Unknown')[:20] for c in layer_comps[:4]]
                if len(layer_comps) > 4:
                    comp_names.append(f"...+{len(layer_comps)-4}")
                debug_lines.append(f"   Layer {layer_num}: {', '.join(comp_names)}")
            
            # Show final positions with component identification
            debug_lines.append(f"\n   Final positions (with connection info):")
            for comp in selected:
                comp_name = getattr(comp, 'Name', 'Unknown')[:20]
                if comp in positioned:
                    x, y = positioned[comp]
                    # Show what this component connects to
                    conn_info = ""
                    if len(comp_param_offsets[comp]) > 0:
                        targets = set()
                        for target_comp in selected:
                            if target_comp in positioned:
                                for src, _, _ in comp_param_offsets[target_comp]:
                                    if src == comp:
                                        targets.add(getattr(target_comp, 'Name', 'Unknown')[:15])
                        if targets:
                            conn_info = f" → {', '.join(targets)}"
                    debug_lines.append(f"   {comp_name}: Y={y:.1f}{conn_info}")
            
            # Add spacing debug information
            if spacing_debug:
                debug_lines.append(f"\n   🎯 Adaptive Spacing Details:")
                
                # Show auto-optimization results if applicable
                if spacing_analysis.get('mode') == 'auto':
                    debug_lines.append(f"   🚀 AUTO-OPTIMIZATION MODE:")
                    debug_lines.append(f"      Final spacing_y: {spacing_analysis['final_spacing_y']:.1f}px (auto-calculated)")
                    
                    # Show horizontal spacing mode
                    if spacing_analysis.get('spacing_x_mode') == 'auto':
                        debug_lines.append(f"      Horizontal spacing: AUTO (component width + {spacing_analysis.get('base_margin', 50)}px margin)")
                        debug_lines.append(f"\n      Layer widths:")
                        for layer_num, width in spacing_analysis.get('layer_widths', {}).items():
                            debug_lines.append(f"         Layer {layer_num}: {width:.0f}px")
                    else:
                        debug_lines.append(f"      Horizontal spacing: {spacing_analysis.get('spacing_x', 200)}px (fixed)")
                    
                    debug_lines.append(f"\n      Layer analysis:")
                    for detail in spacing_analysis.get('details', []):
                        param_pct = detail['param_ratio'] * 100
                        debug_lines.append(f"      Layer {detail['layer']}: {detail['comps']} comps, "
                                         f"avg_h={detail['avg_height']:.0f}px, "
                                         f"params={param_pct:.0f}%, "
                                         f"optimal={detail['optimal_spacing']:.0f}px")
                else:
                    debug_lines.append(f"   👤 MANUAL MODE: spacing_y={spacing_analysis.get('final_spacing_y', 0):.1f}px (user-provided)")
                
                # Count spacing types
                param_count = sum(1 for s in spacing_debug if s['type'] == 'param')
                reduced_count = sum(1 for s in spacing_debug if s['type'] == 'reduced')
                adjusted_count = sum(1 for s in spacing_debug if s['adjustment'])
                
                debug_lines.append(f"\n   Applied Spacing:")
                debug_lines.append(f"      • Parameter spacing: {param_count} pairs (60px min)")
                debug_lines.append(f"      • Regular spacing: {reduced_count} pairs (40px min)")
                debug_lines.append(f"      • Position adjustments: {adjusted_count}")
                
                debug_lines.append(f"\n   Spacing breakdown by layer:")
                for layer_num in sorted(set(s['layer'] for s in spacing_debug)):
                    layer_spacings = [s for s in spacing_debug if s['layer'] == layer_num]
                    debug_lines.append(f"   Layer {layer_num}:")
                    for s in layer_spacings[:5]:  # Show first 5 per layer
                        param_marker = ""
                        if s['prev_is_param']:
                            param_marker += "[P]"
                        if s['comp_is_param']:
                            param_marker += "[P]"
                        
                        spacing_str = f"{s['spacing']:.0f}px ({s['type']})"
                        debug_lines.append(f"      {s['prev']} → {s['comp']}: {spacing_str} {param_marker}{s['adjustment']}")
                    
                    if len(layer_spacings) > 5:
                        debug_lines.append(f"      ... and {len(layer_spacings)-5} more")
            
            # Create result message with mode indicator
            mode_indicator = "🚀 AUTO" if spacing_analysis.get('mode') == 'auto' else "👤 MANUAL"
            result_msg = f"✅ [{mode_indicator}] Smart aligned {len(selected)} components into {num_layers} layers\n"
            result_msg += '\n'.join(debug_lines)
            return result_msg
        except Exception as e:
            return f"Parameter-based alignment failed: {str(e)}"
    
    def get_fix_suggestions(self):
        """Get actionable fix suggestions for all issues"""
        try:
            # Ensure document is scanned and checked
            if not self.components:
                self.scan_document()
            if not self.issues:
                self.run_all_checks()
            
            suggestions = []
            
            for issue in self.issues:
                if issue['rule_id'] == 'GH001':
                    suggestions.append({
                        'issue': 'Dangling Inputs',
                        'action': 'Connect required inputs or set default values',
                        'auto_fix': False
                    })
                elif issue['rule_id'] == 'GH002':
                    suggestions.append({
                        'issue': 'Dangling Outputs',
                        'action': 'Use outputs or remove unnecessary components',
                        'auto_fix': False
                    })
                elif issue['rule_id'] == 'GH003':
                    suggestions.append({
                        'issue': 'Unnamed Parameters',
                        'action': 'Run auto_name_parameters() to name them',
                        'auto_fix': True,
                        'auto_fix_command': 'analyzer.auto_name_parameters()'
                    })
                elif issue['rule_id'] == 'GH004':
                    suggestions.append({
                        'issue': 'Missing Groups',
                        'action': 'Select related components and press Ctrl+G',
                        'auto_fix': False
                    })
            
            return suggestions
        except Exception as e:
            return [{'issue': 'Suggestion generation failed', 'action': str(e), 'auto_fix': False}]

    # ==================== PERFORMANCE PROFILING METHODS ====================

    def profile_document(self, mode='quick', iterations=1):
        """
        Profile component execution times in the current document

        Args:
            mode: 'quick' (single pass) or 'detailed' (multiple iterations with averaging)
            iterations: Number of profiling passes (used in 'detailed' mode)

        Returns:
            Dictionary with component timing data:
            {
                'component_guid': {
                    'name': str,
                    'avg_time_ms': float,
                    'times': [float, ...],
                    'category': str,
                    'type': str
                },
                ...
            }
        """
        try:
            import time

            # Ensure document is scanned
            if not self.components:
                self.scan_document()

            if mode == 'detailed':
                actual_iterations = max(1, min(iterations, 10))  # Cap at 10
            else:
                actual_iterations = 1

            component_times = {}

            for comp in self.components:
                try:
                    guid = str(comp.InstanceGuid)
                    comp_name = comp.NickName if hasattr(comp, 'NickName') and comp.NickName else 'Unnamed'
                    comp_type = comp.GetType().Name if hasattr(comp, 'GetType') else 'Unknown'
                    comp_category = comp.Category if hasattr(comp, 'Category') else 'Unknown'

                    times = []

                    for _ in range(actual_iterations):
                        # Measure solution time
                        start_time = time.time()

                        try:
                            # Trigger recomputation
                            if hasattr(comp, 'ExpireSolution'):
                                comp.ExpireSolution(False)

                            # Force recompute by calling ComputeData if available
                            if hasattr(comp, 'ComputeData'):
                                comp.ComputeData()
                        except:
                            pass

                        elapsed = (time.time() - start_time) * 1000  # Convert to ms
                        times.append(elapsed)

                    # Calculate average
                    avg_time = sum(times) / len(times) if times else 0

                    component_times[guid] = {
                        'name': comp_name,
                        'avg_time_ms': avg_time,
                        'times': times,
                        'category': comp_category,
                        'type': comp_type,
                        'component': comp
                    }

                except Exception as e:
                    continue

            return component_times

        except Exception as e:
            return {'error': str(e)}

    def get_component_execution_times(self):
        """
        Get cached or fresh execution time data for all components
        Wrapper around profile_document() for simple access
        """
        return self.profile_document(mode='quick', iterations=1)

    def find_performance_bottlenecks(self, threshold_ms=100, top_n=10):
        """
        Identify performance bottlenecks in the document

        Args:
            threshold_ms: Minimum execution time to be considered "slow" (ms)
            top_n: Number of slowest components to return

        Returns:
            List of bottleneck dictionaries sorted by execution time (slowest first)
        """
        try:
            timing_data = self.get_component_execution_times()

            if 'error' in timing_data:
                return []

            # Filter and sort by execution time
            slow_components = []
            total_time = sum(data['avg_time_ms'] for data in timing_data.values())

            for guid, data in timing_data.items():
                if data['avg_time_ms'] >= threshold_ms:
                    percentage = (data['avg_time_ms'] / total_time * 100) if total_time > 0 else 0

                    slow_components.append({
                        'guid': guid,
                        'name': data['name'],
                        'time_ms': data['avg_time_ms'],
                        'percentage': percentage,
                        'category': data['category'],
                        'type': data['type'],
                        'component': data['component']
                    })

            # Sort by time (descending)
            slow_components.sort(key=lambda x: x['time_ms'], reverse=True)

            return slow_components[:top_n]

        except Exception as e:
            return []

    def analyze_performance_patterns(self):
        """
        Analyze performance patterns and identify common issues

        Returns:
            Dictionary with pattern analysis:
            {
                'by_category': {...},
                'by_plugin': {...},
                'heavy_preview': [...],
                'data_tree_ops': [...],
                'script_components': [...]
            }
        """
        try:
            timing_data = self.get_component_execution_times()

            if 'error' in timing_data:
                return {}

            # Analyze by category
            by_category = {}
            for data in timing_data.values():
                cat = data['category']
                if cat not in by_category:
                    by_category[cat] = {'total_time': 0, 'count': 0}
                by_category[cat]['total_time'] += data['avg_time_ms']
                by_category[cat]['count'] += 1

            # Identify heavy preview components
            heavy_preview = []
            for guid, data in timing_data.items():
                comp = data['component']
                if hasattr(comp, 'Hidden') and not comp.Hidden:
                    # Component has preview enabled
                    if data['avg_time_ms'] > 50:  # Arbitrary threshold
                        heavy_preview.append({
                            'guid': guid,
                            'name': data['name'],
                            'time_ms': data['avg_time_ms']
                        })

            # Identify data tree operations (Flatten, Graft, Simplify)
            data_tree_ops = []
            tree_op_types = ['Flatten', 'Graft', 'Simplify', 'Flip']
            for guid, data in timing_data.items():
                if any(op in data['type'] for op in tree_op_types):
                    if data['avg_time_ms'] > 10:
                        data_tree_ops.append({
                            'guid': guid,
                            'name': data['name'],
                            'type': data['type'],
                            'time_ms': data['avg_time_ms']
                        })

            # Identify script components (Python, C#)
            script_components = []
            script_types = ['Python', 'CSharp', 'Script']
            for guid, data in timing_data.items():
                if any(s in data['type'] or s in data['category'] for s in script_types):
                    script_components.append({
                        'guid': guid,
                        'name': data['name'],
                        'type': data['type'],
                        'time_ms': data['avg_time_ms']
                    })

            return {
                'by_category': by_category,
                'heavy_preview': heavy_preview,
                'data_tree_ops': data_tree_ops,
                'script_components': script_components
            }

        except Exception as e:
            return {'error': str(e)}

    def get_plugin_performance_breakdown(self):
        """
        Get performance breakdown by plugin/namespace

        Returns:
            Dictionary mapping plugin names to timing data
        """
        try:
            timing_data = self.get_component_execution_times()

            if 'error' in timing_data:
                return {}

            by_plugin = {}

            for data in timing_data.values():
                # Try to extract plugin name from type
                comp_type = data['type']
                plugin_name = 'Rhino Core'

                if 'Python' in comp_type or 'GhPython' in comp_type:
                    plugin_name = 'GhPython'
                elif 'CSharp' in comp_type:
                    plugin_name = 'C# Script'
                elif 'Mesh' in data['category']:
                    plugin_name = 'Mesh Tools'
                elif comp_type.startswith('GH_'):
                    plugin_name = 'Grasshopper'
                else:
                    # Try to get namespace
                    if hasattr(data['component'], 'GetType'):
                        full_type = data['component'].GetType().FullName
                        if '.' in full_type:
                            plugin_name = full_type.split('.')[0]

                if plugin_name not in by_plugin:
                    by_plugin[plugin_name] = {'total_time': 0, 'count': 0, 'components': []}

                by_plugin[plugin_name]['total_time'] += data['avg_time_ms']
                by_plugin[plugin_name]['count'] += 1
                by_plugin[plugin_name]['components'].append({
                    'name': data['name'],
                    'time_ms': data['avg_time_ms']
                })

            return by_plugin

        except Exception as e:
            return {'error': str(e)}

    def calculate_performance_score(self):
        """
        Calculate overall performance score (0-100, higher is better)

        Scoring criteria:
        - Average component time < 10ms: +40 points
        - Slow components (>100ms) < 5: +30 points
        - Total execution time < 1000ms: +30 points
        """
        try:
            timing_data = self.get_component_execution_times()

            if 'error' in timing_data or not timing_data:
                return 0

            score = 0

            # Calculate metrics
            total_time = sum(data['avg_time_ms'] for data in timing_data.values())
            avg_time = total_time / len(timing_data) if timing_data else 0
            slow_count = sum(1 for data in timing_data.values() if data['avg_time_ms'] > 100)

            # Criterion 1: Average component time
            if avg_time < 5:
                score += 40
            elif avg_time < 10:
                score += 30
            elif avg_time < 20:
                score += 20
            elif avg_time < 50:
                score += 10

            # Criterion 2: Slow components
            if slow_count == 0:
                score += 30
            elif slow_count < 3:
                score += 25
            elif slow_count < 5:
                score += 20
            elif slow_count < 10:
                score += 10

            # Criterion 3: Total execution time
            if total_time < 500:
                score += 30
            elif total_time < 1000:
                score += 25
            elif total_time < 2000:
                score += 15
            elif total_time < 5000:
                score += 5

            return min(100, max(0, score))

        except Exception as e:
            return 0

    def generate_performance_report(self, style='full'):
        """
        Generate formatted performance report

        Args:
            style: 'simple', 'compact', or 'full'

        Returns:
            Formatted string report
        """
        try:
            timing_data = self.get_component_execution_times()

            if 'error' in timing_data:
                return "Performance profiling failed: " + timing_data['error']

            if not timing_data:
                return "No components found to profile"

            # Calculate metrics
            total_time = sum(data['avg_time_ms'] for data in timing_data.values())
            avg_time = total_time / len(timing_data) if timing_data else 0
            bottlenecks = self.find_performance_bottlenecks(threshold_ms=100, top_n=10)
            patterns = self.analyze_performance_patterns()
            plugin_breakdown = self.get_plugin_performance_breakdown()
            perf_score = self.calculate_performance_score()

            lines = []

            if style == 'simple':
                lines.append(f"Performance Score: {perf_score}/100")
                lines.append(f"Total Time: {total_time:.0f}ms | Avg: {avg_time:.1f}ms/component")
                lines.append(f"Slow Components (>100ms): {len(bottlenecks)}")

            elif style == 'compact':
                lines.append("=== PERFORMANCE PROFILE ===")
                lines.append(f"Score: {perf_score}/100")
                lines.append(f"Components: {len(timing_data)} | Total: {total_time:.0f}ms | Avg: {avg_time:.1f}ms")
                lines.append("")
                lines.append(f"Top 5 Slowest:")
                for i, b in enumerate(bottlenecks[:5], 1):
                    lines.append(f"  {i}. {b['name']}: {b['time_ms']:.0f}ms ({b['percentage']:.1f}%)")

            else:  # full
                lines.append("=" * 60)
                lines.append("GRASSHOPPER PERFORMANCE PROFILE")
                lines.append("=" * 60)
                lines.append("")
                lines.append(f"⚡ PERFORMANCE SCORE: {perf_score}/100")
                lines.append(f"   (Higher is better. Target: >80)")
                lines.append("")
                lines.append(f"📊 OVERVIEW:")
                lines.append(f"   Total Components: {len(timing_data)}")
                lines.append(f"   Total Execution Time: {total_time:.0f}ms")
                lines.append(f"   Average Time per Component: {avg_time:.1f}ms")
                lines.append("")

                # Bottlenecks
                if bottlenecks:
                    lines.append(f"🐌 TOP {min(10, len(bottlenecks))} SLOWEST COMPONENTS:")
                    for i, b in enumerate(bottlenecks, 1):
                        lines.append(f"  {i}. [{b['percentage']:.1f}%] {b['name']} - {b['time_ms']:.0f}ms")
                        lines.append(f"      Category: {b['category']} | Type: {b['type']}")
                    lines.append("")

                # Category breakdown
                if patterns.get('by_category'):
                    lines.append("📊 BY CATEGORY:")
                    sorted_cats = sorted(patterns['by_category'].items(),
                                       key=lambda x: x[1]['total_time'], reverse=True)
                    for cat, data in sorted_cats[:5]:
                        pct = (data['total_time'] / total_time * 100) if total_time > 0 else 0
                        lines.append(f"   {cat}: {data['total_time']:.0f}ms ({pct:.1f}%) - {data['count']} components")
                    lines.append("")

                # Plugin breakdown
                if plugin_breakdown:
                    lines.append("📊 BY PLUGIN:")
                    sorted_plugins = sorted(plugin_breakdown.items(),
                                          key=lambda x: x[1]['total_time'], reverse=True)
                    for plugin, data in sorted_plugins:
                        if 'error' not in data:
                            pct = (data['total_time'] / total_time * 100) if total_time > 0 else 0
                            lines.append(f"   {plugin}: {data['total_time']:.0f}ms ({pct:.1f}%)")
                    lines.append("")

                # Performance warnings
                warnings = []
                if len(bottlenecks) > 5:
                    warnings.append(f"{len(bottlenecks)} components exceed 100ms threshold")
                if patterns.get('heavy_preview') and len(patterns['heavy_preview']) > 5:
                    warnings.append(f"{len(patterns['heavy_preview'])} heavy preview geometries")
                if patterns.get('data_tree_ops') and len(patterns['data_tree_ops']) > 10:
                    warnings.append(f"{len(patterns['data_tree_ops'])} data tree operations")

                if warnings:
                    lines.append("⚠️ PERFORMANCE WARNINGS:")
                    for w in warnings:
                        lines.append(f"   • {w}")
                    lines.append("")

                lines.append("=" * 60)

            return '\n'.join(lines)

        except Exception as e:
            return f"Performance report generation failed: {str(e)}"

    def highlight_slow_components(self, threshold_ms=100):
        """
        Select slow components in the canvas for easy identification

        Args:
            threshold_ms: Minimum execution time to be considered "slow"

        Returns:
            Number of components highlighted
        """
        try:
            bottlenecks = self.find_performance_bottlenecks(threshold_ms=threshold_ms, top_n=999)

            if not bottlenecks:
                return 0

            # Deselect all first
            for comp in self.components:
                if hasattr(comp, 'Attributes'):
                    comp.Attributes.Selected = False

            # Select slow components
            count = 0
            for b in bottlenecks:
                comp = b['component']
                if hasattr(comp, 'Attributes'):
                    comp.Attributes.Selected = True
                    count += 1

            # Refresh canvas
            if hasattr(gh.Instances, 'ActiveCanvas') and gh.Instances.ActiveCanvas:
                gh.Instances.ActiveCanvas.Refresh()

            return count

        except Exception as e:
            return 0

    def get_optimization_suggestions(self):
        """
        Generate specific optimization suggestions based on performance analysis

        Returns:
            List of suggestion dictionaries
        """
        try:
            bottlenecks = self.find_performance_bottlenecks(threshold_ms=100, top_n=5)
            patterns = self.analyze_performance_patterns()

            suggestions = []

            # Suggestions for slow components
            for b in bottlenecks:
                suggestion = {
                    'component': b['name'],
                    'issue': f"Slow execution ({b['time_ms']:.0f}ms)",
                    'suggestions': []
                }

                # Type-specific suggestions
                if 'Python' in b['type'] or 'Script' in b['type']:
                    suggestion['suggestions'].extend([
                        "Profile internal loops for optimization",
                        "Consider caching results if inputs rarely change",
                        "Check for redundant calculations",
                        "Consider moving to compiled GHPython"
                    ])
                elif 'Mesh' in b['category'] or 'Boolean' in b['type']:
                    suggestion['suggestions'].extend([
                        "Reduce input mesh complexity before operations",
                        "Check for overlapping/duplicate meshes",
                        "Consider splitting into smaller operations"
                    ])
                elif 'Brep' in b['type'] or 'Intersection' in b['type']:
                    suggestion['suggestions'].extend([
                        "Simplify geometry before intersection",
                        "Check for unnecessary intersections",
                        "Consider using bounding box tests first"
                    ])
                else:
                    suggestion['suggestions'].append("Review component logic for optimization opportunities")

                suggestions.append(suggestion)

            # Suggestions for heavy preview
            if patterns.get('heavy_preview') and len(patterns['heavy_preview']) > 5:
                suggestions.append({
                    'component': 'Multiple components',
                    'issue': f"{len(patterns['heavy_preview'])} heavy preview geometries",
                    'suggestions': [
                        "Disable preview on heavy geometry components",
                        "Use 'Preview Off' for intermediate calculations",
                        "Consider using Custom Preview only where needed"
                    ]
                })

            # Suggestions for data tree operations
            if patterns.get('data_tree_ops') and len(patterns['data_tree_ops']) > 10:
                suggestions.append({
                    'component': 'Data tree operations',
                    'issue': f"{len(patterns['data_tree_ops'])} tree operations detected",
                    'suggestions': [
                        "Review data structure design to minimize tree operations",
                        "Consider restructuring data flow to avoid excessive Flatten/Graft",
                        "Use Path Mapper for complex tree transformations"
                    ]
                })

            return suggestions

        except Exception as e:
            return [{'component': 'Error', 'issue': str(e), 'suggestions': []}]


# ==================== HELPER FUNCTIONS ====================

def quick_check():
    """Quick health check - for use in GH Python component"""
    try:
        analyzer = GHLiveAnalyzer()
        return analyzer.format_report(style='compact')
    except Exception as e:
        return "Quick check failed: " + str(e) + "\n\nTry checking:\n- Grasshopper version compatibility\n- Document is open and active\n- Component is connected properly"


def full_analysis():
    """Full analysis - for use in GH Python component"""
    try:
        analyzer = GHLiveAnalyzer()
        return analyzer.format_report(style='full')
    except Exception as e:
        return "Full analysis failed: " + str(e) + "\n\nTry checking:\n- Grasshopper version compatibility\n- Document is open and active\n- Component is connected properly"


def get_health_score():
    """Get just the health score"""
    try:
        analyzer = GHLiveAnalyzer()
        analyzer.run_all_checks()
        return analyzer.calculate_health_score()
    except Exception as e:
        return -1


def safe_analysis():
    """Safe analysis with basic fallback"""
    try:
        analyzer = GHLiveAnalyzer()
        stats = analyzer.get_statistics()
        
        if stats.get('scan_error'):
            return "Analysis completed with warnings:\n" + stats['scan_error'] + "\n\nBasic stats:\nComponents: " + str(stats['total_components']) + "\nWires: " + str(stats['total_wires']) + "\nGroups: " + str(stats['total_groups'])
        else:
            return analyzer.format_report(style='compact')
    except Exception as e:
        return "Analysis failed: " + str(e) + "\n\nPlease verify:\n1. Grasshopper document is open\n2. Python component is properly connected\n3. No circular references in definition"
