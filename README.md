# Browser History Scanner

## Overview
A Python utility to scan and consolidate browser history data from multiple browsers into a unified SQLite database. The tool supports configuration-based path resolution for different browsers and provides statistical insights into the collected history data.

## Features
- Cross-platform support (Windows, macOS, Linux)
- Configurable browser history paths
- Unified database storage
- History statistics reporting
- Modular architecture with separate configuration and database modules

## Requirements
Ensure you have Python 3.7+ installed. Install dependencies using:
```bash
pip install -r requirements.txt
```

## Configuration
1. Copy the sample config from the repository
2. Configure browser path patterns in `config.ini` according to your system
3. Ensure all required browser history files are accessible

## Usage
```bash
python main.py
```
This will:
1. Detect your operating system
2. Load configuration from `config.ini`
3. Locate browser history files
4. Create a unified database at `unified_history.db`
5. Display statistical information about the collected data

## Project Structure
- `main.py` - Entry point and core logic
- `config.ini` - Browser path configuration
- `database.py` - Database operations module
- `requirements.txt` - Dependency list
- `utils.py` - Utility functions

## Output
A SQLite database file (`unified_history.db`) containing consolidated browser history data, along with logging output showing the scanning process and statistics.
