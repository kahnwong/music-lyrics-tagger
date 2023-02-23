import glob
import logging as log
from typing import Dict
from typing import List

import azapi
import mutagen


log.basicConfig(format="%(asctime)s - [%(levelname)s] %(message)s", level=log.DEBUG)


def _get_files(path: str) -> List[str]:
    extensions = ["mp3", "flac", "m4a"]
    search_patterns = [f"{path}/**/*.{ext}" for ext in extensions]

    files = []
    for i in search_patterns:
        files.extend(glob.glob(i, recursive=True))

    return files


def _get_metadata(file: str) -> Dict[str, str]:
    metadata = mutagen.File(file).tags
    # print(metadata.keys())
    extension = file.split(".")[-1]

    if extension == "m4a":
        return {
            "extension": extension,
            "artist": metadata["©ART"][0],
            "title": metadata["©nam"][0],
        }


def _get_lyrics(metadata: Dict[str, str]) -> str:
    API = azapi.AZlyrics("google", accuracy=0.5)

    API.artist = metadata["artist"]
    API.title = metadata["title"]

    API.getLyrics()

    return API.lyrics


if __name__ == "__main__":
    path = r"D:\Music\# Rock\Amanda Somerville"
    # path = r"D:\# tagginig\Music\z-staging\Avril Lavigne"
    files = _get_files(path)

    for i in files:
        log.info(f"Processing: {i}")

        metadata = _get_metadata(i)
        lyrics = _get_lyrics(metadata)

        break
