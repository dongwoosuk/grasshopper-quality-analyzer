"""
Enhanced GHX Parser
Parses GHX files directly without needing Grasshopper
"""
import xml.etree.ElementTree as ET
import base64
from typing import Dict, List, Any
from collections import defaultdict


class GHXParser:
    """Parse GHX files directly"""
    
    def __init__(self, ghx_path: str):
        self.tree = ET.parse(ghx_path)
        self.root = self.tree.getroot()
        self.data = {
            "document": {},
            "components": [],
            "params": [],
            "wires": [],
            "groups": []
        }
        self._parse()
    
    def _parse(self):
        """Parse the GHX file"""
        # Document info
        doc_props = self.root.find('.//chunk[@name="DefinitionProperties"]')
        if doc_props:
            self.data["document"] = {
                "title": self._get_item_value(doc_props, "Name"),
                "gh_version": "Unknown"
            }
        
        # Get GH version
        gh_libs = self.root.find('.//chunk[@name="GHALibraries"]')
        if gh_libs:
            version_elem = gh_libs.find('.//item[@name="Version"]')
            if version_elem is not None:
                self.data["document"]["gh_version"] = version_elem.text
        
        # Parse objects
        def_objects = self.root.find('.//chunk[@name="DefinitionObjects"]')
        if def_objects:
            for obj in def_objects.findall('.//chunk[@name="Object"]'):
                self._parse_object(obj)
    
    def _get_item_value(self, parent, name):
        """Get value of an item by name"""
        item = parent.find(f'.//item[@name="{name}"]')
        return item.text if item is not None else ""
    
    def _parse_object(self, obj):
        """Parse a single object (component or parameter)"""
        guid = self._get_item_value(obj, "GUID")
        name = self._get_item_value(obj, "Name")
        
        container = obj.find('.//chunk[@name="Container"]')
        if not container:
            return
        
        # Get position
        attrs = container.find('.//chunk[@name="Attributes"]')
        pos = [0, 0]
        if attrs:
            pivot = attrs.find('.//item[@name="Pivot"]')
            if pivot:
                x_elem = pivot.find('X')
                y_elem = pivot.find('Y')
                if x_elem is not None and y_elem is not None:
                    pos = [float(x_elem.text), float(y_elem.text)]
        
        obj_data = {
            "guid": guid,
            "name": name,
            "pos": pos,
            "type": self._get_item_value(container, "Description")
        }
        
        # Check if it's a component (has inputs/outputs)
        param_data = container.find('.//chunk[@name="ParameterData"]')
        if param_data:
            # It's a component
            input_count = int(self._get_item_value(param_data, "InputCount") or "0")
            output_count = int(self._get_item_value(param_data, "OutputCount") or "0")
            
            obj_data["inputs"] = []
            obj_data["outputs"] = []
            
            # Parse inputs
            for i in range(input_count):
                inp = param_data.find(f'.//chunk[@name="InputParam"][@index="{i}"]')
                if inp:
                    obj_data["inputs"].append({
                        "index": i,
                        "name": self._get_item_value(inp, "NickName") or self._get_item_value(inp, "Name")
                    })
            
            # Parse outputs
            for i in range(output_count):
                out = param_data.find(f'.//chunk[@name="OutputParam"][@index="{i}"]')
                if out:
                    obj_data["outputs"].append({
                        "index": i,
                        "name": self._get_item_value(out, "NickName") or self._get_item_value(out, "Name")
                    })
            
            self.data["components"].append(obj_data)
        else:
            # It's a parameter (slider, panel, etc)
            obj_data["param_kind"] = name
            
            # Try to get slider values
            slider_val = self._get_item_value(container, "CurrentValue")
            if slider_val:
                obj_data["slider_value"] = slider_val
            
            # Try to get panel text
            panel_text = self._get_item_value(container, "UserText")
            if panel_text:
                obj_data["panel_text"] = panel_text
            
            self.data["params"].append(obj_data)
    
    def to_json_format(self) -> Dict[str, Any]:
        """Convert to same format as export_to_json.py for compatibility"""
        return {
            "document": self.data["document"],
            "components": self.data["components"],
            "params": self.data["params"],
            "wires": self.data["wires"],  # Wire parsing is complex, may need enhancement
            "stats": {
                "total_components": len(self.data["components"]),
                "total_params": len(self.data["params"]),
                "total_wires": len(self.data["wires"]),
                "warnings_count": 0
            }
        }
    
    def generate_report(self) -> str:
        """Generate analysis report"""
        report = []
        report.append("=" * 60)
        report.append("GHX FILE ANALYSIS")
        report.append("=" * 60)
        report.append("")
        
        doc = self.data["document"]
        report.append(f"📄 Document: {doc.get('title', 'Untitled')}")
        report.append(f"   Version: {doc.get('gh_version', 'Unknown')}")
        report.append("")
        
        report.append("📊 Statistics:")
        report.append(f"   Components: {len(self.data['components'])}")
        report.append(f"   Parameters: {len(self.data['params'])}")
        report.append(f"   Groups: {len(self.data['groups'])}")
        report.append("")
        
        # Component types
        comp_types = defaultdict(int)
        for comp in self.data['components']:
            comp_types[comp.get('type', 'Unknown')] += 1
        
        if comp_types:
            report.append("🔧 Component Types:")
            for ctype, count in sorted(comp_types.items(), key=lambda x: x[1], reverse=True)[:10]:
                if ctype:
                    report.append(f"   {ctype}: {count}")
            report.append("")
        
        report.append("=" * 60)
        return "\n".join(report)


def parse_ghx(ghx_path: str):
    """Parse a GHX file and return parser"""
    parser = GHXParser(ghx_path)
    print(parser.generate_report())
    return parser


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        parse_ghx(sys.argv[1])
    else:
        print("Usage: python ghx_parser.py <path_to_ghx>")
