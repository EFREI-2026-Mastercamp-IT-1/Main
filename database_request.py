from sqlite3 import connect, Error

def get_all_station() -> list:
    try:
        with connect("data/database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM stops WHERE parent_station = ''")
            return cursor.fetchall()
    except Error as e:
        print(f"An error occurred: {e}")
        return []

def get_all_pathways():
    try:
        with connect("data/database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pathways")
            return cursor.fetchall()
    except Error as e:
        print(f"An error occurred: {e}")
        return []
    
