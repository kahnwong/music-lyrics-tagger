import glob

# import mutagen
# import azapi


def _get_files(path: str):
    extensions = ["mp3", "flac", "m4a"]
    search_patterns = [f"{path}/**/*.{ext}" for ext in extensions]

    files = []
    for i in search_patterns:
        files.extend(glob.glob(i, recursive=True))

    return files


if __name__ == "__main__":
    path = r"D:\Music\# Pop\Abalone Dots"
    files = _get_files(path)
    print(files)
