#!/bin/sh

# uv

## install

uv venv && . .venv/bin/activate && uv pip sync requirements.txt

## forbid pip

### disclaimer

alias pip="echo \"pip is forbidden, use 'uv pip' instead\""

### force

alias force_pip="/usr/local/bin/pip"

# dev server

fastapi dev src/main.py
