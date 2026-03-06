# 📦 Distribución e Instalación de FreeLauncher

Este documento explica cómo instalar FreeLauncher de manera fácil.

## 🚀 Métodos de Instalación

### Option 1: Script de Instalación (Recomendado)

#### Windows
```powershell
# Como administrador en PowerShell:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/marquistallman/OpenLauncherProyect/main/scripts/install.ps1'))
```

O descarga el script manualmente:
1. Ve a: `scripts/install.ps1`
2. Click derecho → "Ejecutar con PowerShell"

#### Linux / macOS
```bash
curl -sSL https://raw.githubusercontent.com/marquistallman/OpenLauncherProyect/main/scripts/install.sh | bash
```

O descarga el script:
```bash
wget https://raw.githubusercontent.com/[YOUR_REPO]/FreeLauncher/main/scripts/install.sh
chmod +x install.sh
./install.sh
```

---

### Option 2: Docker (Sin instalación en el PC)

#### Requisitos
- Docker instalado ([descargar](https://www.docker.com/products/docker-desktop))

#### Instalación
```bash
# Clonar repositorio
git clone https://github.com/[YOUR_REPO]/FreeLauncher.git
cd FreeLauncher

# Ejecutar con Docker
docker-compose up -d
```

#### En Windows (con Docker Desktop)
```powershell
docker-compose up -d
```

**Ventajas:**
- ✅ No interfiere con tu sistema
- ✅ Fácil de desinstalar (solo borrar el contenedor)
- ✅ Compatible con Windows/Mac/Linux

---

### Option 3: Descarga Manual

#### Windows
1. Ve a [Releases](https://github.com/marquistallman/OpenLauncherProyect/releases)
2. Descarga `freelauncher-X.X.X.zip`
3. Descomprime en `C:\Program Files\FreeLauncher` (o donde prefieras)
4. Abre Command Prompt o PowerShell en esa carpeta
5. Ejecuta:
```cmd
python -m pip install -r requirements.txt
python main.py
```

#### Linux/macOS
1. Ve a [Releases](https://github.com/marquistallman/OpenLauncherProyect/releases)
2. Descarga `freelauncher-X.X.X.tar.gz`
3. Descomprime:
```bash
tar -xzf freelauncher-X.X.X.tar.gz
cd freelauncher-X.X.X
```
4. Instala dependencias:
```bash
python3 -m pip install -r requirements.txt
```
5. Ejecuta:
```bash
python3 main.py
```

---

### Option 4: Instalar desde PyPI (pip)

```bash
pip install freelauncher
freelauncher
```

---

## ✅ Requisitos Previos

### Windows
- **Python 3.11+** ([descargar](https://www.python.org/downloads/))
  - ⚠️ Marca "Add Python to PATH" durante la instalación
- **Java 17+** ([descargar](https://www.oracle.com/java/technologies/downloads/)) - Minecraft lo necesita
- **Git** (opcional, solo si clonas el repo)

### Linux
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip python3-tk default-jre

# Fedora
sudo dnf install python3 python3-pip python3-tkinter java-latest-openjdk

# Arch
sudo pacman -S python python-pip tk jre-openjdk
```

### macOS
```bash
# Con Homebrew
brew install python3 java

# Tkinter ya viene con Python en macOS
```

---

## 🔍 Verificación

Después de instalar, verifica que todo funciona:

```bash
# Windows (Command Prompt o PowerShell)
python -c "import tkinter; print('Tkinter OK')"
java -version

# Linux/macOS
python3 -c "import tkinter; print('Tkinter OK')"
java -version
```

---

## 🐳 Docker Avanzado

### Ejecutar con Volúmenes Persistentes
```bash
docker-compose -f docker-compose.yml up -d \
  -v ~/.freelauncher:/root/.freelauncher \
  -v ~/.minecraftLauncher:/root/.minecraftLauncher
```

### Ver Logs
```bash
docker-compose logs -f freelauncher
```

### Detener
```bash
docker-compose down
```

### Eliminar Todo (Limpieza completa)
```bash
docker-compose down -v
docker image rm freelauncher
```

---

## 🆘 Solución de Problemas

### "Python no encontrado"
**Solución:** Python no está en PATH o no está instalado
- Windows: Reinstala Python y marca "Add to PATH"
- Linux: `sudo apt-get install python3 python3-pip`

### "No module named 'tkinter'"
**Solución:** Tkinter no está instalado
- Windows: Reinstala Python y marca "tcl/tk and IDLE"
- Linux: `sudo apt-get install python3-tk`

### "Java no encontrado"
**Solución:** Java no está instalado o en PATH
- Descarga desde https://www.oracle.com/java/technologies/downloads/

### SmartScreen advierte en Windows
**Solución:** Es normal para ejecutables sin certificar. Haz clic en "Más información" → "Ejecutar de todas formas"

### Docker no funciona en Windows
**Solución:** Instala [Docker Desktop para Windows](https://www.docker.com/products/docker-desktop)

---

## 📝 Desinstalación

### Windows (Manual)
1. Elimina la carpeta: `C:\Program Files\FreeLauncher`
2. En PowerShell como admin:
```powershell
[Environment]::GetEnvironmentVariable("Path", "Machine") -replace ';?C:\\Program Files\\FreeLauncher', '' | ?{$_} | % { [Environment]::SetEnvironmentVariable("Path", $_, "Machine") }
```

### Windows (Script)
```powershell
# Como admin en PowerShell
$InstallPath = "C:\Program Files\FreeLauncher"
Remove-Item -Recurse -Force $InstallPath
```

### Linux/macOS
```bash
rm -rf ~/.local/share/freelauncher
rm ~/.local/bin/freelauncher
rm ~/.local/share/applications/freelauncher.desktop  # Linux solo
```

### Docker
```bash
docker-compose down -v
```

---

## 🆕 Actualizar

### Script de Instalación
```powershell
# Windows
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/[YOUR_REPO]/FreeLauncher/main/scripts/install.ps1'))
```

```bash
# Linux/macOS
curl -sSL https://raw.githubusercontent.com/[YOUR_REPO]/FreeLauncher/main/scripts/install.sh | bash
```

### Docker
```bash
docker-compose pull
docker-compose up -d
```

---

## 📞 Soporte

¿Problemas? Abre un [issue en GitHub](https://github.com/[YOUR_REPO]/FreeLauncher/issues)

---

Hecho con ❤️ por la comunidad de FreeLauncher
