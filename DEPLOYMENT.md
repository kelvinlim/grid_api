# GridAPI CLI Deployment Guide

This guide explains how to deploy GridAPI CLI executables through GitHub releases, providing users with easy access to pre-built executables for Windows, macOS, and Linux.

## Overview

The deployment system consists of:
- **GitHub Actions**: Automated builds for all platforms
- **Release Management**: Automated release creation and asset management
- **Local Tools**: Scripts for local testing and manual releases

## Quick Start

### 1. Automated Release (Recommended)
```bash
# Create a version tag
git tag v1.0.0
git push origin v1.0.0

# GitHub Actions will automatically:
# - Build executables for Windows, macOS, and Linux
# - Create a GitHub release with downloadable assets
# - Generate checksums for verification
```

### 2. Manual Release
```bash
# Build and create release locally
python release_script.py --version 1.0.0 --create-release
```

## Deployment Methods

### Method 1: GitHub Actions (Automated)

#### Prerequisites
- GitHub repository with Actions enabled
- Proper repository permissions for releases

#### Process
1. **Create Version Tag**:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **GitHub Actions Workflow**:
   - Automatically triggered on version tags
   - Builds executables for Windows, macOS, and Linux
   - Creates GitHub release with assets
   - Generates checksums for verification

3. **Release Assets**:
   - `gridapi-windows.exe` - Windows executable
   - `gridapi-macos` - macOS executable  
   - `gridapi-linux` - Linux executable
   - `checksums.txt` - SHA256 checksums

#### Workflow Configuration
The workflow is configured in `.github/workflows/build-release.yml`:

```yaml
on:
  push:
    tags:
      - 'v*'  # Trigger on version tags
  workflow_dispatch:  # Manual triggering
```

### Method 2: Local Release Management

#### Prerequisites
- Python 3.8+
- GitHub CLI (`gh`) installed and authenticated
- All build dependencies installed

#### Installation
```bash
# Install GitHub CLI
# Windows: winget install GitHub.cli
# macOS: brew install gh
# Linux: apt install gh

# Authenticate
gh auth login
```

#### Commands
```bash
# Build executables locally
python release_script.py --version 1.0.0 --build-only

# Create GitHub release
python release_script.py --version 1.0.0 --create-release

# List existing releases
python release_script.py --list-releases

# Create draft release
python release_script.py --version 1.0.0 --create-release --draft
```

### Method 3: Manual GitHub Release

#### Process
1. **Build Executables**:
   ```bash
   python build_script.py --exe
   python build_script.py --prepare-release
   ```

2. **Create Release on GitHub**:
   - Go to GitHub repository → Releases → Create a new release
   - Tag: `v1.0.0`
   - Title: `GridAPI CLI v1.0.0`
   - Upload executables from `release-assets/` directory

## Release Assets

### Executable Files
- **Windows**: `gridapi-windows.exe` (~15-20 MB)
- **macOS**: `gridapi-macos` (~15-20 MB)
- **Linux**: `gridapi-linux` (~15-20 MB)

### Verification Files
- **checksums.txt**: SHA256 checksums for all executables
- **RELEASE_NOTES.md**: Release notes and installation instructions

### File Structure
```
release-assets/
├── gridapi-windows.exe
├── gridapi-macos
├── gridapi-linux
└── checksums.txt
```

## User Installation

### Download
Users can download executables from:
- GitHub Releases page: `https://github.com/username/gridapi/releases`
- Direct download links for each platform

### Installation Steps
1. **Download**: Get the appropriate executable for your platform
2. **Make Executable** (Linux/macOS):
   ```bash
   chmod +x gridapi-macos
   chmod +x gridapi-linux
   ```
3. **Verify** (Optional):
   ```bash
   sha256sum -c checksums.txt
   ```
4. **Configure**: Create `grid_token` file:
   ```
   grid_token=your-api-token-here
   base_url=https://your-api-url.com
   ```
5. **Run**:
   ```bash
   # Windows
   gridapi-windows.exe studies list
   
   # macOS/Linux
   ./gridapi-macos studies list
   ./gridapi-linux studies list
   ```

## Release Management

### Versioning
- Use semantic versioning: `v1.0.0`, `v1.1.0`, `v2.0.0`
- Pre-release versions: `v1.0.0-alpha.1`, `v1.0.0-beta.1`

### Release Types
- **Stable**: Full releases with all features
- **Pre-release**: Alpha/beta versions for testing
- **Draft**: Work-in-progress releases

### Release Notes
Automatically generated from `RELEASE_NOTES.md` template:
- What's new in this version
- Installation instructions
- Platform requirements
- Verification steps

## Troubleshooting

### Common Issues

#### 1. GitHub Actions Not Triggering
- Ensure the tag starts with `v` (e.g., `v1.0.0`)
- Check repository Actions permissions
- Verify workflow file is in `.github/workflows/`

#### 2. Build Failures
- Check Python version compatibility
- Ensure all dependencies are installed
- Review build logs in GitHub Actions

#### 3. Release Creation Fails
- Verify GitHub CLI authentication: `gh auth status`
- Check repository permissions for releases
- Ensure tag doesn't already exist

#### 4. Executable Not Working
- Verify platform compatibility
- Check file permissions (Linux/macOS)
- Test with `--help` flag first

### Debug Commands
```bash
# Check GitHub CLI status
gh auth status

# List releases
gh release list

# View release details
gh release view v1.0.0

# Download release assets
gh release download v1.0.0
```

## Advanced Configuration

### Custom Workflow Triggers
Modify `.github/workflows/build-release.yml`:

```yaml
on:
  push:
    tags: ['v*']
  schedule:
    - cron: '0 0 * * 0'  # Weekly builds
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to release'
        required: true
```

### Release Channels
Set up different release channels:

```yaml
# Stable releases
on:
  push:
    tags: ['v*']

# Pre-release builds
on:
  push:
    branches: ['develop']
```

### Asset Customization
Modify release asset preparation in the workflow:

```yaml
- name: Prepare release assets
  run: |
    mkdir -p release-assets
    cp artifacts/gridapi-windows/gridapi.exe release-assets/gridapi-windows.exe
    cp artifacts/gridapi-macos/gridapi release-assets/gridapi-macos
    cp artifacts/gridapi-linux/gridapi release-assets/gridapi-linux
    
    # Add additional assets
    cp README.md release-assets/
    cp LICENSE release-assets/
```

## Security Considerations

### Code Signing
For production releases, consider code signing:

#### Windows
- Use Authenticode signing
- Obtain code signing certificate
- Sign executables before release

#### macOS
- Use Apple Developer certificate
- Enable notarization
- Sign and notarize executables

#### Linux
- Use GPG signing
- Sign checksums file
- Provide signature verification

### Verification
- Always provide checksums
- Use SHA256 for integrity verification
- Consider GPG signatures for authenticity

## Monitoring and Analytics

### Release Metrics
- Download counts per platform
- Release adoption rates
- User feedback and issues

### GitHub Insights
- Release page views
- Asset download statistics
- User engagement metrics

## Best Practices

### Release Frequency
- **Major releases**: Every 6-12 months
- **Minor releases**: Every 1-3 months
- **Patch releases**: As needed for bug fixes

### Quality Assurance
- Test executables on target platforms
- Verify all CLI commands work
- Check file permissions and compatibility

### Documentation
- Update release notes for each version
- Maintain installation instructions
- Provide troubleshooting guides

### Communication
- Announce releases on project channels
- Update project documentation
- Notify users of breaking changes

## Integration with CI/CD

### Automated Testing
```yaml
- name: Test executable
  run: |
    ./dist/gridapi --help
    ./dist/gridapi config
    ./dist/gridapi studies list
```

### Quality Gates
- Require all tests to pass
- Verify executable functionality
- Check file sizes and permissions

### Deployment Pipeline
1. **Build**: Create executables
2. **Test**: Verify functionality
3. **Package**: Prepare release assets
4. **Release**: Create GitHub release
5. **Notify**: Announce to users
