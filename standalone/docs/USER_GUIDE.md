# 🎯 Grasshopper Quality Analyzer - User Guide

**Version: 0.3.0-alpha** | **Last Updated: 2025-11-15**

A complete quality analysis toolkit for Grasshopper definitions with 9 specialized components.

---

## 🚀 Quick Start

### Installation
1. Add a Python component to your Grasshopper canvas
2. Open the desired `.py` file from the `standalone` folder
3. Copy the entire script into the Python component
4. Configure inputs and connect outputs
5. Done! 🎉

### Component Selection Guide

| Component | Category | Purpose | Difficulty |
|-----------|----------|---------|------------|
| **Health Check** | Analysis | Overall quality score | ⭐ Easy |
| **Issue Finder** | Analysis | Detailed problem detection | ⭐⭐ Medium |
| **Statistics** | Analysis | Component breakdown | ⭐ Easy |
| **Performance Profiler** ⚡ | Analysis | Bottleneck detection | ⭐⭐ Medium |
| **Parameter Namer** | Automation | Batch rename by type | ⭐⭐ Medium |
| **Auto Alignment** | Automation | Component layout | ⭐⭐⭐ Advanced |
| **Preview Control** | Automation | Enable/disable previews | ⭐ Easy |
| **Display Mode** | Automation | Icon/Name/Both | ⭐ Easy |
| **Python I/O Manager** | Automation | Auto input/output setup | ⭐⭐ Medium |

---

## 📊 Analysis Components (4)

### 1. Health Check

**Quick quality assessment with actionable feedback**

#### Inputs:
- `run` (Button): Execute analysis
- `style` (Text): Report style
  - `'simple'` - Score + summary (default)
  - `'compact'` - + Issue counts
  - `'full'` - + All issue details

#### Outputs:
- `report` (Panel): Formatted health report
- `score` (Number): Health score (0-100)
- `issue_count` (Number): Total issues found

#### Health Score System:
- **90-100**: ✅ Excellent - Production ready
- **70-89**: 👍 Good - Minor improvements needed
- **50-69**: ⚠️ Needs Attention - Significant issues
- **0-49**: ❌ Critical - Major problems

#### When to use:
- Quick check during work
- Before saving/sharing files
- Regular quality verification
- Team code reviews

---

### 2. Issue Finder

**Detailed issue detection with filtering**

#### Inputs:
- `run` (Button): Execute search
- `find_errors` (Boolean): Include errors (default: True)
- `find_warnings` (Boolean): Include warnings (default: True)
- `find_info` (Boolean): Include info (default: False)
- `highlight` (Boolean): Select issues on canvas (default: False)

#### Outputs:
- `errors` (List): Error-level issues (GH001, GHRT1)
- `warnings` (List): Warning-level issues (GH002, GH003, GH016, etc.)
- `info` (List): Info-level issues (GH004, GH012, GH017, GH018, etc.)
- `summary` (Text): Issue breakdown by type

#### Issue Severity Levels:
- **❌ Errors (2)**: Critical problems affecting functionality
  - GH001: Dangling Inputs
  - GHRT1: Runtime Errors
  
- **⚠️ Warnings (6)**: Problems requiring attention
  - GH002: Dangling Outputs
  - GH003: Unnamed Parameters
  - GH016: Slow Component Execution (>100ms) ⚡ NEW
  - GHRT2: Runtime Warnings
  - And more...
  
- **ℹ️ Info (10)**: Suggestions for improvement
  - GH004: Missing Groups
  - GH012: Preview Disabled
  - GH017: Computational Bottleneck (>20% total time) ⚡ NEW
  - GH018: Heavy Preview Geometry ⚡ NEW
  - And more...

#### When to use:
- Focus on specific issue types
- Pre-delivery quality checks
- Identifying technical debt
- Component debugging

---

### 3. Statistics

**Comprehensive document metrics**

#### Inputs:
- `run` (Button): Generate statistics

#### Outputs:
- `total_components` (Number): Component count
- `total_wires` (Number): Wire count
- `total_groups` (Number): Group count
- `by_category` (Text): Breakdown by category (Params, Math, Vector, etc.)
- `detailed_breakdown` (Text): Complete component analysis

#### Metrics Provided:
- Total component/wire/group counts
- Component distribution by category
- Most used component types
- File complexity indicators
- Documentation metadata

#### When to use:
- Understanding file complexity
- Analyzing component distribution
- Documentation and reporting
- Refactoring planning

---

### 4. Performance Profiler ⚡ NEW v0.3.0

**Identify performance bottlenecks and optimization opportunities**

#### Inputs:
- `run` (Button): Start profiling
- `mode` (Number 0-2): Profiling mode
  - `0` = Quick (1 pass) - Fast overview
  - `1` = Detailed (5 passes avg) - Accurate timing
  - `2` = Live - Continuous monitoring
- `threshold_ms` (Number): Slow component threshold in milliseconds (default: 100)
- `auto_select` (Boolean): Select slow components on canvas (default: False)
- `report_style` (Text): Report format
  - `'simple'` - Score + top bottlenecks
  - `'compact'` - + Performance breakdown
  - `'full'` - + All component timings

#### Outputs:
- `report` (Panel): Performance analysis report
- `performance_score` (Number): Performance score (0-100)
- `slow_components` (List): Components exceeding threshold
- `total_time_ms` (Number): Total execution time
- `bottlenecks` (Text): Top performance issues

#### Performance Score Calculation:
- **90-100**: ⚡ Excellent - Highly optimized
- **70-89**: 👍 Good - Acceptable performance
- **50-69**: ⚠️ Slow - Optimization recommended
- **0-49**: 🐌 Critical - Severe bottlenecks

#### Analysis Features:
- **Execution Time Tracking**: Per-component timing with <1ms overhead
- **Bottleneck Detection**: Identifies components using >20% total time
- **Plugin Analysis**: Performance breakdown by plugin/category
- **Pattern Recognition**: Heavy preview geometry, data tree operations, scripts
- **Smart Suggestions**: Context-aware optimization advice

#### Profiling Modes Explained:
- **Quick (0)**: Single execution pass
  - Use for: Large files (500+ components)
  - Accuracy: ±10-20ms variation
  - Speed: <1 second
  
- **Detailed (1)**: Average of 5 passes
  - Use for: Accurate bottleneck identification
  - Accuracy: ±2-5ms variation
  - Speed: 5-10 seconds
  
- **Live (2)**: Continuous monitoring
  - Use for: Real-time optimization work
  - Updates: After each solution
  - Speed: Minimal overhead

#### When to use:
- Definition running slowly
- Before scaling to larger datasets
- Optimization and refactoring
- Performance documentation
- Comparing algorithm alternatives

#### Optimization Suggestions:
The profiler provides context-aware recommendations:
- Flatten data trees before heavy operations
- Use simpler preview geometry
- Replace slow components with faster alternatives
- Batch operations instead of iteration
- Disable unnecessary previews
- Consider plugin-specific optimizations

---

## 🔧 Automation Components (5)

### 5. Parameter Namer

**Batch rename parameters by component type with prefix/suffix support**

#### Inputs:
- `run` (Button): Execute naming
- `component_type` (Text): Type to rename
  - `'Number Slider'` - Rename all number sliders
  - `'Panel'` - Rename all panels
  - `'Boolean Toggle'` - Rename all toggles
  - `'All'` - Rename all parameter components
- `name_prefix` (Text): Prefix for names (default: "Param")
- `name_suffix` (Text): Suffix for names (optional)
- `start_number` (Number): Starting index (default: 1)

#### Outputs:
- `report` (Text): Rename summary
- `renamed_count` (Number): Number of components renamed
- `component_list` (Text): List of renamed components

#### Naming Pattern:
- Format: `{prefix}_{type}_{number}{suffix}`
- Example: `Param_Slider_001`, `Input_Panel_01_Required`

#### When to use:
- Cleaning up unnamed parameters
- Standardizing parameter names
- Before sharing definitions
- Documentation preparation

---

### 6. Auto Alignment

**Smart component layout with wire-based flow analysis**

#### Inputs:
- `run` (Button): Execute alignment
- `vertical_spacing` (Number): Spacing between layers (default: 150)
- `horizontal_spacing` (Number): Spacing within layer (default: 100)
- `auto_apply` (Boolean): Apply immediately (default: False)
- `align_parameters` (Boolean): Include parameter components (default: True)

#### Outputs:
- `report` (Text): Alignment summary
- `total_moved` (Number): Components repositioned
- `layer_count` (Number): Number of logical layers

#### Algorithm Features:
- **Wire Flow Analysis**: Creates logical layers based on connections
- **Longest Path**: Accurate layer assignment for complex graphs
- **Anchor-Based Positioning**: Prevents component drift
- **Parameter Alignment**: Horizontally aligns parameter components with targets
- **Preview Mode**: Test before applying (auto_apply = False)

#### When to use:
- Organizing complex definitions
- After major refactoring
- Improving readability
- Before screenshots/documentation

#### Known Limitations:
- Parameter components with multiple targets may need manual adjustment
- Very complex cyclic dependencies may need manual intervention
- Undo with Ctrl+Z if result is unexpected

---

### 7. Preview Control ⚡ NEW v0.3.0

**Batch enable/disable component previews**

#### Inputs:
- `run` (Button): Execute control
- `enable_all` (Boolean): Enable all previews (True = enable, False = disable)

#### Outputs:
- `report` (Text): Summary of changes
- `modified_count` (Number): Components modified

#### When to use:
- Improving viewport performance
- Debugging specific components
- Large file optimization
- Presentation preparation

---

### 8. Display Mode Manager ⚡ NEW v0.3.0

**Control component display mode (Icon/Name/Both)**

#### Inputs:
- `run` (Button): Execute change
- `mode` (Number 0-2): Display mode
  - `0` = Icon only
  - `1` = Name only
  - `2` = Icon + Name (default)
- `apply_to_selection` (Boolean): Only affect selected components (default: False)

#### Outputs:
- `report` (Text): Change summary
- `modified_count` (Number): Components modified

#### When to use:
- Customizing canvas appearance
- Reducing visual clutter
- Improving readability
- Screenshot preparation

---

### 9. Python I/O Manager

**Automatically manage Python script component inputs and outputs**

#### Inputs:
- `run` (Button): Execute management
- `auto_detect` (Boolean): Auto-detect required I/O (default: True)
- `clean_unused` (Boolean): Remove unused I/O (default: False)

#### Outputs:
- `report` (Text): Management summary
- `inputs_added` (Number): Inputs added
- `outputs_added` (Number): Outputs added
- `removed_count` (Number): Unused I/O removed

#### Features:
- Scans Python code for variable usage
- Adds missing inputs/outputs automatically
- Optionally removes unused I/O
- Updates component immediately

#### When to use:
- After modifying Python scripts
- Cleaning up old code
- Syncing I/O with script changes
- Quick Python component setup

---

## 💡 Real-World Workflows

### Workflow 1: Daily Development
```
1. Work on definition normally
2. Run Health Check (simple mode) every 30min
3. Keep score above 80
4. Fix issues as they appear
5. Run Performance Profiler if slow
```

### Workflow 2: Pre-Delivery Quality Check
```
1. Run Health Check (full mode)
2. Target: 0 errors, minimize warnings
3. Run Issue Finder to see all problems
4. Fix errors first, then warnings
5. Run Parameter Namer for consistency
6. Run Auto Alignment for organization
7. Run Statistics for documentation
8. Final Health Check → aim for 90+
```

### Workflow 3: Performance Optimization
```
1. Run Performance Profiler (detailed mode)
2. Identify components >100ms
3. Check suggestions for each bottleneck
4. Apply optimizations:
   - Flatten data trees
   - Simplify geometry
   - Replace slow components
5. Re-run profiler to verify improvements
6. Repeat until score >80
```

### Workflow 4: Large File Cleanup
```
1. Run Statistics to understand complexity
2. Run Issue Finder (all types)
3. Use Parameter Namer on 'All' components
4. Disable unnecessary previews (Preview Control)
5. Run Auto Alignment for organization
6. Run Performance Profiler
7. Document findings with Health Check (full)
```

### Workflow 5: Team Collaboration Setup
```
1. Establish team standards:
   - Minimum health score: 80
   - No errors allowed
   - All parameters named
   - Performance score: >70
2. Run full check before commits
3. Use consistent naming conventions
4. Share performance profiling results
5. Document bottlenecks for review
```

---

## 🎯 Best Practices

### Quality Standards
- **Always maintain**: Health score >80
- **Zero tolerance**: Errors (GH001, GHRT1)
- **Minimize**: Warnings <5
- **Document**: Complex algorithms with groups

### Performance Standards
- **Target**: Performance score >70
- **Monitor**: Components >100ms execution time
- **Optimize**: Bottlenecks using >20% total time
- **Test**: Profile with realistic data sizes

### Organization Standards
- **Name all parameters**: Use Parameter Namer
- **Group components**: 10+ components = create group
- **Clean layout**: Use Auto Alignment regularly
- **Optimize previews**: Disable where not needed

### Collaboration Standards
- **Pre-commit check**: Run Health Check + Performance Profiler
- **Documentation**: Include Statistics in README
- **Naming convention**: Team-wide parameter naming scheme
- **Performance baseline**: Document initial performance scores

---

## 🔍 Lint Rules Reference

### ❌ Errors (2)
| Code | Name | Description | Fix |
|------|------|-------------|-----|
| GH001 | Dangling Inputs | Unconnected required inputs | Connect all inputs |
| GHRT1 | Runtime Errors | Component execution errors | Check error message |

### ⚠️ Warnings (6)
| Code | Name | Description | Fix |
|------|------|-------------|-----|
| GH002 | Dangling Outputs | Unused outputs | Use or remove |
| GH003 | Unnamed Parameters | Parameters without names | Use Parameter Namer |
| GH016 | Slow Component | Execution >100ms | Optimize or replace |
| GHRT2 | Runtime Warnings | Component warnings | Check warning |
| ... | And more | Various warnings | Context-specific |

### ℹ️ Info (10)
| Code | Name | Description | Suggestion |
|------|------|-------------|------------|
| GH004 | Missing Groups | Large file without organization | Create groups (Ctrl+G) |
| GH012 | Preview Disabled | Components with disabled preview | Enable where useful |
| GH017 | Performance Bottleneck | Component >20% total time | Critical optimization target |
| GH018 | Heavy Preview | Large preview geometry | Simplify or disable preview |
| ... | And more | Various suggestions | Context-specific |

---

## 🐛 Troubleshooting

### "No active Grasshopper document"
- **Cause**: Grasshopper not open or no file loaded
- **Fix**: Open Grasshopper and load a definition

### "Module not found" or "Import error"
- **Cause**: Script path incorrect or file moved
- **Fix**: Update path at top of script
```python
# Update this path to match your installation
sys.path.append(r"C:\...\RhinoScripts\src\gh\standalone")
```

### Performance Profiler returns 0ms for all
- **Cause**: Document hasn't been solved yet
- **Fix**: Force a solution (F5) before profiling

### Auto Alignment creates unexpected layout
- **Cause**: Complex cyclic dependencies or unusual connections
- **Fix**: 
  1. Undo (Ctrl+Z)
  2. Simplify connections
  3. Try again with different spacing values
  4. Use preview mode first (auto_apply = False)

### Component drift after repeated alignments
- **Issue**: This was fixed in v0.3.0-alpha with anchor-based positioning
- **Fix**: Update to latest version

### Python I/O Manager not detecting variables
- **Cause**: Non-standard variable naming or complex code
- **Fix**: Use clear variable names (x, y, a, b, etc.)

---

## 📈 Version History

### v0.3.0-alpha (Current)
- ⚡ Added Performance Profiler component
- 🎨 Split Display component into Preview Control + Display Mode
- 📊 Added 3 new lint rules (GH016-GH018)
- 🔧 Enhanced component organization
- 📝 Consistent naming convention

### v0.2.0-alpha
- Added Component Organizer
- Improved auto-alignment algorithm

### v0.1.0-alpha
- Initial public release
- 5 core components
- 15 lint rules

[📖 Full Changelog](../../CHANGELOG.md)

---

## 💬 Getting Help

### Documentation
- [Quick Start Guide](../QUICKSTART.md) - 5-minute setup
- [Installation Guide](INSTALLATION.md) - Detailed setup
- [Best Practices](../../docs/best-practices.md) - Quality standards
- [API Reference](../../docs/api-reference.md) - For developers

### Support Channels
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/dongwoosuk/grasshopper-quality-analyzer/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/dongwoosuk/grasshopper-quality-analyzer/discussions)
- 📧 **Email**: dongwoosuk0219@gmail.com

### Contributing
We welcome contributions! See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

---

## 🚀 What's Next?

### Planned Features
- [ ] More auto-fix capabilities (wire cleanup, group creation)
- [ ] Custom lint rule creation
- [ ] Performance history tracking
- [ ] Team standard templates
- [ ] Integration with version control
- [ ] Automated testing framework

### Stay Updated
- ⭐ Star the project on GitHub
- 👀 Watch for updates
- 📢 Join discussions
- 🤝 Contribute improvements

---

**Happy Grasshoppering! 🦗**

Built with ❤️ for the AEC community  
Improving computational design, one definition at a time.
