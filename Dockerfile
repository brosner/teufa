# syntax=docker/dockerfile:1

## base image
FROM python:3.12-slim as base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION="1.8.3" \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    VENV_PATH="/opt/venv" \
    APP_HOME="/opt/app"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
ENV VIRTUAL_ENV=$VENV_PATH

RUN set -ex \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
      libpq5 \
    && rm -rf /var/lib/apt/lists/*


## builder-base image
FROM base as builder-base
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
      curl \
      build-essential \
      libpq-dev \
      python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | python -

WORKDIR $APP_HOME
COPY poetry.lock pyproject.toml ./

RUN --mount=type=cache,target=/root/.cache \
    python -m venv $VENV_PATH && \
    poetry install --no-root --only=main

COPY . .
RUN --mount=type=cache,target=/root/.cache \
    poetry install --only-root


## dev image
FROM base as dev

COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $VENV_PATH $VENV_PATH
COPY --from=builder-base $APP_HOME $APP_HOME

WORKDIR $APP_HOME

RUN --mount=type=cache,target=/root/.cache \
    poetry install --with=dev && \
    rm -rf $APP_HOME

EXPOSE 8000

ENTRYPOINT ["teufa"]
CMD ["server", "--dev"]


## ci image
FROM base as ci

COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $VENV_PATH $VENV_PATH
COPY --from=builder-base $APP_HOME $APP_HOME

WORKDIR $APP_HOME

RUN --mount=type=cache,target=/root/.cache \
    poetry install --with=test


## prod image
FROM base as prod

COPY --from=builder-base $VENV_PATH $VENV_PATH
COPY --from=builder-base /opt/app /opt/app

WORKDIR $APP_HOME

ENTRYPOINT ["teufa"]
CMD ["server"]
