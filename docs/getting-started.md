# ⚡ Quick Start - Get Running in 5 Minutes

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
Extract to: C:\GH_Tools\standalone\
```

What's inside:
- ✅ gh_live_analyzer.py (core engine!)
- ✅ component_*.py (5 files)
- ✅ Documentation

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
"""Quick Test"""
import sys
gh_path = r"C:\GH_Tools\standalone"  # UPDATE THIS PATH!
sys.path.insert(0, gh_path)

from gh_live_analyzer import GHLiveAnalyzer

if x:
    analyzer = GHLiveAnalyzer()
    stats = analyzer.get_statistics()
    score = analyzer.calculate_health_score()
    
    a = f"✅ SUCCESS!\nScore: {score}/100\nComponents: {stats['total_components']}"
else:
    a = "Press button"
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
Panel shows "✅ SUCCESS!" = You're ready!
```

---

### 3️⃣ Real Usage (2 min)

#### Upgrade to All-in-One Component

**Add New Python Component:**

1. **Copy Code**
   - Open `component_all_in_one.py`
   - Copy all
   - Paste into Python component

2. **Connect Inputs**
   ```
   [Button] → run
   [Slider 0-4] → mode (default: 0)
   ```

3. **Connect Outputs**
   ```
   report → [Panel]
   score → [Panel]
   ```

4. **Run!**
   ```
   Click button → Panel shows report
   ```

---

## 🎨 Mode Explanation (Slider values)

```
0 = Quick Check    (fastest) ⚡
1 = Full Analysis  (most detailed) 📊
2 = Statistics     (stats only) 📈
3 = Find Issues    (issue search) 🔍
4 = Auto-Fix       (auto repair) 🔧
```

---

## ✅ Success Confirmation

### You should see:
```
==================================================
GRASSHOPPER HEALTH CHECK
==================================================

📊 Score: 85/100
🔧 Components: 15
🔗 Connections: 23
📁 Groups: 2

✅ No issues found!
==================================================
```

---

## 🎯 What You Can Do Now

### Basic Usage
```python
# Check frequently while working
mode = 0  # Quick Check
[Click Button]

# Check score
90+ = ✅ Perfect!
70-89 = 👍 Good
50-69 = ⚠️  Needs attention
0-49 = ❌ Requires fixes
```

### Problem Solving
```python
# Find issues
mode = 3  # Find Issues
[Click Button]
→ Detailed issue list

# Auto-fix
mode = 4  # Auto-Fix
auto_fix = True
[Click Button]
→ Auto-names parameters
```

---

## 🐛 Troubleshooting

### "Module not found"
```python
# Path is incorrect
# Update at top of script:
gh_path = r"ACTUAL_PATH"

# How to find correct path:
# 1. Open standalone folder in Explorer
# 2. Copy address bar
# 3. Use as r"copied_path"
```

### "No active document"
```
→ Check if Grasshopper file is open
→ Restart Rhino
```

### "Too slow"
```
→ Use mode = 0 (fastest)
→ For large files (1000+ components)
```

---

## 📚 Next Steps

### Learn More
```
1. USER_GUIDE.md - Complete guide
2. Try all 5 components
3. Integrate into workflow
```

### Share with Team
```
1. Introduce to teammates
2. Set standard score (e.g., 80+)
3. Include in code review
```

---

## 🎉 Congratulations!

**You mastered the Grasshopper analysis tool in 5 minutes!**

### Next Checks:
- [ ] Test on real project
- [ ] Try all modes
- [ ] Use Auto-Fix
- [ ] Read USER_GUIDE.md
- [ ] Share with team

---

## 💡 Tips

```
✨ Once before starting work
✨ Every 30 minutes
✨ Always before saving
✨ Must before sharing!
```

---

**Happy Analyzing! ⚡**

```
Start time: Now
Complete time: 5 minutes later
Result: Better Grasshopper definitions! 🦗
```

---

## 🔗 Links

- **Full Guide**: USER_GUIDE.md
- **Detailed Setup**: INSTALLATION.md
- **Project Info**: README.md
- **Complete Docs**: COMPLETE.md

---

Questions? Check USER_GUIDE.md or open an issue on GitHub!

**Start now! 🚀**
