# Arxiv Intelligence

Highlighting the relationship between authors and scientists.

This software highlights the relationships between authors and scientists, from articles published on arxiv.org. For this, it generates an ontology (owl file), from the named entities located in the articles.
After execution, the owl file is generated in the 'owl' folder.
The category is fixed to cs.AI.

# Install

## With Docker

    docker build -t arxiv_intelligence .

## Dependencies

First, you must install the following NER (Named Entity Recognition) Web service:
https://github.com/snook9/arxiv_intelligence_ner_ws

### Debian, Ubuntu, and friends

    sudo apt install gcc python-dev libkrb5-dev python3-docopt python3-gssapi

## Application

Create a virtual environment and activate it:

    python3 -m venv venv
    . venv/bin/activate

Install arXiv Intelligence:

    pip install -r requirements.txt

# Run

## With Docker

    docker run -v /path/to/owl/:/app/owl -v /path/to/log/:/app/log -ti arxiv_intelligence -n 1 -w http://172.17.0.2:5000/

*Replace the 172.17.0.2:5000 IP and port by the real IP and port of the 'arxiv_intelligence_ner_ws' web service.*</br>
*'/path/to/owl/' must be the folder where the file 'template-arxiv-intelligence.owl' is*</br>
*'/path/to/log/' will be the folder to write log files*</br>

### Help

    docker run -ti arxiv_intelligence -h

## With Python

    python3 main.py

### Help

    python3 main.py -h

During runtime, you could watch the log files in the 'log' folder.
After running, an ontology file, named "output_[datetime].owl", will be generated in the 'owl' folder. This output file will be populated with individuals, from the template "template-arxiv-intelligence.owl".

### Usage

    -h | --help: show this help
    -v | --version: show the version of this software
    -w | --webservice=[url]: set the url of the named entities web service (you must use an instance of the following web service: 'https://github.com/snook9/arxiv_intelligence_ner_ws'),
    default value is 'http://localhost:5000/'
    -n | --number=[value]: set the max articles number extracted from arxiv.org
    default value is 2
    -d | --hdfs: enable writing to HDFS for big data projects,
    default disabled. Nota: HDFS server URL is hardcoded currently)

# Test

## pylint

    apt install pylint
    export PYTHONPATH="venv/lib/python3.9/site-packages/"
    pylint --disable too-few-public-methods --disable too-many-instance-attributes --disable too-many-branches --disable too-many-statements ./main.py ./services ./entities ./tests

## pytest

    pytest

Run with coverage report:

    export PYTHONPATH="venv/lib/python3.9/site-packages/"
    coverage run -m pytest
    coverage report
    coverage html  # open htmlcov/index.html in a browser
