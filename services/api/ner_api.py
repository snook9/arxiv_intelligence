"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

import urllib.request
from .ner_api_interface import NerApiInterface

class NerApi(NerApiInterface):
    """API of the arXiv Intelligence NER web service"""
    def _get(self: object, base_url: str, parameters: str):
        try:
            # We open the URL
            with urllib.request.urlopen(base_url + parameters) as response:
                return response.read()
        # Except, error in the given URL
        except ValueError as err:
            print(f"Incorrect URL: {err}")
        except urllib.error.URLError as err:
            print(f"Incorrect URL: {err}")

    def post_document(self: object, doc_url: str):
        """Post a document URL to arXiv Intelligence web service"""
        return self._get("http://localhost:5000/", "?doc_url=" + doc_url)

    def get_document_metadata(self: object, document_id: int):
        """Get metadata form a document"""
        return self._get("http://localhost:5000/", "document/metadata/" + str(document_id))
