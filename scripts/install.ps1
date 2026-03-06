# FreeLauncher Installation Script (Windows)
# This script downloads and installs FreeLauncher with minimal user interaction

param(
    [string]$InstallPath = "$env:ProgramFiles\FreeLauncher",
    [string]$Version = "latest",
    [switch]$CreateDesktopShortcut = $true
)

# Colors for output
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Error { Write-Host $args -ForegroundColor Red }
function Write-Info { Write-Host $args -ForegroundColor Cyan }

# Check if running as administrator
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Error "❌ Este script debe ejecutarse como administrador"
    Write-Info "Por favor, ejecuta PowerShell como administrador y vuelve a intentar"
    exit 1
}

Write-Info "🎮 FreeLauncher - Instalador"
Write-Info "============================`n"

# Check Python installation
Write-Info "1️⃣  Verificando Python..."
$python = Get-Command python.exe -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Error "❌ Python no está instalado o no está en PATH"
    Write-Info "Descárgalo desde: https://www.python.org/downloads/"
    Write-Info "Asegúrate de marcar 'Add Python to PATH' durante la instalación"
    exit 1
}

$pythonVersion = & python --version 2>&1
Write-Success "✅ $pythonVersion encontrado"

# Check Java installation
Write-Info "`n2️⃣  Verificando Java..."
$java = Get-Command java.exe -ErrorAction SilentlyContinue
if (-not $java) {
    Write-Error "⚠️  Java no está instalado. Minecraft lo necesita."
    Write-Info "Descárgalo desde: https://www.oracle.com/java/technologies/downloads/"
    Write-Info "❓ ¿Continuar de todas formas? (S/n)"
    $response = Read-Host
    if ($response -ne "S" -and $response -ne "s") {
        exit 1
    }
} else {
    $javaVersion = & java -version 2>&1
    Write-Success "✅ Java encontrado"
}

# Create installation directory
Write-Info "`n3️⃣  Creando directorio de instalación..."
if (-not (Test-Path $InstallPath)) {
    New-Item -ItemType Directory -Force -Path $InstallPath | Out-Null
    Write-Success "✅ Directorio creado: $InstallPath"
} else {
    Write-Info "ℹ️  Directorio ya existe: $InstallPath"
}

# Download release from GitHub
Write-Info "`n4️⃣  Descargando FreeLauncher..."

if ($Version -eq "latest") {
    $apiUrl = "https://api.github.com/repos/marquistallman/OpenLauncherProyect/releases/latest"
} else {
    $apiUrl = "https://api.github.com/repos/marquistallman/OpenLauncherProyect/releases/tags/$Version"
}

try {
    $release = Invoke-RestMethod -Uri $apiUrl -Headers @{"Accept"="application/vnd.github.v3+json"}
    $downloadUrl = $release.assets[0].browser_download_url
    
    if (-not $downloadUrl) {
        Write-Error "❌ No se encontró release disponible"
        exit 1
    }
    
    $zipPath = Join-Path $InstallPath "freelauncher.zip"
    Write-Info "Descargando: $($release.tag_name)"
    
    Invoke-WebRequest -Uri $downloadUrl -OutFile $zipPath
    Write-Success "✅ Descarga completada"
    
    # Extract zip
    Write-Info "`n5️⃣  Extrayendo archivos..."
    Expand-Archive -Path $zipPath -DestinationPath $InstallPath -Force
    Remove-Item $zipPath
    Write-Success "✅ Archivos extraídos"
    
} catch {
    Write-Error "❌ Error durante la descarga: $_"
    exit 1
}

# Install Python dependencies
Write-Info "`n6️⃣  Instalando dependencias de Python..."
$reqFile = Join-Path $InstallPath "requirements.txt"
if (Test-Path $reqFile) {
    & python -m pip install -r $reqFile --quiet
    Write-Success "✅ Dependencias instaladas"
} else {
    Write-Error "❌ No se encontró requirements.txt"
}

# Create launcher script
Write-Info "`n7️⃣  Creando script de lanzamiento..."
$launcherScript = @"
@echo off
cd "$InstallPath"
python main.py %*
"@

$batFile = Join-Path $InstallPath "launchar.bat"
$launcherScript | Out-File -FilePath $batFile -Encoding ASCII
Write-Success "✅ Script de lanzamiento creado"

# Add to PATH
Write-Info "`n8️⃣  Agregando FreeLauncher a PATH..."
$currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
if ($currentPath -notlike "*$InstallPath*") {
    [Environment]::SetEnvironmentVariable(
        "Path",
        "$currentPath;$InstallPath",
        "Machine"
    )
    Write-Success "✅ Agregado a PATH"
} else {
    Write-Info "ℹ️  Ya está en PATH"
}

# Create desktop shortcut
if ($CreateDesktopShortcut) {
    Write-Info "`n9️⃣  Creando atajo en Escritorio..."
    
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $shortcutPath = Join-Path $desktopPath "FreeLauncher.lnk"
    
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $batFile
    $shortcut.WorkingDirectory = $InstallPath
    $shortcut.IconLocation = (Join-Path $InstallPath "icon.ico"), 0
    $shortcut.Description = "Modern Minecraft Launcher"
    $shortcut.Save()
    
    Write-Success "✅ Atajo creado en: $shortcutPath"
}

# Final message
Write-Success "`n✨ ¡Instalación completada!`n"
Write-Info "Para iniciar FreeLauncher:"
Write-Info "  • Haz doble clic en el atajo del Escritorio"
Write-Info "  • O ejecuta: freelauncher"
Write-Info "  • O abre: $InstallPath\main.py`n"

Write-Success "¡Diviértete lanzando Minecraft!"

# Keep window open
Write-Info "Presiona cualquier tecla para cerrar..."
Read-Host
