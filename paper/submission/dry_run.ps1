<#
.SYNOPSIS
  Dry-run the GitHub push for Task Gravity.
  Does NOT modify git state; just checks environment + file inventory.

.DESCRIPTION
  Run this BEFORE push_to_github.ps1 to make sure:
    * git is installed and on PATH
    * (optional) SSH key is set up
    * All files that will be pushed are accounted for
    * No accidentally huge files (checkpoints, etc.)
    * .gitignore covers everything it should

.EXAMPLE
    .\paper\submission\dry_run.ps1
#>

[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

function Write-Step($msg) { Write-Host "`n===> $msg" -ForegroundColor Cyan }
function Write-Ok   ($msg) { Write-Host "     [OK]   $msg" -ForegroundColor Green }
function Write-Warn ($msg) { Write-Host "     [WARN] $msg" -ForegroundColor Yellow }
function Write-Err  ($msg) { Write-Host "     [ERR]  $msg" -ForegroundColor Red }
function Format-Size($bytes) {
    if     ($bytes -ge 1GB) { return "{0:N2} GB" -f ($bytes/1GB) }
    elseif ($bytes -ge 1MB) { return "{0:N2} MB" -f ($bytes/1MB) }
    elseif ($bytes -ge 1KB) { return "{0:N2} KB" -f ($bytes/1KB) }
    else                    { return "$bytes B" }
}

$ProjectRoot = (Get-Item $PSScriptRoot).Parent.Parent.FullName
Set-Location $ProjectRoot
Write-Step "Project root: $ProjectRoot"

# ---------- 1. git ----------
Write-Step "1. Git environment"
$git = Get-Command git -ErrorAction SilentlyContinue
if (-not $git) {
    Write-Err "git NOT found in PATH"
    Write-Warn "Install from https://git-scm.com/download/win"
} else {
    $version = (& git --version).Trim()
    Write-Ok "$version"
}

if ($git) {
    $name  = (& git config --global user.name  2>$null)
    $email = (& git config --global user.email 2>$null)
    if ($name  -and $email) {
        Write-Ok "user.name  = $name"
        Write-Ok "user.email = $email"
    } else {
        Write-Warn "git identity not set yet. push_to_github.ps1 will set it."
    }
}

# ---------- 2. SSH ----------
Write-Step "2. SSH environment (optional)"
$ssh = Get-Command ssh -ErrorAction SilentlyContinue
if (-not $ssh) {
    Write-Warn "ssh not in PATH (will use HTTPS+Token instead)"
} else {
    try {
        $sshVer = ssh -V 2>&1 | Out-String
        $sshVer = $sshVer.Trim().Split([Environment]::NewLine)[0]
        Write-Ok "$sshVer"
    } catch {
        Write-Warn "ssh -V failed: $_"
    }
    $keyPath = Join-Path $env:USERPROFILE ".ssh\id_ed25519.pub"
    if (Test-Path $keyPath) {
        Write-Ok "SSH public key present: $keyPath"
        $pubKey = Get-Content $keyPath
        $fingerprint = (& ssh-keygen -lf $keyPath 2>$null).Trim()
        if ($fingerprint) { Write-Ok "Fingerprint: $fingerprint" }
    } else {
        Write-Warn "No SSH key at $keyPath. Run push_to_github.ps1 -GenerateSshKey"
    }

    # Test if known_hosts has github
    $knownHosts = Join-Path $env:USERPROFILE ".ssh\known_hosts"
    if (Test-Path $knownHosts) {
        $hasGithub = Select-String -Path $knownHosts -Pattern "github.com" -SimpleMatch -Quiet
        if ($hasGithub) {
            Write-Ok "github.com is in known_hosts"
        } else {
            Write-Warn "github.com NOT in known_hosts (first ssh will prompt)"
        }
    }
}

# ---------- 3. files ----------
Write-Step "3. File inventory (what would be pushed)"
$gitignore = Get-Content ".gitignore" -ErrorAction SilentlyContinue
if ($gitignore) {
    Write-Ok ".gitignore present ($(($gitignore | Measure-Object).Count) lines)"
} else {
    Write-Warn "No .gitignore at project root"
}

$bigFiles = @()
$totalSize = 0L
$fileCount = 0
$dirCount  = 0

Get-ChildItem -Recurse -File -Force | Where-Object {
    $_.FullName -notmatch '[\\/]\.git[\\/]'
} | ForEach-Object {
    $fileCount++
    $totalSize += $_.Length
    $relPath = $_.FullName.Substring($ProjectRoot.Length).TrimStart('\','/')
    # report large files
    if ($_.Length -gt 1MB) {
        $bigFiles += [pscustomobject]@{ Path = $relPath; Size = $_.Length }
    }
}

Write-Ok "Total files: $fileCount"
Write-Ok "Total size:  $(Format-Size $totalSize)"

if ($bigFiles.Count -gt 0) {
    Write-Warn "Files > 1 MB (consider .gitignore-ing these):"
    foreach ($f in $bigFiles | Sort-Object Size -Descending) {
        Write-Host "     $($f.Path)  --  $(Format-Size $f.Size)" -ForegroundColor Yellow
    }
} else {
    Write-Ok "No files > 1 MB"
}

# ---------- 4. .gitignore sanity ----------
Write-Step "4. .gitignore coverage check"
$expectedPatterns = @(
    @{Needle='__pycache__'; Desc='__pycache__/'},
    @{Needle='*.pyc';      Desc='*.pyc / *.py[cod]'},
    @{Needle='checkpoints'; Desc='checkpoints/'},
    @{Needle='.zip';       Desc='*.zip'}
)
foreach ($pat in $expectedPatterns) {
    $matched = $false
    if ($gitignore) {
        foreach ($line in $gitignore) {
            if ($line.Trim() -match [regex]::Escape($pat.Needle)) { $matched = $true; break }
        }
    }
    if ($matched) {
        Write-Ok ".gitignore covers: $($pat.Desc)"
    } else {
        Write-Warn ".gitignore MISSING: $($pat.Desc)"
    }
}

# ---------- 5. pycache spot check ----------
Write-Step "5. Will __pycache__/ be ignored?"
$pycFiles = Get-ChildItem -Recurse -Filter "__pycache__" -Directory -ErrorAction SilentlyContinue
if ($pycFiles.Count -eq 0) {
    Write-Ok "No __pycache__ directories present"
} else {
    Write-Warn "$($pycFiles.Count) __pycache__/ dirs present (should be ignored by .gitignore)"
    foreach ($d in $pycFiles | Select-Object -First 5) {
        Write-Host "     $($d.FullName.Substring($ProjectRoot.Length))" -ForegroundColor Yellow
    }
    if ($pycFiles.Count -gt 5) {
        Write-Host "     ... and $($pycFiles.Count - 5) more" -ForegroundColor Yellow
    }
}

# ---------- 6. critical files present? ----------
Write-Step "6. Critical files present?"
$critical = @(
    @{Path="README.md";                  Desc="Project root README"},
    @{Path="paper\position\paper.md";   Desc="Position paper (markdown)"},
    @{Path="paper\position\paper.html"; Desc="Position paper (HTML)"},
    @{Path="paper\theory\task_gravity_theory.tex"; Desc="LaTeX theory supplement"},
    @{Path="paper\submission\cover_letter.md"; Desc="English cover letter"},
    @{Path="paper\submission\cover_letter_zh.md"; Desc="Chinese cover letter"},
    @{Path="paper\submission\CITATION.cff"; Desc="GitHub citation metadata"},
    @{Path="paper\submission\.zenodo.json"; Desc="Zenodo metadata"},
    @{Path="paper\submission\DOI.md"; Desc="DOI minting guide"},
    @{Path="paper\submission\ZH_ABSTRACT.md"; Desc="ChinaXiv Chinese abstract"},
    @{Path="paper\submission\push_to_github.ps1"; Desc="Push script"},
    @{Path="experiment\requirements.txt"; Desc="Tabular deps"},
    @{Path="experiment\src\env.py"; Desc="Tabular env"},
    @{Path="experiment\results\trr_ctrr_table.csv"; Desc="Tabular results CSV"},
    @{Path="experiment\deep\requirements.txt"; Desc="Deep deps (in check: experiment\deep\)"},
    @{Path="experiment\deep\src\run.py"; Desc="Deep PPO runner"},
    @{Path="experiment\deep\results\deep_trr_ctrr_table.csv"; Desc="Deep results CSV"}
)
foreach ($c in $critical) {
    $full = Join-Path $ProjectRoot $c.Path
    if (Test-Path $full) {
        Write-Ok "$($c.Desc): $($c.Path)"
    } else {
        Write-Err "MISSING: $($c.Path)  ($($c.Desc))"
    }
}

# ---------- 7. summary ----------
Write-Step "7. Summary"
if ($git) {
    Write-Host "     Ready to push." -ForegroundColor Green
    Write-Host "     Run:  .\paper\submission\push_to_github.ps1" -ForegroundColor Cyan
} else {
    Write-Host "     Install git first, then re-run this dry-run." -ForegroundColor Red
}

Write-Host ""