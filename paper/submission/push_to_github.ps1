<#
.SYNOPSIS
  One-shot helper to push the Task Gravity repo to GitHub.

.DESCRIPTION
  Run this from the project root:

    cd "C:\Users\Administrator\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a5f59719ea42441f41e2578"
    .\paper\submission\push_to_github.ps1

  The script will:
    1. Check git is installed.
    2. Set your git user.name / user.email (you'll be prompted once).
    3. (Optional) Generate an SSH key pair if you don't have one.
    4. Initialize the repo if needed, add files, commit.
    5. Create main branch and push.

  After it runs once, just `git push` for future updates.

.NOTES
  Tested with PowerShell 5.1 on Windows 10/11.
  Requires git in PATH (https://git-scm.com/download/win).
#>

[CmdletBinding()]
param(
    [string]$RepoUrl = "",
    [string]$GitUserName = "",
    [string]$GitUserEmail = "",
    [switch]$GenerateSshKey,
    [switch]$SkipPush
)

$ErrorActionPreference = "Stop"

# ---------- helpers ----------
function Write-Step($msg) { Write-Host "`n===> $msg" -ForegroundColor Cyan }
function Write-Ok   ($msg) { Write-Host "     $msg" -ForegroundColor Green }
function Write-Warn ($msg) { Write-Host "     $msg" -ForegroundColor Yellow }
function Write-Err  ($msg) { Write-Host "     $msg" -ForegroundColor Red }

# ---------- 0. locate project root ----------
$ProjectRoot = (Get-Item $PSScriptRoot).Parent.Parent.FullName
Write-Step "Project root: $ProjectRoot"
Set-Location $ProjectRoot

# ---------- 1. check git ----------
Write-Step "Checking git installation"
$git = Get-Command git -ErrorAction SilentlyContinue
if (-not $git) {
    Write-Err "git not found in PATH."
    Write-Warn "Install from https://git-scm.com/download/win and re-run."
    exit 1
}
$gitVersion = (& git --version).Trim()
Write-Ok "$gitVersion"

# ---------- 2. git identity ----------
Write-Step "Configuring git identity (one-time)"
if (-not $GitUserName) {
    $GitUserName = (& git config --global user.name) 2>$null
}
if (-not $GitUserName) {
    $GitUserName = Read-Host "Enter your full name (will appear in commits)"
    if (-not $GitUserName) { Write-Err "name cannot be empty"; exit 1 }
    & git config --global user.name "$GitUserName"
}
if (-not $GitUserEmail) {
    $GitUserEmail = (& git config --global user.email) 2>$null
}
if (-not $GitUserEmail) {
    $GitUserEmail = Read-Host "Enter your email (use a real one for DOI)"
    if (-not $GitUserEmail) { Write-Err "email cannot be empty"; exit 1 }
    & git config --global user.email "$GitUserEmail"
}
Write-Ok "user.name  = $GitUserName"
Write-Ok "user.email = $GitUserEmail"

# ---------- 3. SSH key (optional) ----------
if ($GenerateSshKey) {
    Write-Step "Generating SSH key pair"
    $sshDir = Join-Path $env:USERPROFILE ".ssh"
    if (-not (Test-Path $sshDir)) {
        New-Item -ItemType Directory -Path $sshDir | Out-Null
    }
    $keyPath = Join-Path $sshDir "id_ed25519"
    if (-not (Test-Path $keyPath)) {
        & ssh-keygen -t ed25519 -C $GitUserEmail -f $keyPath
        Write-Ok "key generated at $keyPath"
        Write-Warn "Now add this public key to GitHub:"
        Write-Warn "  1. open https://github.com/settings/keys"
        Write-Warn "  2. New SSH key"
        Write-Warn "  3. paste the contents of: $keyPath.pub"
        Read-Host "Press Enter after adding the key to GitHub"
    } else {
        Write-Ok "existing key at $keyPath"
    }
    Write-Warn "Test connection: ssh -T git@github.com"
}

# ---------- 4. repo URL ----------
Write-Step "GitHub repository URL"
if (-not $RepoUrl) {
    $default = "https://github.com/$($GitUserEmail -replace '@.*$','')/task-gravity.git"
    $RepoUrl = Read-Host "Paste the repo URL (Enter for default: $default)"
    if (-not $RepoUrl) { $RepoUrl = $default }
}
Write-Ok "Target: $RepoUrl"

# ---------- 5. init / commit ----------
Write-Step "Initializing local repo"
if (-not (Test-Path ".git")) {
    & git init
    & git branch -M main
    Write-Ok "git initialized"
} else {
    Write-Ok ".git already exists"
}

Write-Step "Adding and committing files"
& git add .
$status = (& git status --porcelain | Measure-Object).Count
if ($status -gt 0) {
    & git commit -m "Task Gravity: initial submission package (v1.0)

Includes:
- Position paper (Markdown + HTML)
- LaTeX theory supplement
- Reference implementation (NumPy tabular baseline + SB3 PPO)
- Submission materials (cover letters, open problems, venues)
- DOI minting guide (Zenodo + ChinaXiv)
- CITATION.cff + .zenodo.json for automatic DOI generation
"
    Write-Ok "committed"
} else {
    Write-Ok "no changes to commit"
}

# ---------- 6. push ----------
if ($SkipPush) {
    Write-Warn "SkipPush specified; not pushing."
} else {
    Write-Step "Pushing to $RepoUrl"
    try {
        & git remote add origin $RepoUrl 2>$null
        & git push -u origin main
        Write-Ok "pushed to main"
    } catch {
        Write-Warn "Push failed. Common fixes:"
        Write-Warn "  - Auth: use a Personal Access Token (Settings > Developer settings)"
        Write-Warn "  - URL: ensure the repo exists on GitHub (create it first, empty)"
        Write-Warn "  - Try again: git push -u origin main"
        exit 2
    }
}

# ---------- 7. tag v1.0 ----------
Write-Step "Tagging v1.0 (triggers Zenodo DOI)"
try {
    & git tag -a v1.0 -m "Task Gravity v1.0 - initial submission"
    & git push origin v1.0
    Write-Ok "tag v1.0 pushed"
} catch {
    Write-Warn "Tag failed (might already exist): $_"
}

# ---------- 8. next steps ----------
Write-Step "Next steps"
Write-Host @"

  GitHub side:
    1. Open https://github.com/settings/keys (SSH)
       OR https://github.com/settings/tokens (HTTPS, classic PAT)

  Zenodo side (instant international DOI):
    1. https://zenodo.org  ->  Log in with GitHub
    2. GitHub menu -> Enable on your task-gravity repo
    3. Upload -> GitHub -> select task-gravity, tag v1.0
    4. Click Publish -> DOI is generated immediately
       Format: 10.5281/zenodo.NNNNNNN

  ChinaXiv side (Chinese DOI, ~3 days):
    1. http://www.chinaxiv.org -> register (real name + ID)
    2. Submit PDF + Chinese abstract (see ZH_ABSTRACT.md)
    3. Wait 1-3 days for review

"@ -ForegroundColor Yellow

Write-Ok "Done."