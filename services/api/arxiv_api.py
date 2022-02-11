"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

import arxiv
from .arxiv_api_interface import ArxivApiInterface

class ArxivApi(ArxivApiInterface):
    """Arxiv Api using arxiv python library"""

    def __init__(self: object, max_results: int = 10):
        self.max_results = max_results

    def get_pdf(self: object):
        """Returns the pdf list from arxiv web site"""
        search = arxiv.Search(
            # Only IA subject
            query = "cat:cs.AI",
            max_results = self.max_results,
            sort_by = arxiv.SortCriterion.SubmittedDate
        )

        pdf_list = []
        for result in search.results():
            #print("Categories:", result.categories)
            pdf_list.append(result.pdf_url)

        return pdf_list
