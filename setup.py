"""
Development setup and build scripts
"""
import os
import sys
import subprocess
from pathlib import Path


def install_dev_dependencies():
    """Install development dependencies"""
    print("Installing development dependencies...")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
    ])
    subprocess.check_call([
        sys.executable, "-m", "pip", "install",
        "pytest", "pytest-cov", "black", "flake8", "mypy"
    ])
    print("✅ Dependencies installed")


def run_tests():
    """Run unit tests"""
    print("Running tests...")
    result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v", "--cov=src"])
    return result.returncode == 0


def format_code():
    """Format code with black"""
    print("Formatting code...")
    subprocess.check_call([sys.executable, "-m", "black", "src/"])
    print("✅ Code formatted")


def lint_code():
    """Lint code with flake8"""
    print("Linting code...")
    result = subprocess.run([sys.executable, "-m", "flake8", "src/"])
    return result.returncode == 0


def type_check():
    """Type check with mypy"""
    print("Type checking...")
    result = subprocess.run([sys.executable, "-m", "mypy", "src/"])
    return result.returncode == 0


def build_executable():
    """Build standalone executable"""
    print("Building executable...")
    subprocess.check_call([
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "FreeLauncher",
        "--icon", "icon.ico" if Path("icon.ico").exists() else None,
        "main.py"
    ])
    print("✅ Executable built in dist/")


def all_checks():
    """Run all development checks"""
    print("🔍 Running all checks...\n")
    
    if not run_tests():
        print("❌ Tests failed")
        return False
    
    if not lint_code():
        print("⚠️  Linting issues found")
    
    if not type_check():
        print("⚠️  Type checking issues found")
    
    print("\n✅ All checks completed!")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python setup.py [install|test|format|lint|typecheck|build|all]")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "install":
        install_dev_dependencies()
    elif command == "test":
        success = run_tests()
        sys.exit(0 if success else 1)
    elif command == "format":
        format_code()
    elif command == "lint":
        success = lint_code()
        sys.exit(0 if success else 1)
    elif command == "typecheck":
        success = type_check()
        sys.exit(0 if success else 1)
    elif command == "build":
        build_executable()
    elif command == "all":
        all_checks()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
