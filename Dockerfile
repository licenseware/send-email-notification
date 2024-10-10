FROM python:3.13-alpine AS base

LABEL author="Meysam Azad <meysam@licenseware.io>"

WORKDIR /licenseware

RUN addgroup -S licenseware && \
  adduser -S licenseware -G licenseware

ENV PYTHONUNBUFFERED=1

FROM python:3.13-alpine AS deps

COPY requirements.txt /
RUN pip install -U pip wheel && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r /requirements.txt


FROM base AS runner

COPY --from=deps /wheels /wheels
RUN apk add --no-cache --update libmagic && \
  pip install --no-cache /wheels/* && \
  rm -rf /wheels

USER licenseware:licenseware

COPY main.py ./

ENTRYPOINT ["/licenseware/main.py"]
CMD ["--help"]
