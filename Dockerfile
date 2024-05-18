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
    VENV_PATH="/opt/venv"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
ENV VIRTUAL_ENV=$VENV_PATH


## builder-base image
FROM base as builder-base
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
      curl \
      build-essential

RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | python -

WORKDIR /opt/app
COPY poetry.lock pyproject.toml ./

RUN --mount=type=cache,target=/root/.cache \
    python -m venv $VENV_PATH && \
    poetry install --no-root --without=dev

COPY . .
RUN --mount=type=cache,target=/root/.cache \
    poetry install --only-root


## dev image
FROM base as dev

COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $VENV_PATH $VENV_PATH

WORKDIR /opt/app
COPY . .

RUN --mount=type=cache,target=/root/.cache \
    poetry install --with=dev && \
    rm -rf /opt/app

EXPOSE 8000

CMD ["teufa", "server", "--dev"]


## prod image
FROM base as prod

COPY --from=builder-base $VENV_PATH $VENV_PATH
COPY --from=builder-base /opt/app /opt/app

CMD ["teufa", "server"]
