import glob
import logging as log
from typing import List

import mutagen

# import azapi
log.basicConfig(format="%(asctime)s - [%(levelname)s] %(message)s", level=log.DEBUG)


def _get_files(path: str) -> List[str]:
    extensions = ["mp3", "flac", "m4a"]
    search_patterns = [f"{path}/**/*.{ext}" for ext in extensions]

    files = []
    for i in search_patterns:
        files.extend(glob.glob(i, recursive=True))

    return files


def _get_metadata(file: str):
    metadata = mutagen.File(file).tags
    # print(metadata.keys())
    extension = file.split(".")[-1]

    if extension == "m4a":
        return {
            "extension": extension,
            "artist": metadata["©ART"],
            "title": metadata["©nam"],
        }


if __name__ == "__main__":
    path = r"D:\Music\# Rock\Amanda Somerville"
    # path = r"D:\# tagginig\Music\z-staging\Avril Lavigne"
    files = _get_files(path)

    for i in files:
        log.info(f"Processing: {i}")

        print(_get_metadata(i))

        break
