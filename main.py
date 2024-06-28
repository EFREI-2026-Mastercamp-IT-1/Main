from typing import List, Tuple ,Dict
import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from src.kruskal import Graph
from src.dijkstra import GraphDijkstra
from src.request_caching import get_cached_result, cache_result

app: FastAPI = FastAPI()

class Stop(BaseModel):
    """
    Class representing a stop.
    """
    stop_id: str
    stop_sequence: int
    lon: float
    lat: float
    stop_name: str

class DijkstraResponse(BaseModel):
    distance: float
    path: List[int]

def get_db_connection() -> sqlite3.Connection:
    conn: sqlite3.Connection = sqlite3.connect('src/mon_database.db')
    conn.row_factory: sqlite3.Row = sqlite3.Row
    return conn

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://localhost:4000",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stops/{line_name}", response_model=List[Stop])
def read_stops(line_name: str) -> List[Stop]:
    conn: sqlite3.Connection = get_db_connection()
    cursor: sqlite3.Cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {line_name} ORDER BY stop_sequence")
    stops: List[dict] = cursor.fetchall()
    return [Stop(**dict(stop)) for stop in stops]

@app.get("/stop/{line_name}/{stop_id}", response_model=Stop)
def read_stop(line_name: str, stop_id: str) -> Stop:
    conn: sqlite3.Connection = get_db_connection()
    cursor: sqlite3.Cursor = conn.cursor()
    cursor.execute(
        f"SELECT * FROM {line_name} WHERE stop_id = ?", (stop_id,)
        )
    stop: dict = cursor.fetchone()
    if stop is None:
        raise HTTPException(status_code=404, detail="Stop not found")
    return Stop(**dict(stop))


@app.get("/acpm")
def get_kruskal() -> List[tuple[str, str]]:
    conn: sqlite3.Connection = get_db_connection()
    cursor: sqlite3.Cursor = conn.cursor()
    cursor.execute("SELECT * FROM new_table")
    nb_vertices: List[int] = cursor.fetchall()
    nb_vertices: List[int] = len(nb_vertices)
    g: Graph = Graph(nb_vertices)

    cursor.execute("SELECT * FROM concatligne")
    liaisons: List[List[str]] = [list(row) for row in cursor.fetchall()]

    for u, v, w in liaisons:
        g.add_edge(int(u), int(v), int(w))

    acpm: List[tuple[int, int]] = g.kruskal()

    cursor.execute("SELECT stop_ids,id FROM new_table")
    stop_ids: List[Tuple[str, int]] = cursor.fetchall()
    stop_ids: Dict[int, str] = {id: stop_id.split(',')[0] for stop_id, id in stop_ids}
    acpm_id: List[tuple[str, str]] = [(stop_ids[u], stop_ids[v]) for u, v in acpm]

    return acpm_id


@app.get("/acpm/points")
def get_kruskal_points() -> List[Stop]:
    kruskal: List[Tuple[str, str]] = get_kruskal()
    points: List[str] = []

    for u, v in kruskal:
        if u not in points:
            points.append(u)
        if v not in points:
            points.append(v)

    lines: List[str] = [
        "ligne1",
        "ligne2","ligne3","ligne3b", "ligne4", "ligne5", "ligne6", 
        "ligne7", "ligne7b", "ligne8", "ligne9", "ligne10", 
        "ligne11", "ligne12", "ligne13", "ligne14"
        ]

    conn: sqlite3.Connection = get_db_connection()
    cursor: sqlite3.Cursor = conn.cursor()

    stops: List[Stop] = []
    for line in lines:
        cursor.execute(f"SELECT * FROM {line}")
        stops += cursor.fetchall()

    stops: List[Stop] = [Stop(**dict(stop)) for stop in stops]
    points: List[Stop] = [stop for stop in stops if stop.stop_id in points]

    return points

@app.get("/dijkstra/{src}/{dest}", response_model=DijkstraResponse)
def get_dijkstra(src: int, dest: int) -> DijkstraResponse:
    """
    implements dijkstra algorithm
    """
    conn: sqlite3.Connection = get_db_connection()
    cursor: sqlite3.Cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM new_table")
    nb_vertices: int = cursor.fetchone()[0]

    g: GraphDijkstra = GraphDijkstra(nb_vertices)

    cursor.execute("SELECT * FROM concatligne")
    liaisons: List[List[str]] = [list(row) for row in cursor.fetchall()]

    for u, v, w in liaisons:
        g.graph[int(u)][int(v)] = int(w)
        g.graph[int(v)][int(u)] = int(w)  # Assuming undirected graph

    if src >= nb_vertices or src < 0 or dest >= nb_vertices or dest < 0:
        raise HTTPException(status_code=400, detail="Invalid source or destination vertex")

    distance, path = g.shortest_path(src, dest)

    return DijkstraResponse(distance=distance, path=path)


@app.get("/stations/")
def read_stations() -> List[Dict[str, str]]:
    """reads all stations from the database"""
    lines = [
        "ligne1","ligne2","ligne3","ligne3b", "ligne4", "ligne5", 
        "ligne6", "ligne7", "ligne7b", "ligne8", "ligne9", 
        "ligne10", "ligne11", "ligne12", "ligne13", "ligne14"
        ]
    conn: sqlite3.Connection = get_db_connection()
    cursor: sqlite3.Cursor = conn.cursor()
    stations: List[Dict[str, str]] = []
    for line in lines:
        cursor.execute(
        f"""
            SELECT nt.*, l.lon, l.lat, l.stop_sequence, l.stop_id as line_stop_id
            FROM new_table nt
            JOIN {line} l ON nt.stop_ids LIKE '%' || l.stop_id || '%'
            ORDER BY l.stop_sequence
        """
        )
        line_stations: List[Dict[str, str]] = cursor.fetchall()
        for i, station in enumerate(line_stations):
            station_dict: dict = dict(station)
            station_dict["line"]: str = line
            # Add the stop_id of the next station
            if i < len(line_stations) - 1:
                next_station_id: str = line_stations[i + 1]["line_stop_id"]
                cursor.execute(
                f"""
                    SELECT id
                    FROM new_table
                    WHERE stop_ids LIKE '%' || ? || '%'
                """, (next_station_id,)
                )
                next_station_new_table_id: Dict[str, int] = cursor.fetchone()
                station_dict["next_stop_id"]: str = next_station_new_table_id["id"] if next_station_new_table_id else ""
            else:
                station_dict["next_stop_id"]: str = ""
            # Add the stop_id of the previous station
            if i > 0:
                prev_station_id: str = line_stations[i - 1]["line_stop_id"]
                cursor.execute(
                f"""
                    SELECT id
                    FROM new_table
                    WHERE stop_ids LIKE '%' || ? || '%'
                """, (prev_station_id,)
                )
                prev_station_new_table_id: Dict[str, int] = cursor.fetchone()
                station_dict["prev_stop_id"]: str = prev_station_new_table_id["id"] if prev_station_new_table_id else ""
            else:
                station_dict["prev_stop_id"]: str = ""
            stations.append(station_dict)
    return stations
