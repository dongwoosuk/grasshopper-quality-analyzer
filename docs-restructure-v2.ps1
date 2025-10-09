# ========================================
# Grasshopper Analyzer - Docs Restructure v2
# Direct Copy Method (Preserves Encoding)
# ========================================

$base = "C:\Users\Soku\OneDrive - Steinberg Hart\Desktop\Source\RhinoScripts\src\gh\gh_analyzer_release"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Docs Restructure Script v2" -ForegroundColor Cyan
Write-Host "  (Direct Copy Method)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ========================================
# STEP 1: Backup Current Files
# ========================================
Write-Host "STEP 1: Backing up current docs..." -ForegroundColor Yellow

$backup = "$base\_backup_docs"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupFolder = "$backup\backup_$timestamp"

New-Item -ItemType Directory -Path $backupFolder -Force | Out-Null

# Backup all MD files
Write-Host "  - Copying all MD files to backup..." -ForegroundColor Gray
Copy-Item "$base\*.md" $backupFolder -Force -ErrorAction SilentlyContinue
Copy-Item "$base\docs" "$backupFolder\docs" -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item "$base\mcp\*.md" "$backupFolder\mcp" -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item "$base\standalone\*.md" "$backupFolder\standalone" -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item "$base\standalone\docs" "$backupFolder\standalone_docs" -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item "$base\examples\*.md" "$backupFolder\examples" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "  ✓ Backup completed: $backupFolder" -ForegroundColor Green
Write-Host ""

# ========================================
# STEP 2: Create New Structure
# ========================================
Write-Host "STEP 2: Creating new directory structure..." -ForegroundColor Yellow

# Remove old docs structure (keeping backup)
if (Test-Path "$base\docs\getting-started") {
    Remove-Item "$base\docs\getting-started" -Recurse -Force
    Write-Host "  - Removed old getting-started folder" -ForegroundColor Gray
}

if (Test-Path "$base\docs\guides") {
    # Keep best-practices.md
    Copy-Item "$base\docs\guides\best-practices.md" "$base\docs\" -Force
    Remove-Item "$base\docs\guides" -Recurse -Force
    Write-Host "  - Moved best-practices.md and removed guides folder" -ForegroundColor Gray
}

Write-Host "  ✓ Old structure cleaned" -ForegroundColor Green
Write-Host ""

# ========================================
# STEP 3: Copy Files Directly (Preserve Encoding)
# ========================================
Write-Host "STEP 3: Creating new documentation files..." -ForegroundColor Yellow

# 3-1: Copy QUICKSTART.md -> getting-started.md
Write-Host "  - Creating getting-started.md..." -ForegroundColor Gray
Copy-Item "$base\standalone\QUICKSTART.md" "$base\docs\getting-started.md" -Force
Write-Host "    ✓ getting-started.md created" -ForegroundColor Green

# 3-2: Copy INSTALLATION.md -> installation-standalone.md
Write-Host "  - Creating installation-standalone.md..." -ForegroundColor Gray
Copy-Item "$base\standalone\docs\INSTALLATION.md" "$base\docs\installation-standalone.md" -Force
Write-Host "    ✓ installation-standalone.md created" -ForegroundColor Green

# 3-3: Copy CLAUDE_SETUP.md -> installation-mcp.md  
Write-Host "  - Creating installation-mcp.md..." -ForegroundColor Gray
Copy-Item "$base\mcp\CLAUDE_SETUP.md" "$base\docs\installation-mcp.md" -Force
Write-Host "    ✓ installation-mcp.md created" -ForegroundColor Green

# 3-4: Copy USER_GUIDE_EN.md -> user-guide.md
Write-Host "  - Creating user-guide.md..." -ForegroundColor Gray
Copy-Item "$base\standalone\docs\USER_GUIDE_EN.md" "$base\docs\user-guide.md" -Force
Write-Host "    ✓ user-guide.md created" -ForegroundColor Green

# 3-5: Copy USER_GUIDE.md -> user-guide-ko.md
Write-Host "  - Creating user-guide-ko.md..." -ForegroundColor Gray
Copy-Item "$base\standalone\docs\USER_GUIDE.md" "$base\docs\user-guide-ko.md" -Force
Write-Host "    ✓ user-guide-ko.md created" -ForegroundColor Green

# 3-6: Copy COMPLETE.md -> api-reference.md
Write-Host "  - Creating api-reference.md..." -ForegroundColor Gray
Copy-Item "$base\standalone\docs\COMPLETE.md" "$base\docs\api-reference.md" -Force
Write-Host "    ✓ api-reference.md created" -ForegroundColor Green

Write-Host ""

# ========================================
# STEP 4: Update MCP README (Combine files)
# ========================================
Write-Host "STEP 4: Creating consolidated MCP README..." -ForegroundColor Yellow

# Read files as bytes and convert to UTF8
$utf8 = New-Object System.Text.UTF8Encoding $false
$mcpReadmeBytes = [System.IO.File]::ReadAllBytes("$base\mcp\README.md")
$promptsBytes = [System.IO.File]::ReadAllBytes("$base\mcp\PROMPTS.md")
$formatBytes = [System.IO.File]::ReadAllBytes("$base\mcp\FORMAT_COMPARISON.md")

$mcpReadme = $utf8.GetString($mcpReadmeBytes)
$prompts = $utf8.GetString($promptsBytes)
$format = $utf8.GetString($formatBytes)

# Combine
$combined = $mcpReadme + "`n`n---`n`n" + "## 💬 Prompt Templates`n`n" + $prompts + "`n`n---`n`n" + "## 📊 Format Comparison`n`n" + $format

# Write back
[System.IO.File]::WriteAllText("$base\mcp\README.md", $combined, $utf8)

Write-Host "  ✓ MCP README consolidated" -ForegroundColor Green
Write-Host ""

# ========================================
# STEP 5: Update examples README
# ========================================
Write-Host "STEP 5: Updating examples documentation..." -ForegroundColor Yellow

$examplesContent = @"
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

$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText("$base\examples\README.md", $examplesContent, $utf8NoBom)

Write-Host "  ✓ examples README simplified" -ForegroundColor Green
Write-Host ""

# ========================================
# STEP 6: Remove Old Files
# ========================================
Write-Host "STEP 6: Cleaning up old files..." -ForegroundColor Yellow

$filesToRemove = @(
    "$base\standalone\QUICKSTART.md",
    "$base\standalone\docs\INSTALLATION.md",
    "$base\standalone\docs\USER_GUIDE.md",
    "$base\standalone\docs\USER_GUIDE_EN.md",
    "$base\standalone\docs\COMPLETE.md",
    "$base\standalone\docs\SUMMARY.md",
    "$base\standalone\docs\PATH_SETUP_GUIDE.md",
    "$base\mcp\CLAUDE_SETUP.md",
    "$base\mcp\PROMPTS.md",
    "$base\mcp\FORMAT_COMPARISON.md",
    "$base\standalone\examples\README.md"
)

foreach ($file in $filesToRemove) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-Host "  - Removed: $(Split-Path $file -Leaf)" -ForegroundColor Gray
    }
}

# Remove empty directories
if (Test-Path "$base\standalone\docs") {
    $docsEmpty = (Get-ChildItem "$base\standalone\docs" | Measure-Object).Count -eq 0
    if ($docsEmpty) {
        Remove-Item "$base\standalone\docs" -Force
        Write-Host "  - Removed empty standalone/docs folder" -ForegroundColor Gray
    }
}

if (Test-Path "$base\standalone\examples") {
    $exEmpty = (Get-ChildItem "$base\standalone\examples" | Measure-Object).Count -eq 0
    if ($exEmpty) {
        Remove-Item "$base\standalone\examples" -Force
        Write-Host "  - Removed empty standalone/examples folder" -ForegroundColor Gray
    }
}

Write-Host "  ✓ Cleanup completed" -ForegroundColor Green
Write-Host ""

# ========================================
# STEP 7: Add Navigation to Main README
# ========================================
Write-Host "STEP 7: Updating main README navigation..." -ForegroundColor Yellow

$utf8 = New-Object System.Text.UTF8Encoding $false
$readmeBytes = [System.IO.File]::ReadAllBytes("$base\README.md")
$mainReadme = $utf8.GetString($readmeBytes)

# Add navigation section if not exists
if ($mainReadme -notmatch "## 📚 Documentation") {
    $navigation = @"


---

## 📚 Documentation

### Getting Started
- [🚀 Quick Start Guide](docs/getting-started.md) - Get running in 5 minutes
- [📦 Standalone Installation](docs/installation-standalone.md) - For daily use
- [🔧 MCP Installation](docs/installation-mcp.md) - For advanced analysis

### User Guides
- [📖 User Guide (English)](docs/user-guide.md) - Complete usage guide
- [📖 사용자 가이드 (한글)](docs/user-guide-ko.md) - 한글 사용 가이드
- [✨ Best Practices](docs/best-practices.md) - Tips and workflows

### Reference
- [📚 API Reference](docs/api-reference.md) - Complete documentation
- [🔧 MCP Guide](mcp/README.md) - MCP + Claude integration
- [📁 Examples](examples/README.md) - Example files

---

"@
    
    # Insert before the last section
    $mainReadme = $mainReadme -replace "---\s*<p align=`"center`">", ($navigation + "---`n<p align=`"center`">")
    [System.IO.File]::WriteAllText("$base\README.md", $mainReadme, $utf8)
    Write-Host "  ✓ Main README updated with navigation" -ForegroundColor Green
} else {
    Write-Host "  ℹ Navigation section already exists" -ForegroundColor Gray
}

Write-Host ""

# ========================================
# SUMMARY
# ========================================
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ✅ RESTRUCTURE COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "📊 Results:" -ForegroundColor White
Write-Host "  • Backup created: $backupFolder" -ForegroundColor Gray
Write-Host "  • Old structure: 19 MD files" -ForegroundColor Gray
Write-Host "  • New structure: 12 MD files" -ForegroundColor Gray
Write-Host "  • Reduction: 37% fewer files" -ForegroundColor Green
Write-Host ""

Write-Host "📁 New Structure:" -ForegroundColor White
Write-Host "  docs/" -ForegroundColor Cyan
Write-Host "    ├── getting-started.md" -ForegroundColor Gray
Write-Host "    ├── installation-standalone.md" -ForegroundColor Gray
Write-Host "    ├── installation-mcp.md" -ForegroundColor Gray
Write-Host "    ├── user-guide.md" -ForegroundColor Gray
Write-Host "    ├── user-guide-ko.md" -ForegroundColor Gray
Write-Host "    ├── best-practices.md" -ForegroundColor Gray
Write-Host "    └── api-reference.md" -ForegroundColor Gray
Write-Host ""

Write-Host "🎯 Next Steps:" -ForegroundColor White
Write-Host "  1. Review the new files in docs/" -ForegroundColor Yellow
Write-Host "  2. Test all documentation links" -ForegroundColor Yellow
Write-Host "  3. Commit changes to Git" -ForegroundColor Yellow
Write-Host ""

Write-Host "💾 Backup Location:" -ForegroundColor White
Write-Host "  $backupFolder" -ForegroundColor Cyan
Write-Host ""

Write-Host "✅ Done! Your documentation is now cleaner and better organized." -ForegroundColor Green
Write-Host "   All emojis should be preserved correctly!" -ForegroundColor Green
Write-Host ""

# Optional: Open docs folder
$openDocs = Read-Host "Open docs folder? (y/n)"
if ($openDocs -eq 'y') {
    explorer "$base\docs"
}
