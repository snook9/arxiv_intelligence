from abc import ABC, abstractmethod

class ApiInterface(ABC):
    """Interface of an ApiController"""
    @abstractmethod
    def getData():
        pass
