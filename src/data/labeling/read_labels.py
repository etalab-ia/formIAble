from src.data.utils import fs
from pathlib import Path
import os
import sys
import tempfile
import json


def main(labels_path):
    with tempfile.TemporaryDirectory() as tmpdirname:
        try:
            fs.get(
                labels_path + "/",
                tmpdirname + "/",
                recursive=True,
            )
        except FileNotFoundError:
            pass

        image_paths = [
            Path(os.path.join(tmpdirname + "/", x))
            for x in os.listdir(tmpdirname + "/")
        ]
        for path in image_paths:
            with open(path) as f:
                data = json.load(f)
                print(data)


if __name__ == "__main__":
    labels_path = sys.argv[1]
    main(labels_path)
