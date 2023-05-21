from __future__ import annotations

import logging
logging.basicConfig(level=logging.DEBUG)

logging.info("Checking paddleocr installation ...")

import paddleocr  # noqa: E402

image_path: str = "data/synthetic_forms/cerfa_12485_03_fake1.jpg"

ocrModel = paddleocr.PaddleOCR(use_angle_cls=False, lang='fr')
ocrResult: list[list[list[list[float]] | tuple[str, float]]] = ocrModel.ocr(image_path, cls=False)

logging.info("Checking paddleocr installation [OK]")
