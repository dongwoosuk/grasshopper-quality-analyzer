# 🎯 Grasshopper Live Analyzer - User Guide

## 📦 Complete Package - For General Users

A **complete analysis tool** that works directly inside Grasshopper!

---

## 🚀 Quick Start

### Step 1: Installation
1. Add Python component to canvas
2. Copy and paste one of the scripts below
3. Connect inputs/outputs
4. Done! 🎉

### Step 2: Choose Component
Select the right component for your needs:

| Component | Purpose | Difficulty |
|-----------|---------|------------|
| **All-in-One** | All features (Recommended!) | ⭐⭐ |
| **Health Check** | Quick check | ⭐ |
| **Issue Finder** | Detailed issue search | ⭐⭐ |
| **Auto-Fix** | Automatic fixes | ⭐⭐ |
| **Statistics** | Stats only | ⭐ |

---

## 🎨 Component Detailed Guide

### 1. All-in-One (Recommended ⭐)

**The most powerful all-in-one tool**

#### Inputs:
- `run` (Button): Execute analysis
- `mode` (Number Slider 0-4): Analysis mode
  - `0` = Quick Check
  - `1` = Full Analysis
  - `2` = Statistics Only
  - `3` = Find Issues
  - `4` = Auto-Fix
- `auto_fix` (Boolean): Enable automatic fixes
- `highlight_issues` (Boolean): Highlight on canvas

#### Outputs:
- `report` (Panel): Main report
- `score` (Number): Health score (0-100)
- `errors` (Panel): Error list
- `warnings` (Panel): Warning list
- `stats` (Panel): Statistics summary
- `fixed` (Panel): Fixed items

#### Usage Example:
```
[Button] → run
[Slider 0-4] → mode
[Toggle] → auto_fix
[Toggle] → highlight_issues

     ↓

[All-in-One Python Component]

     ↓

report → [Panel]
score → [Panel]
errors → [Panel]
warnings → [Panel]
```

---

### 2. Health Check

**Simplest health check**

#### Inputs:
- `x` (Button): Run
- `style` (Text): 'simple', 'compact', 'full'

#### Outputs:
- `report` (Panel): Report
- `score` (Number): Score
- `issues` (Number): Issue count

#### When to use?
- Quick check while working
- Check before saving
- Simple health verification

---

### 3. Issue Finder

**Find specific issue types**

#### Inputs:
- `x` (Button): Run
- `check_errors` (Boolean): Check errors
- `check_warnings` (Boolean): Check warnings
- `check_info` (Boolean): Check info

#### Outputs:
- `errors` (List): Error list
- `warnings` (List): Warning list
- `info` (List): Info list
- `summary` (Text): Summary

#### When to use?
- Want to see specific issue types only
- Focus on fixing errors
- Need detailed issue list

---

### 4. Auto-Fix

**Automatic fixing tool**

#### Inputs:
- `x` (Button): Run
- `fix_names` (Boolean): Auto-name parameters
- `highlight` (Boolean): Highlight issues
- `name_prefix` (Text): Name prefix (default: "Param")

#### Outputs:
- `report` (Text): Fix details
- `fixed_count` (Number): Number of fixed items

#### When to use?
- Quickly fix unnamed parameters
- Find problematic components
- Batch fixing

---

### 5. Statistics

**Document statistics**

#### Inputs:
- `x` (Button): Run

#### Outputs:
- `component_count` (Number): Component count
- `wire_count` (Number): Wire count
- `group_count` (Number): Group count
- `by_category` (Text): Analysis by category
- `breakdown` (Text): Complete analysis

#### When to use?
- Check file complexity
- Analyze component distribution
- Documentation data

---

## 📊 Health Score System

### Score Calculation:
- Start: 100 points
- Error: -10 points each
- Warning: -5 points each
- Info: -2 points each

### Grades:
- **90-100 points**: ✅ Excellent - Perfect!
- **70-89 points**: 👍 Good - Nice
- **50-69 points**: ⚠️ Needs Attention - Requires work
- **0-49 points**: ❌ Critical - Serious issues

---

## 🔍 Items Checked

### ❌ Errors
1. **GH001: Dangling Inputs**
   - Unconnected inputs
   - May use unexpected default values
   - **Fix**: Connect required inputs

2. **GHRT1: Runtime Errors**
   - Errors during execution
   - Component not working properly
   - **Fix**: Check error message and fix

### ⚠️ Warnings
1. **GH002: Dangling Outputs**
   - Unused outputs
   - Unnecessary calculations
   - **Fix**: Use outputs or remove component

2. **GH003: Unnamed Parameters**
   - Parameters without names
   - Hard to understand
   - **Fix**: Give meaningful names
   - **Auto-fix available!**

3. **GHRT2: Runtime Warnings**
   - Warnings during execution
   - Potential problems
   - **Fix**: Check warning message

### ℹ️ Info
1. **GH004: Missing Groups**
   - No groups
   - Complex definition needs organization
   - **Fix**: Create groups with Ctrl+G

2. **GH012: Preview Disabled**
   - Preview turned off
   - Hard to debug
   - **Fix**: Enable preview where needed

---

## 💡 Real-World Workflows

### Scenario 1: Quick Check While Working
```
1. Use Health Check component
2. mode = 0 (Quick Check)
3. Check score
4. If 90+ → continue working
5. If 70- → check issues
```

### Scenario 2: File Cleanup
```
1. Use All-in-One
2. mode = 1 (Full Analysis)
3. Review all issues
4. mode = 4 (Auto-Fix)
5. auto_fix = True
6. Manually fix remaining issues
7. Check again
```

### Scenario 3: Before Sharing
```
1. Use All-in-One
2. mode = 3 (Find Issues)
3. Confirm 0 errors
4. Minimize warnings
5. Check file size with Statistics
6. Organize groups/names
7. Final check
```

### Scenario 4: Large File Optimization
```
1. Check status with Statistics
2. Find problems with Issue Finder
3. Fix simple ones with Auto-Fix
4. Manually fix complex ones
5. Verify improvements with Statistics
```

---

## 🎯 Tips & Tricks

### Performance Tips
- Start with mode=0 for large files
- Check frequently while working
- Aim to maintain 90+ score

### Organization Tips
- Always name parameters
- Create groups when 10+ components
- Clean up unused outputs
- Add comments/scribbles

### Collaboration Tips
- Always check before sharing
- Aim for 0 errors
- Set score standard (e.g., 80+)
- Establish naming conventions

---

## 🐛 Troubleshooting

### "No active Grasshopper document"
- Check if Grasshopper is open
- Verify file is loaded

### "Module not found"
- Check path at top of script
- Verify path is correct
```python
gh_path = r"C:\Users\...\RhinoScripts\src\gh\standalone"
```

### "Analysis is too slow"
- Use mode=0 for large files
- Only view Statistics (mode=2)
- Enable only some checks

### "Auto-fix not working"
- Verify auto_fix = True
- Currently only supports parameter naming
- Other fixes require manual work

---

## 📈 Future Features (Planned)

- [ ] More auto-fixes
- [ ] Automatic component alignment
- [ ] Wire cleanup
- [ ] Performance optimization suggestions
- [ ] History tracking
- [ ] Team standard checks
- [ ] Custom rules

---

## 🎓 Learn More

### Documentation
- `README.md` - Project overview
- `FORMAT_COMPARISON.md` - GHX vs JSON
- `PROMPTS.md` - How to use Claude

### For Developers
- MCP server with Claude integration
- More lint rules
- JSON analysis (100% accurate)

---

## 💬 Feedback

If you have problems or suggestions:
1. GitHub Issues (if available)
2. Team Slack
3. dongwoosuk0219@gmail.com

---

**Happy Grasshoppering! 🦗**

Version: 0.1.0-alpha
Last Updated: 2025-10-08
