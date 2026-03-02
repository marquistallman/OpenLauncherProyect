# 🎮 FreeLauncher

A modern, feature-rich Minecraft launcher built with Python using SOLID principles and clean architecture.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## ✨ Features

- 🎯 **Profile Management**: Create and manage multiple Minecraft profiles with custom settings
- 🚀 **Easy Launcher**: Simple one-click Minecraft game launching
- 📦 **Mod Manager**: Search and install mods from Modrinth
- 🌳 **Clean Architecture**: SOLID principles, well-organized codebase
- 🐳 **Docker Support**: Run in containers for isolation
- 🔍 **Version Control Optimized**: Proper .gitignore and project structure
- 📝 **Comprehensive Logging**: Detailed logs for debugging

## 📋 Requirements

- **Python 3.8+**
- **Java 8+** (for Minecraft)
- **pip** (Python package manager)

### Optional
- **Docker & Docker Compose** (for containerized deployment)

## 🚀 Quick Start

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/freelauncher.git
   cd freelauncher
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows:
   .\venv\Scripts\activate
   
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

### Docker Deployment

1. **Build the image**
   ```bash
   docker build -t freelauncher:latest .
   ```

2. **Run with docker-compose**
   ```bash
   docker-compose up
   ```

3. **Or run with Docker directly**
   ```bash
   docker run -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix freelauncher:latest
   ```

## 📁 Project Structure

```
FreeLauncher/
├── src/
│   ├── core/                    # Business logic
│   │   ├── profile_manager.py   # Profile management with SOLID
│   │   ├── minecraft_launcher.py # Game launching
│   │   └── mod_manager.py        # Mod handling
│   │
│   ├── ui/                       # User interface
│   │   ├── main_window.py       # Main application window
│   │   ├── components.py        # Reusable UI components
│   │   └── profile_dialogs.py   # Profile dialogs
│   │
│   └── utils/                    # Utilities
│       ├── config.py            # Centralized configuration
│       ├── logger.py            # Logging setup
│       └── exceptions.py         # Custom exceptions
│
├── tests/                        # Unit tests
├── main.py                       # Entry point
├── requirements.txt              # Dependencies
├── .env.example                  # Environment template
├── Dockerfile                    # Docker image
├── docker-compose.yml            # Docker Compose config
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## 🏗️ Architecture & SOLID Principles

### Single Responsibility Principle
- Each class has one clear responsibility
- Profile management, Minecraft launching, and UI are separate concerns

### Open/Closed Principle
- Code is open for extension, closed for modification
- Abstract repository pattern allows different storage backends

### Liskov Substitution Principle
- Subclasses can replace base classes without breaking functionality

### Interface Segregation Principle
- Focused interfaces for specific needs
- Separated UI components for reusability

### Dependency Inversion Principle
- Services depend on abstractions, not concrete implementations
- Repository pattern enables flexible storage

## 🔧 Configuration

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Available options:
```properties
LOG_LEVEL=INFO
APP_NAME=FreeLauncher
APP_VERSION=2.0.0
MINECRAFT_DIR=~/.minecraftLauncher
DEFAULT_RAM_GB=2
```

## 📝 Usage

### Creating a Profile

1. Click **+ New** button
2. Enter profile name (e.g., "Vanilla")
3. Enter Minecraft username
4. Set RAM allocation
5. Click **Create**

### Launching the Game

1. Select profile from dropdown
2. Choose Minecraft version
3. (Optional) Override username/RAM
4. Click **PLAY**

## 🧪 Development

### Running Tests

```bash
pytest tests/ -v --cov=src
```

### Code Quality

```bash
# Format code
black src/

# Lint
flake8 src/

# Type checking
mypy src/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details

## 🙋 Support

For issues or suggestions, please open an Issue on GitHub
Minecraft no premium launcher, only for educational and research purpouses
Bassed in KeimaSenpai proyect, Xlauncher, link:https://github.com/KeimaSenpai/XLauncher-Script/tree/main

OpenLauncherProyect - Open Source
This is an open-source Minecraft Launcher designed to easily manage Minecraft versions, Forge/Fabric installation, and custom profiles. This project is built to be lightweight and simple to use, with no additional bloatware.

Features
Install Minecraft versions (Vanilla, Forge, and Fabric).

Create and manage custom user profiles.

Easily switch between different Minecraft versions.

Check Java installation.

Install mods automatically for Minecraft.

Generate unique UUID for offline players.

Installation
Download the .exe file from the releases section.

Run the file and follow the installation steps.

Open the launcher and configure your Minecraft settings.

Usage
Select the Minecraft version you want to play.

Install Forge/Fabric if required for specific versions.

Adjust RAM settings for performance.

Launch the game with a custom profile.

License
This project is licensed under the GNU GENERAL License - see the LICENSE.md file for details.

Contributors
In instagram- @davidhackstallman

OpenLauncherProyect - Código Abierto
Este es un lanzador de Minecraft de código abierto diseñado para gestionar fácilmente las versiones de Minecraft, la instalación de Forge/Fabric y los perfiles personalizados. Este proyecto está construido para ser ligero y fácil de usar, sin software innecesario.

Características
Instalar versiones de Minecraft (Vanilla, Forge y Fabric).

Crear y gestionar perfiles personalizados de usuario.

Cambiar fácilmente entre diferentes versiones de Minecraft.

Verificar la instalación de Java.

Instalar mods automáticamente para Minecraft.

Generar UUID único para jugadores offline.

Instalación
Descarga el archivo .exe desde la sección de lanzamientos.

Ejecuta el archivo y sigue los pasos de instalación.

Abre el lanzador y configura tus ajustes de Minecraft.

Uso
Selecciona la versión de Minecraft que deseas jugar.

Instala Forge/Fabric si es necesario para versiones específicas.

Ajusta la configuración de RAM para un mejor rendimiento.

Lanza el juego con un perfil personalizado.

Licencia
Este proyecto está licenciado bajo la Licencia GNU GENERAL - consulta el archivo LICENSE.md para más detalles.

Contribuyentes
En instagram- @davidhackstallman

OpenLauncherProyect - Open Source
Dies ist ein Open-Source-Minecraft-Launcher, der entwickelt wurde, um Minecraft-Versionen, die Installation von Forge/Fabric und benutzerdefinierte Profile einfach zu verwalten. Das Projekt ist leichtgewichtig und einfach zu bedienen – ohne unnötige Software.

Funktionen
Installiere Minecraft-Versionen (Vanilla, Forge und Fabric).

Erstelle und verwalte benutzerdefinierte Profile.

Wechsle problemlos zwischen verschiedenen Minecraft-Versionen.

Überprüfe die Java-Installation.

Installiere automatisch Mods für Minecraft.

Generiere eine einzigartige UUID für Offline-Spieler.

Installation
Lade die .exe-Datei aus dem Release-Bereich herunter.

Führe die Datei aus und folge den Installationsschritten.

Öffne den Launcher und konfiguriere deine Minecraft-Einstellungen.

Verwendung
Wähle die Minecraft-Version aus, die du spielen möchtest.

Installiere Forge/Fabric, wenn dies für bestimmte Versionen erforderlich ist.

Passe die RAM-Einstellungen für die Leistung an.

Starte das Spiel mit einem benutzerdefinierten Profil.

Lizenz
Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe die LICENSE.md-Datei für Details.

Mitwirkende
In instagram- @davidhackstallman

