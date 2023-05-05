from pathlib import Path
from typing import List

from doctr.io import Document, DocumentFile
from doctr.models import ocr_predictor


def get_list_words_in_page(page: Document):
    list_words_in_page = []
    for block in page.blocks:
        for line in block.lines:
            list_words_in_page.extend(line.words)
    return list_words_in_page


class DoctrTransformer:
    def __init__(self):
        pass

    def fit(self):
        return self

    def transform(self, raw_documents):
        doctr_documents = self._get_doctr_docs(raw_documents=raw_documents)
        return doctr_documents

    def _get_doctr_docs(self, raw_documents: List[Path]):
        if not hasattr(self, "doctr_model"):
            self.doctr_model = ocr_predictor(
                det_arch="db_resnet50",
                reco_arch="crnn_vgg16_bn",
                pretrained=True,
            )
        list_doctr_docs = []
        for doc in raw_documents:
            if not doc.exists():
                print(f"Doc {doc} could not be found.")
                continue
            res_doctr = None
            try:
                if doc.suffix == "pdf":
                    doc_doctr = DocumentFile.from_pdf(doc)
                else:
                    doc_doctr = DocumentFile.from_images(doc)
                res_doctr = self.doctr_model(doc_doctr)
            except Exception as e:
                print(f"Could not analyze document {doc}. Error: {e}")
            if res_doctr:
                list_doctr_docs.append(res_doctr)

        return list_doctr_docs
