from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from custom_parser import *



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agency_list, routes_list, trips_list, calendar_list, calendar_dates_list, stop_times_list, stops_list, transfer_list, stop_extensions_list, pathways_list = parse_all()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/agency")
async def get_agency():
    return agency_list

@app.get("/routes")
async def get_routes():
    return routes_list

@app.get("/trips")
async def get_trips():
    return trips_list

@app.get("/calendar")
async def get_calendar():
    return calendar_list

@app.get("/calendar_dates")
async def get_calendar_dates():
    return calendar_dates_list

@app.get("/stop_times")
async def get_stop_times():
    return stop_times_list

@app.get("/stops")
async def get_stops():
    return stops_list

@app.get("/transfer")
async def get_transfer():
    return transfer_list

@app.get("/stop_extensions")
async def get_stop_extensions():
    return stop_extensions_list

@app.get("/pathways")
async def get_pathways():
    return pathways_list
