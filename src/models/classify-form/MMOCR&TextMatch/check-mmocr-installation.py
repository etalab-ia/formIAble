import logging
import os
import torch.hub
from mmocr.apis import MMOCRInferencer
logging.basicConfig(level=logging.DEBUG)

logging.debug(torch.hub.get_dir())  # look here if download fails
logging.debug(os.getcwd())

ocr = MMOCRInferencer(det='DBNet', rec='CRNN')
ocr('data/synthetic_forms/cerfa_12485_03_fake1.jpg',
    out_dir="results/MMOCR/example/cerfa_12485_03_fake1",
    save_pred=True,
    save_vis=True)
