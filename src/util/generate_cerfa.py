import datetime
import json
import os
import random
import rstr

import numpy as np
from faker import Faker
from PIL import Image, ImageOps
from PIL import ImageFont
from PIL import ImageDraw
from src.util.utils import ajout_retour_ligne


class Champ:

    def __init__(self, type_champ, proprietes, multiline=False, marge="bas"):
        self.type_champ = type_champ
        self.pos = proprietes["pos"]
        self.donnees = proprietes["type"] if "type" in proprietes.keys() else None
        self.intervalle = proprietes["intervalle"] if "intervalle" in proprietes.keys() else None
        self.min_cochees = proprietes["min_cochees"] if "min_cochees" in proprietes.keys() else None
        self.max_cochees = proprietes["max_cochees"] if "max_cochees" in proprietes.keys() else None
        self.phrases = proprietes["phrases"] if "phrases" in proprietes.keys() else None
        self.regex = proprietes["regex"] if "regex" in proprietes.keys() else None
        self.liste = proprietes["liste"] if "liste" in proprietes.keys() else None
        self.multiline = multiline
        self.marge = marge


class Formulaire:

    def __init__(self, nom, structure):
        self.fake = Faker(locale="fr_FR")
        self.nom = nom
        self.champs_libres = []
        for champ, proprietes in structure["champs_libres"].items():
            multiline = False if isinstance(proprietes["pos"][0], int) else True
            marge = proprietes["marge"] if "marge" in proprietes.keys() else "bas"
            self.champs_libres.append(Champ("libre", proprietes, multiline, marge))
        self.champs_cases = []
        for champ, proprietes in structure["champs_avec_cases"].items():
            self.champs_cases.append(Champ("cases", proprietes))
        self.champs_image = []
        for champ, proprietes in structure["champs_image"].items():
            self.champs_image.append(Champ("libre", proprietes))
        self.cases_a_cocher = []
        for champ, proprietes in structure["cases_a_cocher"].items():
            self.cases_a_cocher.append(Champ("cases_a_cocher", proprietes))

    def creation_fausse_info(self, type_champ, champ, draw, font):

        info = []
        for type_donnes in champ.donnees:
            if type_donnes == "nom":
                info.append(self.fake.last_name())
            elif type_donnes == "prenom":
                info.append(self.fake.first_name())
            elif type_donnes == "nom_prenom":
                info.append(self.fake.name())
            elif type_donnes == "nom_cabinet":
                prefix = np.random.choice(["Cabinet médical", "Centre médical"])
                info.append(f"{prefix} {self.fake.last_name()}\n")
            elif type_donnes == "organisme_emetteur":
                _dep = self.fake.department()
                info.append(f"Préfecture de {_dep[1]} ({_dep[0]})")
            elif type_donnes == "chiffre":
                info.append("".join([str(x) for x in np.random.randint(0, 9, len(champ.pos))]))
            elif type_donnes == "nombre":
                if champ.intervalle is not None:
                    _min_value, _max_value = champ.intervalle
                else:
                    _min_value, _max_value = [1, 100]
                info.append(str(np.random.randint(_min_value, _max_value)))
            elif type_donnes == "adresse":
                info.append(self.fake.address().replace("\n", " "))
            elif type_donnes == "ville":
                info.append(self.fake.city())
            elif type_donnes == "code_postal":
                info.append(self.fake.postcode())
            elif type_donnes == "pays":
                if random.random() <= 0.1:
                    info.append(self.fake.country())
                else:
                    info.append("France")
            elif type_donnes == "extension_adresse":
                _ext = random.choices(["", "bis", "ter"], weights=[0.9, 0.07, 0.03])[0]
                info.append(_ext)
            elif type_donnes == "type_voie":
                info.append(self.fake.street_name().split(' ')[0])
            elif type_donnes == "nom_voie":
                info.append(" ".join(self.fake.street_name().split(' ')[1:]))
            elif type_donnes == "date":
                delta = datetime.datetime.now() - datetime.datetime(1900, 1, 1)
                int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
                random_second = np.random.randint(0, int_delta)
                rand_date = datetime.datetime(1900, 1, 1) + datetime.timedelta(seconds=random_second)
                info.append(rand_date.strftime("%d%m%Y"))
            elif type_donnes == "telephone":
                info.append(" ".join(self.fake.phone_number()))
            elif type_donnes == "email":
                info.append(" ".join(self.fake.ascii_free_email()))
            elif type_donnes == "texte":
                if champ.phrases is not None:
                    _phrases = champ.phrases
                else:
                    _phrases = 3
                info.append(self.fake.paragraph(nb_sentences=_phrases, variable_nb_sentences=True))
            elif type_donnes == "mot":
                info.append(self.fake.word().capitalize())
            elif type_donnes == "element_liste":
                info.append(random.choice(champ.liste))
            elif type_donnes == "regex":
                _num = rstr.xeger(f'{champ.regex}')
                info.append(_num)
            else:
                info.append("")

        info = " ".join(info)
        if type_champ == "cases":
            return zip(champ.pos, [*info])
        if type_champ == "cases":
            return zip(champ.pos, [*info])
        elif type_champ == "champ_libre":
            if champ.multiline:
                info_lines = []
                for n in range(len(champ.pos)):
                    if len(info) == 0:
                        info_lines.append("")
                        continue
                    _, _, w, _ = draw.multiline_textbbox((0, 0), info, font=font)
                    splitted_info = info.split(" ")
                    i_max = len(splitted_info)
                    info_cut = info
                    while w > champ.pos[n][2]:
                        i_max += -1
                        info_cut = " ".join(splitted_info[:i_max])
                        _, _, w, _ = draw.multiline_textbbox((0, 0), info_cut, font=font)
                    info_lines.append(info_cut)
                    info = " ".join(splitted_info[i_max:])
                return zip(champ.pos, info_lines, [font for _ in range(len(champ.pos))])
            else:
                _, _, w, h = draw.multiline_textbbox((0, 0), info, font=font)
                while w > champ.pos[2]:
                    _, _, w, h = draw.multiline_textbbox((0, 0), info, font=font)
                    font = ImageFont.truetype(font.path.split("/")[-1].replace(".ttf", ""), font.size - 1)
                while h > champ.pos[3]:
                    _, _, w, h = draw.multiline_textbbox((0, 0), info, font=font)
                    font = ImageFont.truetype(font.path.split("/")[-1].replace(".ttf", ""), font.size - 1)
                return zip([champ.pos], [info], [font])

    def generation_faux_exemplaire(self, _cerfa_path, font, color_list):

        image = Image.open(_cerfa_path)
        draw = ImageDraw.Draw(image)
        x_noise_range = 0.02
        y_noise_range = 0.05
        for champ in self.champs_cases:
            largeur_moyenne_case = np.mean([x[2] for x in champ.pos])
            hauteur_moyenne_case = np.mean([x[3] for x in champ.pos])
            x_eps = np.random.randint(0, max(1, int(x_noise_range * largeur_moyenne_case)))
            y_eps = np.random.randint(0, max(1, int(y_noise_range * hauteur_moyenne_case)))
            color = np.random.choice(list(color_list.keys()))
            fausse_info = self.creation_fausse_info("cases", champ, draw, font)
            for box, text in fausse_info:
                draw.text((box[0] + x_eps, box[1] - y_eps), text, color_list[color], font=font)
        for champ in self.champs_libres:
            sign = -1 if champ.marge == "bas" else 1
            largeur_moyenne_case = np.mean([x[2] for x in champ.pos]) if champ.multiline else champ.pos[2]
            hauteur_moyenne_case = np.mean([x[3] for x in champ.pos]) if champ.multiline else champ.pos[3]
            x_eps = np.random.randint(0, min(10, max(1, int(x_noise_range * largeur_moyenne_case))))
            y_eps = np.random.randint(0, min(20, max(1, int(y_noise_range * hauteur_moyenne_case))))
            color = np.random.choice(list(color_list.keys()))
            fausse_info = self.creation_fausse_info("champ_libre", champ, draw, font)
            for box, text, box_font in fausse_info:
                _, _, w, _ = draw.multiline_textbbox((0, 0), text, font=box_font)
                if w > box[2]:
                    text = ajout_retour_ligne(text, box[2] - x_eps, font, draw)
                draw.text((box[0] + x_eps, box[1] + sign * y_eps), text, color_list[color], font=box_font)
        for champ in self.champs_image:
            chosen_signature = np.random.choice(os.listdir('data/signatures'))
            signature = Image.open(os.path.join('data/signatures', chosen_signature))
            signature = signature.resize((champ.pos[2], champ.pos[3]))
            image.paste(signature, (champ.pos[0], champ.pos[1]))
        for champ in self.cases_a_cocher:
            largeur_moyenne_case = np.mean([x[2] for x in champ.pos])
            hauteur_moyenne_case = np.mean([x[3] for x in champ.pos])
            x_eps = np.random.randint(0, max(1, int(x_noise_range * largeur_moyenne_case)))
            y_eps = np.random.randint(0, max(1, int(y_noise_range * hauteur_moyenne_case)))
            color = np.random.choice(list(color_list.keys()))
            n_coches = random.randint(champ.min_cochees, champ.max_cochees)
            coches = ["X" for _ in range(n_coches)] + ["" for _ in range(len(champ.pos) - n_coches)]
            random.shuffle(coches)
            for coche, box in zip(coches, champ.pos):
                draw.text((box[0] + box[2] / 4 + x_eps, box[1] + y_eps), coche, color_list[color], font=font)

        return image


def creation_faux_cerfa_non_editables(nom_cerfa, _cerfa_structure, _cerfa_path, n_cerfa):

    cerfa = Formulaire(nom_cerfa, _cerfa_structure)
    with open("data/synthetic_forms/usable_fonts.json", "r") as file:
        all_fonts = json.load(file)["fonts"]
    font_list = []
    for font in all_fonts:
        font_list.append(ImageFont.truetype(font, 40))
    color_list = {"noir": (1, 1, 1)}
    for n in range(n_cerfa):
        font = np.random.choice(font_list)
        image = cerfa.generation_faux_exemplaire(_cerfa_path, font, color_list)
        add_rotation, make_grayscale, add_noise = [x > 0.5 for x in np.random.random(3)]
        if add_rotation:
            image = image.rotate((np.random.random() - 0.5) * 6, expand=True)
        if make_grayscale:
            image = ImageOps.grayscale(image)
        if make_grayscale and add_noise:
            gaussian = np.random.normal(0, 10, (image.size[1], image.size[0]))
            image = Image.fromarray(image + gaussian)
        font_name = font.path.split("/")[-1].replace(".ttf", "")
        save_dir = f"data/synthetic_forms"
        if not os.path.isdir(save_dir):
            os.mkdir(save_dir)
        image.convert('RGB').save(os.path.join(save_dir, f"{n}_{font_name}.jpg"))


if __name__ == "__main__":

    cerfa_path: str = "data/empty_forms/non-editable/cerfa_13749_05.png"
    with open("data/elements_to_fill_forms/non-editable/cerfa_13749_05.json", "r") as f:
        cerfa_structure = json.load(f)
    creation_faux_cerfa_non_editables(nom_cerfa="cerfa_113749_05", _cerfa_structure=cerfa_structure,
                                      _cerfa_path=cerfa_path, n_cerfa=10)
