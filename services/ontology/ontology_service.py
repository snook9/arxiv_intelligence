"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

from pathlib import Path
from owlready2 import get_ontology
from xml.sax.saxutils import escape
from entities.named_entity import NamedEntity, NamedEntityTypeEnum

class OntologyService():
    """Ontology service"""

    def __init__(self: object):
        self._onto = get_ontology("file://owl/template-arxiv-intelligence.owl").load()
        #self._foaf = get_namespace("http://xmlns.com/foaf/0.1/")
        #self._foaf = get_ontology("http://xmlns.com/foaf/spec/index.rdf").load()

        try:
            self._foaf = self._onto.get_imported_ontologies().first().load()
        except AttributeError as err:
            print(f"Warning! the foaf ontology is not imported in the local ontology: {err}")

    def add_authors(self: object, authors):
        """Add an authors list to the ontology"""
        for author in authors:
            with self._onto:
                # We escape XML character data
                author.name = escape(author.name)
                # We create the individual
                author_object = self._onto.Author(author.name)
                # We split the text after the first space
                full_name = author.name.split(" ", 1)
                try:
                    # We suppose the first word is the first name
                    author_object.firstName.append(full_name[0])
                except IndexError:
                    pass
                try:
                    # We rest is the last name
                    author_object.lastName.append(full_name[1])
                except IndexError:
                    pass

    def add_named_entity(self: object, named_entity: NamedEntity):
        """Add a named entity to the ontology"""
        if named_entity.type == NamedEntityTypeEnum.PERSON:
            with self._onto:
                # We escape XML character data
                named_entity.text = escape(named_entity.text)
                # We create the individual
                person = self._foaf.Person(named_entity.text)
                # We split the text after the first space
                full_name = named_entity.text.split(" ", 1)
                try:
                    # We suppose the first word is the first name
                    person.firstName.append(full_name[0])
                except IndexError:
                    pass
                try:
                    # We rest is the last name
                    person.lastName.append(full_name[1])
                except IndexError:
                    pass
                return person

        # Else, we return none
        return None

    def save(self: object, filepath: Path):
        """Save the current ontology built in an OWL file"""
        self._onto.save(filepath)
