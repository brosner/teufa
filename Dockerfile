# syntax=docker/dockerfile:1

## base image
FROM python:3.13-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    VENV_PATH="/opt/app/.venv" \
    APP_HOME="/opt/app"
ENV PATH="$VENV_PATH/bin:$PATH"
ENV VIRTUAL_ENV=$VENV_PATH

RUN set -ex \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
      libpq5 \
    && rm -rf /var/lib/apt/lists/*


## builder-base image
FROM base AS builder-base
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
      curl \
      build-essential \
      libpq-dev \
      python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.6 /uv /uvx /bin/

WORKDIR $APP_HOME
COPY . .

RUN uv sync --frozen


## dev image
FROM base AS dev

COPY --from=builder-base $APP_HOME $APP_HOME
COPY --from=ghcr.io/astral-sh/uv:0.6 /uv /uvx /bin/

WORKDIR $APP_HOME

RUN uv sync --frozen --dev

EXPOSE 8000

CMD ["teufa", "server", "--dev"]


## ci image
FROM base AS ci

COPY --from=builder-base $APP_HOME $APP_HOME
COPY --from=ghcr.io/astral-sh/uv:0.6 /uv /uvx /bin/

WORKDIR $APP_HOME

RUN uv sync --frozen --group=test


## prod image
FROM base AS prod

COPY --from=builder-base /opt/app /opt/app

WORKDIR $APP_HOME

CMD ["teufa", "server"]
