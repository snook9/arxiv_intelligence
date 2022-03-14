FROM debian:11

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install dependencies and pip requirements
COPY requirements.txt .
RUN apt-get update -q -y
RUN apt-get install -yf \
    gcc python-dev libkrb5-dev python3-docopt python3-gssapi \
    python3 \
    python3-pip
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

ENTRYPOINT ["python3", "main.py"]
