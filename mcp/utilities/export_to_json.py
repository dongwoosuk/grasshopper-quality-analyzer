"""CPython Script Component: Export GH Definition to JSON
Exports the current Grasshopper definition to a structured JSON file for analysis

Inputs:
    out_path: str (e.g. r"C:\...\my_def.json")

Outputs:
    a: string  # Status message
"""
import json
import rhinoscriptsyntax as rs
import Rhino
import Grasshopper as gh
import scriptcontext as sc

# Get the active Grasshopper document
try:
    doc = ghenv.Component.OnPingDocument()
except:
    a = "ERROR: Could not access Grasshopper document"
    raise Exception(a)

# Get document properties safely
doc_title = ""
doc_path = ""
gh_version = ""

try:
    if hasattr(doc, 'Properties') and doc.Properties:
        doc_title = str(doc.Properties.Description) if hasattr(doc.Properties, 'Description') else ""
except:
    pass

try:
    if hasattr(doc, 'FilePath') and doc.FilePath:
        doc_path = str(doc.FilePath)
except:
    pass

try:
    gh_version = str(gh.Folders.GrasshopperVersion)
except:
    pass

data = {
    "document": {
        "title": doc_title,
        "path": doc_path,
        "gh_version": gh_version
    },
    "components": [],
    "params": [],
    "wires": [],
    "warnings": []
}

def pt_to_xy(pt):
    try:
        return [float(pt.X), float(pt.Y)]
    except:
        return [0.0, 0.0]

def get_group_id(obj):
    """Safely get group ID"""
    try:
        if hasattr(obj, 'Attributes') and obj.Attributes:
            if hasattr(obj.Attributes, 'GetTopLevel'):
                container = obj.Attributes.GetTopLevel
                if container and hasattr(container, 'InstanceGuid'):
                    return str(container.InstanceGuid)
    except:
        pass
    return None

def get_owner_guid(param):
    """Get the GUID of the component or parameter that owns this parameter"""
    try:
        # Try to get parent component/parameter
        if hasattr(param, 'Attributes') and param.Attributes:
            if hasattr(param.Attributes, 'Parent') and param.Attributes.Parent:
                parent_obj = param.Attributes.Parent.DocObject
                if parent_obj and hasattr(parent_obj, 'InstanceGuid'):
                    return str(parent_obj.InstanceGuid)
        
        # If no parent, the param itself might be the target (standalone parameter)
        if hasattr(param, 'InstanceGuid'):
            return str(param.InstanceGuid)
    except:
        pass
    return None

def extract_volatile_data(param):
    """Extract actual data from parameter's VolatileData"""
    try:
        if not hasattr(param, 'VolatileData') or param.VolatileData is None:
            return None
        
        volatile_data = param.VolatileData
        if volatile_data.IsEmpty:
            return None
        
        # Extract data from all branches
        result = []
        for i in range(volatile_data.PathCount):
            path = volatile_data.get_Path(i)
            branch = volatile_data.get_Branch(path)
            
            branch_data = []
            for item in branch:
                try:
                    # Try to get the actual value
                    if hasattr(item, 'Value'):
                        val = item.Value
                    else:
                        val = item
                    
                    # Convert to string representation
                    if val is not None:
                        branch_data.append(str(val))
                except:
                    pass
            
            if branch_data:
                result.append(branch_data)
        
        return result if result else None
    except:
        return None

# First pass - collect all objects
for obj in doc.Objects:
    try:
        dobj = {
            "guid": str(obj.InstanceGuid),
            "name": str(obj.NickName or obj.Name or obj.Description or ""),
            "type": str(obj.GetType().FullName),
            "category": str(getattr(obj, "Category", "")),
            "subcategory": str(getattr(obj, "SubCategory", "")),
            "pos": pt_to_xy(obj.Attributes.Pivot) if hasattr(obj, 'Attributes') else [0, 0],
            "group": get_group_id(obj)
        }
        
        # Check if component
        if isinstance(obj, gh.Kernel.IGH_Component):
            ins = []
            try:
                for i, ip in enumerate(obj.Params.Input):
                    param_info = {
                        "index": i,
                        "name": str(ip.NickName or ip.Name or ""),
                        "tree_access": str(ip.Access) if hasattr(ip, 'Access') else "",
                        "source_count": ip.SourceCount if hasattr(ip, 'SourceCount') else 0
                    }
                    if hasattr(ip, "TypeHint"):
                        param_info["type_hint"] = str(ip.TypeHint)
                    ins.append(param_info)
            except Exception as e:
                data["warnings"].append(f"input_error: {e}")
            
            outs = []
            try:
                for i, op in enumerate(obj.Params.Output):
                    out_info = {
                        "index": i,
                        "name": str(op.NickName or op.Name or ""),
                        "tree_access": str(op.Access) if hasattr(op, 'Access') else "",
                        "recipient_count": op.RecipientCount if hasattr(op, 'RecipientCount') else 0
                    }
                    
                    # Extract volatile data from output parameters
                    volatile = extract_volatile_data(op)
                    if volatile:
                        out_info["data"] = volatile
                    
                    outs.append(out_info)
            except Exception as e:
                data["warnings"].append(f"output_error: {e}")
            
            dobj["inputs"] = ins
            dobj["outputs"] = outs
            data["components"].append(dobj)
        else:
            # Parameter objects
            dobj["param_kind"] = str(obj.GetType().Name)
            
            # Add source/recipient counts for parameters too
            try:
                if hasattr(obj, 'SourceCount'):
                    dobj["source_count"] = obj.SourceCount
                if hasattr(obj, 'RecipientCount'):
                    dobj["recipient_count"] = obj.RecipientCount
            except:
                pass
            
            # Slider values and Panel data
            try:
                from Grasshopper.Kernel.Special import GH_NumberSlider, GH_Panel
                if isinstance(obj, GH_NumberSlider):
                    dobj["slider"] = {
                        "value": float(obj.CurrentValue),
                        "min": float(obj.Slider.Minimum),
                        "max": float(obj.Slider.Maximum),
                        "rounding": int(obj.Slider.Rounding)
                    }
                elif isinstance(obj, GH_Panel):
                    # Get user text (static text)
                    dobj["panel_text"] = str(obj.UserText)
                    
                    # Get volatile data (actual displayed data from connected components)
                    volatile = extract_volatile_data(obj)
                    if volatile:
                        dobj["panel_data"] = volatile
            except:
                pass
            
            data["params"].append(dobj)
    
    except Exception as e:
        data["warnings"].append(f"critical_error: {obj.GetType().Name if hasattr(obj, 'GetType') else 'unknown'} -> {e}")

# Second pass - collect wires from ALL objects (components and parameters)
for obj in doc.Objects:
    try:
        # Check if this object has output parameters
        outputs = None
        
        if isinstance(obj, gh.Kernel.IGH_Component):
            outputs = obj.Params.Output
        elif hasattr(obj, 'Recipients'):  # Standalone parameter with output
            # Treat the parameter itself as having one output
            outputs = [obj]
        
        if outputs:
            for oi, op in enumerate(outputs):
                try:
                    if hasattr(op, 'Recipients'):
                        for rec in op.Recipients:
                            try:
                                target_guid = get_owner_guid(rec)
                                
                                wire_info = {
                                    "from": {
                                        "guid": str(obj.InstanceGuid),
                                        "out_index": oi if isinstance(obj, gh.Kernel.IGH_Component) else 0,
                                        "out_name": str(op.NickName or op.Name or "") if hasattr(op, 'NickName') else str(obj.NickName or obj.Name or "")
                                    },
                                    "to": {
                                        "guid": target_guid if target_guid else "",
                                        "in_name": str(rec.NickName or rec.Name or "")
                                    }
                                }
                                data["wires"].append(wire_info)
                            except Exception as wire_e:
                                pass  # Skip individual wire errors
                except:
                    pass
    except:
        pass

# Plugin summary
try:
    plugins = sorted(list(set([(c.get("category", ""), c.get("subcategory", ""))
                               for c in data["components"] if c.get("category") or c.get("subcategory")])))
    data["plugins"] = [{"category": c, "subcategory": s} for (c, s) in plugins]
except:
    data["plugins"] = []

# Stats
data["stats"] = {
    "total_components": len(data["components"]),
    "total_params": len(data["params"]),
    "total_wires": len(data["wires"]),
    "warnings_count": len(data["warnings"])
}

# Write JSON
try:
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    a = f"✓ Exported to: {out_path}\n{data['stats']['total_components']} components, {data['stats']['total_params']} params, {data['stats']['total_wires']} wires"
    if data['stats']['warnings_count'] > 0:
        a += f"\n⚠ {data['stats']['warnings_count']} warnings (check JSON file)"
except Exception as write_e:
    a = f"ERROR: Failed to write file - {write_e}"
