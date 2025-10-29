```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0/).

## [1.0.8] - 2025-10-29

### Changed
- Bumped package version to 1.0.8.
- CLI configuration lookup now prefers a local `grid_token` file and falls back to `~/.grid_token` in the user's home directory when no explicit `--config-file` is provided. Command-line options still override config files.

### Fixed
- Ensure token authentication exposes a standard `Authorization: Token <token>` header while preserving legacy `X-API-Key` header for backward compatibility.
- Fixed test expectations for token auth; updated tests now pass.

### Docs
- Updated `README.md` and `INSTALLATION.md` to document the new config-file fallback behavior.

## [1.0.0] - 2024-01-XX

### Added
- Initial release of GridAPI Python client library
- Comprehensive support for all Grid API endpoints
- Type-safe Pydantic models for all data structures
- Intuitive resource managers with nested resource support
- Advanced querying and filtering capabilities
- Command-line interface (CLI) with configuration file support
- Robust authentication handling (token and session-based)
- Comprehensive error handling with custom exceptions
- Pagination support for large datasets
- Rich documentation and examples
- Unit tests and integration tests
- Support for Python 3.8+

### Features
- **Grid API**: Studies, Datatypes, Subjects, Events, Procedures, Contacts
- **Image API**: Acquisitions, Actions, ActionTypes, Destinations, RawData, ScannerTypes
- **Taskflow API**: Measures, Participants
- **CLI Tools**: Full command-line interface with `grid_token` configuration file
- **Query Builder**: Advanced filtering, searching, and pagination
- **Type Safety**: Full Pydantic model validation and type hints
- **Error Handling**: Comprehensive exception handling with detailed error messages

### Technical Details
- Built with modern Python packaging (pyproject.toml)
- Uses requests for HTTP communication
- Pydantic for data validation and serialization
- Click and Rich for CLI interface
- Comprehensive test suite with pytest
- Type checking with mypy
- Code formatting with black and isort

```
