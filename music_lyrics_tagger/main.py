import contextlib
from random import random
from time import sleep

from tqdm import tqdm

from music_lyrics_tagger.utils.io import get_files
from music_lyrics_tagger.utils.io import get_lyrics_from_tag
from music_lyrics_tagger.utils.io import get_metadata
from music_lyrics_tagger.utils.io import write_lyrics
from music_lyrics_tagger.utils.lyrics import get_lyrics


if __name__ == "__main__":
    with open("folders.txt", "r", encoding="utf-8") as f:
        paths = [i.strip() for i in f.readlines()]

    files = get_files(paths)

    for i in (t := tqdm(files)):
        t.set_description(f"Processing: {i}")

        metadata = get_metadata(i)
        if lyrics_from_tag := get_lyrics_from_tag(i):
            write_lyrics(file=i, lyrics=lyrics_from_tag)
        else:
            with contextlib.suppress(AttributeError, TimeoutError, IndexError):
                lyrics = get_lyrics(metadata)
                write_lyrics(file=i, lyrics=lyrics)

                sleep(3 * random())

        # break
