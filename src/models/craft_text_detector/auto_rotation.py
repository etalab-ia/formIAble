import cv2
import numpy as np
from src.models.craft_text_detector import Craft


def display_image(img, title, resize=False):

    size_max = 1000
    if resize:
        height = img.shape[0]
        width = img.shape[1]
        if height / width <= 1:
            img = cv2.resize(img, (size_max, int(size_max * height / width)))
        else:
            img = cv2.resize(img, (int(size_max * width / height), size_max))

    cv2.imshow(title, img)
    cv2.waitKey()


def rotate_without_cropping(angle, img):

    h, w, _ = img.shape
    M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0)
    abs_cos = abs(M[0, 0])
    abs_sin = abs(M[0, 1])
    bound_w = int(h * abs_sin + w * abs_cos)
    bound_h = int(h * abs_cos + w * abs_sin)
    M[0, 2] += bound_w / 2 - w//2
    M[1, 2] += bound_h / 2 - h//2
    rotated = cv2.warpAffine(img, M, (bound_w, bound_h))
    return rotated


def straighten_image(img):

    angle = 100
    iterations = 0
    while (abs(angle) >= 1) and iterations < 10:
        # Text boxes detection
        craft = Craft(output_dir="figures/test", rectify=False, export_extra=False, text_threshold=0.7, link_threshold=0.4,
                      low_text=0.4, cuda=False, long_size=1280, refiner=True, crop_type="box",)
        detected_text = craft.detect_text(image=img)
        # Angle calculation and image rotation
        angle, img = straighten_image_from_text_boxes(img, detected_text)
        iterations += 1
    return img


def straighten_image_from_text_boxes(img, detected_text):

    h, w, _ = img.shape
    box_sizes = np.array(
        [(max(box[:, 0]) - min(box[:, 0]), max(box[:, 1]) - min(box[:, 1])) for box in detected_text["boxes"]])
    largest_dim = np.argmax([np.mean(box_sizes[:, 0]), np.mean(box_sizes[:, 1])])
    i_max = np.argmax(box_sizes[:, largest_dim])
    largest_box = detected_text["boxes"][i_max]
    if largest_dim == 0:
        opposite = -(largest_box[3, 1] - largest_box[2, 1])
        adjacent = largest_box[2, 0] - largest_box[3, 0]
    else:
        opposite = -(largest_box[1, 1] - largest_box[2, 1])
        adjacent = largest_box[2, 0] - largest_box[1, 0]

    angle = np.arctan(opposite / adjacent) / np.pi * 180
    rotated_img = rotate_without_cropping(angle, img)

    return angle, rotated_img


if __name__ == "__main__":

    img = cv2.imread("data/synthetic_forms/cerfa_12485_03_fake1.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    display_image(img, "image brute", resize=True)
    img = straighten_image(img)
    display_image(img, "image redressee", resize=True)
