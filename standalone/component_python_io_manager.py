"""
Python Script Auto-Manager for Grasshopper
Automatic I/O management tool for Python3 components

Automatically supports almost all comment formats using smart pattern matching

Supported format examples:
- @input: var1, var2
- Input Parameters:
- Inputs (from Grasshopper):
- REQUIRED INPUT:
- 입력:
- # Input:

@input: run
@output: info, updated

Inputs:
- run (bool): When set to True, scans all Python3 components in the document and automatically configures I/O parameters

Outputs:
- info (str): Detailed scan and update results (total count, status for each component)
- updated (int): Number of successfully updated components

Version: 2.0.1 (Bug Fix)
Date: 2025-01-21
"""

import Grasshopper as gh
from Grasshopper.Kernel import GH_ParamAccess
import re
import System
import clr

clr.AddReference("RhinoCodePluginGH")
from RhinoCodePluginGH.Parameters import ScriptVariableParam

def is_section_header(line):
    """Check if line looks like a section header"""
    stripped = line.strip()
    lower = stripped.lower()

    # Empty line is not a header
    if not stripped:
        return False

    # Ends with colon means section header
    if stripped.endswith(':'):
        return True

    # Separator line is a section header (next line is actual header)
    if stripped.startswith('===') or stripped.startswith('───') or stripped.startswith('---'):
        return True

    return False

def has_input_keywords(line):
    """Check if line contains input-related keywords"""
    lower = line.lower()

    input_keywords = [
        'input',
        'inputs',
        '입력',
        'parameter',
        'parameters',
        'control',
        'controls',
        'required',
        'optional'
    ]

    return any(keyword in lower for keyword in input_keywords)

def has_output_keywords(line):
    """Check if line contains output-related keywords"""
    lower = line.lower()

    output_keywords = [
        'output',
        'outputs',
        '출력',
        'result',
        'results',
        'return'
    ]

    return any(keyword in lower for keyword in output_keywords)

def is_code_start(line):
    """Check if actual code starts"""
    stripped = line.strip()

    if not stripped:
        return False

    code_starters = ['import ', 'from ', 'if ', 'def ', 'class ', 'try:', 'for ', 'while ']
    return any(stripped.startswith(starter) for starter in code_starters)

def is_docstring_end(line, line_num):
    """Check if docstring ends"""
    # First 5 lines are considered docstring start
    if line_num <= 5:
        return False

    return '"""' in line or "'''" in line

def parse_docstring(code):
    """
    Extract inputs/outputs from comments using smart pattern matching
    """
    inputs = []
    outputs = []

    # Method 1: @input/@output tags (most reliable)
    for line in code.split('\n'):
        if '@input' in line.lower():
            match = re.search(r'@input\s*:\s*(.+)', line, re.IGNORECASE)
            if match:
                vars_list = match.group(1).split(',')
                inputs.extend([v.strip() for v in vars_list if v.strip()])
        
        if '@output' in line.lower():
            match = re.search(r'@output\s*:\s*(.+)', line, re.IGNORECASE)
            if match:
                vars_list = match.group(1).split(',')
                outputs.extend([v.strip() for v in vars_list if v.strip()])
    
    if inputs or outputs:
        return inputs, outputs

    # Method 2: Smart section detection
    lines = code.split('\n')
    in_input = False
    in_output = False

    for i, line in enumerate(lines[:200]):  # Scan sufficient number of lines
        # Stop if docstring ends
        if is_docstring_end(line, i):
            break

        # Stop if actual code starts
        if is_code_start(line):
            break

        # Continue if section separator
        stripped = line.strip()
        if stripped.startswith('===') or stripped.startswith('───'):
            continue

        # Stop if Usage or Example section
        lower = line.lower()
        if 'usage:' in lower or 'example:' in lower:
            break

        # Detect section headers
        if is_section_header(line):
            # Is it input section?
            if has_input_keywords(line) and not has_output_keywords(line):
                in_input = True
                in_output = False
                continue

            # Is it output section?
            if has_output_keywords(line) and not has_input_keywords(line):
                in_output = True
                in_input = False
                continue

            # End section if header is unclear
            in_input = False
            in_output = False
            continue

        # Extract variables within sections
        if not stripped or stripped.startswith('#'):
            continue

        if in_input:
            # Pattern 1: - var_name: description
            # Pattern 2: - var1, var2, var3: description (comma separated)
            match = re.match(r'^\s*-\s*([^:]+):', stripped)
            if match:
                vars_part = match.group(1).strip()
                # Process comma-separated variables
                var_list = [v.strip() for v in vars_part.split(',')]
                for var in var_list:
                    if var and re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', var):
                        inputs.append(var)
                continue

            # Pattern 3: var_name (type): description
            match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*[\(\[]', stripped)
            if match:
                inputs.append(match.group(1))
                continue

        if in_output:
            # Apply same patterns
            match = re.match(r'^\s*-\s*([^:]+):', stripped)
            if match:
                vars_part = match.group(1).strip()
                var_list = [v.strip() for v in vars_part.split(',')]
                for var in var_list:
                    if var and re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', var):
                        outputs.append(var)
                continue

            match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*[\(\[]', stripped)
            if match:
                outputs.append(match.group(1))
                continue

    return inputs, outputs

def get_existing_connections(comp):
    """Save existing connection information"""
    input_connections = {}
    output_connections = {}

    # Input connections
    for param in comp.Params.Input:
        param_name = param.NickName
        sources = []
        for j in range(param.SourceCount):
            sources.append(param.Sources[j])
        if sources:
            input_connections[param_name] = sources

    # Output connections
    for param in comp.Params.Output:
        param_name = param.NickName
        recipients = []
        for recipient_param in param.Recipients:
            recipients.append(recipient_param)
        if recipients:
            output_connections[param_name] = recipients

    return input_connections, output_connections

def update_params_preserve_wires(comp, inputs, outputs):
    """Update parameters while preserving connections"""
    try:
        # 1. Save existing connections
        input_connections, output_connections = get_existing_connections(comp)

        # 2. Save current parameter info (type hints, access modes, etc.)
        existing_input_info = {}
        for param in comp.Params.Input:
            existing_input_info[param.NickName] = {
                'TypeHint': param.TypeHint if hasattr(param, 'TypeHint') else None,
                'Access': param.Access,
                'Optional': param.Optional if hasattr(param, 'Optional') else False
            }

        existing_output_info = {}
        for param in comp.Params.Output:
            existing_output_info[param.NickName] = {
                'TypeHint': param.TypeHint if hasattr(param, 'TypeHint') else None,
                'Access': param.Access
            }

        # 3. Clear parameters
        comp.Params.Clear()

        # 4. Recreate input parameters
        for var_name in inputs:
            param = ScriptVariableParam(var_name)
            param.NickName = var_name
            param.Name = var_name
            param.Description = f"Script variable {var_name}"
            param.Access = GH_ParamAccess.item
            param.Optional = False

            # Restore previous settings
            if var_name in existing_input_info:
                info = existing_input_info[var_name]
                if info['TypeHint']:
                    param.TypeHint = info['TypeHint']
                param.Access = info['Access']
                param.Optional = info['Optional']

            comp.Params.RegisterInputParam(param)

        # 5. Recreate output parameters
        for var_name in outputs:
            param = ScriptVariableParam(var_name)
            param.NickName = var_name
            param.Name = var_name
            param.Description = f"Script variable {var_name}"
            param.Access = GH_ParamAccess.item

            # Restore previous settings
            if var_name in existing_output_info:
                info = existing_output_info[var_name]
                if info['TypeHint']:
                    param.TypeHint = info['TypeHint']
                param.Access = info['Access']

            comp.Params.RegisterOutputParam(param)

        # 6. Add 'out' parameter (standard)
        if 'out' not in outputs:
            out_param = ScriptVariableParam("out")
            out_param.NickName = "out"
            out_param.Name = "out"
            out_param.Description = "The execution information, as output and error streams"
            out_param.Access = GH_ParamAccess.item
            comp.Params.RegisterOutputParam(out_param)

        # 7. Restore connections
        for new_param in comp.Params.Input:
            param_name = new_param.NickName
            if param_name in input_connections:
                for source in input_connections[param_name]:
                    new_param.AddSource(source)

        for new_param in comp.Params.Output:
            param_name = new_param.NickName
            if param_name in output_connections:
                for recipient in output_connections[param_name]:
                    recipient.AddSource(new_param)

        # Python3 special handling
        try:
            if hasattr(comp, 'SetParametersFromScript'):
                comp.SetParametersFromScript()
        except:
            pass

        comp.ExpireSolution(True)

        return True

    except Exception as e:
        print(f"Update error: {str(e)}")
        return False

# ============= Main Execution =============

info = ""
updated = 0

if run:
    doc = ghenv.Component.OnPingDocument()

    if not doc:
        info = "Document not found"
    else:
        doc.Enabled = False

        count = 0
        total = 0
        details = []

        # Python3 component GUID
        py3_guid = System.Guid("719467e6-7cf5-4848-99b0-c5dd57e5442c")

        try:
            for obj in doc.Objects:
                if hasattr(obj, 'ComponentGuid') and obj.ComponentGuid == py3_guid:
                    # Exclude self
                    if obj.InstanceGuid == ghenv.Component.InstanceGuid:
                        continue

                    total += 1
                    name = obj.NickName if obj.NickName else f"Py3_{total}"

                    try:
                        ok, code = obj.TryGetSource()
                        if ok and code:
                            inputs, outputs = parse_docstring(code)

                            if inputs or outputs:
                                if update_params_preserve_wires(obj, inputs, outputs):
                                    count += 1
                                    details.append(f"✓ [{total}] {name}: {len(inputs)}in/{len(outputs)}out")
                                else:
                                    details.append(f"- [{total}] {name}: No changes")
                            else:
                                details.append(f"○ [{total}] {name}: No comments")
                    except Exception as ex:
                        details.append(f"✗ [{total}] {name}: {str(ex)[:40]}")

        finally:
            doc.Enabled = True
            doc.NewSolution(True)

        info = f"🎯 Scanned {total}, Updated {count} (v2.0.1)\n\n" + "\n".join(details)
        updated = count
else:
    info = "Set Run to True"

print(info)
