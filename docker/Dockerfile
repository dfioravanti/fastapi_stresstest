ARG DOCKER_ARCH=arm64
FROM --platform=$DOCKER_ARCH python:3.11-slim-bookworm AS python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.5.1 \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/build" \
    VENV_PATH="/opt/build/.venv" \
    ROOT_BIN="/root/.local/bin" \
    PIPX_PATH="/root/.local/pipx" \
    WORKDIR="/app"

ENV PATH="$ROOT_BIN:$VENV_PATH/bin:$PATH"

ENTRYPOINT []

# `builder-base` stage is used to build deps + create our virtual environment
FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y build-essential

RUN python3 -m pip install --user pipx \
    && pipx ensurepath \
    && pipx install poetry==$POETRY_VERSION

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --without dev,test --no-root

COPY ./ ./
RUN poetry install --only-root

# `development` image is used during development / testing
FROM python-base as test
ENV FASTAPI_ENV=development
WORKDIR $PYSETUP_PATH

# copy in our built poetry + venv
COPY --from=builder-base $ROOT_BIN $ROOT_BIN
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY --from=builder-base $PIPX_PATH $PIPX_PATH

# quicker install as runtime deps are already installed
RUN poetry install --no-root

# `production` image used for runtime
FROM python-base as prod
ENV FASTAPI_ENV=production

WORKDIR $WORKDIR

RUN groupadd -g 999 notroot && \
    useradd -r -u 999 -g notroot notroot

COPY --chown=notroot:notroot --from=builder-base $VENV_PATH $VENV_PATH
COPY --chown=notroot:notroot  ./ ./

USER notroot

ENTRYPOINT ["gunicorn", "app.main:app", "--workers", "5", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0"]
