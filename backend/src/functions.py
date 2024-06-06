class Station:
    def __init__(self, id, stationName, isTerminus, x, y):
        self.id = id
        self.stationName = stationName
        self.ligneNumber = []
        self.isTerminus = isTerminus
        self.x = x
        self.y = y
        self.liaisons = []
        

def read_metro_file(filename):
    stations = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('V'):
                _, id, stationName, ligneNumber, isTerminus = line.strip().split(';')
                # Vérifier si la station existe déjà dans la liste
                station_exists = False
                for station in stations:
                    if station.stationName == stationName:
                        station.ligneNumber.append(ligneNumber)
                        station_exists = True
                        break
                if not station_exists:
                    stations.append(Station(int(id), stationName, isTerminus, 0 , 0))
                    stations[-1].ligneNumber.append(ligneNumber)

    return stations


def read_pospoints_file(filename, stations):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            x, y, stationName = line.strip().split(';')
            for station in stations:

                if station.stationName.strip() == stationName.strip():
                    station.x = float(x)
                    station.y = float(y)
                    break

