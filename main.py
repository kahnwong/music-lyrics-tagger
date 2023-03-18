import contextlib
import glob
import logging as log
import os
import re
from random import random
from time import sleep
from typing import Dict
from typing import List

import azapi
import lyricsgenius
import mutagen
from tqdm import tqdm


log.basicConfig(format="%(asctime)s - [%(levelname)s] %(message)s", level=log.INFO)

########################
# init provider choice
########################
lyrics_provider = os.getenv("lyrics_provider")

########################
# init genius provider
########################
genius = lyricsgenius.Genius(os.getenv("GENIUS_TOKEN"))

########################
# helpers
########################
def _get_files(path: str) -> List[str]:
    extensions = ["flac", "m4a"]
    search_patterns = [f"{path}/**/*.{ext}" for ext in extensions]
    log.debug(f"search pattern: {search_patterns}")

    files = []
    for i in search_patterns:
        files.extend(glob.glob(i, recursive=True))

    log.debug(f"files: {files}")

    return [i for i in files if "Instrumental" not in i]


def _get_metadata(file: str) -> Dict[str, str]:
    metadata = mutagen.File(file).tags
    log.debug(f"metadata keys: {metadata.keys()}")

    extension = file.split(".")[-1]
    if extension == "m4a":
        return {
            "artist": metadata["aART"][0],
            "title": metadata["©nam"][0],
        }
    elif extension == "flac":
        return {
            "artist": metadata["albumartist"][0],
            "title": metadata["title"][0],
        }


def _get_lyrics(
    metadata: Dict[str, str],
    provider: str = lyrics_provider,
    genius: lyricsgenius.Genius = genius,
) -> str:
    ################################################################
    if provider == "azlyrics":
        API = azapi.AZlyrics("google", accuracy=0.5)

        API.artist = metadata["artist"]
        API.title = metadata["title"].split("(")[0]

        API.getLyrics()

        lyrics = API.lyrics

    elif provider == "genius":
        song = genius.search_song(
            metadata["title"].split("(")[0].split("-")[0], metadata["artist"]
        )

        lyrics = (
            song.lyrics.replace(f"{song.title} Lyrics", "")
            .replace("You might also like", "")
            .replace("Embed", "")
        )
    ################################################################

    lyrics = "\r\n".join(lyrics.splitlines())
    return re.sub(r"\d+$", "", lyrics)


def _write_lyrics(file: str, lyrics: str):
    metadata = mutagen.File(file)

    extension = file.split(".")[-1]
    if extension == "m4a":
        metadata["©lyr"] = [lyrics]
    elif extension == "flac":
        metadata["unsyncedlyrics"] = [lyrics]

    metadata.save()


########################
# main
########################
if __name__ == "__main__":
    with open("folders.txt", "r", encoding="utf-8") as f:
        paths = [i.strip() for i in f.readlines()]

    for path in paths:
        files = _get_files(path)

        for i in (t := tqdm(files)):
            t.set_description(f"Processing: {i}")
            print(i)

            metadata = _get_metadata(i)
            log.debug(metadata)

            with contextlib.suppress(AttributeError, TimeoutError, IndexError):
                lyrics = _get_lyrics(metadata)
                _write_lyrics(file=i, lyrics=lyrics)

                sleep(3 * random())

            # break
