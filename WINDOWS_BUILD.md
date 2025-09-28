# Cross-Platform Executable Build Guide

This guide explains how to create standalone executables for the GridAPI CLI tool using PyInstaller on Windows, macOS, and Linux.

## Supported Platforms

- **Windows**: `gridapi.exe` (15-20 MB)
- **macOS**: `gridapi` (15-20 MB) 
- **Linux**: `gridapi` (15-20 MB)

## Prerequisites

### 1. Install Python
- Download and install Python 3.8+ from [python.org](https://www.python.org/downloads/)
- Ensure Python is added to your PATH

### 2. Install Required Tools
```bash
pip install pyinstaller build twine
```

### 3. Install Project Dependencies
```bash
pip install -e ".[dev]"
```

## Building the Executable

### Method 1: Using the Build Script (Recommended)
```bash
# Build for current platform
python build_script.py --exe

# Build for all platforms (current platform only)
python build_script.py --all-platforms
```

### Method 2: Direct PyInstaller Commands
```bash
# Generic build (auto-detects platform)
pyinstaller gridapi.spec --clean

# Platform-specific builds
pyinstaller gridapi-windows.spec --clean    # Windows
pyinstaller gridapi-macos.spec --clean      # macOS
pyinstaller gridapi-linux.spec --clean      # Linux
```

## Output

The executable will be created in the `dist/` directory:
- **Windows**: `dist/gridapi.exe`
- **macOS**: `dist/gridapi`
- **Linux**: `dist/gridapi`
- **Size**: Approximately 15-20 MB

## Testing the Executable

### 1. Basic Test
```bash
# Windows
dist\gridapi.exe --help

# macOS/Linux
./dist/gridapi --help
```

### 2. Configuration Test
```bash
# Windows
dist\gridapi.exe config

# macOS/Linux
./dist/gridapi config
```

### 3. API Test (requires grid_token file)
```bash
# Windows
dist\gridapi.exe studies list

# macOS/Linux
./dist/gridapi studies list
```

## Distribution

### For All Platforms
1. Copy the appropriate executable to the target machine:
   - **Windows**: `dist/gridapi.exe`
   - **macOS**: `dist/gridapi`
   - **Linux**: `dist/gridapi`

2. Create a `grid_token` file with API credentials:
   ```
   grid_token=your-api-token-here
   base_url=https://your-api-url.com
   ```

3. Run the executable from command line:
   ```bash
   # Windows
   gridapi.exe studies list
   
   # macOS/Linux
   ./gridapi studies list
   ```

### File Structure
```
dist/
├── gridapi.exe          # Windows executable
├── gridapi              # macOS/Linux executable
├── gridapi-1.0.0-py3-none-any.whl  # Python wheel
└── gridapi-1.0.0.tar.gz           # Source distribution
```

## Troubleshooting

### Common Issues

#### 1. "PyInstaller not found"
```cmd
pip install pyinstaller
```

#### 2. "Module not found" errors
- Ensure all dependencies are installed: `pip install -e ".[dev]"`
- Check that the project is properly installed in development mode

#### 3. Large executable size
- This is normal for PyInstaller executables
- The executable includes Python runtime and all dependencies
- Consider using `--onefile` option for single-file distribution

#### 4. Antivirus false positives
- Some antivirus software may flag PyInstaller executables
- This is a known issue with PyInstaller
- Add the executable to antivirus exclusions if needed

### Advanced Options

#### Custom Icon
Add an icon to the spec file:
```python
exe = EXE(
    # ... other options ...
    icon='path/to/icon.ico',
)
```

#### Console vs Windowed
For a GUI application (no console window):
```python
exe = EXE(
    # ... other options ...
    console=False,
)
```

#### Single File Distribution
Modify the spec file to create a single file:
```python
exe = EXE(
    # ... other options ...
    onefile=True,
)
```

## Cross-Platform Building

### Platform-Specific Considerations

#### Windows
- **Executable**: `gridapi.exe`
- **Requirements**: Windows 7+ (depending on Python version)
- **Dependencies**: Visual C++ Redistributable may be required

#### macOS
- **Executable**: `gridapi`
- **Requirements**: macOS 10.13+ (depending on Python version)
- **Code Signing**: Optional but recommended for distribution

#### Linux
- **Executable**: `gridapi`
- **Requirements**: glibc 2.17+ (most modern distributions)
- **Dependencies**: May require additional system libraries

### Automated Multi-Platform Builds

For automated builds across multiple platforms, consider using:

#### GitHub Actions
```yaml
name: Build Executables
on: [push, release]
jobs:
  build:
    strategy:
      matrix:
        os: [windows-latest, macos-latest, ubuntu-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install pyinstaller
      - run: python build_script.py --exe
      - uses: actions/upload-artifact@v3
        with:
          name: gridapi-${{ matrix.os }}
          path: dist/
```

## Build Script Options

The `build_script.py` provides several options:

```bash
python build_script.py --clean          # Clean build artifacts
python build_script.py --build          # Build package only
python build_script.py --exe            # Build standalone executable
python build_script.py --all-platforms  # Build for all platforms
python build_script.py --test           # Test package installation
python build_script.py --test-pypi      # Publish to Test PyPI
python build_script.py --publish        # Publish to PyPI
python build_script.py                  # Full build, test, and publish
```

## Performance Notes

- **Startup Time**: First run may be slower due to unpacking
- **Memory Usage**: Executable uses more memory than Python script
- **File Size**: ~15-20 MB due to included Python runtime
- **Compatibility**: Works on Windows 7+ (depending on Python version)

## Security Considerations

- The executable contains your API credentials if embedded
- Use external configuration files for sensitive data
- Consider code signing for production distribution
- Test thoroughly before distributing to end users
