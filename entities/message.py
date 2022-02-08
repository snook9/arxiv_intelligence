"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

import json

class MessageEntity:
    """Class for returning a generic message"""

    # ID of the inserted object
    object_id = None
    # Generic user message
    message = ""

    def __init__(self: object, object_id: int = None, message: str = None):
        self.object_id = object_id
        self.message = message

    def get_message(self: object):
        """Returns message"""
        return self.message

    def get_object_id(self: object):
        """Returns ID"""
        return self.object_id

class MessageDecoder(json.JSONDecoder):
    """Class for converting json to full object"""

    def __init__(self: object):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object)

    def dict_to_object(self: object, dictionary):
        """Convert dict to message object"""
        obj = MessageEntity(dictionary["id"], dictionary["message"])
        return obj
