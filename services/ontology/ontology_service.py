"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

from pathlib import Path
from datetime import datetime
from xml.sax.saxutils import escape
from owlready2 import get_ontology, AllDifferent
from entities.named_entity import NamedEntity, NamedEntityTypeEnum
from entities.named_entity import NamedEntityRelationshipEnum
from entities.document import DocumentEntity

class OntologyService():
    """Ontology service"""

    def __init__(self: object):
        self._onto = get_ontology("file://owl/template-arxiv-intelligence.owl").load()
        try:
            self._foaf = self._onto.get_imported_ontologies().first().load()
        except AttributeError as err:
            print(f"Warning! the foaf ontology is not imported in the local ontology: {err}")
        today = datetime.today().strftime("%Y-%m-%d-%H-%M-%S.%f")
        self._filename = "output_" + today + ".owl"

    @staticmethod
    def _escape_value(text: str) -> str:
        """Escape the illegal characters for an ontology property"""
        if text is None:
            return None
        # function to escape XML character data
        text = escape(text)
        text = text.replace('|', '')
        text = text.replace('\\', '')
        text = text.replace('{', '')
        text = text.replace('}', '')
        text = text.replace('', '')
        text = text.replace('', '')
        text = text.replace('', '')
        text = text.replace('', '')
        text = text.replace('𝒜', '')
        text = text.replace('𝐸', '')
        return text

    @staticmethod
    def _escape_iri(text: str) -> str:
        """For IRI, we replace space character by _"""
        if text is None:
            return None
        text = OntologyService._escape_value(text)
        text = text.replace(' ', '_')
        return text

    def _add_authors(self: object, authors, arxiv_document):
        """Add an authors list to the ontology"""
        for author in authors:
            with self._onto:
                # We create the individual
                author_object = self._onto.Author(self._escape_iri(author.name))
                author_object.has_written.append(arxiv_document)
                # We split the text after the first space
                full_name = author.name.split(" ", 1)
                try:
                    # We suppose the first word is the first name
                    author_object.firstName.append(self._escape_value(full_name[0]))
                except IndexError:
                    pass
                try:
                    # We rest is the last name
                    author_object.lastName.append(self._escape_value(full_name[1]))
                except IndexError:
                    pass

    def _add_primary_category(self: object, category, arxiv_document):
        """Add a primary category to the ontology"""
        with self._onto:
            category_object = self._onto.ArxivDocumentCategory(self._escape_iri(category))
            category_object.title.append(self._escape_value(category))
            arxiv_document.has_as_primary_category.append(category_object)

    def _add_categories(self: object, categories, arxiv_document):
        """Add categories to the ontology"""
        for category in categories:
            with self._onto:
                category_object = self._onto.ArxivDocumentCategory(self._escape_iri(category))
                category_object.title.append(self._escape_value(category))
                arxiv_document.has_as_category.append(category_object)

    def add_document(self: object, document: DocumentEntity):
        """Add an arxiv document to the ontology"""
        with self._onto:
            if document.entry_id is None:
                # If entry_id is not None, we return because entry_id is mandatory
                return None
            # Creating the onto object
            document_object = self._onto.ArxivDocument(self._escape_iri(document.entry_id))
            # Adding all data properties
            document_object.entry_id.append(self._escape_value(document.entry_id))
            if document.updated is not None:
                document_object.updated.append(
                    self._escape_value(document.updated.strftime("%Y-%m-%dT%H:%M:%S"))
                    )
            if document.published is not None:
                document_object.published.append(
                    self._escape_value(document.published.strftime("%Y-%m-%dT%H:%M:%S"))
                    )
            if document.title is not None:
                document_object.title.append(self._escape_value(document.title))
            if document.summary is not None:
                document_object.summary.append(self._escape_value(document.summary))
            if document.comment is not None:
                document_object.comment.append(self._escape_value(document.comment))
            if document.journal_ref is not None:
                document_object.journal_ref.append(self._escape_value(document.journal_ref))
            if document.doi is not None:
                document_object.doi.append(self._escape_value(document.doi))
            if document.pdf_url is not None:
                document_object.pdf_url.append(self._escape_value(document.pdf_url))
            self._add_authors(document.authors, document_object)
            self._add_primary_category(document.primary_category, document_object)
            self._add_categories(document.categories, document_object)
            return document_object

    def add_named_entity(self: object, named_entity: NamedEntity, arxiv_document):
        """Add a named entity to the ontology"""
        if named_entity.type == NamedEntityTypeEnum.PERSON:
            with self._onto:
                # We create the individual
                person = self._foaf.Person(self._escape_iri(named_entity.text))
                # We split the text after the first space
                full_name = named_entity.text.split(" ", 1)
                try:
                    # We suppose the first word is the first name
                    person.firstName.append(self._escape_value(full_name[0]))
                except IndexError:
                    pass
                try:
                    # We rest is the last name
                    person.lastName.append(self._escape_value(full_name[1]))
                except IndexError:
                    pass
                if named_entity.relationship == NamedEntityRelationshipEnum.REFERENCED:
                    person.is_referenced.append(arxiv_document)
                else:
                    person.is_quoted.append(arxiv_document)

                return person

        # Else, we return none
        return None

    def save(self: object, folder: str):
        """Save the current ontology built in an OWL file"""
        # Before to save the ontology, we make sure that all documents are differents
        AllDifferent(self._foaf.Document.instances())

        self._onto.save(str(Path().joinpath(folder, self._filename)))
        return self._filename
