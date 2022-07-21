#!/bin/sh

set -e

exec poetry run pytest --cov=api api