import glob
import os

from modules.browser import ChromiumHandler

# TODO Multi User Support / Selection
def get_chromium_history_files(users=None):
    """Retrieves folders in %localappdata% that follow the Chromuim folder structure."""
    local_appdata = os.environ.get('LOCALAPPDATA')
    search_pattern = os.path.join(local_appdata, '*', '*', 'User Data', 'Default', 'History') 

    return glob.glob(search_pattern)


if __name__ == "__main__":
    entries = []

    # Search For Database Paths
    history_files = get_chromium_history_files()
    
    for file in history_files:
        handler = ChromiumHandler(file)
        entries.extend(handler.get_history())