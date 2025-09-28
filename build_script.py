#!/usr/bin/env python3
"""
Build and publish script for GridAPI package.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n[RUNNING] {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"[SUCCESS] {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {description} failed")
        print(f"Error: {e}")
        if e.stdout:
            print(f"Stdout: {e.stdout}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        return False


def clean_build():
    """Clean build artifacts."""
    print("\n[CLEAN] Cleaning build artifacts...")
    
    # Remove build directories
    dirs_to_remove = ["build", "dist", "*.egg-info"]
    for pattern in dirs_to_remove:
        for path in Path(".").glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"  Removed {path}")
    
    # Remove Python cache
    for path in Path(".").rglob("__pycache__"):
        if path.is_dir():
            shutil.rmtree(path)
            print(f"  Removed {path}")
    
    print("[SUCCESS] Clean completed")


def check_requirements():
    """Check if required tools are installed."""
    print("\n[CHECK] Checking requirements...")
    
    required_tools = ["python", "pip", "twine"]
    optional_tools = ["pyinstaller"]
    missing_tools = []
    missing_optional = []
    
    for tool in required_tools:
        try:
            subprocess.run([tool, "--version"], capture_output=True, check=True)
            print(f"  [SUCCESS] {tool} is available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"  [ERROR] {tool} is missing")
            missing_tools.append(tool)
    
    for tool in optional_tools:
        try:
            subprocess.run([tool, "--version"], capture_output=True, check=True)
            print(f"  [SUCCESS] {tool} is available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"  [WARNING]  {tool} is missing (optional for executables)")
            missing_optional.append(tool)
    
    if missing_tools:
        print(f"\n[ERROR] Missing required tools: {', '.join(missing_tools)}")
        print("Please install them before building:")
        print("  pip install twine build")
        return False
    
    if missing_optional:
        print(f"\n[WARNING]  Missing optional tools: {', '.join(missing_optional)}")
        print("Install them to create standalone executables:")
        print("  pip install pyinstaller")
    
    return True


def build_package():
    """Build the package."""
    print("\n[BUILD] Building package...")
    
    # Build source distribution and wheel
    if not run_command("python -m build", "Building source distribution and wheel"):
        return False
    
    # Check the built package
    if not run_command("twine check dist/*", "Checking built package"):
        return False
    
    return True


def test_package():
    """Test the package installation."""
    print("\n🧪 Testing package installation...")
    
    # Create a temporary virtual environment for testing
    test_dir = Path("test_install")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    
    test_dir.mkdir()
    
    try:
        # Install the package in test mode
        if not run_command(f"cd {test_dir} && python -m venv venv", "Creating test virtual environment"):
            return False
        
        # Activate venv and install
        if os.name == 'nt':  # Windows
            activate_cmd = f"{test_dir}/venv/Scripts/activate"
            pip_cmd = f"{test_dir}/venv/Scripts/pip"
        else:  # Unix/Linux/macOS
            activate_cmd = f"source {test_dir}/venv/bin/activate"
            pip_cmd = f"{test_dir}/venv/bin/pip"
        
        # Install the package
        install_cmd = f"{pip_cmd} install ../dist/*.whl"
        if not run_command(install_cmd, "Installing package in test environment"):
            return False
        
        # Test import
        test_import_cmd = f"{pip_cmd} run python -c \"import gridapi; print('GridAPI imported successfully')\""
        if not run_command(test_import_cmd, "Testing package import"):
            return False
        
        print("[SUCCESS] Package test completed successfully")
        return True
        
    finally:
        # Clean up test directory
        if test_dir.exists():
            shutil.rmtree(test_dir)


def get_platform_info():
    """Get platform information."""
    import platform
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == 'windows':
        return 'windows', '.exe'
    elif system == 'darwin':
        return 'macos', ''
    elif system == 'linux':
        return 'linux', ''
    else:
        return 'unknown', ''

def build_executable():
    """Build standalone executable using PyInstaller."""
    print("\n[EXECUTABLE] Building standalone executable...")
    
    # Get platform information
    platform_name, ext = get_platform_info()
    print(f"   Platform: {platform_name}")
    
    # Check if PyInstaller is available
    try:
        subprocess.run(["pyinstaller", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[ERROR] PyInstaller not found. Install it with: pip install pyinstaller")
        return False
    
    # Choose the appropriate spec file
    spec_file = f"gridapi-{platform_name}.spec"
    if not Path(spec_file).exists():
        spec_file = "gridapi.spec"  # Fallback to generic spec
        print(f"   Using generic spec file: {spec_file}")
    else:
        print(f"   Using platform-specific spec file: {spec_file}")
    
    # Build the executable
    if not run_command(f"pyinstaller {spec_file} --clean", "Building standalone executable"):
        return False
    
    # Check if executable was created
    exe_name = f"gridapi{ext}" if ext else "gridapi"
    exe_path = Path(f"dist/{exe_name}")
    
    # Debug: List contents of dist directory
    print(f"   Debug: Contents of dist directory:")
    dist_dir = Path("dist")
    if dist_dir.exists():
        for item in dist_dir.iterdir():
            print(f"     - {item.name}")
    else:
        print("     - dist directory does not exist")
    
    print(f"   Debug: Looking for executable: {exe_path}")
    
    if exe_path.exists():
        print(f"[SUCCESS] Executable created: {exe_path}")
        print(f"   Platform: {platform_name}")
        print(f"   Size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
        
        # Test the executable
        print(f"   Testing executable...")
        try:
            result = subprocess.run([str(exe_path), "--help"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"   [SUCCESS] Executable test passed")
            else:
                print(f"   [WARNING]  Executable test failed (return code: {result.returncode})")
        except subprocess.TimeoutExpired:
            print(f"   [WARNING]  Executable test timed out")
        except Exception as e:
            print(f"   [WARNING]  Executable test error: {e}")
        
        return True
    else:
        print("[ERROR] Executable not found after build")
        return False


def build_all_platforms():
    """Build executables for all supported platforms."""
    print("\n[PLATFORMS] Building executables for all platforms...")
    
    # Get current platform
    current_platform, _ = get_platform_info()
    print(f"   Current platform: {current_platform}")
    
    # Build for current platform
    print(f"\n[BUILD] Building for {current_platform}...")
    if build_executable():
        print(f"[SUCCESS] {current_platform} build completed")
    else:
        print(f"[ERROR] {current_platform} build failed")
        return False
    
    # Note about cross-platform building
    print(f"\n💡 Cross-platform building notes:")
    print(f"   - Executables are built for the current platform only")
    print(f"   - For Windows executables: Build on Windows")
    print(f"   - For macOS executables: Build on macOS")
    print(f"   - For Linux executables: Build on Linux")
    print(f"   - Use CI/CD pipelines for automated multi-platform builds")
    
    return True


def prepare_release_assets():
    """Prepare release assets for GitHub release."""
    print("\n[BUILD] Preparing release assets...")
    
    # Get platform information
    platform_name, ext = get_platform_info()
    exe_name = f"gridapi{ext}" if ext else "gridapi"
    exe_path = Path(f"dist/{exe_name}")
    
    # Build executable if it doesn't exist
    if not exe_path.exists():
        print(f"   Executable not found: {exe_path}")
        print(f"   Building executable first...")
        if not build_executable():
            print(f"[ERROR] Failed to build executable")
            return False
    
    # Create release directory
    release_dir = Path("release-assets")
    release_dir.mkdir(exist_ok=True)
    
    # Copy executable with platform-specific name
    platform_exe_name = f"gridapi-{platform_name}{ext}" if ext else f"gridapi-{platform_name}"
    platform_exe_path = release_dir / platform_exe_name
    
    import shutil
    shutil.copy2(exe_path, platform_exe_path)
    
    print(f"[SUCCESS] Copied executable: {platform_exe_path}")
    print(f"   Size: {platform_exe_path.stat().st_size / (1024*1024):.1f} MB")
    
    # Create checksums
    checksum_file = release_dir / "checksums.txt"
    try:
        import hashlib
        
        with open(checksum_file, "w") as f:
            sha256_hash = hashlib.sha256()
            with open(platform_exe_path, "rb") as exe_file:
                for chunk in iter(lambda: exe_file.read(4096), b""):
                    sha256_hash.update(chunk)
            
            checksum = sha256_hash.hexdigest()
            f.write(f"{checksum}  {platform_exe_name}\n")
        
        print(f"[SUCCESS] Created checksums: {checksum_file}")
        
        # Show checksum
        with open(checksum_file, "r") as f:
            print(f"   Checksum: {f.read().strip()}")
        
    except Exception as e:
        print(f"[ERROR] Failed to create checksums: {e}")
        return False
    
    print(f"\n[INFO] Release assets prepared in: {release_dir}")
    print(f"   - {platform_exe_name}")
    print(f"   - checksums.txt")
    
    return True


def publish_package(test_pypi=False):
    """Publish the package to PyPI."""
    print("\n[RELEASE] Publishing package...")
    
    if test_pypi:
        print("  Publishing to Test PyPI...")
        upload_cmd = "twine upload --repository testpypi dist/*"
    else:
        print("  Publishing to PyPI...")
        upload_cmd = "twine upload dist/*"
    
    if not run_command(upload_cmd, "Uploading package"):
        return False
    
    print("[SUCCESS] Package published successfully")
    return True


def main():
    """Main build and publish workflow."""
    print("GridAPI Package Build and Publish Script")
    print("=" * 50)
    print("Note: This script has been renamed from build.py to build_script.py")
    print("to avoid conflicts with the Python 'build' module.")
    print("=" * 50)
    
    # Parse command line arguments
    clean_only = "--clean" in sys.argv
    build_only = "--build" in sys.argv
    build_exe = "--exe" in sys.argv
    build_all = "--all-platforms" in sys.argv
    prepare_release = "--prepare-release" in sys.argv
    test_only = "--test" in sys.argv
    publish_test = "--test-pypi" in sys.argv
    publish_prod = "--publish" in sys.argv
    
    # Clean build artifacts
    clean_build()
    
    if clean_only:
        print("\n[SUCCESS] Clean completed. Exiting.")
        return
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Build package
    if build_only or not (test_only or publish_test or publish_prod):
        if not build_package():
            sys.exit(1)
    
    if build_only:
        print("\n[SUCCESS] Build completed. Exiting.")
        return
    
    # Build executable
    if build_exe:
        if not build_executable():
            sys.exit(1)
        print("\n[SUCCESS] Executable build completed. Exiting.")
        return
    
    # Build for all platforms
    if build_all:
        if not build_all_platforms():
            sys.exit(1)
        print("\n[SUCCESS] Multi-platform build completed. Exiting.")
        return
    
    # Prepare release assets
    if prepare_release:
        if not prepare_release_assets():
            sys.exit(1)
        print("\n[SUCCESS] Release assets prepared. Exiting.")
        return
    
    # Test package
    if test_only or not (publish_test or publish_prod):
        if not test_package():
            sys.exit(1)
    
    if test_only:
        print("\n[SUCCESS] Test completed. Exiting.")
        return
    
    # Publish package
    if publish_test:
        if not publish_package(test_pypi=True):
            sys.exit(1)
        print("\n[SUCCESS] Package published to Test PyPI")
    elif publish_prod:
        if not publish_package(test_pypi=False):
            sys.exit(1)
        print("\n[SUCCESS] Package published to PyPI")
    
    print("\n[COMPLETE] All operations completed successfully!")
    print("\n[INFO] Available commands:")
    print("  python build_script.py --clean          # Clean build artifacts")
    print("  python build_script.py --build          # Build package only")
    print("  python build_script.py --exe            # Build standalone executable")
    print("  python build_script.py --all-platforms  # Build for all platforms")
    print("  python build_script.py --prepare-release # Prepare release assets")
    print("  python build_script.py --test           # Test package installation")
    print("  python build_script.py --test-pypi      # Publish to Test PyPI")
    print("  python build_script.py --publish        # Publish to PyPI")
    print("  python build_script.py                  # Full build, test, and publish")
    print("\n[RELEASE] Release Management:")
    print("  python release_script.py --version 1.0.0 --build-only")
    print("  python release_script.py --version 1.0.0 --create-release")
    print("  python release_script.py --list-releases")


if __name__ == "__main__":
    main()
