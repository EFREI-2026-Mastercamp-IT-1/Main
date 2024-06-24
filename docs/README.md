# the server

## open virtual environement (usually automatic, but if you use codespaces you have to run it manually)
. .devcontainer/script/onCreate.sh

## install dependencies (normally done by the above command)
uv pip install -r requirements.txt

## run server
fastapi dev main.py

## open server endpoints documentation
http://127.0.0.1:8000/docs
