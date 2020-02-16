FROM python:3.6.1-alpine

RUN apk update \
  && apk add \
    build-base \
    postgresql \
    postgresql-dev \
    libffi-dev \
    python-dev \
    libpq

RUN pip install --upgrade pip
RUN pip install 'poetry==1.0.0a0'

WORKDIR ./
COPY pyproject.toml /
RUN poetry export -f requirements.txt > requirements.txt
RUN pip install -r requirements.txt
COPY ./ ./


EXPOSE 5000
