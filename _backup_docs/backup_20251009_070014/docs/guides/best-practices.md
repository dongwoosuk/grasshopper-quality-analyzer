# Best Practices for Grasshopper Definitions

Learn how to create high-quality, maintainable Grasshopper definitions.

## Table of Contents

- [Naming Conventions](#naming-conventions)
- [Organization](#organization)
- [Data Flow](#data-flow)
- [Performance](#performance)
- [Documentation](#documentation)
- [Collaboration](#collaboration)

---

## Naming Conventions

### ✅ DO: Use Descriptive Names

**Good:**
```
✅ Wall Height
✅ Floor Count
✅ Grid Spacing X
✅ Facade Rotation Angle
```

**Bad:**
```
❌ Number Slider
❌ Panel
❌ h
❌ x1
```

### Parameter Naming Rules

1. **Be specific**: "Wall Height" not "Height"
2. **Include units**: "Spacing_mm" or "Angle_deg"
3. **Use conventions**: PascalCase or snake_case consistently
4. **Avoid abbreviations**: "Height" not "Ht"

### Component Naming

For components that need identification:
```
✅ Rotate_Facade
✅ Calculate_Floor_Area
✅ Generate_Grid
```

---

## Organization

### Use Groups

**When to group:**
- Related operations (5+ components)
- Logical sections (Input, Process, Output)
- Repeated patterns
- Complex subsystems

**Group naming:**
```
✅ INPUT - Parameters
✅ PROCESS - Geometry Generation
✅ OUTPUT - Bake & Display
✅ UTIL - Helper Functions
```

### Layout Guidelines

1. **Left to right flow**: Inputs → Process → Outputs
2. **Top to bottom**: Main flow on top, utilities below
3. **Align components**: Use grid (Alt + drag)
4. **Minimize wire crossings**: Use relay or reorganize

**Good Layout:**
```
[Input Params] → [Generate Grid] → [Create Geometry] → [Output]
       ↓
[Settings Group]
```

---

## Data Flow

### Tree Structure

**Keep it simple:**
```
✅ Consistent branching
✅ Clear path structure {0;0;0}
✅ Documented tree logic
✅ Minimal flatten/graft
```

**Avoid:**
```
❌ Excessive flatten
❌ Multiple graft/flatten chains
❌ Unclear branching
❌ Unintended tree mixing
```

### Wire Management

**Best practices:**
```
✅ Short wires when possible
✅ Use relay for long distances
✅ Avoid wire tangles
✅ Group crossing wires
```

### Component Connection

**Good patterns:**
```
Param → Component → Component → Output
    ↘ Helper Component ↗
```

**Bad patterns:**
```
Tangled mess of wires ❌
Back-and-forth connections ❌
Circular dependencies ❌
```

---

## Performance

### Optimization Strategies

#### 1. Use Data Dam Wisely
```
Expensive Operation → Data Dam → Next Operation
```

#### 2. Minimize Tree Operations
```
✅ One flatten at start
❌ Flatten → Process → Flatten → Process
```

#### 3. Native > Expression
```
✅ Use Addition component
❌ Use Expression "x + y"
```

#### 4. Bake vs Preview
```
✅ Disable preview when not needed
✅ Use selective bake
❌ Everything previewed always
```

### Performance Checklist

- [ ] Remove unused components
- [ ] Minimize tree manipulation
- [ ] Use native components
- [ ] Strategic Data Dam placement
- [ ] Disable unnecessary previews
- [ ] Simplify complex operations

---

## Documentation

### Self-Documenting Definitions

#### 1. Use Scribbles
```
Add text scribbles for:
- Section headers
- Complex logic explanation
- Important notes
- Version history
```

#### 2. Panel Documentation
```
Add panels with:
- Input parameter descriptions
- Expected value ranges
- Output descriptions
- Usage instructions
```

#### 3. Group Labels
```
Every group should have:
- Clear descriptive name
- Purpose or function
- Dependencies (if any)
```

### Documentation Template

```
=== DEFINITION INFO ===
Project: [Name]
Version: [v1.0]
Author: [Your Name]
Date: [YYYY-MM-DD]
Purpose: [What this does]

=== INPUTS ===
- Param1: Description (Range: 0-100)
- Param2: Description (Type: Number)

=== OUTPUTS ===
- Output1: Description
- Output2: Description

=== NOTES ===
- Important considerations
- Known limitations
- Dependencies
```

---

## Collaboration

### Team Standards

#### Version Control
```
File naming: ProjectName_vX.X_Date.gh
Example: Tower_Facade_v2.1_20250106.gh
```

#### Pre-Share Checklist
```
✅ Run analyzer (score > 80)
✅ Fix all errors
✅ Add documentation
✅ Name all parameters
✅ Organize into groups
✅ Test with sample inputs
✅ Remove dead code
```

#### Code Review
```
Before sharing:
1. Self-review
2. Run analyzer
3. Document changes
4. Test thoroughly

When receiving:
1. Open with analyzer
2. Review documentation
3. Check for issues
4. Test with own data
```

---

## Quality Targets

### Recommended Scores

**Production Files:**
```
Score: 90-100 ✅
Errors: 0
Warnings: < 5
Info: < 10
```

**Work in Progress:**
```
Score: 70-89 👍
Errors: 0
Warnings: < 10
Info: Any
```

**Minimum Acceptable:**
```
Score: 50+ ⚠️
Errors: 0
Warnings: < 20
```

---

## Common Patterns

### Pattern 1: Parametric Grid
```
Sliders (U, V, Spacing)
    ↓
Generate Grid Component
    ↓
Process Grid Points
    ↓
Create Geometry
```

### Pattern 2: Iteration
```
Input List → Repeat Component → Process Each → Collect Results
```

### Pattern 3: Conditional Logic
```
Test Condition → Stream Filter → True Path / False Path → Merge
```

---

## Anti-Patterns to Avoid

### ❌ Don't: Magic Numbers
```
❌ Hard-coded values: Multiply by 3.14159
✅ Use named parameters: Multiply by {Pi}
```

### ❌ Don't: Spaghetti Code
```
❌ Tangled wires everywhere
✅ Clear left-to-right flow
```

### ❌ Don't: Giant Single Definition
```
❌ 500 components in one file
✅ Break into clusters/modules
```

### ❌ Don't: Ignore Warnings
```
❌ "It works, warnings don't matter"
✅ Understand and fix warnings
```

---

## Quick Tips

### Daily Habits
```
✅ Name parameters as you create them
✅ Group components immediately
✅ Delete unused components promptly
✅ Run quick check before saving
```

### Before Sharing
```
✅ Full analysis
✅ Fix all errors
✅ Document purpose
✅ Test edge cases
```

### When Stuck
```
✅ Check analyzer suggestions
✅ Review data tree structure
✅ Simplify to debug
✅ Ask for code review
```

---

## Further Reading

- [Lint Rules Reference](../../mcp/FORMAT_COMPARISON.md)
- [User Guide](../../standalone/USER_GUIDE.md)
- [Team Workflow](./team-workflow.md)

---

## Remember

> "Good code is its own best documentation." - Steve McConnell

But in Grasshopper:
> "Good definitions document themselves through clear names, logical organization, and helpful annotations."

---

[← Back to Docs](../README.md) | [Next: Team Workflow →](./team-workflow.md)
