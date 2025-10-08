"""
Grasshopper Definition Analyzer
Simple JSON analysis tool for GH definitions
"""
import json
from collections import defaultdict, Counter
from typing import Dict, List, Any


class GHAnalyzer:
    """Analyzes Grasshopper definition JSON files"""
    
    def __init__(self, json_path: str):
        with open(json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.components = self.data.get('components', [])
        self.params = self.data.get('params', [])
        self.wires = self.data.get('wires', [])
        self.warnings = self.data.get('warnings', [])
    
    def get_overview(self) -> Dict[str, Any]:
        """Get basic overview of the definition"""
        doc = self.data.get('document', {})
        stats = self.data.get('stats', {})
        
        # Category breakdown
        category_counts = Counter([c.get('category', 'Unknown') for c in self.components])
        
        # Parameter types
        param_types = Counter([p.get('param_kind', 'Unknown') for p in self.params])
        
        return {
            "document": {
                "title": doc.get('title', 'Untitled'),
                "path": doc.get('path', ''),
                "gh_version": doc.get('gh_version', '')
            },
            "stats": {
                "total_components": stats.get('total_components', len(self.components)),
                "total_params": stats.get('total_params', len(self.params)),
                "total_wires": stats.get('total_wires', len(self.wires)),
                "warnings": stats.get('warnings_count', len(self.warnings))
            },
            "breakdown": {
                "by_category": dict(category_counts),
                "param_types": dict(param_types)
            }
        }
    
    def find_dangling_inputs(self) -> List[Dict[str, Any]]:
        """Find components with unconnected inputs"""
        dangling = []
        
        # Build wire map: {to_guid: [input_names]}
        wire_targets = defaultdict(list)
        for wire in self.wires:
            to_guid = wire.get('to', {}).get('guid', '')
            in_name = wire.get('to', {}).get('in_name', '')
            if to_guid:
                wire_targets[to_guid].append(in_name)
        
        # Check each component
        for comp in self.components:
            guid = comp.get('guid')
            connected_inputs = set(wire_targets.get(guid, []))
            
            for inp in comp.get('inputs', []):
                inp_name = inp.get('name')
                if inp_name not in connected_inputs:
                    dangling.append({
                        "component": comp.get('name'),
                        "guid": guid,
                        "input": inp_name,
                        "pos": comp.get('pos')
                    })
        
        return dangling
    
    def find_dangling_outputs(self) -> List[Dict[str, Any]]:
        """Find components with unconnected outputs"""
        dangling = []
        
        # Build wire map: {from_guid: [output_names]}
        wire_sources = defaultdict(list)
        for wire in self.wires:
            from_guid = wire.get('from', {}).get('guid', '')
            out_name = wire.get('from', {}).get('out_name', '')
            if from_guid:
                wire_sources[from_guid].append(out_name)
        
        # Check each component
        for comp in self.components:
            guid = comp.get('guid')
            connected_outputs = set(wire_sources.get(guid, []))
            
            for out in comp.get('outputs', []):
                out_name = out.get('name')
                if out_name not in connected_outputs:
                    dangling.append({
                        "component": comp.get('name'),
                        "guid": guid,
                        "output": out_name,
                        "pos": comp.get('pos')
                    })
        
        return dangling
    
    def find_unnamed_params(self) -> List[Dict[str, Any]]:
        """Find panels/sliders without custom names"""
        unnamed = []
        
        for param in self.params:
            name = param.get('name', '')
            param_kind = param.get('param_kind', '')
            
            # Check if name is default/generic
            if not name or name == param_kind or name.startswith('Number Slider') or name.startswith('Panel'):
                unnamed.append({
                    "type": param_kind,
                    "name": name,
                    "guid": param.get('guid'),
                    "pos": param.get('pos')
                })
        
        return unnamed
    
    def get_plugin_usage(self) -> List[Dict[str, Any]]:
        """Get list of plugins/categories used"""
        return self.data.get('plugins', [])
    
    def generate_report(self) -> str:
        """Generate a comprehensive analysis report"""
        overview = self.get_overview()
        dangling_in = self.find_dangling_inputs()
        dangling_out = self.find_dangling_outputs()
        unnamed = self.find_unnamed_params()
        plugins = self.get_plugin_usage()
        
        report = []
        report.append("=" * 60)
        report.append(f"GRASSHOPPER DEFINITION ANALYSIS")
        report.append("=" * 60)
        report.append("")
        
        # Document info
        doc = overview['document']
        report.append(f"📄 Document: {doc['title']}")
        report.append(f"   Version: {doc['gh_version']}")
        report.append("")
        
        # Statistics
        stats = overview['stats']
        report.append("📊 Statistics:")
        report.append(f"   Components: {stats['total_components']}")
        report.append(f"   Parameters: {stats['total_params']}")
        report.append(f"   Wires: {stats['total_wires']}")
        report.append(f"   Warnings: {stats['warnings']}")
        report.append("")
        
        # Category breakdown
        report.append("🔧 Components by Category:")
        for cat, count in sorted(overview['breakdown']['by_category'].items()):
            if cat:
                report.append(f"   {cat}: {count}")
        report.append("")
        
        # Issues
        report.append("⚠️  Issues Found:")
        report.append("")
        
        if dangling_in:
            report.append(f"❌ Dangling Inputs: {len(dangling_in)}")
            for item in dangling_in[:5]:  # Show first 5
                report.append(f"   • {item['component']} → {item['input']}")
            if len(dangling_in) > 5:
                report.append(f"   ... and {len(dangling_in) - 5} more")
            report.append("")
        
        if dangling_out:
            report.append(f"❌ Dangling Outputs: {len(dangling_out)}")
            for item in dangling_out[:5]:
                report.append(f"   • {item['component']} → {item['output']}")
            if len(dangling_out) > 5:
                report.append(f"   ... and {len(dangling_out) - 5} more")
            report.append("")
        
        if unnamed:
            report.append(f"⚠️  Unnamed Parameters: {len(unnamed)}")
            for item in unnamed[:5]:
                report.append(f"   • {item['type']} at {item['pos']}")
            if len(unnamed) > 5:
                report.append(f"   ... and {len(unnamed) - 5} more")
            report.append("")
        
        # Plugins
        if plugins:
            report.append("🔌 Plugins/Categories Used:")
            for plugin in plugins[:10]:
                cat = plugin.get('category', '')
                subcat = plugin.get('subcategory', '')
                if cat:
                    report.append(f"   • {cat}" + (f" / {subcat}" if subcat else ""))
            report.append("")
        
        report.append("=" * 60)
        
        return "\n".join(report)


def analyze_gh_json(json_path: str):
    """Analyze a GH JSON file and print report"""
    analyzer = GHAnalyzer(json_path)
    print(analyzer.generate_report())
    return analyzer


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        analyze_gh_json(sys.argv[1])
    else:
        print("Usage: python gh_analyzer.py <path_to_json>")
