import glob
import os
from typing import List


def get_current_dir_files() -> List[str]:
    current_dir = os.getcwd()

    extensions = ["flac", "m4a"]
    search_patterns = [f"{current_dir}/**/*.{ext}" for ext in extensions]

    files = []
    for i in search_patterns:
        matched_files = glob.glob(i, recursive=True)
        matched_files = [i for i in matched_files if "Instrumental" not in i]
        files.extend(matched_files)

    return sorted(files)
