import os
import glob
import platform
import configparser
from pathlib import Path
from dataclasses import dataclass
from typing import List


@dataclass
class HistoryLocation:
    browser: str
    path: str


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
    config_path = "config.ini"
    os_key = get_os_key()

    if not os_key:
        raise RuntimeError("Unsupported platform")

    config = load_config(config_path)
    history_locations = find_browser_history_files(config, os_key)

    for loc in history_locations:
        print(f"{loc.browser}: {loc.path}")
