from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from create_network import *
from database_request import *


## Lien de la base de donnée:
## https://www.swisstransfer.com/d/cb521c72-9847-419f-9567-6c95aae4fca0

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/nodes")
async def get_nodes():
    station_list = get_all_station()
    return create_nodes(station_list)

@app.get("/edges")
async def get_edges():
    pathways_list = get_all_pathways()
    return create_edges(pathways_list)


@app.get("/network")
async def get_network():
    station_list = get_all_station()
    return {
        "nodes": create_nodes(station_list),
    }
