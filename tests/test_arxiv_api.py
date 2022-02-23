"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

import urllib.request
from services.api.arxiv_api import ArxivApi

def test_get_documents():
    """Test the PDF list from arxiv web site"""
    api = ArxivApi(1)
    # We get a document
    documents = api.get_documents()

    for document in documents:
        # For each PDF, we test if the URL exists
        with urllib.request.urlopen(document.pdf_url) as response:
            assert response.getcode() == 200
