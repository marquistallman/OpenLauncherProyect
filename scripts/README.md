# 📜 Scripts disponibles

Esta carpeta contiene scripts de utilidad para el desarrollo, construcción y distribución de FreeLauncher.

## 🔧 Scripts

### `install.ps1` - Instalador Windows
Instala FreeLauncher en Windows automáticamente.

**Uso:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\install.ps1
```

**Características:**
- ✅ Verifica Python y Java
- ✅ Descarga la última versión
- ✅ Instala dependencias
- ✅ Crea acceso directo en Escritorio
- ✅ Agrega a PATH para usar desde terminal

**Opciones:**
```powershell
.\install.ps1 -InstallPath "C:\Program Files\FreeLauncher"
.\install.ps1 -Version "v1.2.3"
.\install.ps1 -CreateDesktopShortcut $false
```

---

### `install.sh` - Instalador Linux/macOS
Instala FreeLauncher en sistemas Unix.

**Uso:**
```bash
chmod +x install.sh
./install.sh
```

**O mediante curl:**
```bash
curl -sSL https://raw.githubusercontent.com/..../install.sh | bash
```

**Características:**
- ✅ Verifica Python3 y Java
- ✅ Detecta distribución (apt, dnf, brew)
- ✅ Instala dependencias del sistema
- ✅ Crea script ejecutable en ~/.local/bin
- ✅ Crea acceso directo (Linux)

**Variables de entorno:**
```bash
INSTALL_PATH=$HOME/.local/share/freelauncher ./install.sh
VERSION=v1.2.3 ./install.sh
CREATE_SHORTCUT=false ./install.sh
```

---

### `build.py` - Script de construcción
Construye distribuciones (.whl, .tar.gz, .zip) y Docker image.

**Uso:**
```bash
python scripts/build.py

# Solo distribuciones
python scripts/build.py --dist

# Solo Docker
python scripts/build.py --skip-tests --skip-lint

# Build completo (recomendado)
python scripts/build.py --all
```

**Flags:**
- `--all` - Build completo (tests + linting + compilación)
- `--dist` - Solo crear distribuciones
- `--skip-tests` - Saltarse tests
- `--skip-lint` - Saltarse linting
- `--skip-docker` - No compilar Docker

**Salida:**
- `dist/freelauncher-X.X.X.whl` - Python wheel
- `dist/freelauncher-X.X.X.tar.gz` - Tarball comprimido
- `dist/freelauncher-X.X.X.zip` - ZIP comprimido
- Docker image: `freelauncher:X.X.X` y `freelauncher:latest`

---

## 🎯 Workflow de Desarrollo

### 1. Desarrollo Local
```bash
# Setup
git clone https://github.com/.../FreeLauncher.git
cd FreeLauncher
make dev

# Trabajo diario
make run        # Ejecutar
make test       # Probar
make lint       # Revisar código
make format     # Formatear
```

### 2. Antes de Hacer Push
```bash
make test
make lint
```

### 3. Para Hacer un Release
```bash
# Asegurar que todo funciona
make test
make lint

# Actualizar versión en src/utils/config.py
# APP_VERSION = "X.X.X"

# Commit
git add .
git commit -m "Release vX.X.X"

# Tag
git tag -a vX.X.X -m "Release X.X.X"
git push origin vX.X.X

# GitHub Actions hace el resto automáticamente
```

---

## 🐳 Docker Build

Para compilar la imagen según cambios sin crear release:

```bash
# Compilar localmente
docker build -t freelauncher:dev .

# Ejecutar
docker-compose -f docker-compose.yml run --rm freelauncher

# O con docker-compose
docker-compose up
```

---

## 📦 Makefile Helpers

Para facilitar el trabajo, usa el `Makefile`:

```bash
make help           # Ver todos los comandos
make install        # Instalar dependencias
make dev           # Instalar dev dependencies
make run           # Ejecutar la app
make test          # Correr tests
make lint          # Revisar código
make format        # Formatear código
make build         # Build distributions
make docker        # Build Docker image
make release       # Full release build
make clean         # Limpiar artifacts
make clean-all     # Limpiar todo
```

---

## 🚀 Distribución Automática

Los scripts se usan automáticamente por GitHub Actions cuando:
1. Haces push a un tag `v*`
2. Se dispara el workflow `.github/workflows/build.yml`
3. Se crean automáticamente:
   - Releases en GitHub
   - Distribuciones (wheel, tarball, zip)
   - Docker image

---

## 🔒 Seguridad

Los scripts ejecutan verificaciones:
- ✅ Verifican requisitos (Python, Java, Tkinter)
- ✅ Descargan desde repositorios oficiales
- ✅ Usan HTTPS para descargas
- ✅ No ejecutan código arbitrario

---

## 🐛 Troubleshooting

### Script no se ejecuta en PowerShell
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Permiso denegado en Linux/macOS
```bash
chmod +x install.sh
```

### Build falla sin cambios
```bash
make clean
make release
```

---

## 📝 Crear un Script Nuevo

Para agregar un nuevo script:

1. Crear en `scripts/`
2. Hacer executable: `chmod +x script.sh` o `chmod +x script.py`
3. Agregar comentarios de uso
4. Documentar aquí en este README
5. Commit y push

