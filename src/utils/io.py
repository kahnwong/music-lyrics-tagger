import glob
from typing import Dict
from typing import List

import mutagen

from src.utils.log import log


##################
# read
##################
def get_files(paths: List[str]) -> List[str]:
    files = []

    for path in paths:
        extensions = ["flac", "m4a"]
        search_patterns = [f"{path}/**/*.{ext}" for ext in extensions]
        log.debug(f"search pattern: {search_patterns}")

        for i in search_patterns:
            matched_files = glob.glob(i, recursive=True)
            matched_files = [i for i in matched_files if "Instrumental" not in i]
            files.extend(matched_files)

    log.debug(f"files: {files}")

    return files


def get_metadata(file: str) -> Dict[str, str]:
    metadata = mutagen.File(file).tags
    log.debug(f"metadata keys: {metadata.keys()}")

    extension = file.split(".")[-1]

    if extension == "flac":
        return {
            "artist": metadata["albumartist"][0],
            "title": metadata["title"][0],
        }
    elif extension == "m4a":
        return {
            "artist": metadata["aART"][0],
            "title": metadata["©nam"][0],
        }


##################
# write
##################
def write_lyrics(file: str, lyrics: str):
    metadata = mutagen.File(file)

    extension = file.split(".")[-1]
    if extension == "flac":
        metadata["unsyncedlyrics"] = [lyrics]
    elif extension == "m4a":
        metadata["©lyr"] = [lyrics]

    metadata.save()
