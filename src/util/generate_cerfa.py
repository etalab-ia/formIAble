import datetime
import json
import os
import numpy as np
from faker import Faker
from PIL import Image, ImageOps
from PIL import ImageFont
from PIL import ImageDraw
from src.util.utils import ajout_retour_ligne


class Champ:

    def __init__(self, type, position, donnees, multiline=False, marge="bas"):
        self.type = type
        self.pos = position
        self.donnees = donnees
        self.multiline = multiline
        self.marge = marge


class Formulaire:

    def __init__(self, nom, structure):
        self.fake = Faker(locale="fr_FR")
        self.nom = nom
        self.champs_libres = []
        for champ, prop in structure["champs_libres"].items():
            multiline = False if isinstance(prop["pos"][0], int) else True
            marge = prop["marge"] if "marge" in prop.keys() else "bas"
            self.champs_libres.append(Champ("libre", prop["pos"], prop["type"], multiline, marge))
        self.champs_cases = []
        for champ, prop in structure["champs_avec_cases"].items():
            self.champs_cases.append(Champ("cases", prop["pos"], prop["type"]))
        self.champs_image = []
        for champ, prop in structure["champs_image"].items():
            self.champs_image.append(Champ("libre", prop["pos"], prop["type"]))

    def creation_fausse_info(self, type, champ):

        info = []
        for type_donnes in champ.donnees:
            if type_donnes == "nom":
                info.append(self.fake.last_name())
            elif type_donnes == "prenom":
                info.append(self.fake.first_name())
            elif type_donnes == "nom_cabinet":
                prefix = np.random.choice(["Cabinet médical", "Centre médical"])
                info.append(f"{prefix} {self.fake.last_name()}\n")
            elif type_donnes == "adresse":
                info.append(self.fake.address().replace("\n", " "))
            elif type_donnes == "numero":
                info.append("".join([str(x) for x in np.random.randint(0, 9, len(champ.pos))]))
            elif type_donnes == "date":
                delta = datetime.datetime.now() - datetime.datetime(1900, 1, 1)
                int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
                random_second = np.random.randint(0, int_delta)
                rand_date = datetime.datetime(1900, 1, 1) + datetime.timedelta(seconds=random_second)
                info.append(rand_date.strftime("%d%m%Y"))
            else:
                info.append("")

        info = " ".join(info)
        if type == "cases":
            return zip(champ.pos, [*info])
        if type == "cases":
            return zip(champ.pos, [*info])
        elif type == "champ_libre":
            if champ.multiline:
                splitted_info = info.split(" ")
                ind = sorted(set(np.random.randint(1, len(splitted_info), len(champ.pos) - 1)))
                info = []
                i_prev = 0
                for i in ind:
                    info.append(" ".join(splitted_info[i_prev:i]))
                    i_prev = i
                info.append(" ".join(splitted_info[i:]))
                return zip(champ.pos[:len(ind)+1], info)
            else:
                return zip([champ.pos], [info])

    def generation_faux_exemplaire(self, cerfa_path, font, color_list):

        image = Image.open(cerfa_path)
        draw = ImageDraw.Draw(image)
        for champ in self.champs_cases:
            largeur_moyenne_case = np.mean([x[2] for x in champ.pos])
            hauteur_moyenne_case = np.mean([x[3] for x in champ.pos])
            x_eps = np.random.randint(0, int(0.1 * largeur_moyenne_case))
            y_eps = np.random.randint(0, int(0.1 * hauteur_moyenne_case))
            color = np.random.choice(list(color_list.keys()))
            fausse_info = self.creation_fausse_info("cases", champ)
            for box, text in fausse_info:
                draw.text((box[0] + x_eps, box[1] - y_eps), text, color_list[color], font=font)
        for champ in self.champs_libres:
            sign = -1 if champ.marge == "bas" else 1
            largeur_moyenne_case = np.mean([x[2] for x in champ.pos]) if champ.multiline else champ.pos[2]
            hauteur_moyenne_case = np.mean([x[3] for x in champ.pos]) if champ.multiline else champ.pos[3]
            x_eps = np.random.randint(10, min(20, int(0.1 * largeur_moyenne_case)))
            y_eps = np.random.randint(0, min(20, int(0.1 * hauteur_moyenne_case)))
            color = np.random.choice(list(color_list.keys()))
            fausse_info = self.creation_fausse_info("champ_libre", champ)
            for box, text in fausse_info:
                _, _, w, _ = draw.multiline_textbbox((0, 0), text, font=font)
                if w > box[2]:
                    text = ajout_retour_ligne(text, box[2] - x_eps, font, draw)
                draw.text((box[0] + x_eps, box[1] + sign * y_eps), text, color_list[color], font=font)
        for champ in self.champs_image:
            chosen_signature = np.random.choice(os.listdir('data/signatures'))
            signature = Image.open(os.path.join('data/signatures', chosen_signature))
            signature = signature.resize((champ.pos[2], champ.pos[3]))
            image.paste(signature, (champ.pos[0], champ.pos[1]))
        return image


def creation_faux_cerfa(nom_cerfa, cerfa_structure, cerfa_path, n_cerfa):

    cerfa = Formulaire(nom_cerfa, cerfa_structure)
    with open("data/usable_fonts.json", "r") as f:
        all_fonts = json.load(f)["fonts"]
    font_list = []
    for font in all_fonts:
        font_list.append(ImageFont.truetype(font, 60))
    color_list = {"noir": (1, 1, 1)}
    for n in range(n_cerfa):
        font = np.random.choice(font_list)
        image = cerfa.generation_faux_exemplaire(cerfa_path, font, color_list)
        add_rotation, make_grayscale, add_noise = [x > 0.5 for x in np.random.random(3)]
        if add_rotation:
            image = image.rotate((np.random.random() - 0.5) * 6, expand=True)
        if make_grayscale:
            image = ImageOps.grayscale(image)
        if make_grayscale and add_noise:
            gaussian = np.random.normal(0, 10, (image.size[1], image.size[0]))
            image = Image.fromarray(image + gaussian)
        font_name = font.path.split("/")[-1].replace(".ttf", "")
        image.convert('RGB').save(f"data/CERFA/fake/{n}_{font_name}.jpg")


if __name__ == "__main__":

    cerfa_path: str = "data/empty_forms/non-editable/cerfa_12485_03.png"
    with open("data/elements_to_fill_forms/non-editable/cerfa_12485_03.json", "r") as f:
        cerfa_structure: dict[str, dict[str, dict[str, list]]] = json.load(f)
    creation_faux_cerfa(nom_cerfa="cerfa_12485_03",
                        cerfa_structure=cerfa_structure,
                        cerfa_path=cerfa_path,
                        n_cerfa=1)
