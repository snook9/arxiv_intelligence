"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

from abc import ABC, abstractmethod
from entities.message import MessageEntity
from entities.document import DocumentEntity

class NerApiInterface(ABC):
    """Interface of the arXiv Intelligence NER web service"""
    @abstractmethod
    def post_document(self: object, doc_url: str) -> MessageEntity:
        """Post a document URL to arXiv Intelligence web service"""

    @abstractmethod
    def get_document_metadata(self: object, document_id: int) -> DocumentEntity:
        """Get metadata form a document"""
