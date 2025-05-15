import argparse
import os
import glob
from pathlib import Path
import platform
import configparser
import logging
from typing import List
from database import HistoryLocation, create_unified_history_db, display_unified_db_stats

parser = argparse.ArgumentParser()
parser.add_argument('--analyze-history', action='store_true', help='Generate domain/subdomain statistics')
args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
    os_key = get_os_key()
    config_path = Path("config.ini")

    if not os_key:
        raise RuntimeError("Unsupported platform")
    
    if not config_path.exists():
        raise RuntimeError("Browser Config Missing, Please Pull Down a Fresh Copy From https://github.com/Maddest-Lad/Browser-History-Scanner")

    config = load_config(config_path)
    
    history_locations = find_browser_history_files(config, os_key)

    for loc in history_locations:
        logging.info(f"Found history for {loc.browser}: {loc.path}")
    
    unified_db_path = "unified_history.db"
    create_unified_history_db(unified_db_path, history_locations)
    logging.info(f"Unified history database created at: {unified_db_path}")

    if args.analyze_history:
        display_unified_db_stats(unified_db_path)
