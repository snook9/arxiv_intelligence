"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

from abc import ABC, abstractmethod

class NerApiInterface(ABC):
    """Interface of the arXiv Intelligence NER web service"""
    @abstractmethod
    def post_document(self: object, doc_url: str):
        """Post a document URL to arXiv Intelligence web service"""
