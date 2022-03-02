FROM python:3.10-alpine

LABEL author="Meysam Azad <meysam@licenseware.io>"

ENV PYTHONUNBUFFERED=1

RUN pip install -U pip

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "send-email.py"]
