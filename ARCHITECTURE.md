# 🏗️ Architecture Documentation

## Overview

FreeLauncher follows a clean architecture with three main layers:

```
┌─────────────────────────────────────────┐
│           Presentation Layer            │
│        (UI - Tkinter Components)        │
│  main_window.py, components.py, etc     │
└──────────────────┬──────────────────────┘
                   │ depends on
┌──────────────────▼──────────────────────┐
│           Domain/Business Layer         │
│   (Core Logic - No UI Dependencies)     │
│  profile_manager.py, minecraft_launcher │
└──────────────────┬──────────────────────┘
                   │ uses
┌──────────────────▼──────────────────────┐
│          Infrastructure Layer           │
│   (Data, Config, Exceptions, Logging)   │
│  config.py, logger.py, exceptions.py    │
└─────────────────────────────────────────┘
```

## Layer Descriptions

### 1. Presentation Layer (UI)
**Files:** `src/ui/*`

Responsible for:
- User interface
- User input handling
- Displaying results
- Dialog management

**Key Classes:**
- `MainWindow`: Main application window
- `ProfileSelector`: Profile selection widget
- `VersionSelector`: Version selection widget
- `ProfileDialog`: Base dialog class
- `NewProfileDialog`: Create profile dialog
- `EditProfileDialog`: Edit profile dialog
- Custom components: `PlayButton`, `PlaceholderEntry`, etc.

**Dependencies:**
- Core services (ProfileService, MinecraftManager)
- UI components (Tkinter)

### 2. Domain/Business Layer (Core)
**Files:** `src/core/*`

Responsible for:
- Business logic
- Data processing
- Economic operations
- No direct UI dependencies

**Key Classes:**
- `ProfileService`: Profile business logic
- `ProfileRepository`: Abstract repository interface
- `JsonProfileRepository`: JSON storage implementation
- `MinecraftManager`: Minecraft game management
- `MinecraftLauncher`: Game launching
- `ModManager`: Mod handling
- `ModDownloader`: Mod downloading

**Design Patterns Used:**
- **Repository Pattern**: Abstraction for data persistence
- **Service Pattern**: Business logic encapsulation
- **Factory Pattern**: Object creation
- **Singleton Pattern**: Configuration

### 3. Infrastructure Layer (Utils)
**Files:** `src/utils/*`

Responsible for:
- Configuration management
- Logging setup
- Custom exceptions
- Cross-cutting concerns

**Key Classes:**
- `Config`: Centralized configuration
- `Logger`: Logging system
- Custom exceptions: `ProfileException`, `MinecraftException`, etc.

## SOLID Principles Implementation

### Single Responsibility Principle (S)

Each class has one reason to change:

```python
# Good: ProfileService handles profile business logic only
class ProfileService:
    def create_profile(self, name, username, ram) -> Profile:
        ...

# Repository handles persistence only
class JsonProfileRepository(ProfileRepository):
    def load(self) -> Dict[str, Profile]:
        ...

# UI handles presentation only
class ProfileSelector(ThemedFrame):
    def _build_ui(self):
        ...
```

### Open/Closed Principle (O)

Open for extension, closed for modification:

```python
# Abstract base class
class ProfileRepository(ABC):
    @abstractmethod
    def load(self) -> Dict[str, Profile]:
        pass

# Can be extended with different implementations
class JsonProfileRepository(ProfileRepository):
    def load(self) -> Dict[str, Profile]:
        # JSON implementation
        pass

class DatabaseProfileRepository(ProfileRepository):
    def load(self) -> Dict[str, Profile]:
        # Database implementation
        pass
```

### Liskov Substitution Principle (L)

Subtypes are substitutable without breaking code:

```python
def initialize_service(repo: ProfileRepository):
    service = ProfileService(repo)
    return service

# Works with both implementations
json_service = initialize_service(JsonProfileRepository())
db_service = initialize_service(DatabaseProfileRepository())
```

### Interface Segregation Principle (I)

Clients depend on specific interfaces:

```python
# Small, focused interface
class MinecraftVersionManager:
    def get_installed_versions(self) -> List[str]:
        ...
    
    def verify_version_installation(self, version: str) -> bool:
        ...

# Separate concern for Java verification
class JavaVerifier:
    @staticmethod
    def is_java_installed() -> bool:
        ...
```

### Dependency Inversion Principle (D)

Depend on abstractions, not concretions:

```python
# Good: Depends on abstract repository
class ProfileService:
    def __init__(self, repository: ProfileRepository):
        self.repository = repository

# UI depends on service abstraction
profile_service = ProfileService(JsonProfileRepository())
```

## Design Patterns

### 1. Repository Pattern

**Purpose:** Abstract data persistence

```python
# Abstract interface
class ProfileRepository(ABC):
    @abstractmethod
    def load(self) -> Dict[str, Profile]:
        pass
    
    @abstractmethod
    def save(self, profiles: Dict[str, Profile]) -> None:
        pass

# Concrete implementation
class JsonProfileRepository(ProfileRepository):
    def load(self) -> Dict[str, Profile]:
        # Load from JSON
        pass
    
    def save(self, profiles: Dict[str, Profile]) -> None:
        # Save to JSON
        pass
```

**Benefits:**
- Easy to test (use mock repository)
- Easy to swap implementations
- Centralized data logic

### 2. Service Pattern

**Purpose:** Encapsulate business logic

```python
class ProfileService:
    def __init__(self, repository: ProfileRepository):
        self.repository = repository
        self._profiles = self.repository.load()
    
    def create_profile(self, name: str, username: str, ram: int) -> Profile:
        # Business logic: validation, error handling
        if name in self._profiles:
            raise ProfileAlreadyExistsError()
        
        profile = Profile(name, username, ram)
        self._profiles[name] = profile
        self.repository.save(self._profiles)
        return profile
```

**Benefits:**
- Business logic separate from persistence
- Reusable across different UIs
- Easy to test
- Easy to add features

### 3. Factory Pattern

**Purpose:** Create objects with proper initialization

```python
class MinecraftManager:
    def __init__(self):
        self.launcher = MinecraftLauncher()
        self.version_manager = MinecraftVersionManager()
        self.java_verifier = JavaVerifier()
    
    def get_status(self) -> dict:
        return {
            'java_installed': self.java_verifier.is_java_installed(),
            'installed_versions': self.version_manager.get_installed_versions(),
        }
```

**Benefits:**
- Centralized object creation
- Ensures proper initialization
- Easy to configure

### 4. Singleton Pattern

**Purpose:** Ensure single instance across application

```python
class Config:
    # Class-level initialization
    @classmethod
    def initialize(cls) -> None:
        cls.APP_DIR.mkdir(parents=True, exist_ok=True)
        # ... setup

# Used throughout application
Config.initialize()
app_dir = Config.APP_DIR
```

**Benefits:**
- Global access to configuration
- Single source of truth
- Consistent behavior

## Error Handling

### Exception Hierarchy

```python
FreeLauncherException (base)
├── ProfileException
│   ├── ProfileNotFoundError
│   ├── ProfileAlreadyExistsError
│   └── InvalidProfileError
├── MinecraftException
│   ├── MinecraftVersionNotFoundError
│   └── MinecraftLaunchError
└── ModException
```

### Error Handling Strategy

1. **Specific Exceptions**: Use specific exception types
2. **Logging**: Log all errors with context
3. **User Feedback**: Show user-friendly messages
4. **Graceful Degradation**: Continue when possible

```python
def launch_game(self, profile: Profile, version: str) -> None:
    try:
        self._verify_prerequisites(version)
        # ... launch logic
    except MinecraftLaunchError as e:
        logger.error(f"Launch failed: {e}")
        messagebox.showerror("Error", str(e))
    except Exception as e:
        logger.critical(f"Unexpected error: {e}")
        raise
```

## Testing Strategy

### Unit Tests

Test individual components in isolation:

```python
class TestProfile(unittest.TestCase):
    def test_valid_profile_creation(self):
        profile = Profile(name="Test", username="Steve", ram=4)
        self.assertEqual(profile.name, "Test")
    
    def test_invalid_profile(self):
        with self.assertRaises(InvalidProfileError):
            Profile(name="", username="Steve", ram=4)
```

### Integration Tests

Test component interactions:

```python
class TestProfileService(unittest.TestCase):
    def setUp(self):
        self.repo = JsonProfileRepository(temp_path)
        self.service = ProfileService(self.repo)
    
    def test_create_and_retrieve(self):
        profile = self.service.create_profile("Test", "Steve", 4)
        retrieved = self.service.get_profile("Test")
        self.assertEqual(retrieved.username, "Steve")
```

### Test Coverage

Target: >80% code coverage
Tools: pytest, coverage.py

```bash
pytest tests/ --cov=src --cov-report=html
```

## Data Flow

### Profile Creation Flow

```
UI Input
    │
    ├─ NewProfileDialog._create_profile()
    │
    ├─ ProfileService.create_profile()
    │   ├─ Validation
    │   ├─ Profile object creation
    │   ├─ Storage in memory
    │   └─ Persistence to repository
    │
    ├─ JsonProfileRepository.save()
    │   └─ Write to profiles.json
    │
    └─ UI Refresh
        └─ Update profile list
```

### Game Launch Flow

```
UI: Click Play
    │
    ├─ MainWindow._launch_game()
    │   ├─ Get selected profile
    │   ├─ Get selected version
    │   └─ Get optional overrides
    │
    ├─ MinecraftLauncher.launch()
    │   ├─ Verify prerequisites
    │   ├─ Build launch options
    │   ├─ Get launcher command
    │   └─ Execute process
    │
    └─ Game Running
        ├─ Callback on close
        └─ Update UI status
```

## Performance Considerations

1. **Profile Loading**: Lazy load only when needed
2. **Version Caching**: Cache installed versions
3. **API Calls**: Implement request caching for mod search
4. **UI Updates**: Use threading for long operations

## Security Considerations

1. **Input Validation**: All user inputs validated
2. **File Permissions**: Store user data with proper permissions
3. **Error Messages**: Don't expose sensitive paths in errors
4. **Logging**: Don't log sensitive information

## Future Extensions

The architecture supports:

1. **Different Backends**:
   - `SqliteProfileRepository`
   - `CloudProfileRepository`

2. **Plugin System**:
   - Custom modloaders
   - Custom profile types

3. **Multiple UI Implementations**:
   - Web UI (Flask/Django)
   - CLI interface
   - PyQt instead of Tkinter

4. **Additional Features**:
   - Profile backups
   - Team collaboration
   - Advanced mod management

## Conclusion

FreeLauncher's architecture prioritizes:

- **Maintainability**: Clean code, separation of concerns
- **Testability**: Easy to write tests
- **Extensibility**: Easy to add new features
- **Reliability**: Proper error handling, logging
- **Performance**: Efficient data access

This foundation makes FreeLauncher a solid platform for future development!
