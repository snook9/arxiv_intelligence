"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

import time
import logging
import getopt
import sys
from pathlib import Path
from datetime import datetime
from progress.bar import IncrementalBar
from services.api.arxiv_api import ArxivApi
from services.api.ner_api import NerApi
from services.ontology.ontology_service import OntologyService

PROGRAM_NAME = "arXiv Intelligence"
PROGRAM_VERSION = "0.0.1"

def print_help(script_name: str):
    """Show the software CLI help"""
    print(script_name, '[options]\n'
                       'This software highlights the relationships between authors and scientists, '
                       'from articles published on arxiv.org.'
                       'For this, it generates an ontology (owl file), '
                       'from the named entities located in the articles.\n'
                       'After execution, the owl file is generated in the owl folder.\n'
                       'The category is fixed to cs.AI.\n'
                       '\t-h | --help\t\t\t: show this help\n'
                       '\t-v | --version\t\t\t: show the version of this software\n'
                       '\t-w | --webservice=[url]\t: set the url of the named entities web service '
                       '(you must use an instance of the following web service: '
                       'https://github.com/snook9/arxiv_intelligence_ner_ws)\n'
                       'default value is http://localhost:5000/\n'
                       '\t-n | --number=[value]\t: '
                       'set the max articles number extracted from arxiv.org\n'
                       'default value is 1')

def parse_opt(script_name: str, argv):
    """Parse options from CLI"""
    options = {"webservice": "http://localhost:5000/", "number": 2}
    try:
        opts, _ = getopt.getopt(argv, "hvw:n:", ["help", "version", "webservice=", "number="])
    except getopt.GetoptError:
        print_help(script_name)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help(script_name)
            sys.exit()
        elif opt in ("-v", "--version"):
            print(PROGRAM_NAME, PROGRAM_VERSION)
            sys.exit()
        elif opt in ("-w", "--webservice"):
            options["webservice"] = arg
        elif opt in ("-n", "--number"):
            options["number"] = int(arg)

    return options

if __name__ == '__main__':
    cli_options = parse_opt(sys.argv[0], sys.argv[1:])

    print(PROGRAM_NAME, PROGRAM_VERSION)

    # We create the log folder
    log_folder = Path("log")
    if False is log_folder.exists():
        # If the folder doesn't exist, we create it
        log_folder.mkdir()
    # Creating log config
    today = datetime.today().strftime("%Y-%m-%d-%H-%M-%S.%f")
    logging.basicConfig(filename=log_folder.joinpath(today + ".log"), level=logging.DEBUG)

    # We retreive the PDF documents
    documents = ArxivApi(cli_options["number"]).get_documents()
    print(len(documents), "PDF file(s) retrieved")
    logging.info("%s PDF file(s) retrieved", len(documents))

    # We instantiate an ontology
    ontology_service = OntologyService()

    # We create a progress bar
    progress_bar = IncrementalBar('Processed files', max = len(documents))

    # For each PDF document
    for document in documents:
        # We give the PDF URL to the NER Web Service
        ner_api = NerApi(cli_options["webservice"])
        message = ner_api.post_document(document.pdf_url)
        if message is None:
            logging.error("Error while sending the file: %s", document.pdf_url)
            continue

        logging.info("ID: %s | %s", message.object_id, message.message)

        # If the PDF has been sent
        if message.object_id != -1:
            # Here, all it's ok, so we save the object id
            document.object_id = message.object_id
            # We get the metadata of the PDF
            # As the process is async, we try the request several times
            while document.status != "SUCCESS":
                time.sleep(2)
                document_metadata = ner_api.get_document_metadata(document.object_id)
                # We keep the metadata
                document.number_of_pages = document_metadata.number_of_pages
                document.raw_info = document_metadata.raw_info
                document.named_entities = document_metadata.named_entities
                document.status = document_metadata.status

            logging.info("ID: %s | named entities retrieved", document.object_id)

            # Then, we add each named entity of the document
            # to the ontology
            arxiv_onto_document = ontology_service.add_document(document)
            for named_entity in document.named_entities:
                ontology_service.add_named_entity(named_entity, arxiv_onto_document)

            logging.info("ID: %s | named entities added to the ontology", document.object_id)
            progress_bar.next()

            # At the end of the PDF
            # We write the ontology in a folder
            filename = ontology_service.save("owl")

    progress_bar.finish()
    print("The ontology '" + filename + "' has been saved!")
    logging.info("The ontology '%s' has been saved!", filename)
