"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

import urllib.request
from services.api.arxiv_api import ArxivApi

def test_get_pdf():
    """Test the PDF list from arxiv web site"""
    api = ArxivApi()
    # We get all pdf
    pdf_list = api.get_pdf()

    for pdf in pdf_list:
        # For each PDF, we test if the URL exists
        with urllib.request.urlopen(pdf) as response:
            assert response.getcode() == 200
