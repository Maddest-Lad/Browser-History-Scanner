# Browser History Scanner

## Overview
A Python utility to scan and consolidate browser history data from multiple browsers into a unified SQLite database. The tool supports configuration-based path resolution for different browsers and provides statistical insights into the collected history data.

## Features
- Cross-platform support (Windows, macOS, Linux)
- Configurable browser history paths
- Unified database storage
- History statistics reporting

## Setup
1. Ensure you have [Python 3.10+](https://www.python.org/downloads/release/python-3100/) installed.
2. Clone the Repository:
```bash
git clone https://github.com/Maddest-Lad/Browser-History-Scanner.git
```
3. _Optionally_ [Create a virtual environment](https://docs.python.org/3/library/venv.html)

4. Install Dependencies
```bash
pip install -r requirements.txt
```
5. Run the Scanner:
```bash
python main.py
```
---
This will:
1. Detect your operating system
2. Load configuration from `config.ini`
3. Locate browser history files
4. Create a unified database at `unified_history.db`
5. Display a preview of collected data

## Project Structure
- `main.py` - Entry point and core logic
- `config.ini` - Browser path configuration
- `database.py` - Database operations module
- `requirements.txt` - Dependencies
- `utils.py` - Utility functions

## Output
A SQLite database file (`unified_history.db`) containing consolidated browser history data, along with logging output showing the scanning process and statistics.
