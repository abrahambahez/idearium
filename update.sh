#!/usr/bin/env bash
set -euo pipefail

jrnl --export json > entries.json
uv run python build.py
