# 🔧 Installation Guide - Grasshopper Live Analyzer

## 📦 Installation Methods

### Method 1: Simple Install (Recommended ⭐)

1. **Download Files**
   ```
   Clone or download the repository:
   https://github.com/dongwoosuk/grasshopper-quality-analyzer
   
   Extract to a safe location:
   Example: C:\GH_Tools\standalone\
   ```

2. **Create Python Component**
   - Add Python component in Grasshopper
   - Copy desired script (component_all_in_one.py recommended)
   - Update path:
   ```python
   gh_path = r"C:\GH_Tools\standalone"  # 👈 Update to actual path
   ```

3. **Connect Inputs/Outputs**
   - Button → run
   - Panel → report
   - Done!

---

### Method 2: Reusable .gh Files

#### A. Create Component File

1. **Create All-in-One Component**
   ```
   1. New Grasshopper file
   2. Add Python component
   3. Paste component_all_in_one.py code
   4. Update path
   5. Connect inputs:
      - Button → run
      - Slider (0-4) → mode
      - Toggle → auto_fix
      - Toggle → highlight_issues
   6. Connect outputs:
      - Panel → report
      - Panel → score
      - Panel → errors
      - Panel → warnings
   ```

2. **Save**
   ```
   Filename: GH_Analyzer_AllInOne.gh
   Location: C:\GH_Tools\components\
   ```

3. **Usage**
   ```
   Whenever needed:
   File → Open
   → Copy component
   → Paste into your file
   ```

#### B. Create Multiple Versions

Save each as separate .gh file:
- `GH_HealthCheck.gh` - Quick check
- `GH_IssueFinder.gh` - Issue search
- `GH_AutoFix.gh` - Auto-fix
- `GH_Statistics.gh` - Statistics
- `GH_AllInOne.gh` - All-in-one

---

### Method 3: Grasshopper UserObjects (Most Convenient!)

**Add to tool palette permanently**

1. **Find UserObjects Folder**
   ```
   File → Special Folders → User Object Folder
   ```

2. **Create Component**
   - Create .gh file as in Method 2
   - Select component on canvas
   - Right-click
   - "Create User Object"

3. **Configure**
   ```
   Name: GH Analyzer
   Nickname: GHA
   Category: Analysis (or your preferred category)
   Subcategory: Quality
   Description: Analyze Grasshopper definition quality
   Icon: (optional)
   ```

4. **Usage**
   ```
   Find in tab:
   Analysis → Quality → GH Analyzer
   
   Or double-click and search:
   "GHA" or "analyzer"
   ```

---

## 🎨 Recommended Layouts

### Layout 1: Simple Version
```
[Button] ──→ [GH Health Check] ──→ [Panel]
                    │
                    ├──→ [Panel] (Score)
                    └──→ [Panel] (Issues)
```

### Layout 2: Full Version
```
[Button] ──────→ run
[Slider 0-4] ──→ mode        [Panel] ← report
[Toggle] ──────→ auto_fix    [Panel] ← score
[Toggle] ──────→ highlight   [Panel] ← errors
                  ↓           [Panel] ← warnings
            [All-in-One]      [Panel] ← stats
                              [Panel] ← fixed
```

### Layout 3: Dashboard Style
```
       ┌─────────────────────────────────┐
       │      🎯 GH ANALYZER              │
       ├─────────────────────────────────┤
       │                                  │
       │  [●] Run   Mode: [==2==]        │
       │  [✓] Auto-fix  [✓] Highlight    │
       │                                  │
       │  ┌─────────────────────────┐   │
       │  │ Score: 85/100           │   │
       │  │ Status: 👍 Good         │   │
       │  └─────────────────────────┘   │
       │                                  │
       │  ❌ Errors: 2                   │
       │  ⚠️  Warnings: 5                │
       │  ℹ️  Info: 3                    │
       │                                  │
       └─────────────────────────────────┘
```

---

## ✅ Installation Verification

### Test 1: Basic Operation
1. Click button
2. Check if report appears in panel
3. Verify score output

### Test 2: All Modes
```
Mode 0: Quick Check - Brief summary
Mode 1: Full Analysis - Detailed report
Mode 2: Statistics - Stats only
Mode 3: Find Issues - Issue search
Mode 4: Auto-Fix - Fix & highlight
```

### Test 3: Auto-Fix
1. Add unnamed slider
2. Select Mode 4
3. Set auto_fix = True
4. Run
5. Check if slider has name

---

## 🐛 Troubleshooting

### "Module not found" Error
**Problem**: Python can't find gh_live_analyzer.py

**Solution**:
```python
# Update path at top of script to actual location
gh_path = r"C:\YourActualPath\standalone"

# How to find correct path:
# 1. Open standalone folder in Explorer
# 2. Copy address bar
# 3. Convert to Python string (\ → \\)
```

### "No active document" Error
**Problem**: No Grasshopper document

**Solution**:
1. Verify Grasshopper is open
2. Check if file is loaded
3. Restart Rhino

### "Analysis is slow"
**Problem**: Large file takes time

**Solution**:
1. Use Mode 0 (Quick Check)
2. Save frequently while working
3. Analyze in sections using groups

### "Auto-fix not working"
**Problem**: Nothing gets fixed

**Check**:
1. `auto_fix = True` is set
2. Mode 4 is selected
3. Currently only parameter naming is automated
4. Other fixes require manual work

---

## 🔄 Updating

### Update to New Version

1. **Backup Files**
   ```
   Backup existing standalone folder
   ```

2. **Copy New Files**
   ```
   Overwrite with new gh_live_analyzer.py
   ```

3. **Update Components**
   ```
   Update Python scripts in .gh files
   ```

4. **Test**
   ```
   Test on simple file
   ```

---

## 📁 File Structure

```
standalone/
├── gh_live_analyzer.py          # Core engine ⭐
├── component_all_in_one.py      # All-in-one component
├── component_health_check.py    # Simple check
├── component_issue_finder.py    # Issue search
├── component_auto_fix.py        # Auto-fix
├── component_statistics.py      # Statistics
├── USER_GUIDE.md               # User guide
└── INSTALLATION.md             # This file
```

### Required Files
- ✅ `gh_live_analyzer.py` - Must have!
- ✅ `component_*.py` - Use what you need

---

## 🎓 Next Steps

### 1. Basic Usage
- [ ] Health Check to start
- [ ] Understand scoring system
- [ ] Learn issue types

### 2. Advanced Usage
- [ ] Master All-in-One
- [ ] Use Auto-Fix
- [ ] Integrate into workflow

### 3. Team Adoption
- [ ] Set standards
- [ ] Define score criteria
- [ ] Create training materials

---

## 💡 Tips

### Performance Optimization
```python
# For large files, use lightweight version
# component_health_check.py
# style = 'simple'
```

### Frequent Usage
```
1. Create as UserObject
2. Include in template files
3. Set up shortcuts (if possible)
```

### Team Deployment
```
1. Place standalone folder on network drive
2. Use same path in all scripts
3. Share .gh files
4. Distribute guide documents
```

---

## 📞 Support

### Having Issues?

1. **USER_GUIDE.md** Check first
2. **This document** Read again
3. **Team Slack** Ask question
4. **GitHub Issues** Report bug

### Suggestions

New features or improvements:
- Share with team
- Modify yourself (open source!)
- Submit Pull Request

---

## 🎉 Installation Complete!

Now you're ready to analyze Grasshopper definitions!

### First Run:
```
1. Open simple definition
2. Add Health Check component
3. Click button
4. Check report
5. Congratulations! 🎊
```

---

**Happy Analyzing! 🚀**

Version: 0.1.0-alpha
Last Updated: 2025-10-08
Contact: GitHub Issues
