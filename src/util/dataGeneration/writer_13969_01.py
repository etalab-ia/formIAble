"""
Ce writer est dédié au Cerfa N°13969*01 :
DÉCLARATION DE LA LISTE DES ASSOCIATIONS MEMBRES D’UNE UNION OU D’UNE FÉDÉRATION D’ASSOCIATIONS
"""

from .baseWriter import Writer

class Writer13969_01(Writer):
    """
    Ce writer est dédié au Cerfa N°13969*01 :
    DÉCLARATION DE LA LISTE DES ASSOCIATIONS MEMBRES D’UNE UNION OU D’UNE FÉDÉRATION D’ASSOCIATIONS
    """

    def __init__(self, **kwargs):
        """
        :param str num_cerfa: Cerfa number
        """
        super().__init__(**kwargs)
        self.D = {
            "name_fields": self.fake.name,
            "title_fields": self.fake['fr-FR'].catch_phrase,
            "adresse_fields": self.fake['fr-FR'].street_address,
            "zip_fields": self.fake['fr-FR'].postcode,
            "city_fields": self.fake['fr-FR'].city,
            "paragraph_fields": self.fill_paragraph,
            "siren_siret_fields": self.fill_siren_siret,
            "txt_pattern": self.fill_txt_pattern,
            "digit_interval_fields": self.fill_digit_interval,
            "date_fields" : self.fill_date,
        }
