from src.data.labeling.json_creator import AnnotationJsonCreator
from src.data.labeling.doctr_utils import DoctrTransformer
from src.data.utils import fs
from pathlib import Path
import os
import sys
import tempfile


def main(data_path, output_path):
    # For now we assume images

    with tempfile.TemporaryDirectory() as tmpdirname:
        # Download data from s3
        fs.get(data_path, tmpdirname + "/", recursive=True)
        image_paths = [
            Path(os.path.join(tmpdirname + "/", x))
            for x in os.listdir(tmpdirname + "/")
            if x.endswith((".jpg", ".jpeg", ".png"))
        ]
        list_doctr_docs = DoctrTransformer().transform(image_paths)
        os.makedirs(tmpdirname + "/labels/")
        annotations = AnnotationJsonCreator(
            image_paths,
            tmpdirname + "/"
        ).transform(
            list_doctr_docs
        )

        # Upload to s3
        fs.put(tmpdirname + "/labels.json", output_path, recursive=True)


if __name__ == "__main__":
    data_path = sys.argv[1]
    output_path = sys.argv[2]

    main(data_path, output_path)
