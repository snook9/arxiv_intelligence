"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

from entities.named_entity import NamedEntity

class DocumentEntity:
    """Document representation"""

    # Field from arXiv Intelligence NER API
    object_id = None
    status = None
    number_of_pages = None
    raw_info = None
    named_entities = None
    # Fields from arxiv python api
    entry_id = None
    updated = None
    published = None
    title = None
    authors = None
    summary = None
    comment = None
    journal_ref = None
    doi = None
    primary_category = None
    categories = None
    pdf_url = None

    @staticmethod
    def from_json(data):
        """Convert a json dict to object"""
        obj = DocumentEntity()
        obj.object_id = data["id"]
        obj.status = data["status"]
        obj.number_of_pages = data["number_of_pages"]
        obj.raw_info = data["raw_info"]
        try:
            obj.named_entities = []
            for item in data["named_entities"]:
                obj.named_entities.append(NamedEntity.from_json(item))
        except KeyError:
            pass
        try:
            obj.entry_id = data["entry_id"]
        except KeyError:
            pass
        try:
            obj.updated = data["updated"]
        except KeyError:
            pass
        try:
            obj.published = data["published"]
        except KeyError:
            pass
        try:
            obj.title = data["title"]
        except KeyError:
            pass
        try:
            obj.authors = data["authors"]
        except KeyError:
            pass
        try:
            obj.summary = data["summary"]
        except KeyError:
            pass
        try:
            obj.comment = data["comment"]
        except KeyError:
            pass
        try:
            obj.journal_ref = data["journal_ref"]
        except KeyError:
            pass
        try:
            obj.doi = data["doi"]
        except KeyError:
            pass
        try:
            obj.primary_category = data["primary_category"]
        except KeyError:
            pass
        try:
            obj.categories = data["categories"]
        except KeyError:
            pass
        try: 
            obj.pdf_url = data["pdf_url"]
        except KeyError:
            pass
        return obj
