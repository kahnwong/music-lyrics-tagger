import contextlib
import logging as log
import os
import re
from random import random
from time import sleep
from typing import Dict

import azapi
import lyricsgenius
from tqdm import tqdm

from src.utils.io import get_files
from src.utils.io import get_metadata
from src.utils.io import write_lyrics


log.basicConfig(format="%(asctime)s - [%(levelname)s] %(message)s", level=log.INFO)

########################
# init lyrics providers
########################
lyrics_provider = os.getenv("LYRICS_PROVIDER")

########################
# init genius provider
########################
azlyrics = azapi.AZlyrics("google", accuracy=0.5)
genius = lyricsgenius.Genius(os.getenv("GENIUS_TOKEN"))

########################
# helpers
########################
def _get_lyrics(
    metadata: Dict[str, str],
    provider: str = lyrics_provider,
    genius: lyricsgenius.Genius = genius,
    azlyrics: azapi.AZlyrics = azlyrics,
) -> str:
    ################################################################
    if provider == "azlyrics":
        azlyrics.artist = metadata["artist"]
        azlyrics.title = metadata["title"].split("(")[0]

        azlyrics.getLyrics()

        lyrics = azlyrics.lyrics

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
    log.debug(lyrics)

    return re.sub(r"\d+$", "", lyrics)


########################
# main
########################
if __name__ == "__main__":
    with open("folders.txt", "r", encoding="utf-8") as f:
        paths = [i.strip() for i in f.readlines()]

    for path in paths:
        files = get_files(path)

        for i in (t := tqdm(files)):
            t.set_description(f"Processing: {i}")
            # print(i)

            metadata = get_metadata(i)
            log.debug(metadata)

            with contextlib.suppress(AttributeError, TimeoutError, IndexError):
                lyrics = _get_lyrics(metadata)
                write_lyrics(file=i, lyrics=lyrics)

                sleep(3 * random())

            # break
