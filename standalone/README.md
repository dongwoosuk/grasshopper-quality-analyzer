# 🦗 Grasshopper Live Analyzer - Standalone Package

## 🎯 Overview

Complete definition analysis tool that **works directly in Grasshopper**!

- ✅ No MCP/Claude required
- ✅ Real-time analysis & performance profiling
- ✅ Auto-fix & automation features
- ✅ 9 modular components
- ✅ 18 lint rules (GH001-GH018)

---

## 🚀 Quick Start

### 30-Second Installation
```
1. Add Python component
2. Choose a component (e.g., component_health_check.py)
3. Update path (1 line)
4. Connect inputs (path, optionally run_profile, etc.)
5. Done!
```

### First Run
```
[Button/Toggle] → [Component] → [Panel]
```

**That's it!** 🎉

---

## 📦 What's Included

### 9 Modular Components

**Analysis Tools (4)**
1. **Health Check** - Quick quality overview
2. **Issue Finder** - Find and highlight issues
3. **Statistics** - Detailed component stats
4. **Performance Profiler** ⭐ NEW - Bottleneck identification

**Automation Tools (5)**
5. **Parameter Namer** - Auto-name sliders/panels
6. **Auto Alignment** - Layout organization
7. **Preview Control** - Enable/disable all previews
8. **Display Mode** - Icon/Name/Both control
9. **Python I/O Manager** - Auto-manage Python script I/O

### Analysis Features
- 🔍 18 lint rules (GH001-GH018)
- 📊 Health score (0-100)
- ⚡ Real-time analysis
- 🚀 Performance profiling ⭐ NEW
- 🔧 Auto-fix & automation
- 🎯 Issue highlighting
- 📈 Detailed statistics

---

## 💡 Key Features

### 1. Real-time Lint Checks
```python
❌ Dangling Inputs (error)
⚠️  Dangling Outputs (warning)
⚠️  Unnamed Parameters (warning)
ℹ️  Missing Groups (info)
... 15+ rules
```

### 2. Health Score
```
100 - errors×10 - warnings×5 - info×2

✅ 90-100: Excellent
👍 70-89: Good
⚠️  50-69: Needs Attention
❌ 0-49: Critical
```

### 3. Auto-Fix
```
✅ Auto-name parameters
🔍 Highlight problem components
📊 Before/after comparison
```

### 4. Report Styles
```
- Simple: One-line summary
- Compact: Panel summary
- Full: Complete detailed report
```

---

## 📖 Documentation

### Getting Started
- **INSTALLATION.md** - Installation guide
- **USER_GUIDE.md** - Complete user guide

### Advanced
- **../analyzer/lint_rules.py** - Rule details
- **gh_live_analyzer.py** - API documentation

---

## 🎨 Usage Examples

### Example 1: Check While Working
```
Work → Click button → Check score → Continue
```

### Example 2: Clean Up File
```
Full Analysis → Review issues → Auto-Fix → Manual fixes
```

### Example 3: Before Sharing
```
Find Issues → Confirm 0 errors → Statistics → Final check
```

---

## 🔧 Technical Specs

### Requirements
- Rhino 7/8
- Grasshopper
- Python 2.7 (built-in GH)

### Supported Features
- ✅ Real-time document scan
- ✅ Component analysis
- ✅ Wire tracking
- ✅ Runtime errors/warnings
- ✅ Auto-fix (partial)

### Limitations
- ⚠️  Large files may be slow (>1000 components)
- ⚠️  Only some fixes automated
- ⚠️  Group creation is manual

---

## 🎯 Use Cases

### Individual
- Real-time checks while working
- Validation before saving
- Maintain code quality

### Team
- Standard quality criteria
- Code reviews
- Onboarding tool

### Education
- Learn best practices
- Avoid common mistakes
- Understand definition quality

---

## 📊 Statistics

### Code
- Core engine: ~3,900 lines (+550%)
- Components: 9 (+80%)
- Lint rules: 18 (+20%)
- Functions: 50+

### Features
- Analysis components: 4
- Automation components: 5
- Performance profiling modes: 3
- Report styles: 3

---

## 🔄 vs MCP Version

### Standalone (This!)
✅ Simple installation
✅ Grasshopper only
✅ Real-time analysis
✅ Quick feedback
⚠️  Basic analysis
⚠️  Limited auto-fix

### MCP + Claude
✅ Complete analysis
✅ AI suggestions
✅ GHX/JSON parsing
✅ Version comparison
⚠️  Complex setup
⚠️  External dependencies

### When to Use What?
```
Daily work → Standalone
Detailed analysis → MCP + Claude
File sharing → Both
Team standards → Both
```

---

## 🚧 Development Roadmap

### v1.0 (Current) ✅
- [x] Core analysis engine
- [x] 5 components
- [x] 15 lint rules
- [x] Auto-fix (basic)
- [x] Complete documentation

### v1.1 (Planned)
- [ ] More auto-fixes
- [ ] Performance optimization
- [ ] Custom rules
- [ ] History tracking

### v2.0 (Future)
- [ ] Auto component arrangement
- [ ] Wire cleanup
- [ ] Performance analysis
- [ ] Team dashboard

---

## 🤝 Contributing

### Bug Reports
1. Reproduction steps
2. Expected result
3. Actual result
4. GH version

### Feature Requests
1. Use case
2. Expected behavior
3. Priority

### Code Contributions
1. Fork
2. Branch
3. Commit
4. Pull Request

---

## 📄 License

MIT License - Free to use/modify/distribute

---

## 🙏 Acknowledgments

- Grasshopper Team
- Rhino Python
- Pilot Testing Team
- All beta testers

---

## 📞 Contact

- **Email**: dongwoosuk0219@gmail.com
- **GitHub**: [@dongwoosuk](https://github.com/dongwoosuk)

---

## 📚 Related Projects

### Same Project
- **MCP Analyzer** - Claude integration
- **dual_save** - Simultaneous GH/GHX save
- **export_to_json** - JSON export

### External Tools
- **Grasshopper** - Rhino parametric design
- **Claude** - AI assistant
- **MCP** - Model Context Protocol

---

## 🎉 Get Started

```
1. Read INSTALLATION.md
2. Install components
3. Read USER_GUIDE.md
4. Run first analysis
5. Enjoy! 🦗
```

---

**Happy Grasshoppering!**

Version: 0.3.0-alpha  
Release Date: 2025-11-15  
Status: ⚡ Alpha - Active Development
