"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

from entities.named_entity import NamedEntity

class DocumentEntity:
    """Document representation"""

    object_id = None
    status = None
    uploaded_date = None
    author = None
    creator = None
    producer = None
    subject = None
    title = None
    number_of_pages = None
    raw_info = None
    content = None
    named_entities = None

    @staticmethod
    def from_json(data):
        """Convert a json dict to object"""
        obj = DocumentEntity()
        obj.object_id = data["id"]
        obj.status = data["status"]
        obj.uploaded_date = data["uploaded_date"]
        obj.author = data["author"]
        obj.creator = data["creator"]
        obj.producer = data["producer"]
        obj.subject = data["subject"]
        obj.title = data["title"]
        obj.number_of_pages = data["number_of_pages"]
        obj.raw_info = data["raw_info"]
        try:
            obj.named_entities = []
            for item in data["named_entities"]:
                obj.named_entities.append(NamedEntity.from_json(item))
        except KeyError:
            pass
        return obj