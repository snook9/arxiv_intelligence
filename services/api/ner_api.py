"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

from .ner_api_interface import NerApiInterface

class NerApi(NerApiInterface):
    """API of the arXiv Intelligence NER web service"""
    def post_document(self: object, pdf_url: str):
        """Post a document URL to arXiv Intelligence web service"""
        print("Document Posted!")
