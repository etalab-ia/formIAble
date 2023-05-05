from pathlib import Path
from typing import List, Optional
import json
import os

from doctr.io import Document

from src.data.labeling.doctr_utils import get_list_words_in_page


class AnnotationJsonCreator:
    """
    Class for generating json files in the LabelStudio
    json format containing the bboxes from doctr.
    """

    def __init__(
        self,
        output_path: Path = None
    ):
        self.output_path = output_path

    def fit(self, doctr_documents: List[Path], **kwargs):
        return self

    def transform(
        self,
        remote_paths: List[Path],
        doctr_documents: List[Document],
        predictions: Optional[List] = None,
    ):
        annotations = []
        counter = 0
        for doc_id, doc in enumerate(doctr_documents):
            image_path = remote_paths[doc_id]
            image_name = image_path.stem
            image_path = str(image_path)
            page = doc.pages[
                0
            ]  # On ne traite que des png/jpg donc que des docs à une page
            dict_image = {
                "data": {"image": "s3://" + image_path},
                "predictions": [{"result": [], "score": None}],
            }  # result: list de dict pour chaque BBox

            list_words_in_page = get_list_words_in_page(page)
            height, width = page.dimensions[0], page.dimensions[1]
            id_annotation = 0
            for word in list_words_in_page:
                prediction = (
                    predictions[counter]
                    if predictions is not None
                    else None
                )
                id_annotation += 1
                label = word.value
                xmin, ymin = word.geometry[0][0], word.geometry[0][1]
                xmax, ymax = word.geometry[1][0], word.geometry[1][1]
                width_a, height_a = xmax - xmin, ymax - ymin
                dict_annotation = {
                    "id": "result{}".format(id_annotation),
                    "meta": {"text": [label]},
                    "type": "rectanglelabels",
                    "from_name": "label",
                    "to_name": "image",
                    "original_width": width,
                    "original_height": height,
                    "image_rotation": 0,
                    "value": {
                        "rotation": 0,
                        "x": xmin * 100,
                        "y": ymin * 100,
                        "width": width_a * 100,
                        "height": height_a * 100,
                        "rectanglelabels": [prediction],
                    },
                }
                dict_image["predictions"][0]["result"].append(dict_annotation)
                counter += 1
            annotations.append(dict_image)

            if self.output_path is not None:
                json_path = os.path.join(
                    self.output_path,
                    f"{image_name}.json"
                )
                with open(json_path, "w") as fp:
                    json.dump(dict_image, fp)

        return annotations
