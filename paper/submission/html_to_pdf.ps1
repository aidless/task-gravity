<#
.SYNOPSIS
  Render the Task Gravity HTML paper to PDF using Microsoft Edge headless.

.DESCRIPTION
  No LaTeX, no wkhtmltopdf, no Chromium download required.
  Uses the Microsoft Edge browser that ships with Windows 10/11.

.EXAMPLE
    .\paper\submission\html_to_pdf.ps1

  Output:
    paper\position\paper.pdf
#>

[CmdletBinding()]
param(
    [string]$HtmlPath = (Join-Path (Split-Path $PSScriptRoot -Parent) "position\paper.html"),
    [string]$PdfPath  = (Join-Path (Split-Path $PSScriptRoot -Parent) "position\paper.pdf")
)

$ErrorActionPreference = "Stop"

# locate Edge
$EdgePaths = @(
    "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "$env:LOCALAPPDATA\Microsoft\Edge\Application\msedge.exe"
)
$Edge = $null
foreach ($p in $EdgePaths) {
    if (Test-Path $p) { $Edge = $p; break }
}
if (-not $Edge) {
    Write-Host "Microsoft Edge not found. Tried:" -ForegroundColor Red
    $EdgePaths | ForEach-Object { Write-Host "  $_" }
    exit 1
}
Write-Host "Using Edge: $Edge"

# resolve absolute paths
$HtmlAbs = (Resolve-Path $HtmlPath).Path
$PdfAbs  = (Resolve-Path (Split-Path $PdfPath -Parent)).Path + "\" + (Split-Path $PdfPath -Leaf)

Write-Host "HTML: $HtmlAbs"
Write-Host "PDF:  $PdfAbs"

# invoke headless print
$args = @(
    "--headless",
    "--disable-gpu",
    "--no-sandbox",
    "--print-to-pdf=`"$PdfAbs`"",
    "--print-to-pdf-no-header",
    "`"file:///$($HtmlAbs -replace '\\','/')`""
)
Write-Host "Command: $Edge $($args -join ' ')" -ForegroundColor DarkGray

$proc = Start-Process -FilePath $Edge -ArgumentList $args -PassThru -Wait -NoNewWindow
if ($proc.ExitCode -ne 0) {
    Write-Host "Edge exited with code $($proc.ExitCode)" -ForegroundColor Red
    exit 2
}

if (Test-Path $PdfAbs) {
    $size = (Get-Item $PdfAbs).Length
    Write-Host "OK: $PdfAbs ($([math]::Round($size/1KB)) KB)" -ForegroundColor Green
} else {
    Write-Host "PDF not produced." -ForegroundColor Red
    exit 3
}