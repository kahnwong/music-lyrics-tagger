import os

import yaml

config_path = os.path.join(
    os.environ.get("HOME"), ".config", "music-lyrics-tagger", "config.yaml"
)

with open(config_path, "r") as file:
    app_config = yaml.safe_load(file)
