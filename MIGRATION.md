# 📚 Migration Guide - v1.0 to v2.0

This guide helps you migrate from the old codebase to the new refactored FreeLauncher v2.0.

## 🆕 What's New

### Architecture
- ✅ Complete refactoring using SOLID principles
- ✅ Separation of concerns: Core logic, UI, Utilities
- ✅ Repository pattern for flexible storage
- ✅ Service layer for business logic
- ✅ Comprehensive error handling

### Project Structure
```
Old Structure          →  New Structure
─────────────────────────────────────────
main.py              →  main.py (updated)
funciones.py         →  src/core/
perfiles.py          →  src/core/profile_manager.py
Window/              →  src/ui/

Legacy files:        →  Archived (can be deleted)
- Window/
- funciones.py
- perfiles.py
```

### Code Organization

**Old approach:**
```python
# Procedural, scattered logic
import perfiles
import funciones

perfiles.inicializar_perfiles()
perfiles.crear_perfil("name", "user", "2")
minecraft_launcher_lib.command.get_minecraft_command(...)
```

**New approach:**
```python
# Organized, maintainable classes
from src.core.profile_manager import ProfileService, JsonProfileRepository
from src.core.minecraft_launcher import MinecraftManager

repository = JsonProfileRepository()
profile_service = ProfileService(repository)
profile_service.create_profile("name", "user", 2)

minecraft_manager = MinecraftManager()
minecraft_manager.launcher.launch(profile, version, callback)
```

## 🔄 Migration Steps

### 1. Backup Your Data
```bash
# Your existing profiles are safely stored in:
~/.openlauncherproyect/perfiles.json

# New location will be:
~/.freelauncher/data/profiles.json
```

### 2. Installation
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. First Run
```bash
python main.py
```

The application will:
- Automatically create `.freelauncher/` directory
- Migrate profiles if they exist
- Set up logging system

### 4. Verify Profiles
- Check if your old profiles appear in the UI
- If not, manually create them (profiles are now validated)

### 5. Clean Up (Optional)
```bash
# Remove old directories if everything works
rm -rf Window/
rm funciones.py
rm perfiles.py
```

## 🔧 API Changes

### Profile Management

**Old API:**
```python
import perfiles

perfiles.inicializar_perfiles()
perfiles.crear_perfil("name", "user", "2")
perfiles.cargar_perfiles()
perfiles.guardar_perfiles(data)
perfiles.listar_perfiles()
```

**New API:**
```python
from src.core.profile_manager import ProfileService, JsonProfileRepository, Profile

# Initialize service
repo = JsonProfileRepository()
service = ProfileService(repo)

# Create profile (with validation)
profile = service.create_profile("name", "user", 2)

# Get profile
profile = service.get_profile("name")

# Update profile
profile = service.update_profile("name", "newuser", 4)

# Delete profile
service.delete_profile("name")

# List profiles
profiles = service.list_profiles()
```

### Minecraft Launching

**Old API:**
```python
from funciones import ejecutar_minecraft

ejecutar_minecraft("username", "1.20.1", "4", window.destroy)
```

**New API:**
```python
from src.core.minecraft_launcher import MinecraftManager
from src.core.profile_manager import Profile

manager = MinecraftManager()
profile = Profile(name="test", username="Steve", ram=4)
manager.launcher.launch(profile, "1.20.1", on_close=window.destroy)
```

### Error Handling

**Old:**
```python
# Errors not consistently handled
try:
    perfiles.crear_perfil(...)
except Exception:
    pass
```

**New:**
```python
from src.utils.exceptions import ProfileAlreadyExistsError, InvalidProfileError

try:
    service.create_profile("name", "user", 2)
except ProfileAlreadyExistsError:
    print("Profile already exists")
except InvalidProfileError as e:
    print(f"Invalid profile: {e}")
```

## 📝 Configuration

### Environment Variables
Create `.env` from `.env.example`:
```bash
cp .env.example .env
```

### Logging
Logs are now stored in:
```
~/.freelauncher/logs/freelauncher_YYYYMMDD.log
```

## 🧪 Testing

Run the new test suite:
```bash
pytest tests/ -v
```

Or use the setup script:
```bash
python setup.py test
```

## 🐛 Troubleshooting

### Profiles Not Loading
1. Check logs: `~/.freelauncher/logs/`
2. Verify JSON format in `~/.freelauncher/data/profiles.json`
3. Ensure usernames are not empty

### Game Not Launching
1. Verify Java is installed: `java -version`
2. Check Minecraft installation: `~/.minecraftLauncher/`
3. Review error messages in status bar

### Old Code References
If you have code that imports from old modules:
```python
# Remove these imports:
# import funciones
# import perfiles
# from Window.Main import lanzar_launcher

# Replace with:
from src.ui.main_window import run_application
from src.core.profile_manager import ProfileService, JsonProfileRepository
from src.core.minecraft_launcher import MinecraftManager
```

## 📊 Performance Improvements

- ⚡ Better error handling = fewer crashes
- ⚡ Proper logging = easier debugging
- ⚡ Repository pattern = flexible storage options
- ⚡ Type hints = better IDE support
- ⚡ Separation of concerns = easier testing

## 🔐 Data Safety

All user data is now validated:
- Profile names must be non-empty strings
- Usernames must be non-empty strings
- RAM must be positive integer (1-32 GB)

Default profile is protected and cannot be deleted.

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Application runs: `python main.py`
- [ ] Profiles load in UI
- [ ] Can create new profile
- [ ] Can launch game
- [ ] Logs created in `~/.freelauncher/logs/`

## 🆘 Need Help?

1. Check logs: `~/.freelauncher/logs/`
2. Review error messages in status bar
3. Open an issue on GitHub
4. Check troubleshooting section above

## 🎉 You're Done!

Welcome to FreeLauncher v2.0! The cleaner architecture makes it easier to:
- Add new features
- Fix bugs
- Write tests
- Maintain code
- Deploy with Docker

Enjoy! 🚀
