FROM python:3.10.5-slim-bullseye AS app
LABEL maintainer="Maksymilian Ratajczyk <kontakt@maksymilianratajczyk.pl>"

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential curl libpq-dev \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean \
  && useradd --create-home python \
  && chown python:python -R /app

RUN pip install poetry==1.1.14

USER python

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

RUN poetry install

COPY alembic.ini alembic.ini
COPY alembic alembic
COPY api api

COPY --chown=python:python deployment/test/docker-entrypoint.sh /opt/docker-entrypoint.sh

RUN chmod 775 /opt/docker-entrypoint.sh

ENTRYPOINT ["/opt/docker-entrypoint.sh"]
