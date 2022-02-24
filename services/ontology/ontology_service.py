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
    
    def _escape_value(self: object, text: str):
        """Escape the illegal characters for an ontology property"""
        if text is None:
            return
        # function to escape XML character data
        text = escape(text)
        text = text.replace('|', '')
        text = text.replace('\\', '')
        text = text.replace('{', '')
        text = text.replace('}', '')
        text = text.replace('', '')
        text = text.replace('', '')
        return text

    def _add_authors(self: object, authors, arxiv_document):
        """Add an authors list to the ontology"""
        for author in authors:
            with self._onto:
                # We escape XML character data
                author.name = self._escape_value(author.name)
                # We create the individual
                author_object = self._onto.Author(author.name)
                author_object.has_written.append(arxiv_document)
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

    def _add_primary_category(self: object, category, arxiv_document):
        """Add a primary category to the ontology"""
        with self._onto:
            category = self._escape_value(category)
            category_object = self._onto.ArxivDocumentCategory(category)
            category_object.title.append(category)
            arxiv_document.has_as_primary_category.append(category_object)

    def _add_categories(self: object, categories, arxiv_document):
        """Add categories to the ontology"""
        for category in categories:
            with self._onto:
                category = self._escape_value(category)
                category_object = self._onto.ArxivDocumentCategory(category)
                category_object.title.append(category)
                arxiv_document.has_as_category.append(category_object)

    def add_document(self: object, document: DocumentEntity):
        """Add an arxiv document to the ontology"""
        with self._onto:
            if document.entry_id is not None:
                entry_id = self._escape_value(document.entry_id)
            else:
                # If entry_id is not None, we return because entry_id is mandatory
                return None
            # Creating the onto object
            document_object = self._onto.ArxivDocument(entry_id)
            # Adding all data properties
            document_object.entry_id.append(entry_id)
            if document.updated is not None:
                document_object.updated.append(self._escape_value(document.updated.strftime("%Y-%m-%dT%H:%M:%S")))
            if document.published is not None:
                document_object.published.append(self._escape_value(document.published.strftime("%Y-%m-%dT%H:%M:%S")))
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
                # We escape XML character data
                named_entity.text = self._escape_value(named_entity.text)
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
                else:
                    person.is_quoted.append(arxiv_document)

                return person

        # Else, we return none
        return None

    def save(self: object, filepath: Path):
        """Save the current ontology built in an OWL file"""
        self._onto.save(filepath)
