from .generate_pdf import VysledkyService as generatePdf
from .get_data import VysledkyService as getData

class VysledkyService (generatePdf, getData):
    pass