import contextlib
import glob
from typing import Dict, List

import mutagen


def get_metadata(file: str) -> Dict[str, str]:
    metadata = mutagen.File(file).tags

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


def write_lyrics(file: str, lyrics: str):
    """
    music format (flac, m4a, etc) has its own lyrics field
    this function writes/transfer lyrics to attr
    specific to file extension
    """

    metadata = mutagen.File(file)

    extension = file.split(".")[-1]
    if extension == "flac":
        metadata["unsynced lyrics"] = [lyrics]

        with contextlib.suppress(KeyError, ValueError):
            metadata.pop("©lyr")
    elif extension == "m4a":
        metadata["©lyr"] = [lyrics]

        with contextlib.suppress(KeyError, ValueError):
            metadata.pop("----:com.apple.iTunes:unsynced lyrics")

        with contextlib.suppress(KeyError, ValueError):
            metadata.pop("----:com.apple.iTunes:UNSYNCED LYRICS")
    metadata.save()
