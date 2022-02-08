"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

from abc import ABC, abstractmethod

class ArxivApiInterface(ABC):
    """Interface of Arxiv web site"""
    @abstractmethod
    def get_pdf(self: object):
        """Returns the PDF list from arxiv"""
