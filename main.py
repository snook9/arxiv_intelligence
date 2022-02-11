"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

import time
import logging
from pathlib import Path
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

    # We create the log folder
    log_folder = Path("log")
    if False is log_folder.exists():
        # If the folder doesn't exist, we create it
        log_folder.mkdir()
    # Creating log config
    today = datetime.today().strftime("%Y-%m-%d-%H-%M-%S.%f")
    logging.basicConfig(filename=log_folder.joinpath(today + ".log"), encoding='utf-8', level=logging.DEBUG)

    # We retreive the PDF documents
    pdf_list = ArxivApi(MAX_PDF_NUMBER).get_pdf()
    print(len(pdf_list), "PDF file(s) retrieved")
    logging.info("%s PDF file(s) retrieved", len(pdf_list))

    # We instantiate an ontology
    ontology_service = OntologyService()

    # For each PDF document
    for pdf in pdf_list:
        # We give the PDF URL to the NER Web Service
        ner_api = NerApi(BASE_WS_URL)
        message = ner_api.post_document(pdf)
        if message is None:
            logging.error("Error while sending the file: %s", pdf)
            continue

        logging.info("ID: %s | %s", message.object_id, message.message)

        # If the PDF has been sent
        if message.object_id != -1:
            STATUS = None
            # We get the metadata of the PDF
            # As the process is async, we try the request several times
            while STATUS != "SUCCESS":
                time.sleep(3)
                document = ner_api.get_document_metadata(message.object_id)
                STATUS = document.status

            logging.info("ID: %s | named entities retrieved", message.object_id)

            # Then, we add each named entity of the document
            # to the ontology
            for named_entity in document.named_entities:
                ontology_service.add_named_entity(named_entity)

            logging.info("ID: %s | named entities added to the ontology", message.object_id)

    # At the end of the PDF list
    # We write the ontology in a folder
    filepath = "owl/output_" + today + ".owl"
    ontology_service.save(filepath)
    print("The ontology '" + filepath + "' has been saved!")
    logging.info("The ontology '%s' has been saved!", filepath)
