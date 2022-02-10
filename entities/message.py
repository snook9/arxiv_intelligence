"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

class MessageEntity:
    """Class for returning a generic message"""

    # ID of the inserted object
    object_id = None
    # Generic user message
    message = ""

    def __init__(self: object, object_id: int = None, message: str = None):
        self.object_id = object_id
        self.message = message

    @staticmethod
    def from_json(data):
        """Convert a json dict to object"""
        return MessageEntity(data["id"], data["message"])
