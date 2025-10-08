# Grasshopper Definition Examples

This directory contains example Grasshopper definitions for testing the analyzer.

## Sample Files

### 1. simple_definition.json
A basic Grasshopper definition with:
- 5-10 components
- Basic wire connections
- Minimal issues
- Good for testing basic functionality

### 2. medium_complexity.json
A medium-sized definition with:
- 50-100 components
- Multiple groups
- Some common issues (unnamed params, dangling outputs)
- Good for testing lint rules

### 3. complex_definition.json
A complex definition with:
- 200+ components
- Multiple plugins
- Various issue types
- Performance testing

### 4. problematic.json
A definition with intentional issues:
- Dangling inputs (errors)
- Dangling outputs (warnings)
- Unnamed parameters
- Missing groups
- All lint rule violations for testing

## How to Use

### With MCP Server
```bash
# Analyze a sample file
python mcp_server.py

# In Claude:
"Analyze examples/simple_definition.json"
```

### With Standalone
1. Open the definition in Grasshopper
2. Add analyzer component
3. Run analysis

## Creating Your Own Examples

To add new examples:

1. Create definition in Grasshopper
2. Export to JSON using utilities/export_to_json.py
3. Add to this directory
4. Update this README

## File Format

All example files should be in JSON format exported from Grasshopper using the export utility.

Required structure:
```json
{
  "document": { ... },
  "components": [ ... ],
  "params": [ ... ],
  "wires": [ ... ],
  "stats": { ... }
}
```
