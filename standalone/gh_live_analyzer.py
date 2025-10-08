"""
Grasshopper Live Analyzer - Standalone Version
Analyzes the current open GH definition without requiring external tools
For use directly in Grasshopper Python components

Author: Soku
Version: 1.0.0
"""

import Grasshopper as gh
import Grasshopper.Kernel as ghk
from Grasshopper.Kernel.Special import GH_NumberSlider, GH_Panel, GH_BooleanToggle
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
        if gh_doc:
            self.doc = gh_doc
        else:
            # Get active Grasshopper document from the component running this code
            import Grasshopper as gh
            self.doc = gh.Instances.ActiveCanvas.Document
        if not self.doc:
            raise Exception("No active Grasshopper document found!")
        
        self.components = []
        self.wires = []
        self.groups = []
        self.issues = []
        
    def scan_document(self):
        """Scan the current document and collect all objects"""
        self.components = []
        self.wires = []
        self.groups = []
        
        # Get all objects
        for obj in self.doc.Objects:
            if isinstance(obj, ghk.IGH_Component):
                self.components.append(obj)
            elif isinstance(obj, ghk.Special.GH_Group):
                self.groups.append(obj)
        
        # Count wires
        for comp in self.components:
            for param in comp.Params.Output:
                self.wires.extend(param.Recipients)
        
        return {
            'components': len(self.components),
            'wires': len(self.wires),
            'groups': len(self.groups)
        }
    
    def get_statistics(self):
        """Get document statistics"""
        stats = self.scan_document()
        
        # Count by category
        by_category = {}
        by_exposure = {}
        param_types = {}
        
        for comp in self.components:
            # Category
            cat = comp.Category if hasattr(comp, 'Category') else 'Unknown'
            by_category[cat] = by_category.get(cat, 0) + 1
            
            # Exposure
            exp = str(comp.Exposure) if hasattr(comp, 'Exposure') else 'Unknown'
            by_exposure[exp] = by_exposure.get(exp, 0) + 1
            
            # Parameter types
            if self._is_param_component(comp):
                type_name = comp.GetType().Name
                param_types[type_name] = param_types.get(type_name, 0) + 1
        
        return {
            'total_components': stats['components'],
            'total_wires': stats['wires'],
            'total_groups': stats['groups'],
            'by_category': by_category,
            'by_exposure': by_exposure,
            'param_types': param_types
        }
    
    def _is_param_component(self, comp):
        """Check if component is a parameter"""
        param_types = (
            GH_NumberSlider,
            GH_Panel,
            GH_BooleanToggle,
            ghk.Special.GH_ValueList
        )
        return isinstance(comp, param_types)
    
    # ==================== LINT CHECKS ====================
    
    def check_dangling_inputs(self):
        """GH001: Find inputs that are not connected"""
        issues = []
        
        for comp in self.components:
            if not isinstance(comp, ghk.IGH_Component):
                continue
            
            for param in comp.Params.Input:
                if param.SourceCount == 0 and not param.Optional:
                    issues.append({
                        'component_name': comp.Name,
                        'component_guid': str(comp.InstanceGuid),
                        'input_name': param.Name,
                        'position': [comp.Attributes.Pivot.X, comp.Attributes.Pivot.Y],
                        'component': comp  # Keep reference for auto-fix
                    })
        
        return issues
    
    def check_dangling_outputs(self):
        """GH002: Find outputs that are not connected"""
        issues = []
        
        for comp in self.components:
            if not isinstance(comp, ghk.IGH_Component):
                continue
            
            for param in comp.Params.Output:
                if param.Recipients.Count == 0:
                    issues.append({
                        'component_name': comp.Name,
                        'component_guid': str(comp.InstanceGuid),
                        'output_name': param.Name,
                        'position': [comp.Attributes.Pivot.X, comp.Attributes.Pivot.Y],
                        'component': comp
                    })
        
        return issues
    
    def check_unnamed_parameters(self):
        """GH003: Find parameters without custom names"""
        issues = []
        default_names = ['Number Slider', 'Panel', 'Boolean Toggle', 'Value List', 'Slider']
        
        for comp in self.components:
            if self._is_param_component(comp):
                # Check if name is default/generic
                if comp.NickName in default_names or comp.NickName == comp.Name:
                    issues.append({
                        'type': comp.GetType().Name,
                        'current_name': comp.NickName,
                        'guid': str(comp.InstanceGuid),
                        'position': [comp.Attributes.Pivot.X, comp.Attributes.Pivot.Y],
                        'component': comp
                    })
        
        return issues
    
    def check_disabled_components(self):
        """Find components that are disabled"""
        issues = []
        
        for comp in self.components:
            if hasattr(comp.Attributes, 'Enabled') and not comp.Attributes.Enabled:
                issues.append({
                    'component_name': comp.Name,
                    'guid': str(comp.InstanceGuid),
                    'position': [comp.Attributes.Pivot.X, comp.Attributes.Pivot.Y],
                    'component': comp
                })
        
        return issues
    
    def check_components_with_errors(self):
        """Find components with runtime errors"""
        issues = []
        
        for comp in self.components:
            if isinstance(comp, ghk.IGH_ActiveObject):
                if comp.RuntimeMessageLevel == ghk.GH_RuntimeMessageLevel.Error:
                    messages = []
                    for msg in comp.RuntimeMessages(ghk.GH_RuntimeMessageLevel.Error):
                        messages.append(str(msg))
                    
                    issues.append({
                        'component_name': comp.Name,
                        'guid': str(comp.InstanceGuid),
                        'errors': messages,
                        'position': [comp.Attributes.Pivot.X, comp.Attributes.Pivot.Y],
                        'component': comp
                    })
        
        return issues
    
    def check_components_with_warnings(self):
        """Find components with runtime warnings"""
        issues = []
        
        for comp in self.components:
            if isinstance(comp, ghk.IGH_ActiveObject):
                if comp.RuntimeMessageLevel == ghk.GH_RuntimeMessageLevel.Warning:
                    messages = []
                    for msg in comp.RuntimeMessages(ghk.GH_RuntimeMessageLevel.Warning):
                        messages.append(str(msg))
                    
                    issues.append({
                        'component_name': comp.Name,
                        'guid': str(comp.InstanceGuid),
                        'warnings': messages,
                        'position': [comp.Attributes.Pivot.X, comp.Attributes.Pivot.Y],
                        'component': comp
                    })
        
        return issues
    
    def check_missing_groups(self):
        """GH004: Check if definition needs organization"""
        if len(self.components) > 10 and len(self.groups) == 0:
            return [{
                'message': f"Definition has {len(self.components)} components but no groups",
                'recommendation': "Consider organizing into logical groups"
            }]
        return []
    
    def check_preview_disabled(self):
        """GH012: Find components with preview disabled"""
        issues = []
        
        for comp in self.components:
            if hasattr(comp.Attributes, 'GetTopLevel'):
                attrs = comp.Attributes.GetTopLevel
                if hasattr(attrs, 'Hidden') and attrs.Hidden:
                    issues.append({
                        'component_name': comp.Name,
                        'guid': str(comp.InstanceGuid),
                        'position': [comp.Attributes.Pivot.X, comp.Attributes.Pivot.Y],
                        'component': comp
                    })
        
        return issues
    
    def run_all_checks(self):
        """Run all lint checks and return results"""
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
            results = check_func()
            if results:
                self.issues.append({
                    'rule_id': rule_id,
                    'severity': severity,
                    'title': title,
                    'count': len(results),
                    'items': results
                })
        
        return self.issues
    
    def calculate_health_score(self):
        """Calculate definition health score (0-100)"""
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
    
    def format_report(self, style='full'):
        """
        Format analysis report
        style: 'full', 'compact', 'simple'
        """
        if not self.issues:
            self.run_all_checks()
        
        if style == 'simple':
            return self._format_simple_report()
        elif style == 'compact':
            return self._format_compact_report()
        else:
            return self._format_full_report()
    
    def _format_simple_report(self):
        """Simple one-liner report"""
        stats = self.get_statistics()
        score = self.calculate_health_score()
        
        error_count = sum(1 for i in self.issues if i['severity'] == 'error')
        warning_count = sum(1 for i in self.issues if i['severity'] == 'warning')
        
        if score >= 90:
            status = "✅ Excellent"
        elif score >= 70:
            status = "👍 Good"
        elif score >= 50:
            status = "⚠️ Needs Attention"
        else:
            status = "❌ Critical"
        
        return f"{status} | Score: {score}/100 | Components: {stats['total_components']} | Errors: {error_count} | Warnings: {warning_count}"
    
    def _format_compact_report(self):
        """Compact report for panel display"""
        lines = []
        stats = self.get_statistics()
        score = self.calculate_health_score()
        
        lines.append("=" * 50)
        lines.append("GRASSHOPPER HEALTH CHECK")
        lines.append("=" * 50)
        lines.append("")
        lines.append(f"📊 Score: {score}/100")
        lines.append(f"🔧 Components: {stats['total_components']}")
        lines.append(f"🔗 Connections: {stats['total_wires']}")
        lines.append(f"📁 Groups: {stats['total_groups']}")
        lines.append("")
        
        if not self.issues:
            lines.append("✅ No issues found!")
        else:
            lines.append(f"Found {len(self.issues)} issue types:")
            lines.append("")
            
            for issue in self.issues:
                icon = {'error': '❌', 'warning': '⚠️', 'info': 'ℹ️'}.get(issue['severity'], '•')
                lines.append(f"{icon} {issue['title']}: {issue['count']}")
        
        lines.append("")
        lines.append("=" * 50)
        
        return "\n".join(lines)
    
    def _format_full_report(self):
        """Full detailed report"""
        lines = []
        stats = self.get_statistics()
        score = self.calculate_health_score()
        
        lines.append("=" * 60)
        lines.append("GRASSHOPPER DEFINITION ANALYSIS")
        lines.append("=" * 60)
        lines.append("")
        
        # Header
        lines.append(f"📄 Document: {self.doc.DisplayName}")
        lines.append(f"📊 Health Score: {score}/100")
        lines.append("")
        
        # Statistics
        lines.append("📈 Statistics:")
        lines.append(f"   Components: {stats['total_components']}")
        lines.append(f"   Connections: {stats['total_wires']}")
        lines.append(f"   Groups: {stats['total_groups']}")
        lines.append("")
        
        # Component breakdown
        lines.append("🔧 Components by Category:")
        for cat, count in sorted(stats['by_category'].items(), key=lambda x: x[1], reverse=True)[:5]:
            lines.append(f"   {cat}: {count}")
        lines.append("")
        
        # Issues
        if not self.issues:
            lines.append("✅ No issues found! Great work!")
        else:
            lines.append(f"⚠️  Found {len(self.issues)} issue types:")
            lines.append("")
            
            for issue in self.issues:
                icon = {'error': '❌', 'warning': '⚠️', 'info': 'ℹ️'}.get(issue['severity'], '•')
                
                lines.append(f"{icon} {issue['rule_id']}: {issue['title']} [{issue['severity'].upper()}]")
                lines.append(f"   Count: {issue['count']}")
                
                # Show examples
                for item in issue['items'][:3]:
                    if 'component_name' in item:
                        name = item.get('component_name', 'Unknown')
                        if 'input_name' in item:
                            lines.append(f"   • {name} → input '{item['input_name']}'")
                        elif 'output_name' in item:
                            lines.append(f"   • {name} → output '{item['output_name']}'")
                        else:
                            lines.append(f"   • {name}")
                    elif 'type' in item:
                        lines.append(f"   • {item['type']} ('{item.get('current_name', '')}')")
                    elif 'message' in item:
                        lines.append(f"   • {item['message']}")
                
                if issue['count'] > 3:
                    lines.append(f"   ... and {issue['count'] - 3} more")
                
                lines.append("")
        
        # Summary
        error_count = sum(1 for i in self.issues if i['severity'] == 'error')
        warning_count = sum(1 for i in self.issues if i['severity'] == 'warning')
        info_count = sum(1 for i in self.issues if i['severity'] == 'info')
        
        lines.append("📊 Summary:")
        lines.append(f"   Errors: {error_count}")
        lines.append(f"   Warnings: {warning_count}")
        lines.append(f"   Info: {info_count}")
        lines.append("")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    # ==================== AUTO-FIX FUNCTIONS ====================
    
    def highlight_issues(self, issue_type=None):
        """Select components with issues in the canvas"""
        if not self.issues:
            self.run_all_checks()
        
        # Deselect all first
        self.doc.DeselectAll()
        
        # Select components with issues
        for issue in self.issues:
            if issue_type and issue['rule_id'] != issue_type:
                continue
            
            for item in issue['items']:
                if 'component' in item:
                    comp = item['component']
                    comp.Attributes.Selected = True
        
        self.doc.Canvas.Refresh()
        return f"Highlighted {sum(i['count'] for i in self.issues if not issue_type or i['rule_id'] == issue_type)} issues"
    
    def auto_name_parameters(self, prefix="Param"):
        """Automatically name unnamed parameters"""
        unnamed = self.check_unnamed_parameters()
        
        counter = 1
        for item in unnamed:
            comp = item['component']
            new_name = f"{prefix}_{counter:02d}"
            comp.NickName = new_name
            counter += 1
        
        if unnamed:
            self.doc.NewSolution(False)
        
        return f"Named {len(unnamed)} parameters"
    
    def create_suggested_groups(self):
        """Suggest and create logical groups based on component proximity"""
        # This would need more complex logic to cluster components
        # For now, just return suggestion
        return "Group creation requires manual selection"
    
    def get_fix_suggestions(self):
        """Get actionable fix suggestions for all issues"""
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


# ==================== HELPER FUNCTIONS ====================

def quick_check():
    """Quick health check - for use in GH Python component"""
    try:
        analyzer = GHLiveAnalyzer()
        return analyzer.format_report(style='compact')
    except Exception as e:
        return f"Error: {str(e)}"


def full_analysis():
    """Full analysis - for use in GH Python component"""
    try:
        analyzer = GHLiveAnalyzer()
        return analyzer.format_report(style='full')
    except Exception as e:
        return f"Error: {str(e)}"


def get_health_score():
    """Get just the health score"""
    try:
        analyzer = GHLiveAnalyzer()
        analyzer.run_all_checks()
        return analyzer.calculate_health_score()
    except Exception as e:
        return -1
