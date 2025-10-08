#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Grasshopper Analyzer MCP Server
Analyzes Grasshopper definitions (JSON and GHX formats)
Provides parsing, linting, suggestions, and diff tools
"""
import asyncio
import json
import sys
import os
from typing import Any, Sequence
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
except ImportError:
    print("Error: mcp package not installed. Install with: pip install mcp", file=sys.stderr)
    sys.exit(1)

# Import analyzer modules
try:
    from analyzer import GHAnalyzer, GHLinter, LINT_RULES
    from analyzer.ghx_parser import GHXParser
except ImportError as e:
    print(f"Error importing analyzer modules: {e}", file=sys.stderr)
    print("Make sure analyzer package is in PYTHONPATH", file=sys.stderr)
    sys.exit(1)


def detect_format(path: str) -> str:
    """Detect file format from extension"""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".json":
        return "json"
    elif ext in [".ghx", ".gh"]:
        return "ghx"
    return "json"


def load_analyzer(path: str, format_type: str = "auto"):
    """Load appropriate analyzer based on format"""
    if format_type == "auto":
        format_type = detect_format(path)
    
    if format_type == "ghx":
        parser = GHXParser(path)
        json_data = parser.to_json_format()
        analyzer = GHAnalyzer.__new__(GHAnalyzer)
        analyzer.data = json_data
        analyzer.components = json_data.get('components', [])
        analyzer.params = json_data.get('params', [])
        analyzer.wires = json_data.get('wires', [])
        analyzer.warnings = json_data.get('warnings', [])
        return analyzer
    else:
        return GHAnalyzer(path)


def load_linter(path: str, format_type: str = "auto"):
    """Load linter for the definition"""
    if format_type == "auto":
        format_type = detect_format(path)
    
    if format_type == "ghx":
        analyzer = load_analyzer(path, format_type)
        linter = GHLinter.__new__(GHLinter)
        linter.analyzer = analyzer
        linter.issues = []
        return linter
    else:
        return GHLinter(path)


def generate_suggestions(overview: dict, issues: list, goal: str) -> list:
    """Generate improvement suggestions based on goal"""
    suggestions = []
    goal_lower = goal.lower()
    
    if "performance" in goal_lower or "speed" in goal_lower or "optimize" in goal_lower:
        suggestions.append({
            "priority": "high",
            "category": "Performance",
            "title": "Optimize Expensive Operations",
            "description": "Look for data tree operations, flatten/graft, and complex geometry",
            "steps": [
                "Use Data Dam strategically before expensive operations",
                "Minimize tree manipulation (flatten/graft)",
                "Cache expensive geometry operations",
                "Consider using native components over expressions"
            ]
        })
    
    if "readable" in goal_lower or "maintain" in goal_lower or "clean" in goal_lower:
        suggestions.append({
            "priority": "high",
            "category": "Readability",
            "title": "Improve Documentation and Organization",
            "description": "Make the definition easier to understand and maintain",
            "steps": [
                "Add descriptive names to all parameters",
                "Create groups for logical sections",
                "Add scribbles to explain complex logic",
                "Use consistent naming conventions"
            ]
        })
    
    if "tree" in goal_lower or "data" in goal_lower:
        suggestions.append({
            "priority": "medium",
            "category": "Data Structure",
            "title": "Stabilize Data Tree Structure",
            "description": "Ensure consistent and predictable data flow",
            "steps": [
                "Standardize tree access patterns",
                "Minimize flatten/graft operations",
                "Use explicit tree path operations",
                "Document expected tree structures"
            ]
        })
    
    for issue in issues[:3]:
        rule = issue['rule']
        suggestions.append({
            "priority": "high" if rule['severity'] == 'error' else "medium",
            "category": "Fix Issues",
            "title": f"Fix: {rule['title']}",
            "description": rule['description'],
            "steps": [rule['how_to_fix']],
            "count": issue.get('count', 1)
        })
    
    return suggestions


def calculate_diff(analyzer_a, analyzer_b) -> dict:
    """Calculate differences between two definitions"""
    guids_a = set(c['guid'] for c in analyzer_a.components)
    guids_b = set(c['guid'] for c in analyzer_b.components)
    
    added = guids_b - guids_a
    removed = guids_a - guids_b
    common = guids_a & guids_b
    
    added_comps = [c for c in analyzer_b.components if c['guid'] in added]
    removed_comps = [c for c in analyzer_a.components if c['guid'] in removed]
    
    wires_a_set = set((w['from']['guid'], w['to']['guid']) for w in analyzer_a.wires)
    wires_b_set = set((w['from']['guid'], w['to']['guid']) for w in analyzer_b.wires)
    
    wires_added = len(wires_b_set - wires_a_set)
    wires_removed = len(wires_a_set - wires_b_set)
    
    return {
        "components": {
            "added": len(added),
            "removed": len(removed),
            "unchanged": len(common),
            "added_details": added_comps[:10],
            "removed_details": removed_comps[:10]
        },
        "wires": {
            "added": wires_added,
            "removed": wires_removed
        },
        "summary": f"{len(added)} components added, {len(removed)} removed, {wires_added} wires added, {wires_removed} wires removed"
    }


# Create MCP server instance
server = Server("gh-analyzer-server")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools"""
    return [
        Tool(
            name="gh_parse",
            description="Parse and analyze a Grasshopper definition file (JSON or GHX format). Returns overview, statistics, and metrics.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Full path to the GH definition file (.json, .ghx, or .gh)"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["auto", "json", "ghx"],
                        "default": "auto",
                        "description": "File format (auto-detected if not specified)"
                    }
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="gh_lint",
            description="Run lint checks on a Grasshopper definition. Returns list of issues with severity levels and fix suggestions.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Full path to the GH definition file"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["auto", "json", "ghx"],
                        "default": "auto"
                    },
                    "rules": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional: Specific rule IDs to check"
                    }
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="gh_suggest",
            description="Generate improvement suggestions for a GH definition based on a specific goal (performance, readability, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Full path to the GH definition file"
                    },
                    "goal": {
                        "type": "string",
                        "description": "Optimization goal (e.g., 'performance', 'readability', 'maintainability')"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["auto", "json", "ghx"],
                        "default": "auto"
                    }
                },
                "required": ["path", "goal"]
            }
        ),
        Tool(
            name="gh_diff",
            description="Compare two GH definitions and show what changed (added/removed/modified components and wires)",
            inputSchema={
                "type": "object",
                "properties": {
                    "path_a": {
                        "type": "string",
                        "description": "Path to first GH definition (baseline)"
                    },
                    "path_b": {
                        "type": "string",
                        "description": "Path to second GH definition (comparison)"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["auto", "json", "ghx"],
                        "default": "auto"
                    }
                },
                "required": ["path_a", "path_b"]
            }
        ),
        Tool(
            name="gh_list_rules",
            description="Get list of all available lint rules with descriptions",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls"""
    
    try:
        if name == "gh_list_rules":
            result = {
                "rules": LINT_RULES,
                "count": len(LINT_RULES)
            }
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "gh_parse":
            path = arguments.get("path")
            format_type = arguments.get("format", "auto")
            
            if not os.path.exists(path):
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": f"File not found: {path}"}, indent=2)
                )]
            
            format_used = format_type if format_type != "auto" else detect_format(path)
            analyzer = load_analyzer(path, format_type)
            overview = analyzer.get_overview()
            report = analyzer.generate_report()
            
            result = {
                "success": True,
                "path": path,
                "format": format_used,
                "overview": overview,
                "report": report
            }
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "gh_lint":
            path = arguments.get("path")
            format_type = arguments.get("format", "auto")
            rules = arguments.get("rules")
            
            if not os.path.exists(path):
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": f"File not found: {path}"}, indent=2)
                )]
            
            format_used = format_type if format_type != "auto" else detect_format(path)
            linter = load_linter(path, format_type)
            issues = linter.lint_all()
            
            if rules:
                issues = [i for i in issues if i['rule']['id'] in rules]
            
            result = {
                "success": True,
                "path": path,
                "format": format_used,
                "issues": issues,
                "summary": {
                    "total": len(issues),
                    "errors": sum(1 for i in issues if i['rule']['severity'] == 'error'),
                    "warnings": sum(1 for i in issues if i['rule']['severity'] == 'warning'),
                    "info": sum(1 for i in issues if i['rule']['severity'] == 'info')
                },
                "report": linter.generate_lint_report()
            }
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "gh_suggest":
            path = arguments.get("path")
            goal = arguments.get("goal")
            format_type = arguments.get("format", "auto")
            
            if not os.path.exists(path):
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": f"File not found: {path}"}, indent=2)
                )]
            
            format_used = format_type if format_type != "auto" else detect_format(path)
            analyzer = load_analyzer(path, format_type)
            linter = load_linter(path, format_type)
            
            overview = analyzer.get_overview()
            issues = linter.get_top_issues(10)
            suggestions = generate_suggestions(overview, issues, goal)
            
            result = {
                "success": True,
                "path": path,
                "format": format_used,
                "goal": goal,
                "suggestions": suggestions
            }
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "gh_diff":
            path_a = arguments.get("path_a")
            path_b = arguments.get("path_b")
            format_type = arguments.get("format", "auto")
            
            if not os.path.exists(path_a):
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": f"File not found: {path_a}"}, indent=2)
                )]
            
            if not os.path.exists(path_b):
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": f"File not found: {path_b}"}, indent=2)
                )]
            
            format_used = format_type if format_type != "auto" else detect_format(path_a)
            analyzer_a = load_analyzer(path_a, format_type)
            analyzer_b = load_analyzer(path_b, format_type)
            
            diff = calculate_diff(analyzer_a, analyzer_b)
            
            result = {
                "success": True,
                "path_a": path_a,
                "path_b": path_b,
                "format": format_used,
                "diff": diff
            }
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        else:
            return [TextContent(
                type="text",
                text=json.dumps({"error": f"Unknown tool: {name}"}, indent=2)
            )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e)}, indent=2)
        )]


async def main():
    """Main entry point - run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
