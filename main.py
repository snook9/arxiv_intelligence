"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

import sys
import time
from datetime import datetime
from services.api.arxiv_api import ArxivApi
from services.api.ner_api import NerApi
from services.ontology.ontology_service import OntologyService

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
        status = None
        while status != "SUCCESS":
            time.sleep(2)
            document = ner_api.get_document_metadata(message.object_id)
            status = document.status

    ontology_service = OntologyService()
    for named_entity in document.named_entities:
        ontology_service.build_ontology(named_entity)

    today = datetime.today().strftime("%Y-%m-%d-%H-%M-%S.%f")
    ontology_service.save("owl/output_" + today + ".owl")
