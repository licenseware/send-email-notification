FROM python:3.11-alpine

LABEL author="Meysam Azad <meysam@licenseware.io>"

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /
RUN apk add --update libmagic && \
    pip install -U pip -r /requirements.txt

COPY main.py ./

ENTRYPOINT ["./main.py"]
