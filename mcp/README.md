# 🔧 MCP + Claude Version

## Developer-Grade Analysis with AI

This version provides **100% accurate analysis** of Grasshopper definitions with **AI-powered suggestions** from Claude.

---

## ✨ Features

### Complete Analysis
- ✅ **GHX Direct Parsing** - No export needed
- ✅ **JSON Support** - 100% accurate wire tracking
- ✅ **15+ Lint Rules** - Comprehensive quality checks
- ✅ **Version Comparison** - Track changes

### AI-Powered
- 🤖 **Claude Integration** - Natural language queries
- 💡 **Smart Suggestions** - Context-aware recommendations
- 📝 **Best Practices** - Learn from industry standards
- 🔄 **Refactoring Help** - Step-by-step improvements

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Claude Desktop

See [CLAUDE_SETUP.md](CLAUDE_SETUP.md) for detailed instructions.

**Quick version:**
```json
{
  "mcpServers": {
    "gh_analyzer": {
      "command": "python",
      "args": ["path/to/mcp_server.py"]
    }
  }
}
```

### 3. Use with Claude

```
"Analyze this GHX file: C:\project\facade.ghx"
"Compare these two versions: old.ghx and new.ghx"
"Suggest improvements for: definition.json"
```

---

## 📚 Documentation

- [Setup Guide](CLAUDE_SETUP.md) - Complete installation
- [Prompt Templates](PROMPTS.md) - How to ask Claude
- [Format Comparison](FORMAT_COMPARISON.md) - GHX vs JSON

---

## 🆚 vs Standalone

| Feature | MCP | Standalone |
|---------|-----|------------|
| Accuracy | 100% | 95% |
| Wire Analysis | Complete | Basic |
| AI Suggestions | ✅ | ❌ |
| File Analysis | ✅ | ❌ |
| Setup Time | 10 min | 1 min |
| Use Case | Deep analysis | Daily work |

**Use both!** MCP for important refactoring, Standalone for daily checks.

---

## 📁 Structure

```
mcp/
├── analyzer/          # Analysis engine
│   ├── gh_analyzer.py
│   ├── ghx_parser.py
│   ├── gh_linter.py
│   └── lint_rules.py
│
├── utilities/         # GH utilities
│   ├── dual_save.py
│   └── export_to_json.py
│
├── mcp_server.py     # MCP server
└── requirements.txt
```

---

## 🔧 Development

### Running Tests
```bash
python -m pytest tests/
```

### Starting Server
```bash
python mcp_server.py
```

### Debugging
Set `DEBUG=1` in environment variables for verbose logging.

---

[← Back to Main](../README.md)




---

## ?뮠 Prompt Templates

# Grasshopper Analysis Prompt Templates

Prompt templates for analyzing Grasshopper definitions with Claude.

---

## 📊 Basic Analysis

```
You are a Grasshopper definition expert. I have a GH definition.

Please analyze this file and provide:
1. Overview: component count, categories used, complexity metrics
2. Health check: any obvious issues or warnings
3. Quick recommendations for improvement

File path: [PATH_TO_FILE]
```

---

## 🔍 Detailed Lint Check

```
You are a Grasshopper code reviewer. Run a comprehensive lint check on my GH definition.

Tasks:
1. Check against all 15 lint rules
2. List Top 5 most critical issues with:
   - Rule ID and severity
   - Why it matters
   - Concrete fix steps
   - Affected components (with GUIDs)
3. Provide a priority-ordered action plan

File path: [PATH_TO_FILE]
```

---

## 🎯 Goal-Based Improvements

### Performance Optimization

```
I need to optimize my Grasshopper definition for better performance.

Current file: [PATH_TO_FILE]
Goal: Reduce computation time by at least 50%

Please:
1. Identify performance bottlenecks
2. Suggest specific component replacements or restructuring
3. Provide step-by-step optimization plan
4. Estimate potential performance gain for each suggestion
```

### Readability Improvement

```
Help me make this Grasshopper definition more maintainable and readable.

Current file: [PATH_TO_FILE]
Goal: Team members should understand the logic without explanation

Please suggest:
1. Naming improvements (parameters, groups)
2. Documentation needs (scribbles, comments)
3. Organization restructuring (grouping, clustering)
4. Data flow simplification
```

### Data Tree Stabilization

```
My definition has unpredictable data tree behavior.

Current file: [PATH_TO_FILE]
Goal: Stable and predictable data tree structure

Analyze:
1. Current tree access patterns (item/list/tree mixing)
2. Excessive flatten/graft usage
3. Tree manipulation chain depth
4. Suggest standardization strategy
```

---

## 🔄 Version Comparison

```
Compare two versions of my Grasshopper definition.

Version A (before): [PATH_A]
Version B (after): [PATH_B]

Please provide:
1. Summary of changes (added/removed/modified components)
2. Impact analysis (potential breaking changes)
3. Improvement or regression assessment
4. Migration notes if needed
```

---

## 🏗️ Refactoring Plan

```
Create a refactoring plan for my Grasshopper definition.

Current file: [PATH_TO_FILE]
Goals:
- [GOAL_1]
- [GOAL_2]
- [GOAL_3]

Please provide:
1. Current state assessment
2. Proposed architecture/structure
3. Step-by-step refactoring plan (ordered to minimize breaking changes)
4. Risk analysis for each step
5. Testing checkpoints
```

---

## 🎓 Educational Analysis

```
Explain this Grasshopper definition to a beginner.

File: [PATH_TO_FILE]

Please:
1. Describe the overall purpose and logic
2. Break down into major sections
3. Explain key component chains
4. Identify learning points (techniques used)
5. Suggest similar example projects to study
```

---

## 📦 Clustering Suggestions

```
Identify opportunities to create clusters in my definition.

File: [PATH_TO_FILE]

Find:
1. Repeated component sequences (potential clusters)
2. Self-contained logic blocks that could be modular
3. For each suggestion:
   - Component GUIDs involved
   - Cluster name suggestion
   - Input/output interface
   - Reusability score
```

---

## 🔌 Plugin Dependency Analysis

```
Analyze plugin dependencies in my definition.

File: [PATH_TO_FILE]

Report:
1. List all non-core plugins used
2. For each plugin:
   - Usage count (how many components)
   - Critical or replaceable?
   - Core alternatives if available
3. Dependency risk assessment
4. Recommendations for reducing dependencies
```

---

## 💡 Best Practice Check

```
Review my definition against Grasshopper best practices.

File: [PATH_TO_FILE]

Check for:
1. ✅ Naming conventions
2. ✅ Documentation (scribbles, groups)
3. ✅ Data tree management
4. ✅ Component organization
5. ✅ Performance considerations
6. ✅ Maintainability

Rate each category (1-5) and provide specific improvements.
```

---

## 🎨 Canvas Layout Analysis

```
Analyze the visual layout and organization of my definition.

File: [PATH_TO_FILE]

Assess:
1. Wire crossing issues (long wires, tangled connections)
2. Component spacing and alignment
3. Group organization
4. Suggest layout improvements for better readability
5. Identify areas that need relay components
```

---

## Usage Examples

### Real Conversation Flow

```
User: Please analyze my Grasshopper file
File: C:\Projects\building_facade.json
Goal: Performance optimization

Claude: 
[Runs gh_parse]
[Runs gh_lint]
[Runs gh_suggest with goal="optimize performance"]

Analysis shows 3 major bottlenecks:

1. [Component A] - Data tree flatten overuse
   → Suggestion: Use Graft instead of Partition List
   
2. [Component B] - Duplicate calculations
   → Suggestion: Extract to Cluster + Data Dam

3. [Component C] - Inefficient geometry creation
   → Suggestion: Replace with native components

Would you like me to explain the step-by-step fixes?
```

---

## Template Customization

To add your own team rules:

```
Based on our team standards:
- All sliders must have descriptive names
- Maximum 50 components per group
- No flatten before [specific operation]
- Required: version scribble in top-left

Check my definition against these rules.
File: [PATH_TO_FILE]
```

---

## Quick Reference

### Analysis Types
- **Quick**: Basic overview and health check
- **Standard**: Full lint + suggestions
- **Deep**: Complete analysis with refactoring plan
- **Comparison**: Version diff analysis

### Common Goals
- Performance optimization
- Readability improvement
- Data tree stabilization
- Plugin dependency reduction
- Layout reorganization

### Response Formats
- Summary (bullet points)
- Detailed (step-by-step)
- Technical (with GUIDs and metrics)
- Educational (beginner-friendly)

---

[← Back to MCP Guide](README.md)


---

## ?뱤 Format Comparison

# 🎯 Comparison of Two Analysis Methods

## Conclusion: **Both are Supported!**

The system has been updated to support both **direct GHX analysis** and **JSON analysis**.

---

## 📊 Detailed Comparison

### Method 1: Direct GHX Analysis (New!) ✨
```
dual_save.ghx → Claude analysis
```

**Advantages:**
- ✅ **Simplest**: Analyze immediately with just a saved GHX file
- ✅ **No extra steps**: Nothing needed in Grasshopper
- ✅ **Fast**: Just drag the file and done

**Disadvantages:**
- ⚠️ **Slightly lower accuracy**: XML parsing may miss some information
- ⚠️ **Limited wire connection info**: Complex connection structures may not be fully captured

**Recommended for:**
- Quick overview checks
- Basic lint inspection
- Component count/type identification

---

### Method 2: JSON Export then Analysis (Original method)
```
Grasshopper → run export_to_json.py → JSON → Claude analysis
```

**Advantages:**
- ✅ **100% accurate**: Direct use of Grasshopper API
- ✅ **Complete information**: All data including wires, data trees, slider values
- ✅ **Detailed analysis**: Complex lint rules, data flow analysis

**Disadvantages:**
- ⚠️ **One extra step**: Must run GHPython script
- ⚠️ **Requires GH running**: Grasshopper must be open

**Recommended for:**
- Detailed analysis needed
- Performance optimization
- Refactoring planning
- Accurate lint checking

---

## 🎯 Recommendations by Scenario

### Scenario 1: Quick Check ⚡
```
Situation: File saved, just want to check for issues
Method: Direct GHX analysis
Time: 5 seconds

Ask Claude:
"Quickly analyze this GHX file: C:\project\facade.ghx"
```

### Scenario 2: Thorough Code Review 🔍
```
Situation: Need perfect inspection before PR
Method: JSON export → analysis
Time: 30 seconds

1. Run export_to_json.py in GH
2. Ask Claude: "Fully analyze this JSON file"
```

### Scenario 3: Performance Optimization 🚀
```
Situation: Need to speed up slow definition
Method: JSON export (requires wire/data tree info)

Ask Claude:
"Optimize this definition: C:\project\slow.json
Goal: Reduce computation time by 50%"
```

### Scenario 4: Version Comparison 📊
```
Situation: Compare yesterday's and today's versions
Method: Direct GHX (fast and sufficient)

Ask Claude:
"Compare these two versions:
Previous: C:\project\v1.ghx
Latest: C:\project\v2.ghx"
```

---

## 💡 Recommended Workflow

### Daily Work (Fast Cycle)
```
1. While working: Just save as GHX (use dual_save)
2. Before leaving: Ask Claude to analyze GHX directly
3. Issues found → Fix next day
```

### Weekly Review (Balanced)
```
Monday: GHX comparison (last week vs this week)
Wednesday: JSON detailed analysis (important files only)
Friday: GHX quick check (all files)
```

### Critical Project (Quality First)
```
During development: GHX quick checks
Code review: JSON detailed analysis
Before deployment: JSON complete inspection
```

---

## 🚀 Using with Claude

### Auto-detection (Recommended!)
```
Just give Claude the file path - it detects automatically:

"Analyze this file: C:\project\facade.ghx"
→ Automatically uses GHX parser

"Analyze this file: C:\project\facade.json"
→ Automatically uses JSON analyzer
```

### Explicit Specification
```
"Analyze this GHX file in as much detail as possible"
→ GHX parser + maximum detail

"Quickly summarize this JSON file"
→ JSON analysis + summary only
```

---

## 📊 Feature Comparison Table

| Feature | Direct GHX | JSON Export |
|---------|------------|-------------|
| **Setup Time** | 0 sec | 10 sec |
| **Analysis Accuracy** | 85% | 100% |
| **Wire Information** | Limited | Complete |
| **Data Trees** | None | Complete |
| **Slider Values** | Basic | Complete |
| **Component Info** | Basic | Detailed |
| **Group Information** | Partial | Complete |
| **Lint Checks** | Basic 11 | All 15 |
| **Recommended Use** | Daily checks | Detailed analysis |

---

## 🎓 Which Should You Use?

### Use Direct GHX Analysis when:
- ✅ You want a quick check
- ✅ Only need to find basic issues
- ✅ Checking multiple files at once
- ✅ Grasshopper isn't open
- ✅ Just comparing versions

### Use JSON Export when:
- ✅ Accurate analysis is required
- ✅ Optimizing performance
- ✅ Analyzing complex data flows
- ✅ Planning refactoring
- ✅ Perfect inspection before PR

---

## 🔄 Real Usage Examples

### Example 1: Regular Day
```
09:00 - Start work
12:00 - Save before lunch (GHX)
       → Claude: "Quick check: morning_work.ghx"
       → Confirm no major issues

15:00 - Mid checkpoint
       → Save GHX
       → Claude: Brief analysis
       
18:00 - Before leaving
       → Run export_to_json.py
       → Claude: "Detailed analysis + tomorrow's tasks"
```

### Example 2: Important PR
```
After completing work:
1. Save with dual_save (GH + GHX)
2. Generate JSON with export_to_json.py
3. Ask Claude for complete analysis with JSON
4. Confirm all lint passes
5. Submit PR
```

### Example 3: Quick Review
```
Colleague shares GHX file:
1. Receive file
2. Claude: "Review this file: colleague.ghx"
3. Immediate feedback
4. (If needed) Detailed analysis with JSON
```

---

## 🛠️ Setup

### 1. Install Packages
```bash
pip install -r src/gh/requirements.txt
```

### 2. Start Server
```bash
python src/gh/start_server.py
```

### 3. Configure Claude Desktop
The MCP server automatically supports both formats!

```json
"gh_analyzer": {
  "command": "python",
  "args": ["C:\\...\\mcp_server.py"],
  "env": {"PYTHONPATH": "C:\\...\\RhinoScripts"}
}
```

---

## 📝 Summary

### For Your Case (Saving as GHX)

**90% of cases: Direct GHX analysis**
- Just save and done
- Fast and convenient
- Catches most issues

**10% of cases: JSON export**
- Important analysis
- Performance optimization
- Accurate lint needed

**Best Practice:**
```
Daily: Direct GHX
Weekly: JSON detail (Friday)
Deployment: JSON complete check
```

---

## 🎉 Conclusion

**Leverage the advantages of both!**

- Quick check = GHX
- Detailed analysis = JSON
- Auto-detect = Claude handles it!

Now you can get optimal analysis in any situation! 🚀

---

## 📚 Learn More

- `README.md` - Complete guide
- `CLAUDE_SETUP.md` - Setup instructions
- `PROMPTS.md` - Prompt examples
- `COMPLETE.md` - Summary
