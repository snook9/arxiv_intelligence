"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

from enum import Enum

class NamedEntityScoreEnum(Enum):
    """Enum for the score of a named entity"""
    # The score is based on the number of models that detect the entity.
    # The used models are AWS Comprehend, NLTK and Spacy
    # The score is high if all models detected the entity
    HIGH = "HIGH"
    # The score is medium if 2 models detected the entity
    MEDIUM = "MEDIUM"
    # The score is low if only 1 model detected the entity
    LOW = "LOW"

class NamedEntityTypeEnum(Enum):
    """Enum for the type of a named entity"""
    # A branded product
    PRODUCT = "PRODUCT"
    # A full date (for example, 11/25/2017), day (Tuesday), month (May), or time (8:30 a.m.)
    DATE = "DATE"
    # An event, such as a festival, concert, election, etc.
    EVENT = "EVENT"
    # A specific location, such as a country, city, lake, building, etc.
    LOCATION = "LOCATION"
    # Large organizations, such as a government, company, religion, sports team, etc.
    ORGANIZATION = "ORGANIZATION"
    # Individuals, groups of people, nicknames, fictional characters
    PERSON = "PERSON"
    # A quantified amount, such as currency, percentages, numbers, bytes, etc.
    QUANTITY = "QUANTITY"
    # An official name given to any creation or creative work, such as movies, books, songs, etc.
    TITLE = "TITLE"
    # Entities that don't fit into any of the other entity categories
    OTHER = "OTHER"

class NamedEntityRelationshipEnum(Enum):
    """Enum for the relationship a named entity"""
    # The named entity is quoted in a document
    QUOTED = "QUOTED"
    # The named entity is referenced in a document
    REFERENCED = "REFERENCED"

class NamedEntity:
    """Named entity class"""
    text: str
    score: NamedEntityScoreEnum
    # Score in percentage given by AWS Comprehend only
    aws_score: float
    type: NamedEntityTypeEnum
    begin_offset: int
    end_offset: int
    relationship: NamedEntityRelationshipEnum

    @staticmethod
    def from_json(data):
        """Convert a json dict to object"""
        obj = NamedEntity()
        obj.text = data["text"]
        obj.score = NamedEntityScoreEnum(data["score"])
        try:
            obj.aws_score = data["aws_score"]
        except KeyError:
            pass
        obj.type = NamedEntityTypeEnum(data["type"])
        obj.begin_offset = data["begin_offset"]
        obj.end_offset = data["end_offset"]
        obj.relationship = data["relationship"]
        return obj
