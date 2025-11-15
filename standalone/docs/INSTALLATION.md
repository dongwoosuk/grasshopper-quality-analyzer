# 🔧 Installation Guide - Grasshopper Quality Analyzer

**Version 0.3.0-alpha** | **Last Updated: 2025-11-15**

Complete installation guide for the standalone version.

---

## 📦 Installation Methods

### Method 1: Quick Install (Recommended ⭐)

**Perfect for: First-time users, quick testing**

1. **Download Files**
   ```
   Clone or download:
   https://github.com/dongwoosuk/grasshopper-quality-analyzer
   
   Extract to:
   C:\GH_Tools\grasshopper-quality-analyzer\standalone\
   ```

2. **Create Python Component**
   - Add Python component in Grasshopper (Math → Script → Python)
   - Choose a component script (e.g., `component_health_check.py`)
   - Copy entire script content
   - Paste into Python component
   - Update path (around line 20-25):
   ```python
   gh_path = r"C:\GH_Tools\grasshopper-quality-analyzer\standalone"
   ```

3. **Connect Inputs/Outputs**
   - Button → `run`
   - Panel → `report`
   - Done!

---

### Method 2: Reusable .gh Files

**Perfect for: Frequent usage, consistent setup**

#### Create Component Files

For each component you use frequently:

1. **Setup Component**
   ```
   1. New Grasshopper file
   2. Add Python component
   3. Paste component script
   4. Update path
   5. Add inputs/outputs with proper names
   6. Test thoroughly
   ```

2. **Save for Reuse**
   ```
   Filename examples:
   - GH_HealthCheck.gh
   - GH_PerformanceProfiler.gh
   - GH_ParameterNamer.gh
   
   Location: C:\GH_Tools\components\
   ```

3. **Usage**
   ```
   File → Open
   → Select component file
   → Copy component
   → Paste into your definition
   ```

---

### Method 3: User Objects (Most Convenient!)

**Perfect for: Power users, permanent tool access**

#### Add to Grasshopper Toolbar

1. **Find UserObjects Folder**
   ```
   File → Special Folders → User Object Folder
   
   Default locations:
   C:\Users\[Username]\AppData\Roaming\Grasshopper\UserObjects
   ```

2. **Create User Object**
   - Create .gh file as in Method 2
   - Select component on canvas
   - Right-click → "Create User Object"

3. **Configure**
   ```
   Name: GH Health Check
   Nickname: GHC
   Category: Analysis (or your choice)
   Subcategory: Quality
   Description: Quick health check for GH definitions
   Exposure: Primary (shows in tab)
   Icon: (optional custom icon)
   ```

4. **Access**
   ```
   From toolbar:
   Analysis → Quality → GH Health Check
   
   Or double-click canvas and search:
   "GHC" or "health"
   ```

---

## 🎨 Recommended Component Setups

### Setup 1: Health Check (Quick Quality Check)
```
[Button] ──→ run          [Panel] ← report
[Text] ────→ style        [Panel] ← score
                          [Panel] ← issue_count
   ↓
[Health Check]
```

### Setup 2: Performance Profiler (Find Bottlenecks)
```
[Button] ──→ run               [Panel] ← report
[Slider 0-2] → mode            [Panel] ← performance_score
[Number] ───→ threshold_ms     [List] ←─ slow_components
[Toggle] ───→ auto_select      [Number] ← total_time_ms
[Text] ─────→ report_style
   ↓
[Performance Profiler]
```

### Setup 3: Parameter Namer (Batch Rename)
```
[Button] ──→ run              [Panel] ← report
[Text] ────→ component_type   [Number] ← renamed_count
[Text] ────→ name_prefix      [Panel] ← component_list
[Text] ────→ name_suffix
[Number] ──→ start_number
   ↓
[Parameter Namer]
```

### Setup 4: Dashboard Style (Multiple Components)
```
┌────────────────────────────────────┐
│   📊 QUALITY DASHBOARD             │
├────────────────────────────────────┤
│                                    │
│  [Health Check]  Score: 85/100    │
│                                    │
│  [Issue Finder]  Errors: 0         │
│                  Warnings: 3       │
│                                    │
│  [Performance]   Avg Time: 45ms    │
│                  Bottlenecks: 2    │
│                                    │
│  [Statistics]    Components: 142   │
│                  Complexity: Med   │
└────────────────────────────────────┘
```

---

## ✅ Installation Verification

### Test 1: Basic Connection
```python
# Paste this test script in Python component
import sys
gh_path = r"YOUR_PATH_HERE"
sys.path.insert(0, gh_path)

try:
    from gh_live_analyzer import GHLiveAnalyzer
    a = "✅ Installation successful!"
except Exception as e:
    a = f"❌ Error: {str(e)}"
```

### Test 2: Health Check
1. Use `component_health_check.py`
2. Click button
3. Verify report appears
4. Check score is reasonable (0-100)

### Test 3: Performance Profiler
1. Use `component_performance_profiler.py`
2. Set mode = 0 (Quick)
3. Click button
4. Verify timing results appear

### Test 4: All Components
Create a test file with all 9 components to ensure they all work.

---

## 🐛 Troubleshooting

### "Module not found" Error

**Problem**: Python can't find `gh_live_analyzer.py`

**Solutions**:
```python
# 1. Check path is correct
gh_path = r"C:\Actual\Path\To\standalone"

# 2. Verify file exists
# Navigate to folder and confirm gh_live_analyzer.py is there

# 3. Use absolute path (not relative)
# ❌ Wrong: gh_path = "standalone"
# ✅ Correct: gh_path = r"C:\Full\Path\standalone"

# 4. Check for typos
# Common mistakes:
# - Missing 'r' before string: r"..."
# - Forward slashes: / instead of \
# - Extra spaces in path
```

### "No active Grasshopper document" Error

**Problem**: No GH file loaded

**Solutions**:
1. Create new file or open existing one
2. Ensure definition has at least one component
3. Try running solution (F5) first
4. Restart Rhino if persists

### "Analysis is Very Slow"

**Problem**: Large file takes long time

**Solutions**:
```python
# 1. Use Quick mode (Health Check)
style = 'simple'  # Faster than 'full'

# 2. Performance Profiler - use Quick mode
mode = 0  # Single pass, fast

# 3. Disable unnecessary checks
# Use specific components instead of checking everything

# 4. Profile your definition first
# Find and fix actual bottlenecks
```

### Scripts Work But No Output

**Problem**: Panels show nothing

**Checklist**:
- [ ] Outputs connected to Panels?
- [ ] Button clicked?
- [ ] `run` input connected?
- [ ] Any error messages in Grasshopper?

### Path Works on One Computer, Not Another

**Problem**: Different computer, different path

**Solution - Auto-detect path**:
```python
import sys
import os

def find_analyzer():
    """Auto-detect installation location"""
    common_paths = [
        r"C:\GH_Tools\grasshopper-quality-analyzer\standalone",
        r"C:\GH_Analyzer\standalone",
        r"C:\Users\{}\Desktop\gh_analyzer\standalone".format(
            os.environ.get('USERNAME', '')
        ),
    ]
    for p in common_paths:
        if os.path.exists(os.path.join(p, "gh_live_analyzer.py")):
            return p
    return None

gh_path = find_analyzer()
if not gh_path:
    gh_path = r"FALLBACK_PATH"  # Manual fallback

if gh_path:
    sys.path.insert(0, gh_path)
```

---

## 🔄 Updating to New Version

### Update Process

1. **Backup Current Version**
   ```
   Rename folder:
   standalone → standalone_backup_v0.2.0
   ```

2. **Download New Version**
   ```
   Download v0.3.0-alpha
   Extract to standalone\
   ```

3. **Update Component Scripts**
   ```
   Replace old scripts with new ones
   Update paths if needed
   ```

4. **Test New Features**
   ```
   Test on simple file first
   Verify all components work
   Check new features (Performance Profiler, etc.)
   ```

5. **Update Team**
   ```
   Notify team of changes
   Share updated .gh files
   Update documentation
   ```

---

## 📁 File Structure Reference

```
standalone/
├── 📜 Core Engine
│   └── gh_live_analyzer.py          (~3,900 lines)
│
├── 🎨 Analysis Components (4)
│   ├── component_health_check.py
│   ├── component_issue_finder.py
│   ├── component_statistics.py
│   └── component_performance_profiler.py  ⚡ NEW
│
├── 🔧 Automation Components (5)
│   ├── component_parameter_namer.py
│   ├── component_auto_alignment.py
│   ├── component_preview_control.py       ⚡ NEW
│   ├── component_display_mode.py          ⚡ NEW
│   └── component_python_io_manager.py
│
├── 📚 Documentation
│   ├── QUICKSTART.md
│   ├── README.md
│   └── docs/
│       ├── USER_GUIDE.md
│       ├── USER_GUIDE_KO.md
│       ├── INSTALLATION.md (this file)
│       └── ...
│
└── 🧪 Examples
    └── test_connection.py
```

### Required Files
- ✅ **gh_live_analyzer.py** - Core engine (REQUIRED)
- ✅ **component_*.py** - Use what you need

---

## 🎓 Next Steps

### Beginner Path
```
1. ✅ Install Health Check
2. ✅ Run on simple file
3. ✅ Read USER_GUIDE.md
4. ✅ Try other components
5. ✅ Integrate into workflow
```

### Advanced Path
```
1. ✅ Install all 9 components
2. ✅ Create User Objects
3. ✅ Set up dashboard
4. ✅ Customize scripts
5. ✅ Share with team
```

### Team Deployment
```
1. ✅ Install on network drive
2. ✅ Standardize paths
3. ✅ Create .gh templates
4. ✅ Document standards
5. ✅ Train team members
```

---

## 💡 Pro Tips

### For Individual Use
```
✨ Create User Objects for frequent components
✨ Save dashboard .gh file for quick access
✨ Run Health Check every 30 minutes
✨ Use Performance Profiler when definition slows down
```

### For Team Use
```
✨ Place on shared network drive
✨ Use consistent paths in all scripts
✨ Create team .gh templates
✨ Set minimum quality standards (e.g., score >80)
✨ Include in code review checklist
```

### For Power Users
```
✨ Customize scripts for your workflow
✨ Create custom auto-detect logic
✨ Integrate with other tools
✨ Contribute improvements back to project
```

---

## 📞 Getting Help

### Resources
1. **[USER_GUIDE.md](USER_GUIDE.md)** - Complete component documentation
2. **[QUICKSTART.md](../QUICKSTART.md)** - 5-minute quick start
3. **[GitHub Issues](https://github.com/dongwoosuk/grasshopper-quality-analyzer/issues)** - Bug reports
4. **[GitHub Discussions](https://github.com/dongwoosuk/grasshopper-quality-analyzer/discussions)** - Questions

### Common Issues
- Path problems → This guide, troubleshooting section
- Usage questions → USER_GUIDE.md
- Performance issues → Use Performance Profiler component
- Bug reports → GitHub Issues

---

## 🎉 Installation Complete!

You're now ready to analyze Grasshopper definitions!

### Quick Checklist:
- [ ] Files extracted to permanent location
- [ ] Path updated in scripts
- [ ] Test connection successful
- [ ] Health Check working
- [ ] Outputs showing in Panels
- [ ] Ready to use!

---

**Happy Analyzing! 🚀**

Version: 0.3.0-alpha  
Last Updated: 2025-11-15  
For support: dongwoosuk0219@gmail.com
