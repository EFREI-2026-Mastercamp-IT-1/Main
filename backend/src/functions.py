class Station:
    def __init__(self, id, stationName, isTerminus, x, y):
        self.id = id
        self.stationName = stationName
        self.ligneNumber = []
        self.isTerminus = isTerminus
        self.x = x
        self.y = y
        self.liaisons = []
        
class Liaison:
    def __init__(self, station1, station2, time):
        self.station1 = station1
        self.station2 = station2
        self.time = time
        

def read_metro_file(filename):
    stations = []
    liaisons = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('V'):
                _, id, stationName, ligneNumber, isTerminus = line.strip().split(';')
                station_exists = False
                for station in stations:
                    if station.stationName == stationName:
                        station.ligneNumber.append(ligneNumber)
                        station_exists = True
                        break
                if not station_exists:
                    stations.append(Station(int(id), stationName, isTerminus, 0 , 0))
                    stations[-1].ligneNumber.append(ligneNumber)
            if line.startswith('E'):
                _, stationid1, stationid2,time = line.strip().split(';')
                liaisons.append(Liaison(int(stationid1), int(stationid2), int(time)))
                                        
                
            

    return stations, liaisons


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

