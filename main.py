from fastapi import FastAPI

from functions import *

from fastapi.middleware.cors import CORSMiddleware

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
    stations,liaisons = read_metro_file('static/metro.txt')
    read_pospoints_file('static/pospoints.txt', stations)
    return stations

@app.get("/liaisons")
def get_liaisons():
    stations,liaisons = read_metro_file('static/metro.txt')
    return liaisons
