import os
import shutil
import tempfile
from pathlib import Path

class temporary_copy(object):
    
    def __init__(self, original_path: Path):
        self.original_path = Path(original_path)

    def __enter__(self):
        self.new_path = Path(tempfile.gettempdir(), self.original_path.name)
        shutil.copy(self.original_path, self.new_path)
        return self.new_path

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.new_path.unlink()
        except (FileNotFoundError, PermissionError):
            pass
