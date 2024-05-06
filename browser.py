from dataclasses import dataclass
import datetime
import glob
import os
from pathlib import Path
import sqlite3
from utils import temporary_copy, get_drive_letter

def get_browsers(users=None):
    """Retrieves all Chromium-based browsers installed on the system."""
    history_files = _get_history_files(users)
    browsers = []
    for history_file in history_files:
        browsers.append(Browser(history_file))
        
    return browsers

def _get_history_files(users=None):
    """Retrieves history files matching chromuim's folder structure"""
    if not users: # Default to Current User
        local_appdata = os.environ.get('LOCALAPPDATA')
        search_pattern = os.path.join(local_appdata, '*', '*', 'User Data', 'Default', 'History') 
        print(search_pattern)
        return glob.glob(search_pattern)
    else:
        paths = []
        for user in users:
            search_pattern = os.path.join(f'{get_drive_letter()}\\', 'Users', user, 'AppData', 'Local', '*', '*', 'User Data', 'Default', 'History')
            print(search_pattern)
            paths.extend(glob.glob(search_pattern))
        return paths

@dataclass
class Entry:
    id: int
    url: str
    title: str
    visit_count: int
    typed_count: int
    last_visit_time: datetime.datetime

class Browser:
    vendor: str
    name: str
    history_path: Path
    
    def __init__(self, history_path: Path):
        self.history_path = history_path
        
        parts = history_path.split(os.sep)
        self.vendor = parts[-5]
        self.name = parts[-4]
        
    def webkit_timestamp_to_datetime(self, webkit_timestamp):
        """Converts a WebKit timestamp to a datetime object."""
        # WebKit timestamp is microseconds since January 1, 1601
        epoch_start = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=webkit_timestamp)
        return epoch_start

    def get_history(self) -> list[Entry]:
        """ Retrieves the history using a temporary copy of the Chromium sqlite database"""
        with temporary_copy(self.history_path) as local_db:
            conn = sqlite3.connect(local_db, timeout=3)
            cursor = conn.cursor()
            
            # Retrieve History
            cursor.execute("SELECT id, url, title, visit_count, typed_count, last_visit_time FROM urls")
            entries = []
            for row in cursor.fetchall():
                id, url, title, visit_count, typed_count, last_visit_time = row
                # Convert WebKit timestamp to datetime
                last_visit_time = self.webkit_timestamp_to_datetime(last_visit_time)
                entry = Entry(id, url, title, visit_count, typed_count, last_visit_time)
                entries.append(entry)
            return entries

    def __repr__(self):
        return f'{self.vendor} {self.name}'
