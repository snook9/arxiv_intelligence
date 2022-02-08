"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

import urllib.request
from .ner_api_interface import NerApiInterface

class NerApi(NerApiInterface):
    """API of the arXiv Intelligence NER web service"""
    def post_document(self: object, doc_url: str):
        """Post a document URL to arXiv Intelligence web service"""
        try:
            # We open the URL
            with urllib.request.urlopen("http://localhost:5000/?doc_url=" + doc_url) as response:
                return response.read()
        # Except, error in the given URL
        except ValueError as err:
            print(f"Incorrect URL: {err}")
        except urllib.error.URLError as err:
            print(f"Incorrect URL: {err}")
