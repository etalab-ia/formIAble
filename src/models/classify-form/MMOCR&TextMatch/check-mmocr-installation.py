import logging
import os
import torch.hub
from mmocr.apis import MMOCRInferencer
logging.basicConfig(level=logging.DEBUG)

logging.debug(torch.hub.get_dir())  # look here if download fails
logging.debug(os.getcwd())

ocr = MMOCRInferencer(det='DBNet', rec='CRNN')
ocr('data/synthetic_forms/cerfa_12485_03_fake1.jpg', show=True, print_result=True)
