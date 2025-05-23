import sqlite3
import logging
from typing import List
from dataclasses import dataclass
from utils import temporary_copy

@dataclass
class HistoryLocation:
    browser: str
    path: str

def create_unified_history_db(db_path: str, history_locations: List[HistoryLocation]) -> None:
    """
    Create a unified history database from multiple browser history files.

    Args:
        db_path (str): Path to the unified database file.
        history_locations (List[HistoryLocation]): List of browser history locations.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Create unified history table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS unified_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            title TEXT,
            visit_count INTEGER DEFAULT 0,
            last_visit_time INTEGER,
            browser TEXT NOT NULL
        )
        ''')

        # Create index on url column
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_url ON unified_history (url)')

        for loc in history_locations:
            try:
                with temporary_copy(loc.path) as temp_db_path:
                    process_browser_history(cursor, temp_db_path, loc.browser)
            except Exception as e:
                logging.error(f"Error processing {loc.browser} history: {str(e)}")

        conn.commit()
    except Exception as e:
        logging.error(f"Error creating unified database: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

def display_unified_db_stats(db_path: str) -> None:
    """
    Display statistics from the unified history database.

    Args:
        db_path (str): Path to the unified database file.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM unified_history")
        total_entries = cursor.fetchone()[0]
        
        cursor.execute("SELECT browser, COUNT(*) FROM unified_history GROUP BY browser")
        browser_stats = cursor.fetchall()
        
        cursor.execute("SELECT url, title, visit_count FROM unified_history ORDER BY visit_count DESC LIMIT 5")
        top_sites = cursor.fetchall()

        logging.info(f"Total entries in unified history: {total_entries}")
        for browser, count in browser_stats:
            logging.info(f"Entries from {browser}: {count}")
        
        logging.info("Top 5 most visited sites:")
        for url, title, visit_count in top_sites:
            logging.info(f"{title} ({url}) - Visited {visit_count} times")

    except Exception as e:
        logging.error(f"Error displaying database stats: {str(e)}")
    finally:
        conn.close()

def process_browser_history(cursor: sqlite3.Cursor, db_path: str, browser: str) -> None:
    """
    Process browser history and insert it into the unified database.

    Args:
        cursor (sqlite3.Cursor): Cursor for the unified database.
        db_path (str): Path to the browser history file.
        browser (str): Name of the browser.
    """
    browser_conn = sqlite3.connect(db_path)
    browser_cursor = browser_conn.cursor()

    match browser:
        case "Chromium":
            browser_cursor.execute("SELECT url, title, visit_count, last_visit_time FROM urls")
        case "Gecko" | "Firefox":
            browser_cursor.execute("SELECT url, title, visit_count, last_visit_date FROM moz_places")
        case "Safari":
            browser_cursor.execute("SELECT url, title, visit_count, last_visit_time FROM history_items")
        case _:
            raise NotImplementedError(f"Browser not supported: {browser}")

    for row in browser_cursor.fetchall():
        url, title, visit_count, last_visit_time = row
        cursor.execute('''
        INSERT INTO unified_history (url, title, visit_count, last_visit_time, browser)
        VALUES (?, ?, ?, ?, ?)
        ''', (url, title, visit_count, last_visit_time, browser))

    browser_conn.close()
