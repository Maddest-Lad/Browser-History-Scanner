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

```
.
├── aggregate_history.py
├── analyze_history.py
├── lib
│   ├── database.py
│   └── files.py
├── config.ini
├── requirements.txt
└── README.md
```

- `aggregate_history.py` - CLI tool: aggregate browser histories to a unified SQLite DB
- `analyze_history.py`   - CLI tool: analyze a unified history database and output stats
- `lib/database.py`      - Database operations, data classes, core aggregation logic
- `lib/files.py`         - Utility (e.g., safe file operations)
- `config.ini`           - Browser path configuration
- `requirements.txt`     - Install dependencies

## Usage

Aggregate all browser histories:
```
python aggregate_history.py --config config.ini --out aggregate_history.db
```

Analyze the database (to .csv or .json):
```
python analyze_history.py --in aggregate_history.db --out output.csv
```

## Output
A SQLite database file (`aggregate_history.db`) containing consolidated browser history data, plus CSV/JSON statistics files as requested.
