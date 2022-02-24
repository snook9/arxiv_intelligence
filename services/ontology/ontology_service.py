"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

from pathlib import Path
from xml.sax.saxutils import escape
from owlready2 import get_ontology
from entities.named_entity import NamedEntity, NamedEntityTypeEnum
from entities.named_entity import NamedEntityRelationshipEnum
from entities.document import DocumentEntity

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

    def _add_authors(self: object, authors, arxiv_document):
        """Add an authors list to the ontology"""
        for author in authors:
            with self._onto:
                # We escape XML character data
                author.name = escape(author.name)
                # We create the individual
                author_object = self._onto.Author(author.name)
                author_object.has_written.append(arxiv_document)
                arxiv_document.has_as_author.append(author_object)
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

    def add_document(self: object, document: DocumentEntity):
        """Add an arxiv document to the ontology"""
        with self._onto:
            entry_id = escape(document.entry_id)
            document_object = self._onto.ArxivDocument(entry_id)
            document_object.entry_id.append(entry_id)
            document_object.updated.append(escape(document.updated))
            document_object.published.append(escape(document.published))
            document_object.title.append(escape(document.title))
            document_object.summary.append(escape(document.summary))
            document_object.comment.append(escape(document.comment))
            document_object.journal_ref.append(escape(document.journal_ref))
            document_object.doi.append(escape(document.doi))
            document_object.pdf_url.append(escape(document.pdf_url))
            self._add_authors(document.authors, document_object)
            return document_object

    def add_named_entity(self: object, named_entity: NamedEntity, arxiv_document):
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
                if named_entity.relationship == NamedEntityRelationshipEnum.REFERENCED:
                    person.is_referenced.append(arxiv_document)
                    arxiv_document.references.append(person)
                else:
                    person.is_quoted.append(arxiv_document)
                    arxiv_document.quotes.append(person)

                return person

        # Else, we return none
        return None

    def save(self: object, filepath: Path):
        """Save the current ontology built in an OWL file"""
        self._onto.save(filepath)
