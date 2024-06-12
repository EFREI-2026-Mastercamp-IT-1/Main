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


station_list = get_metro_stations()
pathways_list = get_metro_pathways()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/nodes")
async def get_metro_nodes():
    return create_nodes(station_list)

@app.get("/edges")
async def get_metro_edges():
    return create_edges(pathways_list)


@app.get("/network")
async def get_network():
    return {
        "nodes": create_nodes(station_list),
        "edges": create_edges(pathways_list)
    }