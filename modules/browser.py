from dataclasses import dataclass
import datetime
from pathlib import Path
import sqlite3
from utils import temporary_copy

@dataclass
class Entry:
    id: int
    url: str
    title: str
    visit_count: int
    typed_count: int
    last_visit_time: datetime.datetime

class ChromiumHandler:

    def __init__(self, history_path: Path):
        self.history_path = history_path
    
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