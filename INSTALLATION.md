# 🚀 Installation & Setup Guide

Complete guide for FreeLauncher installation and configuration.

## 📦 Prerequisites

### Required
- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Java 8+** - [Download](https://www.java.com/download) or [OpenJDK](https://jdk.java.net/)
- **Git** - [Download](https://git-scm.com/) (optional, for cloning)

### Optional
- **Docker** - [Download](https://www.docker.com/products/docker-desktop)
- **Visual Studio Code** - [Download](https://code.visualstudio.com/)

## 🖥️ System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | Dual Core | Quad Core |
| RAM | 4 GB | 8 GB |
| Disk | 1 GB | 5 GB+ |
| OS | Windows/Mac/Linux | Any |

## 💻 Installation Methods

### Method 1: Local Installation (Recommended)

#### Step 1: Clone Repository

```bash
# Using git
git clone https://github.com/yourusername/freelauncher.git
cd freelauncher

# Or download ZIP and extract
# Then navigate to the folder
cd FreeLauncher
```

#### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 4: Run Application

```bash
python main.py
```

### Method 2: Docker Installation

#### Step 1: Build Docker Image

```bash
docker build -t freelauncher:latest .
```

#### Step 2: Run Container

**Linux (with display):**
```bash
docker run -it \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v ~/.freelauncher:/home/freelauncher/.freelauncher \
  -v ~/.minecraftLauncher:/home/freelauncher/.minecraftLauncher \
  freelauncher:latest
```

**Windows:**
```bash
docker run -it freelauncher:latest
```

#### Step 3: Using Docker Compose (Recommended)

```bash
docker-compose up
```

### Method 3: Quick Start (Windows Only)

For Windows, you can create a `.bat` file:

```batch
@echo off
cd /d "%~dp0"
python -m venv venv
call .\venv\Scripts\activate.bat
pip install -r requirements.txt
python main.py
```

Save as `start-freelauncher.bat` and double-click to run.

## ⚙️ Configuration

### Environment Variables

Create `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Edit `.env`:

```properties
# Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO

# Application info
APP_NAME=FreeLauncher
APP_VERSION=2.0.0

# Default RAM for new profiles
DEFAULT_RAM_GB=2

# Minecraft directory (change if needed)
# MINECRAFT_DIR=~/.minecraftLauncher
```

### Data Directories

FreeLauncher creates these directories:

```
~/.freelauncher/
├── data/
│   └── profiles.json
└── logs/
    └── freelauncher_YYYYMMDD.log
```

## ✅ Verification

After installation, verify everything works:

```bash
# Test Python installation
python --version
# Expected: Python 3.8+

# Test Java installation
java -version
# Expected: Java version info

# Test dependencies
python -c "import minecraft_launcher_lib; print('✓ OK')"

# Run application
python main.py
```

## 🐛 Troubleshooting

### Python Not Found

**Error:** `python: command not found`

**Windows Solution:**
1. Reinstall Python
2. Check "Add Python to PATH" during installation
3. Use `python3` instead of `python`

**macOS/Linux Solution:**
```bash
# Try python3 instead
python3 main.py

# Or add alias
echo "alias python=python3" >> ~/.bashrc
source ~/.bashrc
```

### Java Not Found

**Error:** `Java is not installed or not in PATH`

**Solution:**
1. Install Java: [java.com](https://www.java.com/download)
2. Verify installation:
   ```bash
   java -version
   ```
3. If still not found, add to PATH:
   - Windows: System Properties → Environment Variables → Add Java bin folder
   - macOS: `echo 'export PATH="/Applications/Java/Home/bin:$PATH"' >> ~/.bash_profile`
   - Linux: Usually auto-detected

### Virtual Environment Issues

**Error:** `command not found: activate`

**Windows:** Use `.\venv\Scripts\activate` (not `source`)
**macOS/Linux:** Use `source venv/bin/activate`

### Module Not Found

**Error:** `ModuleNotFoundError: No module named 'minecraft_launcher_lib'`

**Solution:**
```bash
# Make sure virtual environment is active
pip install -r requirements.txt
```

### Permission Denied

**Error:** `PermissionError: [Errno 13] Permission denied`

**Windows:** Run as Administrator
**macOS/Linux:** 
```bash
chmod +x main.py
# Or use sudo
sudo python main.py
```

### Minecraft Directory Not Found

**Solution:**
1. Install Minecraft Launcher from [launcher.minecraft.net](https://launcher.minecraft.net/)
2. Run Minecraft at least once
3. This creates `.minecraftLauncher` directory automatically

### Profiles Not Loading

**Debug steps:**
1. Check logs:
   ```bash
   tail ~/.freelauncher/logs/freelauncher_*.log
   ```
2. Verify profiles file exists:
   ```bash
   cat ~/.freelauncher/data/profiles.json
   ```
3. Ensure valid JSON format
4. Delete file and restart (creates default profile):
   ```bash
   rm ~/.freelauncher/data/profiles.json
   python main.py
   ```

### Game Won't Start

**Check these in order:**
1. Java installed: `java -version`
2. Version installed:
   - Check `~/.minecraftLauncher/versions/` directory
   - Install version through launcher if missing
3. RAM setting valid (1-32 GB)
4. Username not empty
5. Check error log: `~/.freelauncher/logs/`

**Common issues:**
- **"Could not find Java"**: Install Java or add to PATH
- **"Version not found"**: Install version through Minecraft Launcher
- **"Insufficient RAM"**: Reduce RAM allocation in profile
- **"Invalid username"**: Username must not be empty

### Docker Issues

**Error:** `Cannot connect to Docker daemon`

**Solution:**
1. Start Docker Desktop (Windows/macOS)
2. For Linux: `sudo systemctl start docker`

**Error:** `No display server found`

**Windows Solution:**
Windows doesn't support X11 display forwarding. Consider:
- Using WSL2 with X server
- Running on native Windows with virtual environment
- Using headless configuration

**Error:** `Permission denied: ~/.freelauncher`

**Solution:**
```bash
sudo chown -R $USER:$USER ~/.freelauncher
```

## 🔄 Updating FreeLauncher

### From Git

```bash
git pull origin main
pip install -r requirements.txt
```

### From Archive

1. Download latest version
2. Extract to new folder
3. Copy `~/.freelauncher/data/profiles.json` to new folder
4. Run new version

## 🗑️ Uninstalling

### Local Installation

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows

# Optional: Remove data directory
rm -rf ~/.freelauncher
rm -rf ~/.minecraftLauncher
```

### Docker

```bash
# Remove container
docker ps -a  # Find container ID
docker rm <container_id>

# Remove image
docker rmi freelauncher:latest

# Remove volume
docker volume rm freelauncher_freelauncher-network
```

## 📱 Mobile/Remote Access

FreeLauncher is desktop-only, but you can:

1. **Use Remote Desktop**: Connect to computer running FreeLauncher
2. **Stream Games**: Use game streaming services
3. **Server Mode**: (Future feature) Run Minecraft server instead

## 🎮 First Launch

1. **Create Profile**
   - Click "+ New"
   - Enter profile name (e.g., "Vanilla")
   - Enter Minecraft username
   - Set RAM (default: 2 GB)
   - Click "Create"

2. **Install Version** (if needed)
   - Click "Instalar Versiones"
   - Select version to install
   - Wait for download

3. **Launch Game**
   - Select profile
   - Select version
   - Click "PLAY"
   - Game window should open

## 📞 Need Help?

1. Check [Troubleshooting](#🐛-troubleshooting) section
2. Check logs: `~/.freelauncher/logs/`
3. Open issue on GitHub
4. Check [Architecture](ARCHITECTURE.md) for technical details

## 🔐 Security Notes

- Profiles are stored in `~/.freelauncher/data/profiles.json`
- Keep backups of important profiles
- Don't share profile files containing sensitive data
- Logs are stored locally and not uploaded

## ✨ Next Steps

After installation:
- [ ] Create your first profile
- [ ] Install Minecraft version
- [ ] Launch and test game
- [ ] Install mods (if desired)
- [ ] Explore advanced features

---

**Congratulations!** FreeLauncher is ready to use! 🎮
