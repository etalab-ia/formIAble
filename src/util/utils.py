from pdf2image import convert_from_path
import os


def ajout_retour_ligne(text, max_length, font, draw):

    new_text = text
    splitted_text = text.split(" ")
    i_start = 0
    for i in range(1, len(splitted_text) + 1):
        if "\n" in splitted_text[i-1]:
            i_start = i
        _, _, size, _ = draw.multiline_textbbox((0, 0), " ".join(splitted_text[i_start:i]), font=font)
        if size > max_length:
            new_text = " ".join(splitted_text[:i-1]) + "\n" + " ".join(splitted_text[i-1:])
            new_text = ajout_retour_ligne(new_text, max_length, font, draw)
    return new_text


def convert_pdf_to_png(pdf_path):

    pages = convert_from_path(pdf_path, 350)
    file_name = pdf_path.split("/")[-1]
    directory_path = pdf_path.replace(file_name, "")
    file_name = file_name.replace(".pdf", "")

    for i, page in enumerate(pages):
        image_name = f"{file_name}_p{i+1}.png"
        page.save(os.path.join(directory_path, image_name), "PNG")
