import os.path
from typing import Optional, TypedDict

import yaml

base_config_dir = os.path.dirname(__file__)
CONFIG_DIR = os.environ.get("CONFIG_PATH", base_config_dir)
ENVIRONMENT_CONFIG_PREFIX = "CONFIG_"


class ConfigStructure(TypedDict):
    API_TITLE: str
    API_VERSION: str
    OPENAPI_VERSION: str
    OPENAPI_URL_PREFIX: str
    OPENAPI_JSON_PATH: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    BLOB_STORAGE_HOST: str
    BLOB_STORAGE_PORT: str
    BLOB_STORAGE_ACCESS_KEY: str
    BLOB_STORAGE_ACCESS_SECRET: str
    BLOB_STORAGE_BUCKET: str
    BLOB_STORAGE_ACCESS_SECURE: bool


def read_from_file(name: str, path: str = base_config_dir) -> Optional[dict]:
    with open(path + f"/{name}") as f:
        content = yaml.safe_load(f)
    return content


def read_from_env(prefix=ENVIRONMENT_CONFIG_PREFIX) -> dict:
    return {
        key.removeprefix(prefix): value
        for key, value in os.environ.items()
        if key.startswith(prefix)
    }


def prepare() -> ConfigStructure:
    """Helper function preparing configuration for application:

    1. base.yaml - basic configuration for application that is not expected to change
    in different environments, values that can be safely committed to repository

    2. config.yaml - configuration specific for different environments, usually injected
    during deployment, overwrites values from base.yaml

    3. environmental variables - used to pass secrets injected during deployment
    """
    base = read_from_file("base.yaml")
    overwrite = read_from_file("config.yaml", path=CONFIG_DIR)
    environment = read_from_env()
    return (
        base | (overwrite if overwrite else {}) | (environment if environment else {})
    )


CONFIG = prepare()
