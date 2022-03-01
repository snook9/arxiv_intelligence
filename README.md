# Arxiv Intelligence

Highlighting the relationship between authors and scientists.

# Install

## Dependencies

First, you must install the following NER (Named Entity Recognition) Web service:
https://github.com/snook9/arxiv_intelligence_ner_ws

## Application

Create a virtual environment and activate it:

    python3 -m venv venv
    . venv/bin/activate

Install arXiv Intelligence:

    pip install -r requirements.txt

# Run

    python3 main.py

An ontology file, named "output_[datetime].owl", will be generated in the owl folder. This output file will be populated with individuals, from the template "template-arxiv-intelligence.owl".

# Test

## pylint

    apt install pylint
    export PYTHONPATH="venv/lib/python3.9/site-packages/"
    pylint ./*

## pytest

    pytest

Run with coverage report:

    export PYTHONPATH="venv/lib/python3.9/site-packages/"
    coverage run -m pytest
    coverage report
    coverage html  # open htmlcov/index.html in a browser
