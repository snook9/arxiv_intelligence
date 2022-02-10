"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

import json
import sys
import time
from services.api.arxiv_api import ArxivApi
from services.api.ner_api import NerApi

if __name__ == '__main__':

    print("arXiv Intelligence v0.0.1")

    pdf_list = ArxivApi().get_pdf()
    for pdf in pdf_list:
        print("PDF:", pdf)

    ner_api = NerApi()
    message = ner_api.post_document(pdf_list.pop())
    if message is None:
        sys.exit()

    print("ID:", message.object_id)
    print("MSG:", message.message)

    if message.object_id != -1:
        STATUS = None
        while STATUS != "SUCCESS":
            time.sleep(2)
            data = ner_api.get_document_metadata(message.object_id)
            data = json.loads(data)
            STATUS = data["status"]
            print(data)
