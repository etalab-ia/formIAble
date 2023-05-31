"""
Ce writer est dédié au Cerfa N°13753*04 :
DÉCLARATION DE LA PERTE/VOL DE CERTIFICAT D’IMMATRICULATION D’UN VÉHICULE
"""

from .baseWriter import Writer

class Writer13753_04(Writer):
    """
    Ce writer est dédié au Cerfa N°13753*04 :
    DÉCLARATION DE LA PERTE/VOL DE CERTIFICAT D’IMMATRICULATION D’UN VÉHICULE
    """

    def __init__(self,  **kwargs):
        """
        :param str num_cerfa: Cerfa number
        """
        super().__init__( **kwargs)
        self.D = {
            "name_fields": self.fake.name,
            # "lieu_fields": self.fake['fr-FR'].catch_phrase,
            "digit_interval_fields": self.fill_digit_interval,
            "date_fields": self.fill_date,
            "city_fields": self.fake['fr-FR'].city,
            "zip_fields": self.fake['fr-FR'].postcode,
            "paragraph_fields": self.fill_paragraph,
            "choice": self.choice,
            "street_prefix_fields": self.fake['fr-FR'].street_prefix,
            "street_name_fields": self.fake['fr-FR'].street_name,
            "immat_fields":self.fake['fr-FR'].license_plate,
            "car_brand_fields": self.fake.vehicle_make,
            "car_fields":   self.fake.vehicle_make_model,
            "siret_fields": self.fill_siret,
        }
