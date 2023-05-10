import contextlib
import glob
from typing import Dict
from typing import List

import mutagen

from src.utils.log import log


##################
# utils
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


##################
# read
##################
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


def get_lyrics_from_tag(file: str) -> str:
    metadata = mutagen.File(file).tags
    log.debug(f"metadata keys: {metadata.keys()}")

    extension = file.split(".")[-1]

    if extension == "m4a":
        # if you convert between formats,
        # the lyrics attr might not be correctly transferred
        if metadata.get("unsyncedlyrics"):
            lyrics = metadata.get("unsyncedlyrics")[0]
        elif metadata.get("----:com.apple.iTunes:unsyncedlyrics"):
            lyrics = metadata.get("----:com.apple.iTunes:unsyncedlyrics")[0].decode(
                "utf-8"
            )
        elif metadata.get("----:com.apple.iTunes:UNSYNCEDLYRICS"):
            lyrics = metadata.get("----:com.apple.iTunes:UNSYNCEDLYRICS")[0].decode(
                "utf-8"
            )
        elif metadata.get("©lyr"):
            lyrics = metadata.get("©lyr")[0]
        else:
            lyrics = None
    else:
        lyrics = None

    log.debug(lyrics)
    return lyrics


##################
# write
##################
def write_lyrics(file: str, lyrics: str):
    """
    music format (flac, m4a, etc) has its own lyrics field
    this function writes/transfer lyrics to attr
    specific to file extension
    """

    metadata = mutagen.File(file)

    extension = file.split(".")[-1]
    if extension == "flac":
        metadata["unsyncedlyrics"] = [lyrics]

        with contextlib.suppress(KeyError, ValueError):
            metadata.pop("©lyr")
    elif extension == "m4a":
        metadata["©lyr"] = [lyrics]

        with contextlib.suppress(KeyError, ValueError):
            metadata.pop("----:com.apple.iTunes:unsyncedlyrics")

        with contextlib.suppress(KeyError, ValueError):
            metadata.pop("----:com.apple.iTunes:UNSYNCEDLYRICS")
    metadata.save()
