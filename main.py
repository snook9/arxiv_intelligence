"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

import time
from datetime import datetime
from services.api.arxiv_api import ArxivApi
from services.api.ner_api import NerApi
from services.ontology.ontology_service import OntologyService

if __name__ == '__main__':
    # Maximum PDF number retreived from arxiv
    MAX_PDF_NUMBER = 2
    # Base URL of the NER Web Service
    BASE_WS_URL = "http://localhost:5000/"

    print("arXiv Intelligence v0.0.1")

    # We retreive the PDF documents
    pdf_list = ArxivApi(MAX_PDF_NUMBER).get_pdf()
    print(len(pdf_list), "PDF file(s) retrieved")

    # We instantiate an ontology
    ontology_service = OntologyService()

    # For each PDF document
    for pdf in pdf_list:
        # We give the PDF URL to the NER Web Service
        ner_api = NerApi(BASE_WS_URL)
        message = ner_api.post_document(pdf)
        if message is None:
            print("Error while sending the file", pdf)
            continue

        print("ID:", message.object_id, "|", message.message)

        # If the PDF has been sent
        if message.object_id != -1:
            STATUS = None
            # We get the metadata of the PDF
            # As the process is async, we try the request several times
            while STATUS != "SUCCESS":
                time.sleep(3)
                document = ner_api.get_document_metadata(message.object_id)
                STATUS = document.status

            print("ID:", message.object_id, "|", "named entities retrieved")

            # Then, we add each named entity of the document
            # to the ontology
            for named_entity in document.named_entities:
                ontology_service.add_named_entity(named_entity)

            print("ID:", message.object_id, "|", "named entities added to the ontology")

    # At the end of the PDF list
    # We write the ontology in a folder
    today = datetime.today().strftime("%Y-%m-%d-%H-%M-%S.%f")
    filepath = "owl/output_" + today + ".owl"
    ontology_service.save(filepath)
    print("The ontology '" + filepath + "' has been saved!")
