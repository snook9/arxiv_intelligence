"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

import json
import urllib.request
from entities.message import MessageEntity
from entities.document import DocumentEntity
from .ner_api_interface import NerApiInterface

class NerApi(NerApiInterface):
    """API of the arXiv Intelligence NER web service"""

    def __init__(self: object, base_ws_url: str = "http://localhost:5000/"):
        self.base_url = base_ws_url

    @staticmethod
    def _get(base_url: str, parameters: str):
        try:
            # We open the URL
            with urllib.request.urlopen(base_url + parameters) as response:
                return response.read()
        # Except, error in the given URL
        except ValueError as err:
            print(f"Incorrect URL: {err}")
        except urllib.error.URLError as err:
            print(f"Incorrect URL: {err}")

        return None

    def post_document(self: object, doc_url: str) -> MessageEntity:
        """Post a document URL to arXiv Intelligence web service"""
        data = self._get(self.base_url, "?doc_url=" + doc_url)
        if data is None:
            return None
        return MessageEntity.from_json(json.loads(data))

    def get_document_metadata(self: object, document_id: int) -> DocumentEntity:
        """Get metadata form a document"""
        data = self._get(self.base_url, "document/metadata/" + str(document_id))
        if data is None:
            return None
        return DocumentEntity.from_json(json.loads(data))
