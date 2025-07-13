FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

ENV POETRY_HOME=/opt/poetry

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl ca-certificates \
        python-is-python3 \
        git \
    && curl -sSL https://install.python-poetry.org | python - \        
    && apt-get -qq purge \
        curl ca-certificates \
    && apt-get -qq autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="${POETRY_HOME}/bin:${PATH}"