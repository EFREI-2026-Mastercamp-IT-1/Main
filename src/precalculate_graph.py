import sqlite3
from datetime import datetime, timedelta
from dijkstra import GraphDijkstra
import pickle
import time


def get_db_connection():
    conn = sqlite3.connect('mon_database.db')
    conn.row_factory = sqlite3.Row
    return conn

def parse_time(time_str):
    hours, minutes, seconds = map(int, time_str.split(':'))
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)

def precalculate_graph():
    start_time = time.time()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Créer le graphe
    g = GraphDijkstra()

    # Récupérer tous les arrêts de métro
    cursor.execute("""
        SELECT DISTINCT s.stop_id
        FROM stops s
        JOIN stop_times st ON s.stop_id = st.stop_id
        JOIN trips t ON st.trip_id = t.trip_id 
        JOIN routes r ON t.route_id = r.route_id
        WHERE r.route_type = 1
    """)
    metro_stops = {row['stop_id'] for row in cursor.fetchall()}

    # Ajouter les arêtes au graphe (seulement pour les lignes de métro)
    cursor.execute("""
        SELECT t1.stop_id as from_stop, t2.stop_id as to_stop, 
               t1.departure_time, t2.arrival_time
        FROM stop_times t1
        JOIN stop_times t2 ON t1.trip_id = t2.trip_id AND t1.stop_sequence = t2.stop_sequence - 1
        JOIN trips ON t1.trip_id = trips.trip_id
        JOIN routes ON trips.route_id = routes.route_id
        WHERE routes.route_type = 1
    """)
    
    for row in cursor:
        u, v = row['from_stop'], row['to_stop']
        if u in metro_stops and v in metro_stops:
            departure_time = parse_time(row['departure_time'])
            arrival_time = parse_time(row['arrival_time'])
            weight = (arrival_time - departure_time).total_seconds()
            g.add_edge(u, v, weight, departure_time.total_seconds())

    # Ajouter les temps de correspondance (seulement pour les arrêts de métro)
    cursor.execute("""
        SELECT from_stop_id, to_stop_id, min_transfer_time
        FROM transfers
        WHERE from_stop_id IN (SELECT stop_id FROM stops WHERE stop_id IN ({}))
        AND to_stop_id IN (SELECT stop_id FROM stops WHERE stop_id IN ({}))
    """.format(','.join('?' * len(metro_stops)), ','.join('?' * len(metro_stops))),
    list(metro_stops) + list(metro_stops))

    for transfer in cursor:
        u, v = transfer['from_stop_id'], transfer['to_stop_id']
        min_transfer_time = transfer['min_transfer_time']
        g.add_edge(u, v, min_transfer_time, 0)

    # Sauvegarder le graphe précalculé
    with open('precalculated_graph.pkl', 'wb') as f:
        pickle.dump(g, f)

    end_time = time.time()
    print(f"Temps d'exécution: {end_time - start_time} secondes")

if __name__ == "__main__":
    precalculate_graph()