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

# Asegurar TLS 1.2 para descargas (GitHub requiere esto)
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# Check if running as administrator
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Info "Solicitando permisos de administrador..."
    $scriptUrl = "https://raw.githubusercontent.com/marquistallman/OpenLauncherProyect/main/scripts/install.ps1"
    try {
        Start-Process powershell.exe -Verb RunAs -ArgumentList "-NoProfile -ExecutionPolicy Bypass -Command `"[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; iex ((New-Object System.Net.WebClient).DownloadString('$scriptUrl'))`""
        exit
    } catch {
        Write-Error "No se pudo elevar permisos. Ejecuta PowerShell como Administrador manualmente."
        exit 1
    }
}

Write-Info "FreeLauncher - Instalador"
Write-Info "============================`n"

# Check Python installation
Write-Info "1. Verificando Python..."

# Detect a working Python, ignoring the Windows Store stub
$pythonCmd = $null
$pythonVersion = $null
foreach ($cmd in @("python", "python3", "py")) {
    $cmdPath = Get-Command $cmd -ErrorAction SilentlyContinue
    if ($cmdPath) {
        $result = & $cmd --version 2>&1
        if ($LASTEXITCODE -eq 0 -and "$result" -notmatch "was not found" -and "$result" -notmatch "Microsoft Store") {
            $pythonCmd = $cmd
            $pythonVersion = "$result"
            break
        }
    }
}

if (-not $pythonCmd) {
    Write-Info "Python no encontrado. Intentando instalar automáticamente..."

    $installed = $false

    # Attempt 1: winget
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if ($winget -and -not $installed) {
        Write-Info "Instalando Python con winget..."
        try {
            winget install --id Python.Python.3 --silent --accept-package-agreements --accept-source-agreements 2>&1 | Out-Null
            $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" +
                        [System.Environment]::GetEnvironmentVariable("Path","User")
            $result = & python --version 2>&1
            if ($LASTEXITCODE -eq 0 -and "$result" -notmatch "was not found" -and "$result" -notmatch "Microsoft Store") {
                $pythonCmd = "python"
                $pythonVersion = "$result"
                $installed = $true
                Write-Success "Python instalado correctamente via winget"
            }
        } catch { }
    }

    # Attempt 2: download installer from python.org
    if (-not $installed) {
        Write-Info "Descargando Python desde python.org..."
        $pythonInstallerUrl = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
        $pythonInstaller = "$env:TEMP\python_installer.exe"
        try {
            Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $pythonInstaller
            Write-Info "Instalando Python..."
            Start-Process $pythonInstaller -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
            Remove-Item $pythonInstaller -Force
            $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" +
                        [System.Environment]::GetEnvironmentVariable("Path","User")
            $result = & python --version 2>&1
            if ($LASTEXITCODE -eq 0 -and "$result" -notmatch "was not found" -and "$result" -notmatch "Microsoft Store") {
                $pythonCmd = "python"
                $pythonVersion = "$result"
                $installed = $true
                Write-Success "Python instalado correctamente"
            }
        } catch {
            Write-Error "Error descargando o instalando Python: $_"
        }
    }

    if (-not $installed) {
        Write-Error "No se pudo instalar Python automáticamente."
        Write-Info "Descárgalo manualmente desde: https://www.python.org/downloads/"
        Write-Info "Asegúrate de marcar 'Add Python to PATH' durante la instalación"
        exit 1
    }
}

Write-Success "$pythonVersion encontrado"

# Check Java installation
Write-Info "`n2. Verificando Java..."

$java = Get-Command java.exe -ErrorAction SilentlyContinue

if (-not $java) {

    Write-Info "Java no encontrado. Descargando Java 21..."

    $javaUrl = "https://api.adoptium.net/v3/installer/latest/21/ga/windows/x64/jdk/hotspot/normal/eclipse"
    $javaInstaller = "$env:TEMP\java21.msi"

    try {

        Invoke-WebRequest -Uri $javaUrl -OutFile $javaInstaller

        Write-Info "Instalando Java 21..."

        Start-Process msiexec.exe -ArgumentList "/i `"$javaInstaller`" /quiet /norestart" -Wait

        Remove-Item $javaInstaller -Force

    } catch {

        Write-Error "Error descargando o instalando Java"
        exit 1
    }

    # refrescar PATH
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" +
                [System.Environment]::GetEnvironmentVariable("Path","User")

    $java = Get-Command java.exe -ErrorAction SilentlyContinue

    if (-not $java) {
        Write-Error "Java no se pudo instalar correctamente"
        exit 1
    }

    Write-Success "Java 21 instalado correctamente"
}

$javaVersion = & java -version 2>&1
Write-Success "Java detectado:"
Write-Host $javaVersion

# Create installation directory
Write-Info "`n3. Creando directorio de instalación..."
if (-not (Test-Path $InstallPath)) {
    New-Item -ItemType Directory -Force -Path $InstallPath | Out-Null
    Write-Success "Directorio creado: $InstallPath"
} else {
    Write-Info "Directorio ya existe: $InstallPath"
}

# Download release from GitHub
Write-Info "`n4. Descargando FreeLauncher..."

if ($Version -eq "latest") {
    $apiUrl = "https://api.github.com/repos/marquistallman/OpenLauncherProyect/releases/latest"
} else {
    $apiUrl = "https://api.github.com/repos/marquistallman/OpenLauncherProyect/releases/tags/$Version"
}

try {
    $release = Invoke-RestMethod -Uri $apiUrl -Headers @{"Accept"="application/vnd.github.v3+json"}
    
    # Find the asset that is a zip file, to make it more robust
    $zipAsset = $release.assets | Where-Object { $_.name -like '*.zip' } | Select-Object -First 1
    $isSourceCode = $false

    if ($zipAsset) {
        $downloadUrl = $zipAsset.browser_download_url
        Write-Info "Descargando: $($zipAsset.name)"
    } elseif ($release.zipball_url) {
        Write-Info "⚠️ No se encontró asset binario. Descargando código fuente..."
        $downloadUrl = $release.zipball_url
        $isSourceCode = $true
    } else {
        Write-Error "No se encontró un archivo .zip en la release de GitHub."
        exit 1
    }
    
    $zipPath = Join-Path $InstallPath "freelauncher.zip"
    
    Invoke-WebRequest -Uri $downloadUrl -OutFile $zipPath
    Write-Success "Descarga completada"
    
    # Extract zip
    Write-Info "`n5. Extrayendo archivos..."
    if ($isSourceCode) {
        $tempExtractPath = Join-Path $InstallPath "temp_extract"
        Expand-Archive -Path $zipPath -DestinationPath $tempExtractPath -Force
        $innerFolder = Get-ChildItem -Path $tempExtractPath -Directory | Select-Object -First 1
        if ($innerFolder) { Get-ChildItem -Path $innerFolder.FullName | Move-Item -Destination $InstallPath -Force }
        Remove-Item $tempExtractPath -Recurse -Force
    } else {
        Expand-Archive -Path $zipPath -DestinationPath $InstallPath -Force
    }
    Remove-Item $zipPath
    Write-Success "Archivos extraídos"
    
} catch {
    # Si falla la descarga de la release (ej. 404 Not Found), intentar descargar el código fuente
    if ("$_" -match "404" -or "$_" -match "Not Found") {
        Write-Info "⚠️ No se encontró una release oficial. Descargando código fuente (main)..."
        $downloadUrl = "https://github.com/marquistallman/OpenLauncherProyect/archive/refs/heads/main.zip"
        $zipPath = Join-Path $InstallPath "source.zip"
        
        try {
            Invoke-WebRequest -Uri $downloadUrl -OutFile $zipPath
            
            # Extraer en carpeta temporal para manejar la estructura del zip de GitHub (Repo-main)
            $tempExtractPath = Join-Path $InstallPath "temp_extract"
            Expand-Archive -Path $zipPath -DestinationPath $tempExtractPath -Force
            
            # Mover archivos de la subcarpeta al directorio de instalación
            $innerFolder = Get-ChildItem -Path $tempExtractPath -Directory | Select-Object -First 1
            if ($innerFolder) {
                Get-ChildItem -Path $innerFolder.FullName | Move-Item -Destination $InstallPath -Force
            }
            
            Remove-Item $zipPath -Force
            Remove-Item $tempExtractPath -Recurse -Force
            Write-Success "Código fuente descargado y extraído"
        } catch {
            Write-Error "Error descargando el código fuente: $_"
            exit 1
        }
    } else {
        Write-Error "Error durante la descarga: $_"
        exit 1
    }
}

# Install Python dependencies
Write-Info "`n6. Instalando dependencias de Python..."
$reqFile = Join-Path $InstallPath "requirements.txt"
if (Test-Path $reqFile) {
    & $pythonCmd -m pip install -r $reqFile --quiet
    Write-Success "Dependencias instaladas"
} else {
    Write-Error "No se encontró requirements.txt"
}

# Create launcher script
Write-Info "`n7. Creando script de lanzamiento..."
$launcherScript = @"
`@echo off
cd "$InstallPath"
$pythonCmd main.py %*
"@

$batFile = Join-Path $InstallPath 'launcher.bat'
$launcherScript | Out-File -FilePath $batFile -Encoding utf8
Write-Success "Script de lanzamiento creado"

# Add to PATH
Write-Info "`n8. Agregando FreeLauncher a PATH..."
$currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
if ($currentPath -notlike "*$InstallPath*") {
    $newPath = $currentPath + ';' + $InstallPath
    [Environment]::SetEnvironmentVariable('Path', $newPath, 'Machine')
    Write-Success "Agregado a PATH"
} else {
    Write-Info "Ya está en PATH"
}

# Create desktop shortcut
if ($CreateDesktopShortcut) {
    Write-Info "`n9. Creando atajo en Escritorio..."
    
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $shortcutPath = Join-Path $desktopPath "FreeLauncher.lnk"
    
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $batFile
    $shortcut.WorkingDirectory = $InstallPath
    $shortcut.Description = "Modern Minecraft Launcher"
    
    # Set icon only if it exists
    $iconFile = Join-Path $InstallPath 'icon.ico'
    if (Test-Path $iconFile) {
        $shortcut.IconLocation = "$iconFile,0"
    }
    
    $shortcut.Save()
    
    Write-Success "Atajo creado en: $shortcutPath"
}

# Final message
Write-Success "`n¡Instalación completada!`n"
Write-Info "Para iniciar FreeLauncher:"
Write-Info "  • Haz doble clic en el atajo del Escritorio"
Write-Info "  • O ejecuta: freelauncher (requiere abrir una nueva terminal)"
Write-Info "  • O abre: $InstallPath\main.py`n"

Write-Success "¡Diviértete lanzando Minecraft!"

# Keep window open
Write-Info "Presiona cualquier tecla para cerrar..."
Read-Host
