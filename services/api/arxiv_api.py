"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

import arxiv
from .api_interface import ApiInterface

class ArxivApi(ApiInterface):
    """Arxiv Api using arxiv python library"""
    def get_pdf(self: object):
        """Returns the pdf list from arxiv web site"""
        search = arxiv.Search(
            # Only IA subject
            query = "cat:cs.AI",
            max_results = 10,
            sort_by = arxiv.SortCriterion.SubmittedDate
        )

        pdf_list = []
        for result in search.results():
            #print("Categories:", result.categories)
            pdf_list.append(result.pdf_url)

        return pdf_list
