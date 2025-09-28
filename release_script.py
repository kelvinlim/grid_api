#!/usr/bin/env python3
"""
GridAPI Release Management Script

This script helps manage releases by:
1. Building executables for all platforms locally
2. Creating GitHub releases
3. Managing version tags
4. Preparing release assets

Usage:
    python release_script.py --version 1.0.0 --create-release
    python release_script.py --version 1.0.0 --build-only
    python release_script.py --list-releases
"""

import argparse
import subprocess
import sys
import os
import json
from pathlib import Path
from typing import List, Dict, Optional


def run_command(cmd: str, description: str = "") -> bool:
    """Run a command and return success status."""
    if description:
        print(f"🔄 {description}...")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if description:
            print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False


def get_current_version() -> str:
    """Get current version from pyproject.toml."""
    try:
        with open("pyproject.toml", "r") as f:
            content = f.read()
            for line in content.split("\n"):
                if line.strip().startswith("version ="):
                    return line.split("=")[1].strip().strip('"')
    except Exception:
        pass
    return "1.0.0"


def update_version(version: str) -> bool:
    """Update version in pyproject.toml."""
    try:
        with open("pyproject.toml", "r") as f:
            content = f.read()
        
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.strip().startswith("version ="):
                lines[i] = f'version = "{version}"'
                break
        
        with open("pyproject.toml", "w") as f:
            f.write("\n".join(lines))
        
        print(f"✅ Updated version to {version}")
        return True
    except Exception as e:
        print(f"❌ Failed to update version: {e}")
        return False


def build_all_platforms() -> bool:
    """Build executables for all platforms locally."""
    print("\n🌍 Building executables for all platforms...")
    
    # Check if we're on a supported platform
    import platform
    current_platform = platform.system().lower()
    
    if current_platform not in ['windows', 'darwin', 'linux']:
        print(f"❌ Unsupported platform: {current_platform}")
        return False
    
    platform_names = {
        'windows': 'Windows',
        'darwin': 'macOS', 
        'linux': 'Linux'
    }
    
    print(f"   Building for {platform_names[current_platform]}...")
    
    # Build executable
    if not run_command("python build_script.py --exe", f"Building {platform_names[current_platform]} executable"):
        return False
    
    # Test executable
    exe_name = "gridapi.exe" if current_platform == "windows" else "gridapi"
    exe_path = Path(f"dist/{exe_name}")
    
    if exe_path.exists():
        print(f"✅ Executable created: {exe_path}")
        print(f"   Size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
        
        # Test the executable
        test_cmd = f"dist\\{exe_name} --help" if current_platform == "windows" else f"./dist/{exe_name} --help"
        if run_command(test_cmd, "Testing executable"):
            print(f"✅ {platform_names[current_platform]} build completed successfully")
            return True
        else:
            print(f"❌ {platform_names[current_platform]} executable test failed")
            return False
    else:
        print(f"❌ Executable not found: {exe_path}")
        return False


def create_git_tag(version: str) -> bool:
    """Create and push a git tag."""
    tag_name = f"v{version}"
    
    print(f"\n🏷️  Creating git tag: {tag_name}")
    
    # Check if tag already exists
    try:
        result = subprocess.run(f"git tag -l {tag_name}", shell=True, capture_output=True, text=True)
        if tag_name in result.stdout:
            print(f"⚠️  Tag {tag_name} already exists")
            return True
    except Exception:
        pass
    
    # Create tag
    if not run_command(f"git tag -a {tag_name} -m 'Release {tag_name}'", f"Creating tag {tag_name}"):
        return False
    
    # Push tag
    if not run_command(f"git push origin {tag_name}", f"Pushing tag {tag_name}"):
        return False
    
    print(f"✅ Tag {tag_name} created and pushed")
    return True


def create_github_release(version: str, draft: bool = True) -> bool:
    """Create a GitHub release using GitHub CLI."""
    tag_name = f"v{version}"
    
    print(f"\n🚀 Creating GitHub release: {tag_name}")
    
    # Check if GitHub CLI is available
    try:
        subprocess.run("gh --version", shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("❌ GitHub CLI (gh) not found. Install it from: https://cli.github.com/")
        return False
    
    # Check if we're authenticated
    try:
        subprocess.run("gh auth status", shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("❌ Not authenticated with GitHub CLI. Run: gh auth login")
        return False
    
    # Create release
    draft_flag = "--draft" if draft else ""
    cmd = f"gh release create {tag_name} {draft_flag} --title 'GridAPI CLI {tag_name}' --notes-file RELEASE_NOTES.md"
    
    if not run_command(cmd, f"Creating GitHub release {tag_name}"):
        return False
    
    print(f"✅ GitHub release {tag_name} created")
    return True


def list_releases() -> bool:
    """List existing releases."""
    print("\n📋 Existing releases:")
    
    try:
        result = subprocess.run("gh release list", shell=True, capture_output=True, text=True, check=True)
        if result.stdout.strip():
            print(result.stdout)
        else:
            print("   No releases found")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to list releases. Make sure GitHub CLI is installed and authenticated.")
        return False


def create_release_notes(version: str) -> bool:
    """Create release notes template."""
    notes_file = Path("RELEASE_NOTES.md")
    
    notes_content = f"""# GridAPI CLI {version}

## What's New
- Cross-platform standalone executables
- No Python installation required
- Full CLI functionality included

## Downloads
- **Windows**: `gridapi-windows.exe` (requires Windows 7+)
- **macOS**: `gridapi-macos` (requires macOS 10.13+)
- **Linux**: `gridapi-linux` (requires glibc 2.17+)

## Installation
1. Download the appropriate executable for your platform
2. Make it executable (Linux/macOS): `chmod +x gridapi-*`
3. Create a `grid_token` file with your API credentials:
   ```
   grid_token=your-api-token-here
   base_url=https://your-api-url.com
   ```
4. Run: `./gridapi-* studies list` (or `gridapi-windows.exe studies list` on Windows)

## Verification
Verify your download using the provided checksums:
```bash
sha256sum -c checksums.txt
```

## Changes
- Initial release with cross-platform executable support
- Full CLI functionality
- Comprehensive documentation
"""
    
    try:
        with open(notes_file, "w") as f:
            f.write(notes_content)
        print(f"✅ Created release notes: {notes_file}")
        return True
    except Exception as e:
        print(f"❌ Failed to create release notes: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="GridAPI Release Management")
    parser.add_argument("--version", help="Version to release (e.g., 1.0.0)")
    parser.add_argument("--build-only", action="store_true", help="Only build executables locally")
    parser.add_argument("--create-release", action="store_true", help="Create GitHub release")
    parser.add_argument("--create-tag", action="store_true", help="Create and push git tag")
    parser.add_argument("--list-releases", action="store_true", help="List existing releases")
    parser.add_argument("--draft", action="store_true", help="Create draft release")
    
    args = parser.parse_args()
    
    if args.list_releases:
        return list_releases()
    
    if not args.version:
        current_version = get_current_version()
        print(f"Current version: {current_version}")
        print("Use --version to specify a different version")
        return True
    
    version = args.version
    
    print(f"🚀 GridAPI Release Management - Version {version}")
    print("=" * 50)
    
    # Update version in pyproject.toml
    if not update_version(version):
        return False
    
    # Build executables
    if not build_all_platforms():
        return False
    
    if args.build_only:
        print("\n✅ Build completed. Use --create-release to create a GitHub release.")
        return True
    
    # Create release notes
    if not create_release_notes(version):
        return False
    
    # Create git tag
    if args.create_tag or args.create_release:
        if not create_git_tag(version):
            return False
    
    # Create GitHub release
    if args.create_release:
        if not create_github_release(version, draft=args.draft):
            return False
    
    print(f"\n🎉 Release {version} completed successfully!")
    print("\nNext steps:")
    print("1. GitHub Actions will automatically build executables for all platforms")
    print("2. The release will be created with downloadable executables")
    print("3. Users can download executables from the GitHub releases page")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
