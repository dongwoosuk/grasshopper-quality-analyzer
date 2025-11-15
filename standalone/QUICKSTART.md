# ⚡ Quick Start - Get Running in 5 Minutes

**Grasshopper Quality Analyzer v0.3.0-alpha**

## 🎯 Goal: Complete Your First Analysis in 5 Minutes!

---

## 📋 Requirements
- ✅ Rhino + Grasshopper
- ✅ 5 minutes
- ✅ This guide

---

## 🚀 Get Started in 3 Steps

### 1️⃣ Prepare Files (1 min)

**Locate the standalone folder:**
```
Download from: https://github.com/dongwoosuk/grasshopper-quality-analyzer
Extract to: C:\GH_Tools\grasshopper-quality-analyzer\standalone\
```

**What's inside:**
- ✅ `gh_live_analyzer.py` (core engine, ~3,900 lines)
- ✅ 9 component files (`component_*.py`)
- ✅ Complete documentation

---

### 2️⃣ Test Connection (2 min)

#### A. Open Grasshopper
```
Launch Rhino → Type "Grasshopper"
```

#### B. Add Python Component
```
Math → Script → Python
```

#### C. Paste Test Script
```python
"""Quick Connection Test"""
import sys

# UPDATE THIS PATH to your actual location!
gh_path = r"C:\GH_Tools\grasshopper-quality-analyzer\standalone"
sys.path.insert(0, gh_path)

from gh_live_analyzer import GHLiveAnalyzer

if x:
    analyzer = GHLiveAnalyzer()
    stats = analyzer.get_statistics()
    score = analyzer.calculate_health_score()
    
    a = f"✅ CONNECTION SUCCESS!\n\nHealth Score: {score}/100\nComponents: {stats['total_components']}\nWires: {stats['total_wires']}\n\nReady to analyze!"
else:
    a = "Click button to test connection"
```

#### D. Connect & Run
```
[Button] → x input
        ↓
[Python Component]
        ↓
a output → [Panel]
```

#### E. Click Button!
```
✅ Panel shows "CONNECTION SUCCESS!" = You're ready!
❌ Error message? → Check path in step C
```

---

### 3️⃣ Choose Your Component (2 min)

#### For First-Time Users: Health Check (Recommended ⭐)

**Simple quality overview in seconds**

1. **Add New Python Component**

2. **Copy Code**
   - Open `component_health_check.py` in text editor
   - Copy entire contents
   - Paste into Python component

3. **Update Path** (line 20-25)
   ```python
   # UPDATE THIS PATH!
   gh_path = r"C:\GH_Tools\grasshopper-quality-analyzer\standalone"
   ```

4. **Connect Inputs**
   ```
   [Button] → run
   [Text "simple"] → style (optional, default is "simple")
   ```

5. **Connect Outputs**
   ```
   report → [Panel]
   score → [Panel]
   issue_count → [Panel]
   ```

6. **Run!**
   ```
   Click button → See your health score!
   ```

---

## 🎨 Understanding Your Results

### Health Score Interpretation:
```
90-100 ✅ Excellent    - Production ready!
70-89  👍 Good         - Minor improvements needed
50-69  ⚠️  Needs Work  - Significant issues found
0-49   ❌ Critical     - Major problems exist
```

### Example Output:
```
==================================================
GRASSHOPPER HEALTH CHECK
==================================================

📊 Health Score: 85/100
🔧 Total Components: 42
🔗 Total Wires: 67
📁 Groups: 3

🔍 Issues Found:
  ❌ Errors: 0
  ⚠️  Warnings: 3
  ℹ️  Info: 5

✅ Good quality! Minor improvements suggested.
==================================================
```

---

## 🎯 What You Can Do Now

### Quick Quality Checks (Health Check)
```python
Work on definition
   ↓
Click button every 30 min
   ↓
Check score
   ↓
Keep score above 80!
```

### Find Specific Problems (Issue Finder)
```python
Use component_issue_finder.py
   ↓
Enable: errors + warnings
   ↓
Review detailed issue list
   ↓
Fix problems
```

### Performance Analysis ⚡ NEW
```python
Use component_performance_profiler.py
   ↓
mode = 1 (Detailed)
   ↓
Find slow components (>100ms)
   ↓
Optimize bottlenecks
```

---

## 📦 All 9 Components at a Glance

### Analysis Tools (4)
| Component | Use When | Difficulty |
|-----------|----------|------------|
| **Health Check** | Quick quality check | ⭐ Easy |
| **Issue Finder** | Need specific problem details | ⭐⭐ Medium |
| **Statistics** | Want component breakdown | ⭐ Easy |
| **Performance Profiler** ⚡ | Definition is slow | ⭐⭐ Medium |

### Automation Tools (5)
| Component | Use When | Difficulty |
|-----------|----------|------------|
| **Parameter Namer** | Need to rename sliders/panels | ⭐⭐ Medium |
| **Auto Alignment** | Layout is messy | ⭐⭐⭐ Advanced |
| **Preview Control** | Need to enable/disable all previews | ⭐ Easy |
| **Display Mode** | Want Icon/Name/Both control | ⭐ Easy |
| **Python I/O Manager** | Auto-manage Python script I/O | ⭐⭐ Medium |

---

## 🐛 Troubleshooting

### "Module not found" Error
```python
# Issue: Python can't find gh_live_analyzer.py
# Fix: Update path in your script

# Correct format:
gh_path = r"C:\Full\Path\To\standalone"

# How to find correct path:
# 1. Open standalone folder in Windows Explorer
# 2. Click address bar
# 3. Copy the full path
# 4. Paste in script with r"..." format
```

### "No active Grasshopper document" Error
```
Issue: No Grasshopper file loaded
Fix: 
  1. Create new GH file or open existing one
  2. Try again
  3. If still failing, restart Rhino
```

### Script Runs But Shows Nothing
```
Issue: Output not connected or button not clicked
Fix:
  1. Connect outputs to Panels
  2. Make sure button is connected to 'run' input
  3. Click the button
```

### Analysis is Slow (>10 seconds)
```
Issue: Large file (500+ components)
Tips:
  - Use Health Check instead of full analysis
  - Use style='simple' for faster results
  - Consider Performance Profiler to find bottlenecks
```

---

## 📚 Next Steps

### 1. Master the Basics
```
✅ Health Check → Use daily
✅ Issue Finder → Use before sharing
✅ Statistics → Understand your file
```

### 2. Explore Advanced Features
```
⚡ Performance Profiler → Find bottlenecks
🔧 Parameter Namer → Standardize names
📐 Auto Alignment → Organize layout
```

### 3. Read Full Documentation
```
📖 USER_GUIDE.md → Complete component guide
📖 INSTALLATION.md → Advanced setup options
📖 ../docs/best-practices.md → Quality standards
```

### 4. Integrate Into Workflow
```
✨ Run Health Check every 30 minutes
✨ Check before saving
✨ Verify before sharing with team
✨ Profile performance for large definitions
```

---

## 💡 Pro Tips

### Daily Workflow
```
Start work
  ↓
Quick Health Check
  ↓
Work for 30 min
  ↓
Check again (keep score >80)
  ↓
Before saving → Full check
```

### Before Sharing
```
1. Health Check → Target 90+
2. Issue Finder → Fix all errors
3. Performance Profiler → Check no major bottlenecks
4. Statistics → Document complexity
5. Share!
```

### Team Standards
```
Minimum Score: 80/100
Zero Errors: Required
Parameter Naming: All must have names
Performance: No components >200ms
```

---

## 🎉 Congratulations!

**You've mastered the basics in 5 minutes!**

### Ready for More?
- [📖 Complete User Guide](docs/USER_GUIDE.md) - All 9 components detailed
- [📖 Installation Guide](docs/INSTALLATION.md) - Advanced setup
- [🌏 한글 가이드](docs/USER_GUIDE_KO.md) - Korean documentation
- [📊 Best Practices](../docs/best-practices.md) - Quality standards

---

## 🔗 Quick Links

- **GitHub**: [grasshopper-quality-analyzer](https://github.com/dongwoosuk/grasshopper-quality-analyzer)
- **Issues**: [Report bugs](https://github.com/dongwoosuk/grasshopper-quality-analyzer/issues)
- **Discussions**: [Ask questions](https://github.com/dongwoosuk/grasshopper-quality-analyzer/discussions)

---

**Happy Analyzing! ⚡**

```
Start time: Now
Complete time: 5 minutes later
Result: Better Grasshopper definitions! 🦗
```

---

Version: 0.3.0-alpha  
Last Updated: 2025-11-15  
For support: dongwoosuk0219@gmail.com
