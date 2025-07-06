FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    curl ca-certificates \
    python3 python-is-python3 \
    && apt-get autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

################################################################################
# Add poetry for python package management & build
################################################################################
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python -
ENV PATH="/etc/poetry/bin:${PATH}"
