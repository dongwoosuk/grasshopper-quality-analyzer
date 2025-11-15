# Changelog

All notable changes to the Grasshopper Quality Analyzer project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0-alpha] - 2025-11-02 - Performance & Architecture ⚡

### Added
- ⚡ **Performance Profiler Component** - New standalone component for performance analysis
  - Real-time component execution time measurement
  - Bottleneck identification (>100ms threshold configurable)
  - Performance score calculation (0-100, higher is better)
  - Plugin performance breakdown analysis
  - Optimization suggestions with actionable advice
  - 3 profiling modes: Quick (1 pass), Detailed (5 passes avg), Live monitoring
  - Auto-select slow components in canvas
  - Comprehensive performance reports (simple/compact/full styles)

- 📊 **Performance Profiling Methods** - gh_live_analyzer.py (+538 lines)
  - `profile_document()` - Core profiling engine with iteration support
  - `find_performance_bottlenecks()` - Identify slow components automatically
  - `analyze_performance_patterns()` - Pattern analysis (heavy preview, data tree ops, scripts)
  - `get_plugin_performance_breakdown()` - Per-plugin timing analysis
  - `calculate_performance_score()` - 0-100 scoring system
  - `generate_performance_report()` - Formatted report generation
  - `highlight_slow_components()` - Canvas selection integration
  - `get_optimization_suggestions()` - Smart, context-aware suggestions
  - `get_component_execution_times()` - Raw timing data access

- 🔍 **Performance Lint Rules** - lint_rules.py (GH016-GH018)
  - **GH016**: Slow Component Execution (warning) - Components >100ms
  - **GH017**: Computational Bottleneck (info) - Components >20% total time
  - **GH018**: Heavy Preview Geometry (info) - Large preview geometries impacting viewport

### Changed
- 📝 **Consistent Naming Convention**
  - Renamed: `python_auto_manager In N Out.py` → `component_python_io_manager.py`
  - All components now follow `component_*.py` naming pattern
  - Improves discoverability and maintains architectural consistency

- 📦 **Project Stats Updated**
  - Code: ~1,500 → ~3,900 lines (+160%)
  - Components: 5 → 9 (+80%)
  - Lint Rules: 15 → 18 (+20%)

- 🎨 **Display Manager Split** - Better modularity and single responsibility
  - Split `component_display.py` into two focused components:
    - `component_preview_control.py` - Simple preview enable/disable for all components
    - `component_display_mode.py` - Per-component display mode control (Icon/Name/Both)
  - Improved usability with clearer component purposes
  - Follows single responsibility principle

### Removed
- ❌ **component_all_in_one.py** - Removed for better modularity
  - Redundant functionality (duplicated Health Check + Issue Finder)
  - Users can now combine specific components as needed
  - Reduces maintenance burden and improves flexibility
  - Follows Unix philosophy: "do one thing and do it well"

### Architecture Improvements
- 🏗️ **Modular Design** - Clear separation of concerns
  - **Analysis Tools** (4 components): Health Check, Issue Finder, Statistics, Performance Profiler
  - **Automation Tools** (5 components): Parameter Namer, Auto Alignment, Preview Control, Display Mode, Python I/O Manager
  - No functional duplication
  - Each component has a single, well-defined purpose

### Performance
- ⚡ Component execution time tracking with <1ms overhead
- 📊 Efficient profiling with configurable iteration counts
- 🎯 Smart bottleneck detection using Pareto principle (80/20 rule)
- 💾 Minimal memory footprint for timing data storage

---

## [0.1.0-alpha] - 2025-10-08 - Alpha Release 🎉

### 🎊 First Public Alpha Release

This is the initial alpha release for public testing and feedback collection.

**⚠️ Alpha Version Notice:**
- This is a preview/testing version
- Some features may be incomplete or unstable
- Feedback and bug reports are highly encouraged
- Not recommended for critical production use yet

### Added
- ✅ **Standalone Components** - 5 ready-to-use Python components
  - All-in-One (with universal path detection)
  - Health Check
  - Issue Finder
  - Auto-Fix
  - Statistics
- ✅ **Core Analysis Engine** - GHLiveAnalyzer with 600+ lines
- ✅ **15+ Lint Rules** - Comprehensive quality checks
  - 2 Error rules
  - 5 Warning rules
  - 8+ Info rules
- ✅ **Health Score System** - 0-100 quality metric
- ✅ **Auto-Fix Features** - Automatic parameter naming
- ✅ **Multiple Report Styles** - Simple, Compact, Full
- ✅ **MCP + Claude Integration** - AI-powered analysis
  - GHX direct parsing (no export needed)
  - JSON format support (100% accuracy)
  - Version comparison tool
  - AI suggestions
- ✅ **Complete Documentation**
  - Installation guides
  - User guides (English + Korean)
  - Quick start guides
  - Best practices
  - Contributing guidelines

### Features

**Standalone Version:**
- Real-time document scanning
- Instant feedback while working
- Works completely offline
- No external dependencies
- 5-minute setup

**MCP Version:**
- 100% accurate file analysis
- Claude AI integration
- Smart improvement suggestions
- Version comparison
- Advanced insights

### Documentation
- 📖 README.md - Project overview
- 📖 INSTALLATION.md - Setup guide
- 📖 USER_GUIDE.md - Complete usage guide
- 📖 QUICKSTART.md - 5-minute start
- 📖 CHANGELOG.md - This file
- 📖 CONTRIBUTING.md - How to contribute
- 📖 Best practices guide
- 📖 Korean documentation included

### Known Issues
- Large files (1000+ components) may be slow
- Auto-fix only supports parameter naming currently
- Some lint rules under development

### Limitations
- Standalone version: Basic analysis only
- MCP version: Requires setup and internet
- Test coverage: In progress

### Next Steps
- 🔄 Collect user feedback
- 🐛 Bug fixes based on reports
- ✨ Feature improvements
- 📚 Documentation improvements
- 🧪 Add test coverage

---

## Future Releases

### [0.2.0-alpha] - Planned
- More auto-fix capabilities
- Performance optimizations
- Additional lint rules
- Better error handling
- User feedback integration

### [0.1.0-alpha] - 2025-10-08 - Alpha Release 🎉 - Planned
- Stable release
- Complete test coverage
- Full documentation
- Food4Rhino listing
- Community plugins

---

## Version History

### Alpha Phase (0.x.x-alpha)
- **0.1.0-alpha**: Initial public release
- Focus: Feedback collection, bug discovery
- Status: Testing

### Beta Phase (0.x.x-beta) - Future
- Feature complete
- Focus: Stability, performance
- Status: Planned

### Stable Release (1.x.x) - Future
- Production ready
- Complete documentation
- Full support
- Status: Goal

---

## Release Types

- **Alpha**: Early testing, incomplete features, feedback collection
- **Beta**: Feature complete, stability testing
- **RC**: Release candidate, final testing
- **Stable**: Production ready

---

## How to Report Issues

Found a bug or have a suggestion?

1. 🐛 **Bug Report**: [Create an issue](https://github.com/dongwoosuk/grasshopper-quality-analyzer/issues)
2. 💡 **Feature Request**: [Start a discussion](https://github.com/dongwoosuk/grasshopper-quality-analyzer/discussions)
3. 📧 **Email**: dongwoosuk0219@gmail.com

---

## Tags

- `Added`: New features
- `Changed`: Changes in existing functionality
- `Deprecated`: Soon-to-be removed features
- `Removed`: Removed features
- `Fixed`: Bug fixes
- `Security`: Security fixes

---

**Thank you for testing the alpha version!** 🙏

Your feedback helps make this tool better for everyone.

---

Last Updated: 2025-11-02
Current Version: 0.3.0-alpha
Status: Alpha Testing


