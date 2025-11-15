# Claude Desktop Integration Guide

## MCP Server Setup

### Step 1: Start MCP Server

```bash
# Install required packages
pip install -r requirements.txt

# Start server
python mcp_server.py
```

Server will run on `http://127.0.0.1:5071`.

### Step 2: Configure Claude Desktop

Claude Desktop configuration file location:
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`

Add to configuration file:

```json
{
  "mcpServers": {
    "gh_analyzer": {
      "command": "python",
      "args": ["/path/to/mcp_server.py"],
      "env": {
        "PYTHONPATH": "/path/to/project"
      }
    }
  }
}
```

### Step 3: Restart Claude Desktop

Save the configuration file and completely restart Claude Desktop.

---

## Available Tools

### 1. gh_parse(path)
Analyze and summarize definition files

**Input:**
```
path: Path to GHX or JSON file
```

**Output:**
- Document information
- Component/parameter/wire statistics
- Category distribution
- Analysis report

### 2. gh_lint(path, rules?)
Run lint checks

**Input:**
```
path: Path to GHX or JSON file
rules: (Optional) List of rule IDs to check (e.g., ["GH001", "GH003"])
```

**Output:**
- List of found issues
- Summary by severity
- Fix suggestions

### 3. gh_suggest(path, goal)
Goal-based improvement suggestions

**Input:**
```
path: Path to file
goal: Goal description (e.g., "optimize performance", "improve readability")
```

**Output:**
- Prioritized suggestions
- Concrete fix steps
- Component-level guidance

### 4. gh_diff(path_a, path_b)
Compare two versions

**Input:**
```
path_a: First file path
path_b: Second file path
```

**Output:**
- Added/removed/modified components
- Wire changes
- Change summary

### 5. gh_list_rules()
List all available lint rules

**Output:**
- Complete list of 15+ lint rules
- Rule IDs, severities, descriptions

---

## Testing

### Direct API Test

```bash
# Check server status
curl http://127.0.0.1:5071/

# List rules
curl http://127.0.0.1:5071/gh/rules

# Analyze (POST)
curl -X POST http://127.0.0.1:5071/gh/parse \
  -H "Content-Type: application/json" \
  -d '{"path": "C:/temp/my_definition.json"}'
```

### Test in Claude Desktop

Ask Claude:

```
Please analyze my Grasshopper definition file:
C:\temp\my_definition.json
```

Claude will automatically use the appropriate MCP tool.

---

## Usage Examples

### Quick Analysis
```
"Analyze this file: C:\project\facade.ghx"
```

### Detailed Lint Check
```
"Run lint check on: C:\project\definition.json
Focus on performance and data tree issues"
```

### Version Comparison
```
"Compare these two versions:
Before: C:\project\v1.ghx
After: C:\project\v2.ghx"
```

### Optimization Suggestions
```
"Suggest performance improvements for: C:\project\slow.json
Goal: Reduce computation time by 50%"
```

---

## Troubleshooting

### Server won't start
- Check Python version (3.8+)
- Install dependencies: `pip install -r requirements.txt`
- Check port 5071 is not in use

### Claude can't find tools
- Verify configuration file path
- Restart Claude Desktop completely
- Check server is running

### Analysis fails
- Verify file path is correct
- Check file format (GHX or JSON)
- Review server logs for errors
