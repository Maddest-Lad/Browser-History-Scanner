import shutil
import tempfile
from pathlib import Path

from contextlib import contextmanager

@contextmanager
def temporary_copy(original_path: Path):
    original_path = Path(original_path)
    new_path = Path(tempfile.gettempdir(), original_path.name)
    try:
        shutil.copy(original_path, new_path)
        yield new_path
    finally:
        try:
            new_path.unlink()
        except (FileNotFoundError, PermissionError):
            pass
