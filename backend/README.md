# Warehouse Backend

Backend consists of:

* **HTTP Api** - modifying Warehouse database by external clients
* **Import process** - for executing database updates

## Configuration

Configuration can be set in following ways:

* `backend/api/config/base.yaml` basic configuration for application that is not expected to change 
in different environments, values that can be safely committed to repository

* `backend/api/config/config.yaml` configuration specific for different environments, usually injected 
during deployment, overwrites values from `base.yaml`, file can be read from dynamically mounted directory
specified by `CONFIG_PATH` environmental variable

* environmental variables - used to pass secrets injected during deployment, prefix for all environmental variables with `CONFIG_`

### Avaliable configuration

| Configuration name         | Default value          |
|----------------------------|------------------------|
| API_TITLE                  | "Warehouse API"        |
| API_VERSION                | v1                     |
| OPENAPI_VERSION            | 3.0.2                  |
| OPENAPI_URL_PREFIX         | api                    |
| OPENAPI_JSON_PATH          | openapi.json           |
| DATABASE_USER              | postgres               |
| DATABASE_PASSWORD          | postgres               |
| DATABASE_NAME              | warehouse              |
| DATABASE_HOST              | localhost              |
| DATABASE_PORT              | 5432                   |
| BLOB_STORAGE_HOST          | localhost              |
| BLOB_STORAGE_PORT          | 9000                   |
| BLOB_STORAGE_ACCESS_KEY    | minio                  |
| BLOB_STORAGE_ACCESS_SECRET | minio-secret           |
| BLOB_STORAGE_BUCKET        | warehouse-import-files |
| BLOB_STORAGE_ACCESS_SECURE | false                  |


## Install for development

With the latest version of `poetry` and `python 3.10`

```shell
poetry run install
```

## Database migration

Database migrations are handled by [Alembic](https://alembic.sqlalchemy.org/en/latest/)

### Upgrade database schema to newest version
```bash
alembic upgrade head
``` 

### Rollback all migrations / clear database
```bash
alembic downgrade base
``` 

### Create new migration

After doing modifications to database schema in `api/persistence/tables.py`

```bash
alembic revision --autogenerate -m "003-slug-with-changes-summary" 
```

Before using `alembic --autogenerate` read and understand its capabilities in [documentation](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)

## Code formatting 

Python codebase is formatted using [black](https://black.readthedocs.io/en/stable/)

To format code:

```bash
black api
```

## @TODO - things to improve

* ‼️ authentication - both in frontend and backend using JSON Web Token (JWT) Bearer
   Token https://datatracker.ietf.org/doc/html/rfc7523
* more mature implementation of import -> replace long-running process with event-based implementation with FIFO
* add code formatting to git pre commit hooks
* better, more resilient to refactoring tests