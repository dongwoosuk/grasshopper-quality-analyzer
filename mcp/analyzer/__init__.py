"""
Grasshopper Analyzer Package
Tools for analyzing and linting Grasshopper definitions
Supports both JSON (from export) and GHX (direct) formats
"""

from .gh_analyzer import GHAnalyzer, analyze_gh_json
from .gh_linter import GHLinter, lint_gh_json
from .ghx_parser import GHXParser, parse_ghx
from .lint_rules import LINT_RULES, get_rule, get_rules_by_severity

__version__ = "0.2.0"

__all__ = [
    'GHAnalyzer',
    'GHLinter',
    'GHXParser',
    'analyze_gh_json',
    'lint_gh_json',
    'parse_ghx',
    'LINT_RULES',
    'get_rule',
    'get_rules_by_severity'
]
