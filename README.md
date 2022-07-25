# 📦 Warehouse Application

## Stack

* [Flask](https://flask.palletsprojects.com/) for simple HTTP layer
* [marshmallow](https://flask.palletsprojects.com/) object serialisation/deserialization, defining API schemas
* [min.io](https://min.io/) block storage used for inventory import
* [PostgreSQL](https://www.postgresql.org/) database for storing inventory and handling transactions
* [SQLAlchemy](https://www.sqlalchemy.org/) used in Python for handling database logic

## Components

This monorepo contains following components:

* [backend](backend/README.md)

## Configuration

No need to configure anything for local deployment, everything runs with reasonable
defaults.

## Running 

Requirement: Docker Compose `1.28.0` 

### Application

```bash
docker compose --profile app up -d 
```

### Backend tests

```bash
docker compose --profile backend-tests up --exit-code-from pytest
```