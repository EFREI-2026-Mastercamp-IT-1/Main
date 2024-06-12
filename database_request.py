from sqlite3 import connect, Error

def get_metro_stations() -> list:
    try:
        with connect("data/database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT *
            FROM stops
                JOIN stop_times ON stop_times.stop_id = stops.stop_id
                JOIN trips ON trips.trip_id = stop_times.trip_id
                JOIN routes ON routes.route_id = trips.route_id
            WHERE routes.route_type = 1
            GROUP BY stops.stop_name
            """)
            
            result = cursor.fetchall()
            return result
        
    except Error as e:
        print(f"An error occurred: {e}")
        return []

def get_metro_pathways():
    try:
        with connect("data/database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT from_stop_id, to_stop_id, min_transfer_time
            FROM transfers  
                JOIN stops ON stops.stop_id = transfers.from_stop_id
                JOIN stop_times ON stop_times.stop_id = stops.stop_id
                JOIN trips ON trips.trip_id = stop_times.trip_id
                JOIN routes ON routes.route_id = trips.route_id
            WHERE routes.route_type = 1
                           LIMIT 100 
            """)
            result = cursor.fetchall()
            return result
    except Error as e:
        print(f"An error occurred: {e}")
        return []