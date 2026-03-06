#!/usr/bin/env python3
"""
Build script for FreeLauncher
Prepares release artifacts: ZIP, TAR.GZ, wheels
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def run_command(cmd, shell=False):
    """Run a command and return exit code"""
    try:
        result = subprocess.run(cmd, shell=shell, check=True, capture_output=True, text=True)
        print(result.stdout)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}", file=sys.stderr)
        return e.returncode

def get_version():
    """Get version from setup.py or git"""
    try:
        result = subprocess.run(['python', 'setup.py', '--version'], 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except:
        return datetime.now().strftime("%Y.%m.%d")

def build_distributions():
    """Build wheel and sdist"""
    print("📦 Building Python distributions...")
    run_command(['python', '-m', 'pip', 'install', 'wheel', 'build', '-q'])
    run_command(['python', '-m', 'build'])
    print("✅ Distributions built\n")

def create_source_archive(version):
    """Create source code archives"""
    print("📦 Creating source archives...")
    
    dist_dir = Path('dist')
    dist_dir.mkdir(exist_ok=True)
    
    archive_name = f"freelauncher-{version}"
    archive_dir = dist_dir / archive_name
    
    # Copy files
    if archive_dir.exists():
        shutil.rmtree(archive_dir)
    archive_dir.mkdir(parents=True)
    
    files_to_copy = ['src', 'main.py', 'requirements.txt', 'requirements-dev.txt',
                     'docker-compose.yml', 'Dockerfile', 'README.md', 'LICENSE',
                     'setup.py', 'pyproject.toml', 'pytest.ini', 'scripts']
    
    for file_item in files_to_copy:
        src = Path(file_item)
        if src.exists():
            dst = archive_dir / file_item
            if src.is_dir():
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
    
    # Create ZIP
    shutil.make_archive(str(dist_dir / archive_name), 'zip', dist_dir, archive_name)
    print(f"  ✅ {archive_name}.zip")
    
    # Create TAR.GZ
    shutil.make_archive(str(dist_dir / archive_name), 'gztar', dist_dir, archive_name)
    print(f"  ✅ {archive_name}.tar.gz")
    
    # Cleanup
    shutil.rmtree(archive_dir)
    print("✅ Source archives created\n")

def build_docker_image(version):
    """Build Docker image"""
    print("🐳 Building Docker image...")
    tags = [f"freelauncher:{version}", "freelauncher:latest"]
    tag_args = ' '.join([f'-t {tag}' for tag in tags])
    
    cmd = f'docker build {tag_args} .'
    if run_command(cmd, shell=True) == 0:
        print(f"✅ Docker image built: {', '.join(tags)}\n")
        return True
    return False

def run_tests():
    """Run tests"""
    print("🧪 Running tests...")
    run_command(['pytest', 'tests/', '-v', '--tb=short'])
    print("✅ Tests completed\n")

def run_linting():
    """Run linting checks"""
    print("🔍 Running linting...")
    
    run_command(['flake8', 'src/', 'main.py', '--count', '--select=E9,F63,F7,F82',
                '--show-source', '--statistics'])
    
    print("✅ Linting completed\n")

def main():
    """Main build process"""
    print("🎮 FreeLauncher Build System")
    print("=" * 50)
    print()
    
    # Get version
    version = get_version()
    print(f"📌 Version: {version}\n")
    
    # Parse arguments
    build_all = '--all' in sys.argv
    skip_tests = '--skip-tests' in sys.argv
    skip_lint = '--skip-lint' in sys.argv
    skip_docker = '--skip-docker' in sys.argv
    dist_only = '--dist' in sys.argv
    
    try:
        # Run checks unless skipped
        if not skip_lint:
            run_linting()
        
        if not skip_tests:
            run_tests()
        
        # Build distributions
        if build_all or dist_only or not skip_tests:
            build_distributions()
            create_source_archive(version)
        
        # Build Docker image
        if (build_all or not skip_docker) and not dist_only:
            if not build_docker_image(version):
                print("⚠️  Docker image build failed (Docker may not be installed)\n")
        
        # Summary
        print("=" * 50)
        print("✨ Build completed successfully!")
        print()
        print("📦 Artifacts in: dist/")
        print("   - freelauncher-*.whl (Python wheel)")
        print("   - freelauncher-*.tar.gz (Source)") 
        print("   - freelauncher-*.zip (Source)")
        print()
        
        if not skip_docker:
            print("🐳 Docker images:")
            print(f"   - freelauncher:{version}")
            print("   - freelauncher:latest")
            print()
        
        print("Next steps:")
        print("1. git tag v{version}")
        print("2. git push origin v{version}")
        print("3. GitHub Actions will create a release")
        print()
        
    except KeyboardInterrupt:
        print("\n❌ Build cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Build failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
