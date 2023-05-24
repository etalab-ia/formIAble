from typing import List
import os
import json
from mmocr.apis import MMOCRInferencer
import logging
logging.basicConfig(level=logging.INFO)

# models for text detection
det_models: List[str] = ["dbnet_resnet18_fpnc_1200e_icdar2015",
                         "dbnet_resnet50-oclip_fpnc_1200e_icdar2015",
                         "dbnet_resnet18_fpnc_1200e_totaltext",
                         "dbnetpp_resnet50_fpnc_1200e_icdar2015",
                         "dbnetpp_resnet50-dcnv2_fpnc_1200e_icdar2015",
                         "dbnetpp_resnet50-oclip_fpnc_1200e_icdar2015",
                         "MaskRCNN_CTW",  # detects all of the text
                         "mask-rcnn_resnet50-oclip_fpn_160e_ctw1500",
                         "MaskRCNN",
                         "DRRG",  # detects all of the text
                         "FCE_CTW_DCNv2",
                         "FCE_IC15",
                         "FCENet",
                         "PANet_CTW",  # detects all of the text
                         "PANet_IC15",
                         "PS_CTW",  # detects all of the text
                         "PS_IC15",
                         "PSENet",
                         "TextSnake"]


input_document_path: str = "data/synthetic_forms/cerfa_12485_03_fake1.jpg"
output_dir: str = "results/MMOCR/text_detection"
logging.info(f"working directory = {os.getcwd()}")
for det_model in det_models:
    logging.info(f"Loading text detection model {det_model} ...")
    ocr = MMOCRInferencer(det=det_model)
    logging.info(f"Loading text detection model {det_model} [OK]")

    logging.info(f"Running text detection model {det_model} ...")
    output = ocr(
        input_document_path,
        out_dir=os.path.join(output_dir, det_model),
        save_vis=True,
        save_pred=True
    )
    logging.info(f"Running text detection model {det_model} [OK]")
