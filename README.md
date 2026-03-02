# 🎮 FreeLauncher

A modern, feature-rich Minecraft launcher built with Python using SOLID principles and clean architecture.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-GPL3.0-blue)

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

This project is licensed under the GPL-3.0 License - see LICENSE file for details

## 🙋 Support

For issues or suggestions, please open an Issue on GitHub


