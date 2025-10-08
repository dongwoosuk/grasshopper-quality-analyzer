"""
Grasshopper Linting Rules
Defines quality checks and best practices for GH definitions
"""

LINT_RULES = {
    "dangling_inputs": {
        "id": "GH001",
        "severity": "error",
        "title": "Dangling Inputs",
        "description": "Component inputs that are not connected to any source",
        "why_it_matters": "Unconnected inputs may use default values unexpectedly, leading to incorrect results",
        "how_to_fix": "Connect all required inputs or remove unused components"
    },
    
    "dangling_outputs": {
        "id": "GH002", 
        "severity": "warning",
        "title": "Dangling Outputs",
        "description": "Component outputs that are not connected to anything",
        "why_it_matters": "Unused outputs indicate dead code or incomplete logic flow",
        "how_to_fix": "Either use the output or consider removing the component"
    },
    
    "unnamed_params": {
        "id": "GH003",
        "severity": "warning",
        "title": "Unnamed Parameters",
        "description": "Sliders, panels, or value lists without descriptive names",
        "why_it_matters": "Makes the definition hard to understand and maintain",
        "how_to_fix": "Right-click parameters and set meaningful names"
    },
    
    "missing_groups": {
        "id": "GH004",
        "severity": "info",
        "title": "Missing Groups",
        "description": "Definition lacks organizational groups",
        "why_it_matters": "Groups help organize complex definitions into logical sections",
        "how_to_fix": "Select related components and use Ctrl+G to create groups with descriptive names"
    },
    
    "tree_access_mixing": {
        "id": "GH005",
        "severity": "warning",
        "title": "Mixed Tree Access",
        "description": "Inconsistent data tree access patterns (item/list/tree)",
        "why_it_matters": "Can lead to unexpected data structure issues and hard-to-debug errors",
        "how_to_fix": "Standardize tree access patterns throughout the definition"
    },
    
    "excessive_expressions": {
        "id": "GH006",
        "severity": "info",
        "title": "Excessive Expression Components",
        "description": "Too many expression components where native components would work",
        "why_it_matters": "Native components are faster, more maintainable, and less error-prone",
        "how_to_fix": "Replace expression components with native math/logic components"
    },
    
    "duplicate_chains": {
        "id": "GH007",
        "severity": "warning",
        "title": "Duplicate Component Chains",
        "description": "Repeated sequences of components that could be clustered",
        "why_it_matters": "Reduces maintainability and increases file size",
        "how_to_fix": "Create a cluster for the repeated logic and reuse it"
    },
    
    "excessive_flatten_graft": {
        "id": "GH008",
        "severity": "warning",
        "title": "Excessive Flatten/Graft",
        "description": "Overuse of flatten and graft operations",
        "why_it_matters": "Often indicates unclear data tree structure, impacts performance",
        "how_to_fix": "Restructure data flow to minimize tree manipulation"
    },
    
    "long_wire_crossings": {
        "id": "GH009",
        "severity": "info",
        "title": "Long Wire Crossings",
        "description": "Wires that cross long distances or intersect many times",
        "why_it_matters": "Makes the canvas hard to read and navigate",
        "how_to_fix": "Use relay components or reorganize layout for cleaner flow"
    },
    
    "large_panel_inputs": {
        "id": "GH010",
        "severity": "info",
        "title": "Large Text Panel Inputs",
        "description": "Panels with large amounts of text used as data input",
        "why_it_matters": "Better to use file references or structured data sources",
        "how_to_fix": "Move data to external files or use Read File components"
    },
    
    "plugin_dependencies": {
        "id": "GH011",
        "severity": "info",
        "title": "Plugin Dependencies",
        "description": "Lists all non-core plugins used in the definition",
        "why_it_matters": "Important for sharing and collaboration",
        "how_to_fix": "Document required plugins or consider core alternatives"
    },
    
    "no_preview": {
        "id": "GH012",
        "severity": "info",
        "title": "Components with Preview Off",
        "description": "Components with preview disabled",
        "why_it_matters": "May hide important visual feedback during development",
        "how_to_fix": "Review and enable preview where needed for debugging"
    },
    
    "data_dam_overuse": {
        "id": "GH013",
        "severity": "warning",
        "title": "Excessive Data Dam Usage",
        "description": "Too many data dams may indicate performance issues",
        "why_it_matters": "Data dams are often used to mask performance problems",
        "how_to_fix": "Optimize expensive operations instead of using data dams"
    },
    
    "deep_nesting": {
        "id": "GH014",
        "severity": "warning",
        "title": "Deep Component Nesting",
        "description": "Very long chains of components (10+ deep)",
        "why_it_matters": "Hard to debug and understand the logic flow",
        "how_to_fix": "Break into smaller, clustered sections with clear purposes"
    },
    
    "missing_comments": {
        "id": "GH015",
        "severity": "info",
        "title": "Missing Scribbles/Comments",
        "description": "Complex sections without explanatory notes",
        "why_it_matters": "Documentation helps future you and collaborators",
        "how_to_fix": "Add scribbles to explain complex logic or data flows"
    }
}


SEVERITY_LEVELS = {
    "error": 3,
    "warning": 2,
    "info": 1
}


def get_rule(rule_id: str):
    """Get a specific lint rule by ID"""
    for rule_key, rule in LINT_RULES.items():
        if rule['id'] == rule_id:
            return rule
    return None


def get_rules_by_severity(severity: str):
    """Get all rules of a specific severity"""
    return {k: v for k, v in LINT_RULES.items() if v['severity'] == severity}


def format_rule_description(rule: dict) -> str:
    """Format a rule as readable text"""
    return f"""
{rule['id']}: {rule['title']} [{rule['severity'].upper()}]
{rule['description']}

Why it matters: {rule['why_it_matters']}
How to fix: {rule['how_to_fix']}
"""
