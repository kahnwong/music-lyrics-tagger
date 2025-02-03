import sys
from random import random
from time import sleep

import click
from tqdm import tqdm

from music_lyrics_tagger.core import lyrics, tag, utils


@click.group()
@click.version_option()
def cli():
    ""


@cli.command(name="tag")
def tag_lyrics():
    "Add lyrics"
    files = utils.get_current_dir_files()

    for i in (t := tqdm(files)):
        metadata = tag.get_metadata(i)
        l = lyrics.get_lyrics(metadata)
        tag.write_lyrics(file=i, lyrics=l)
        sleep(3 * random())
