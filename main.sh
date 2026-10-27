#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 src/main.py
exec python3 -m http.server 8888 --bind 127.0.0.1 --directory docs
