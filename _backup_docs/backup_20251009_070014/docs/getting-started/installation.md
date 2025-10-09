# Getting Started with Grasshopper Quality Analyzer

Welcome! This guide will help you get up and running with the analyzer in just a few minutes.

## Which Version Should I Use?

### 🚀 Standalone - Start Here!
**Perfect for beginners and daily use**

- ✅ No setup required
- ✅ Works directly in Grasshopper
- ✅ Real-time feedback
- ⚡ 5-minute installation

👉 [Skip to Standalone Installation](#standalone-installation)

---

### 🔧 MCP + Claude - Advanced
**For developers and deep analysis**

- ✅ AI-powered suggestions
- ✅ File analysis without opening
- ✅ Version comparison
- ⏱️ 10-minute setup

👉 [Skip to MCP Setup](#mcp-setup)

---

## Standalone Installation

### Step 1: Download Files
```bash
# Option A: Git Clone (recommended)
git clone https://github.com/dongwoosuk/grasshopper-quality-analyzer
cd grasshopper-quality-analyzer/standalone

# Option B: Direct Download
# Download standalone folder from GitHub
```

### Step 2: Open Grasshopper
1. Launch Rhino
2. Type `Grasshopper` in command line
3. Wait for Grasshopper to open

### Step 3: Add Python Component
1. In Grasshopper, press `Ctrl + F` to search
2. Type "Python" and press Enter
3. Place a Python component on canvas

### Step 4: Copy Code
1. Open `component_all_in_one.py` in a text editor
2. Select all (`Ctrl + A`) and copy (`Ctrl + C`)
3. Double-click the Python component in Grasshopper
4. Paste the code (`Ctrl + V`)

### Step 5: Add Button (Optional)
1. Search for "Button" component
2. Connect Button to Python component's first input
3. Or just run Python component directly

### Step 6: First Run
1. Click the button or Python component
2. You should see analysis results!

**That's it! You're ready to use the analyzer.** 🎉

---

## First Analysis

### Quick Check (Default)
```
Just run the component!

Output:
=== QUICK CHECK ===
Score: 85/100
Components: 42
Issues: 0 errors, 3 warnings
Status: ✅ Good
```

### Full Analysis
```
Set mode input to 1

Output:
🦗 FULL ANALYSIS
📊 Score: 85/100
📈 Statistics: ...
🔍 Issues: ...
```

### Available Modes
```
mode = 0: Quick Check (default)
mode = 1: Full Analysis
mode = 2: Statistics Only
mode = 3: Find Issues
mode = 4: Auto-Fix
```

---

## MCP Setup

### Prerequisites
- Python 3.10 or higher
- Claude Desktop app
- Basic command line knowledge

### Step 1: Install Python Dependencies
```bash
# Navigate to mcp directory
cd mcp

# Install requirements
pip install -r requirements.txt
```

### Step 2: Configure Claude Desktop

**Find config file:**
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Add configuration:**
```json
{
  "mcpServers": {
    "gh_analyzer": {
      "command": "python",
      "args": ["C:/full/path/to/mcp_server.py"]
    }
  }
}
```

### Step 3: Restart Claude Desktop
1. Completely quit Claude Desktop
2. Restart the app
3. You should see 🔨 icon in chat

### Step 4: Test Connection
In Claude, type:
```
"List available GH analyzer tools"
```

You should see 5 tools listed!

---

## Your First Analysis

### With Standalone
```python
# In Grasshopper:
# 1. Add component
# 2. Run
# 3. Read results
```

### With MCP + Claude
```
# In Claude Desktop:
"Analyze this definition: C:/path/to/file.ghx"
```

---

## Common Issues

### "gh_live_analyzer.py not found"
**Solution:** Update the path in component code
```python
# Line ~25 in component file
rf"C:\Users\{username}\...\gh_analyzer_release\standalone"
```

### "Module not found" (MCP)
**Solution:** Reinstall requirements
```bash
pip install -r requirements.txt --force-reinstall
```

### "Server not responding" (MCP)
**Solution:** Check paths in config file
- Use absolute paths
- Use forward slashes (/) or escaped backslashes (\\\\)

---

## Next Steps

### For Standalone Users
1. ✅ [Read User Guide](../standalone/USER_GUIDE.md)
2. ✅ [Learn All Modes](../standalone/COMPLETE.md)
3. ✅ [Understand Lint Rules](../mcp/FORMAT_COMPARISON.md)

### For MCP Users
1. ✅ [Learn Prompts](../mcp/PROMPTS.md)
2. ✅ [Understand Tools](../mcp/CLAUDE_SETUP.md)
3. ✅ [Advanced Features](../mcp/FORMAT_COMPARISON.md)

---

## Quick Reference

### Standalone Modes
```
0 = Quick Check     → Fast overview
1 = Full Analysis   → Complete report
2 = Statistics      → Numbers only
3 = Find Issues     → List problems
4 = Auto-Fix        → Automatic fixes
```

### MCP Tools
```
gh_parse    → Parse and analyze
gh_lint     → Run lint checks
gh_suggest  → Get suggestions
gh_diff     → Compare versions
gh_list_rules → Show all rules
```

### Health Score
```
90-100 → ✅ Excellent
70-89  → 👍 Good
50-69  → ⚠️  Needs Work
0-49   → ❌ Critical
```

---

## Getting Help

### Documentation
- 📖 [Main README](../README.md)
- 📚 [User Guide](../standalone/USER_GUIDE.md)
- 🔧 [MCP Guide](../mcp/CLAUDE_SETUP.md)

### Support
- 🐛 [Report Bug](https://github.com/dongwoosuk/grasshopper-quality-analyzer/issues)
- 💬 [Ask Question](https://github.com/dongwoosuk/grasshopper-quality-analyzer/discussions)
- 📧 Email: dongwoosuk0219@gmail.com

---

## What's Next?

Now that you're set up, learn how to:

1. **Understand Issues**: [Lint Rules Guide](../mcp/FORMAT_COMPARISON.md)
2. **Fix Problems**: [Auto-Fix Guide](../standalone/USER_GUIDE.md#auto-fix)
3. **Improve Scores**: [Best Practices](./best-practices.md)
4. **Team Use**: [Team Guide](./team-workflow.md)

---

**Congratulations! You're ready to improve your Grasshopper definitions!** 🦗✨

[← Back to Main](../README.md) | [Next: Best Practices →](./best-practices.md)
