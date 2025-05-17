import argparse
import os
import glob
from pathlib import Path
import platform
import configparser
import logging
from typing import List
from lib.database import HistoryLocation, create_unified_history_db

def get_os_key() -> str:
    return {
        'windows': 'windows',
        'darwin': 'macos',
        'linux': 'linux'
    }.get(platform.system().lower(), '')

def load_config(path: str) -> configparser.ConfigParser:
    config = configparser.RawConfigParser()
    config.read(path)
    return config

def resolve_pattern(pattern: str) -> List[str]:
    expanded = os.path.expandvars(os.path.expanduser(pattern))
    return glob.glob(expanded, recursive=True)

def find_browser_history_files(config: configparser.ConfigParser, os_key: str) -> List[HistoryLocation]:
    results = []
    for section in config.sections():
        if config.has_option(section, os_key):
            pattern = config.get(section, os_key)
            matches = resolve_pattern(pattern)
            for match in matches:
                results.append(HistoryLocation(browser=section, path=match))
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aggregate browser history databases into a unified SQLite DB.")
    parser.add_argument('--config', default="config.ini", help='Path to config.ini (default: config.ini)')
    parser.add_argument('--out', default="aggregate_history.db", help='Output path for unified history database (default: aggregate_history.db)')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    os_key = get_os_key()
    config_path = Path(args.config)

    if not os_key:
        raise RuntimeError("Unsupported platform")
    if not config_path.exists():
        raise RuntimeError("Browser Config Missing, Please Pull Down a Fresh Copy From https://github.com/Maddest-Lad/Browser-History-Scanner")

    config = load_config(str(config_path))
    history_locations = find_browser_history_files(config, os_key)

    for loc in history_locations:
        logging.info(f"Found history for {loc.browser}: {loc.path}")

    create_unified_history_db(args.out, history_locations)
    logging.info(f"Unified history database created at: {args.out}")