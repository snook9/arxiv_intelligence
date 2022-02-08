from abc import ABC, abstractmethod

class ApiInterface(ABC):
    """Interface of an ApiController"""
    @abstractmethod
    def get_pdf(self: object):
        pass
