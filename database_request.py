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
            print(result)
            return result
        
    except Error as e:
        print(f"An error occurred: {e}")
        return []

def get_metro_pathways():
    try:
        with connect("data/database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT pathways.*
                FROM routes
                INNER JOIN trips ON routes.route_id = trips.route_id
                INNER JOIN stop_times ON trips.trip_id = stop_times.trip_id
                INNER JOIN pathways ON stop_times.stop_id = pathways.from_stop_id
                WHERE routes.route_type = 1
            """)
            return cursor.fetchall()
    except Error as e:
        print(f"An error occurred: {e}")
        return []