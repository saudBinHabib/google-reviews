#!/bin/bash
set -e

pip3 install .

exec "$@"