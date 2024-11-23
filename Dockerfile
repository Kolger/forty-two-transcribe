FROM python:3.13-alpine

WORKDIR /code

RUN apk update && \
    apk upgrade && \
    apk add --no-cache ffmpeg libmagic

RUN pip install --upgrade pip && \
    pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

CMD python /code/main.py
