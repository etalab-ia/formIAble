from pathlib import Path
from typing import List
import json

from doctr.io import Document

from src.data.labeling.doctr_utils import get_list_words_in_page


class AnnotationJsonCreator:
    """
    Class for generating json files in the LabelStudio
    json format containing the bboxes from doctr.
    """

    def __init__(
        self,
        raw_documents: List[Path],
        output_path: Path = None,
        predictions: List = None,
    ):
        self.output_path = output_path
        self.raw_documents = raw_documents
        self.predictions = predictions

    def fit(self, doctr_documents: List[Path], **kwargs):
        return self

    def transform(self, doctr_documents: List[Document]):
        print(self.raw_documents)
        annotations = []
        counter = 0
        for doc_id, doc in enumerate(doctr_documents):
            image_name = self.raw_documents[doc_id].name
            image_path_labelstudio = (
                "/data/upload/" + image_name
                if upload
                else f"/data/local-files/?d={image_path}"
            )
            page = doc.pages[
                0
            ]  # On ne traite que des png/jpg donc que des docs à une page
            dict_image = {
                "data": {"image": image_path_labelstudio},
                "predictions": [{"result": [], "score": None}],
            }  # result: list de dict pour chaque BBox

            list_words_in_page = get_list_words_in_page(page)
            height, width = page.dimensions[0], page.dimensions[1]
            id_annotation = 0
            for word in list_words_in_page:
                prediction = (
                    self.predictions[counter]
                    if self.predictions is not None
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
                json_path = self.output_path / f"{image_path}.json"
                with open(self.output_path, "w") as fp:
                    json.dump(dict_image, fp)

        return annotations
