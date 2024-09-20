# music lyrics tagger

Tested on Windows 10 & Linux.

## Setup

```bash
uv sync
```

## Usage

1. Put `$path` in `folders.txt`. Can contain multiple paths. (Sometimes the script won't register a path if it contains certain characters, I haven't tested them all, but renaming the said folders should do the trick.)

2. `uv run python music_lyrics_tagger/main.py`

Required ENV

```env
GENIUS_TOKEN=      # required if you want to fetch lyrics from genius
LYRICS_PROVIDER=   # `genius` or `azlyrics`
```

## Notes

I did not add support for mp3 files, since I mainly use flac and m4a.
