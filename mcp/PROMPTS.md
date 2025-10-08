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
