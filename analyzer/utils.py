import tempfile
import os
from typing import Union

def save_uploaded_file(file_obj) -> str:
    """Save uploaded file to temporary location"""
    temp_dir = tempfile.mkdtemp()
    path = os.path.join(temp_dir, file_obj.name)
    with open(path, "wb") as f:
        f.write(file_obj.read())
    return path

def cleanup_temp_files(path: str):
    """Remove temporary files"""
    if os.path.exists(path):
        os.remove(path)
        os.rmdir(os.path.dirname(path))