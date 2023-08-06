FROM python:3.11-alpine

LABEL author="Meysam Azad <meysam@licenseware.io>"

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN pip install -U pip

COPY requirements.txt /

RUN pip install -r /requirements.txt

COPY main.py ./

ENTRYPOINT ["./main.py"]
