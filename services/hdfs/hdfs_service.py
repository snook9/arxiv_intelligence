"""
Name: arXiv Intelligence
Authors: Jonathan CASSAING
Highlighting the relationship between authors and scientists
"""

import csv
from typing import List
from pathlib import Path
from hdfs.ext.kerberos import KerberosClient
from hdfs.util import HdfsError
from entities.document import DocumentEntity

class HdfsService():
    """Class for writing to HDFS"""
    def __init__(self: object):
        """Initialize a Kerberos client for HDFS connection"""
        self.server = "http://hdfs-nn-1.au.adaltas.cloud:50070"
        self.folder = Path("/education/cs_2022_spring_1/j.cassaing-cs/project/")

        try:
            self._client = KerberosClient(self.server)
        except HdfsError as err:
            print(f"HdfsError: {err}")

    def write_documents(self: object, csv_filename: str, documents: List[DocumentEntity]):
        """Write a Documents list in a CSV file, into the HDFS folder (self.folder)"""
        with self._client.write(
                str(self.folder.joinpath(csv_filename)), encoding="utf-8"
            ) as csv_file:

            fieldnames = ["entry_id", "updated", "published", "title", "authors",
                          "summary", "primary_category",
                          "categories", "pdf_url", "number_of_pages"]
            writer = csv.DictWriter(csv_file, delimiter=';', fieldnames=fieldnames)

            writer.writeheader()
            for document in documents:
                writer.writerow({
                    "entry_id": "\'" + str(document.entry_id).replace("\'", " ") + "\'",
                    "updated": "\'" + document.updated.strftime("%Y-%m-%dT%H:%M:%S") + "\'",
                    "published": "\'" + document.published.strftime("%Y-%m-%dT%H:%M:%S") + "\'",
                    "title": "\'" + str(document.title).replace("\n", " ").replace(";", ":").replace("\'", " ") + "\'",
                    "authors": "\'" + ', '.join(str(author.name) for author in document.authors) + "\'",
                    "summary": "\'" + str(document.summary).replace("\n", " ").replace(";", ":").replace("\'", " ") + "\'",
                    "primary_category": "\'" + str(document.primary_category).replace("\n", " ").replace(";", ":").replace("\'", " ") + "\'",
                    "categories": "\'" + ', '.join(str(category).replace("\n", " ").replace(";", ":").replace("\'", " ") for category in document.categories) + "\'",
                    "pdf_url": "\'" + str(document.pdf_url).replace("\n", " ").replace(";", ":").replace("\'", " ") + "\'",
                    "number_of_pages": document.number_of_pages})
