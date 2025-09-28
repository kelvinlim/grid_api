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
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e}")
        if e.stdout:
            print(f"Stdout: {e.stdout}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        return False


def clean_build():
    """Clean build artifacts."""
    print("\n🧹 Cleaning build artifacts...")
    
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
    
    print("✅ Clean completed")


def check_requirements():
    """Check if required tools are installed."""
    print("\n🔍 Checking requirements...")
    
    required_tools = ["python", "pip", "twine"]
    missing_tools = []
    
    for tool in required_tools:
        try:
            subprocess.run([tool, "--version"], capture_output=True, check=True)
            print(f"  ✅ {tool} is available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"  ❌ {tool} is missing")
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"\n❌ Missing required tools: {', '.join(missing_tools)}")
        print("Please install them before building:")
        print("  pip install twine build")
        return False
    
    return True


def build_package():
    """Build the package."""
    print("\n📦 Building package...")
    
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
        
        print("✅ Package test completed successfully")
        return True
        
    finally:
        # Clean up test directory
        if test_dir.exists():
            shutil.rmtree(test_dir)


def publish_package(test_pypi=False):
    """Publish the package to PyPI."""
    print("\n🚀 Publishing package...")
    
    if test_pypi:
        print("  Publishing to Test PyPI...")
        upload_cmd = "twine upload --repository testpypi dist/*"
    else:
        print("  Publishing to PyPI...")
        upload_cmd = "twine upload dist/*"
    
    if not run_command(upload_cmd, "Uploading package"):
        return False
    
    print("✅ Package published successfully")
    return True


def main():
    """Main build and publish workflow."""
    print("🚀 GridAPI Package Build and Publish Script")
    print("=" * 50)
    
    # Parse command line arguments
    clean_only = "--clean" in sys.argv
    build_only = "--build" in sys.argv
    test_only = "--test" in sys.argv
    publish_test = "--test-pypi" in sys.argv
    publish_prod = "--publish" in sys.argv
    
    # Clean build artifacts
    clean_build()
    
    if clean_only:
        print("\n✅ Clean completed. Exiting.")
        return
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Build package
    if build_only or not (test_only or publish_test or publish_prod):
        if not build_package():
            sys.exit(1)
    
    if build_only:
        print("\n✅ Build completed. Exiting.")
        return
    
    # Test package
    if test_only or not (publish_test or publish_prod):
        if not test_package():
            sys.exit(1)
    
    if test_only:
        print("\n✅ Test completed. Exiting.")
        return
    
    # Publish package
    if publish_test:
        if not publish_package(test_pypi=True):
            sys.exit(1)
        print("\n✅ Package published to Test PyPI")
    elif publish_prod:
        if not publish_package(test_pypi=False):
            sys.exit(1)
        print("\n✅ Package published to PyPI")
    
    print("\n🎉 All operations completed successfully!")


if __name__ == "__main__":
    main()
