import os
import re
from typing import Dict

import azapi
import lyricsgenius

from music_lyrics_tagger.core import app_config

########################
# init lyrics providers
########################
lyrics_provider = app_config["LYRICS_PROVIDER"]  # `azlyrics` or `genius`

azlyrics = azapi.AZlyrics("google", accuracy=0.5)
genius = lyricsgenius.Genius(app_config["GENIUS_TOKEN"])


########################
# methods
########################
def get_lyrics(
    metadata: Dict[str, str],
    provider: str = lyrics_provider,
    genius: lyricsgenius.Genius = genius,
    azlyrics: azapi.AZlyrics = azlyrics,
) -> str:
    ################################################################
    lyrics = ""
    if provider == "azlyrics":
        azlyrics.artist = metadata["artist"]
        azlyrics.title = metadata["title"].split("(")[0]

        azlyrics.getLyrics()

        lyrics = azlyrics.lyrics

    elif provider == "genius":
        song = genius.search_song(metadata["title"].split("(")[0], metadata["artist"])
        lyrics = ""
        try:
            lyrics = (
                song.lyrics.replace(f"{song.title} Lyrics", "")
                .replace("You might also like", "")
                .replace("Embed", "")
                .replace("TranslationsEnglishRomanization", "")
                .replace("TranslationsRomanization", "")
            )

            lyrics = re.sub(r"^[0-9]+ Contributor(s?)", "", lyrics)
        except AttributeError:
            pass
    ################################################################

    lyrics = "\r\n".join(lyrics.splitlines())

    return re.sub(r"\d+$", "", lyrics)
