# the server

## open virtual environement (usually automatic, but if you use codespaces you have to run it manually)
. .devcontainer/script/onCreate.sh

## install dependencies
pip install -r requirements.txt

## run server
fastapi dev main.py