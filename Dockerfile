FROM python:3.8-buster
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y \
    gfortran \
    g++ \
  && rm -rf /var/lib/apt/lists/*
RUN pip install poetry==0.12.*
COPY . /app
WORKDIR /app
RUN poetry config settings.virtualenvs.create false && poetry install
CMD /bin/bash hetzner_invoice
