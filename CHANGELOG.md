# 📝 Changelog

## v1.4.0 (2025-10-23)

**New Features:**

- ⭐ **MF Save Data** - Save data in JSON, XML, CSV, or YAML format
- ⭐ **MF Read Data** - Read data from multiple file formats
- ⭐ **MF Show Data** - Display data with auto-sizing text widget

**Technical:**

- Added PyYAML dependency (requirements.txt)
- Enhanced data handling capabilities
- Multi-format serialization support

**Files:**

- Updated `pipo_nodes_integrated.py` with data nodes
- Updated `web/pipoNodes.js` with MFShowData widget
- Added `requirements.txt` for dependencies

## v1.3.0 (2025-10-22)

**New Features:**

- ⭐ **MF Graph Plotter** - Interactive data visualization with Chart.js
- ⭐ **MF Story Driver** - Project-based step sequencing with seed management

**Technical:**

- Refactored codebase into modular files
- Added API endpoints for reset/save functionality
- Implemented JSON state persistence
- Enhanced initialization with diagnostics
- Improved error handling and logging

**Files:**

- Added `pipo_nodes_integrated.py` for all node logic
- Added `pipo_nodes_server.py` for API routes
- Enhanced `__init__.py` with better diagnostics
- Updated `web/pipoNodes.js` with new node support

## v1.2.0 (2025-01-15)

- Added MF Shot Helper
- Improved modulo operations
- Enhanced logging features

## v1.1.0 (2024-12-01)

- Added advanced modulo with cycle tracking
- Improved text processing
- Bug fixes and optimizations

## v1.0.0 (2024-11-01)

- Initial release
- 8 core nodes