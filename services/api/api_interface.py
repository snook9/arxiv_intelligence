"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

from abc import ABC, abstractmethod

class ApiInterface(ABC):
    """Interface of an ApiController"""
    @abstractmethod
    def get_pdf(self: object):
        """Returns the PDF list from arxiv"""
