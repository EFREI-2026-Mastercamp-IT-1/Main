from fastapi import FastAPI
from pydantic import BaseModel

from functions import *

from fastapi.middleware.cors import CORSMiddleware

class StationModel(BaseModel):
    id: int
    stationName: str
    ligneNumber: str
    isTerminus: str
    x: float
    y: float

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

@app.get("/stations")
def get_stations():
    stations = read_metro_file('./Version1/metro.txt')
    read_pospoints_file('./Version1/pospoints.txt', stations)
    return stations


