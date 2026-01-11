FROM python:3.10-slim

RUN sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources

RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates && \
    update-ca-certificates && \
    rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.7.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml poetry.lock . 

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-ansi

COPY . .
RUN mkdir -p /app/logs

RUN groupadd -r vkbot && useradd -r -g vkbot vkbot
RUN chown -R vkbot:vkbot /app
USER vkbot


CMD ["poetry", "run", "python", "-m", "src.main"]
