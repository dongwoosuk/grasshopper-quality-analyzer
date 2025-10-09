# Fix examples README emoji

$base = "C:\Users\Soku\OneDrive - Steinberg Hart\Desktop\Source\RhinoScripts\src\gh\gh_analyzer_release"

Write-Host "Fixing examples/README.md emojis..." -ForegroundColor Yellow

$content = @"
# 📁 Examples

Example files and test scripts for Grasshopper Quality Analyzer.

## 📂 Structure

- **test_connection.py** - Test analyzer installation
- **test_force_reload.py** - Force reload analyzer module

## 🚀 Usage

See individual example files for detailed usage instructions.

For complete documentation, visit:
- [Getting Started](../docs/getting-started.md)
- [User Guide](../docs/user-guide.md)

"@

# Write with UTF-8 no BOM
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText("$base\examples\README.md", $content, $utf8NoBom)

Write-Host "✓ Fixed! Emojis should display correctly now." -ForegroundColor Green
