import contextlib
import logging as log
from random import random
from time import sleep

from tqdm import tqdm

from src.utils.io import get_files
from src.utils.io import get_metadata
from src.utils.io import write_lyrics
from src.utils.lyrics import get_lyrics


log.basicConfig(format="%(asctime)s - [%(levelname)s] %(message)s", level=log.INFO)


if __name__ == "__main__":
    with open("folders.txt", "r", encoding="utf-8") as f:
        paths = [i.strip() for i in f.readlines()]

    files = get_files(paths)

    for i in (t := tqdm(files)):
        t.set_description(f"Processing: {i}")

        metadata = get_metadata(i)
        log.debug(metadata)

        with contextlib.suppress(AttributeError, TimeoutError, IndexError):
            lyrics = get_lyrics(metadata)
            write_lyrics(file=i, lyrics=lyrics)

            sleep(3 * random())

        # break
