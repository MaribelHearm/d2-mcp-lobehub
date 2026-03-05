# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-03-05

### Added
- Initial release
- D2 MCP server implementation
- SVG to PNG conversion using rsvg-convert
- Nginx static file serving configuration
- Docker Compose deployment
- Complete documentation (installation, architecture)
- MIT License

### Features
- Support for all D2 layouts (elk, tala, dagre)
- Support for D2 themes (0-200)
- Automatic PNG generation and URL return
- 7-day browser caching
- High-resolution output (2400px width)
- CORS support

### Technical Details
- Python 3.11
- Starlette + Uvicorn
- D2 CLI integration
- rsvg-convert for SVG rendering
- Docker containerization
