# the server

## open virtual environement (needs to be run manually the first time)
. .devcontainer/script/onCreate.sh

## install dependencies (normally done by the above command)
uv pip install -r requirements.txt

## run server
fastapi dev main.py

## open server endpoints documentation
http://127.0.0.1:8000/docs

# IDX
if you want to dev trough project idx:

- install uv: https://github.com/astral-sh/uv
curl -LsSf https://astral.sh/uv/install.sh | sh

- run onCreate.sh:
. .devcontainer/script/onCreate.sh
