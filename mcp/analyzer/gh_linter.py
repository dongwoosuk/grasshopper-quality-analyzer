"""
Grasshopper Linter
Applies lint rules to GH definition JSON
"""
import json
from typing import List, Dict, Any
from .lint_rules import LINT_RULES, SEVERITY_LEVELS
from .gh_analyzer import GHAnalyzer


class GHLinter:
    """Lints Grasshopper definitions against quality rules"""
    
    def __init__(self, json_path: str):
        self.analyzer = GHAnalyzer(json_path)
        self.issues = []
    
    def lint_all(self) -> List[Dict[str, Any]]:
        """Run all lint checks"""
        self.issues = []
        
        # GH001: Dangling inputs
        dangling_in = self.analyzer.find_dangling_inputs()
        if dangling_in:
            self.issues.append({
                "rule": LINT_RULES["dangling_inputs"],
                "count": len(dangling_in),
                "items": dangling_in
            })
        
        # GH002: Dangling outputs
        dangling_out = self.analyzer.find_dangling_outputs()
        if dangling_out:
            self.issues.append({
                "rule": LINT_RULES["dangling_outputs"],
                "count": len(dangling_out),
                "items": dangling_out
            })
        
        # GH003: Unnamed parameters
        unnamed = self.analyzer.find_unnamed_params()
        if unnamed:
            self.issues.append({
                "rule": LINT_RULES["unnamed_params"],
                "count": len(unnamed),
                "items": unnamed
            })
        
        # GH004: Missing groups
        has_groups = any(c.get('group') for c in self.analyzer.components)
        if not has_groups and len(self.analyzer.components) > 10:
            self.issues.append({
                "rule": LINT_RULES["missing_groups"],
                "count": 1,
                "items": [{"message": "Definition has no groups"}]
            })
        
        # GH011: Plugin dependencies
        plugins = self.analyzer.get_plugin_usage()
        non_core_plugins = [p for p in plugins if p.get('category') not in ['', 'Params', 'Maths', 'Sets', 'Vector', 'Curve', 'Surface', 'Mesh', 'Intersect', 'Transform', 'Display']]
        if non_core_plugins:
            self.issues.append({
                "rule": LINT_RULES["plugin_dependencies"],
                "count": len(non_core_plugins),
                "items": [{"plugin": f"{p['category']}/{p['subcategory']}"} for p in non_core_plugins]
            })
        
        # Sort by severity
        self.issues.sort(key=lambda x: SEVERITY_LEVELS.get(x['rule']['severity'], 0), reverse=True)
        
        return self.issues
    
    def get_top_issues(self, n: int = 5) -> List[Dict[str, Any]]:
        """Get top N most important issues"""
        if not self.issues:
            self.lint_all()
        return self.issues[:n]
    
    def generate_lint_report(self) -> str:
        """Generate a formatted lint report"""
        if not self.issues:
            self.lint_all()
        
        report = []
        report.append("=" * 60)
        report.append("GRASSHOPPER LINT REPORT")
        report.append("=" * 60)
        report.append("")
        
        if not self.issues:
            report.append("✅ No issues found! Great job!")
            report.append("")
        else:
            report.append(f"Found {len(self.issues)} issue types:")
            report.append("")
            
            for issue in self.issues:
                rule = issue['rule']
                count = issue['count']
                items = issue['items']
                
                # Severity icon
                icon = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}.get(rule['severity'], "•")
                
                report.append(f"{icon} {rule['id']}: {rule['title']} [{rule['severity'].upper()}]")
                report.append(f"   Found: {count} occurrence(s)")
                report.append(f"   {rule['description']}")
                report.append("")
                report.append(f"   Why it matters: {rule['why_it_matters']}")
                report.append(f"   How to fix: {rule['how_to_fix']}")
                report.append("")
                
                # Show examples
                if items:
                    report.append("   Examples:")
                    for item in items[:3]:  # Show first 3
                        if 'component' in item:
                            report.append(f"   • {item.get('component')} → {item.get('input', item.get('output', ''))}")
                        elif 'type' in item:
                            report.append(f"   • {item.get('type')} at {item.get('pos')}")
                        elif 'plugin' in item:
                            report.append(f"   • {item.get('plugin')}")
                        elif 'message' in item:
                            report.append(f"   • {item.get('message')}")
                    if count > 3:
                        report.append(f"   ... and {count - 3} more")
                report.append("")
                report.append("-" * 60)
                report.append("")
        
        # Summary
        error_count = sum(1 for i in self.issues if i['rule']['severity'] == 'error')
        warning_count = sum(1 for i in self.issues if i['rule']['severity'] == 'warning')
        info_count = sum(1 for i in self.issues if i['rule']['severity'] == 'info')
        
        report.append("📊 Summary:")
        report.append(f"   Errors: {error_count}")
        report.append(f"   Warnings: {warning_count}")
        report.append(f"   Info: {info_count}")
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)


def lint_gh_json(json_path: str):
    """Lint a GH JSON file and print report"""
    linter = GHLinter(json_path)
    print(linter.generate_lint_report())
    return linter


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        lint_gh_json(sys.argv[1])
    else:
        print("Usage: python gh_linter.py <path_to_json>")
