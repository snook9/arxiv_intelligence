"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

import json
from entities.message import MessageDecoder
from services.api.arxiv_api import ArxivApi
from services.api.ner_api import NerApi

if __name__ == '__main__':

    print("arXiv Intelligence v0.0.1")

    pdf_list = ArxivApi().get_pdf()
    for pdf in pdf_list:
        print("PDF:", pdf)

    ner_api = NerApi()
    data = ner_api.post_document(pdf_list.pop())

    message = json.loads(data, object_hook=MessageDecoder().dict_to_object)
    print("ID:", message.object_id)
    print("MSG:", message.message)
