# music lyrics tagger

Tested on Windows 10. (Because I manage my media collection on Windows...)

## Notes

I did not add support for mp3 files, since I mainly use flac and m4a.

## Setup

```bash
pipenv install
```

## Usage

1. Put `$path` in `folders.txt`. Can contain multiple paths. (Sometimes the script won't register a path if it contains certain characters, I haven't tested them all, but renaming the said folders should do the trick.)

2. `pipenv run python main.py` (`.env` content would be automatically registered via `pipenv`, even when you're on Windows.)
