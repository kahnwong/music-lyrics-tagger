import logging as log
import os
import re
from typing import Dict

import azapi
import lyricsgenius


log.basicConfig(format="%(asctime)s - [%(levelname)s] %(message)s", level=log.INFO)

########################
# init lyrics providers
########################
lyrics_provider = os.getenv("LYRICS_PROVIDER")

azlyrics = azapi.AZlyrics("google", accuracy=0.5)
genius = lyricsgenius.Genius(os.getenv("GENIUS_TOKEN"))


########################
# functions
########################
def get_lyrics(
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
