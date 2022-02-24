"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

import arxiv
from entities.document import DocumentEntity
from .arxiv_api_interface import ArxivApiInterface

class ArxivApi(ArxivApiInterface):
    """Arxiv Api using arxiv python library"""

    def __init__(self: object, max_results: int = 10):
        self.max_results = max_results

    def get_documents(self: object):
        """Returns the pdf list from arxiv web site"""
        search = arxiv.Search(
            # Only IA subject
            query = "cat:cs.AI",
            max_results = self.max_results,
            sort_by = arxiv.SortCriterion.SubmittedDate
        )

        documents = []
        for result in search.results():
            document = DocumentEntity()
            document.entry_id = result.entry_id
            document.updated = result.updated
            document.published = result.published
            document.title = result.title
            document.authors = result.authors
            document.summary = result.summary
            document.comment = result.comment
            document.journal_ref = result.journal_ref
            document.doi = result.doi
            document.primary_category = result.primary_category
            document.categories = result.categories
            document.pdf_url = result.pdf_url
            documents.append(document)

        return documents
