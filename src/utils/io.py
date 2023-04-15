import glob
import logging as log
from typing import Dict
from typing import List

import mutagen


log.basicConfig(format="%(asctime)s - [%(levelname)s] %(message)s", level=log.INFO)


##################
# read
##################
def get_files(path: str) -> List[str]:
    extensions = ["flac", "m4a"]
    search_patterns = [f"{path}/**/*.{ext}" for ext in extensions]
    log.debug(f"search pattern: {search_patterns}")

    files = []
    for i in search_patterns:
        files.extend(glob.glob(i, recursive=True))

    log.debug(f"files: {files}")

    return [i for i in files if "Instrumental" not in i]


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
