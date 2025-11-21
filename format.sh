#!/usr/bin/env bash
set -e

isort .
black .

echo "Formatting complete."

