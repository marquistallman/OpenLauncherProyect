#!/bin/bash

# FreeLauncher Installation Script (Linux/macOS)
# This script downloads and installs FreeLauncher with minimal user interaction

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }

# Defaults
INSTALL_PATH="${INSTALL_PATH:-$HOME/.local/share/freelauncher}"
VERSION="${VERSION:-latest}"
CREATE_SHORTCUT="${CREATE_SHORTCUT:-true}"

print_info "🎮 FreeLauncher - Instalador"
print_info "============================"
echo

# Check Python installation
print_info "1️⃣  Verificando Python..."
if ! command -v python3 &> /dev/null; then
    print_error "Python no está instalado"
    print_info "Instálalo con:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  macOS: brew install python3"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
print_success "Python $PYTHON_VERSION encontrado"

# Check Java installation
print_info "\n2️⃣  Verificando Java..."
if ! command -v java &> /dev/null; then
    print_warning "Java no está instalado. Minecraft lo necesita."
    print_info "Instálalo con:"
    echo "  Ubuntu/Debian: sudo apt-get install default-jre"
    echo "  macOS: brew install java"
    echo "  Fedora: sudo dnf install java-latest-openjdk"
    read -p "¿Continuar de todas formas? (s/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        exit 1
    fi
else
    print_success "Java encontrado"
fi

# Check Tkinter
print_info "\n3️⃣  Verificando Tkinter..."
if ! python3 -c "import tkinter" 2>/dev/null; then
    print_warning "Tkinter no está instalado (necesario para la GUI)"
    print_info "Instálalo con:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "  macOS: Ya incluido con Python"
    echo "  Fedora: sudo dnf install python3-tkinter"
    exit 1
fi
print_success "Tkinter encontrado"

# Create installation directory
print_info "\n4️⃣  Creando directorio de instalación..."
mkdir -p "$INSTALL_PATH"
print_success "Directorio: $INSTALL_PATH"

# Download release
print_info "\n5️⃣  Descargando FreeLauncher..."

if [ "$VERSION" = "latest" ]; then
    DOWNLOAD_URL=$(curl -s https://api.github.com/repos/marquistallman/OpenLauncherProyect/releases/latest | grep browser_download_url | grep "tar.gz" | head -n1 | cut -d'"' -f4)
else
    DOWNLOAD_URL=$(curl -s https://api.github.com/repos/marquistallman/OpenLauncherProyect/releases/tags/$VERSION | grep browser_download_url | grep "tar.gz" | head -n1 | cut -d'"' -f4)
fi

if [ -z "$DOWNLOAD_URL" ]; then
    print_error "No se encontró release disponible"
    exit 1
fi

print_info "Descargando desde: $DOWNLOAD_URL"
cd /tmp
curl -L -o freelauncher.tar.gz "$DOWNLOAD_URL"
print_success "Descarga completada"

# Extract
print_info "\n6️⃣  Extrayendo archivos..."
cd "$INSTALL_PATH"
tar -xzf /tmp/freelauncher.tar.gz --strip-components=1
rm /tmp/freelauncher.tar.gz
print_success "Archivos extraídos"

# Install dependencies
print_info "\n7️⃣  Instalando dependencias de Python..."
python3 -m pip install -r requirements.txt --quiet
print_success "Dependencias instaladas"

# Create launcher script
print_info "\n8️⃣  Creando script de lanzamiento..."
mkdir -p "$HOME/.local/bin"
cat > "$HOME/.local/bin/freelauncher" << EOF
#!/bin/bash
cd "$INSTALL_PATH"
python3 main.py "\$@"
EOF

chmod +x "$HOME/.local/bin/freelauncher"
print_success "Script creado: $HOME/.local/bin/freelauncher"

# Add to PATH if needed
if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
    print_info "\n9️⃣  Agregando a PATH..."
    
    if [ -f "$HOME/.bashrc" ]; then
        echo "export PATH=\$PATH:$HOME/.local/bin" >> "$HOME/.bashrc"
    fi
    if [ -f "$HOME/.zshrc" ]; then
        echo "export PATH=\$PATH:$HOME/.local/bin" >> "$HOME/.zshrc"
    fi
    
    print_success "Agregado a PATH"
    print_warning "Ejecuta: source ~/.bashrc  (o ~/.zshrc)"
fi

# Create desktop entry (Linux)
if [ -d "$HOME/.local/share/applications" ] && [ "$CREATE_SHORTCUT" = "true" ]; then
    print_info "\n🔟 Creando acceso directo..."
    mkdir -p "$HOME/.local/share/applications"
    cat > "$HOME/.local/share/applications/freelauncher.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=FreeLauncher
Comment=Modern Minecraft Launcher
Exec=$HOME/.local/bin/freelauncher
Icon=application-x-executable
Terminal=true
Categories=Game;
EOF
    print_success "Acceso directo creado"
fi

# Final message
echo
print_success "✨ ¡Instalación completada!"
echo
print_info "Para iniciar FreeLauncher:"
echo "  • Ejecuta: freelauncher"
echo "  • O: python3 $INSTALL_PATH/main.py"
echo
print_success "¡Diviértete lanzando Minecraft!"
