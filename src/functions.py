class Station:
    def __init__(self, id, stationName, ligneNumber, isTerminus, x, y):
        self.id = id
        self.stationName = stationName
        self.ligneNumber = ligneNumber
        self.isTerminus = isTerminus
        self.x = x
        self.y = y
        self.liaisons = []
        

def read_metro_file(filename):
    stations = []
    f = open(filename, 'r',encoding='utf-8')
    for line in f:
        if line.startswith('V'):
            _, id, stationName, ligneNumber, isTerminus = line.strip().split(';')
            stations.append(Station(int(id), stationName, ligneNumber,isTerminus, 0 , 0))
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

stations = read_metro_file('src\Version1\metro.txt')
read_pospoints_file('src\Version1\pospoints.txt', stations)

for station in stations:
    print(station.stationName)



import networkx as nx
# Créer le graphe
graph = nx.Graph()

# Ajouter les noeuds
for station in stations:
    graph.add_node(station.id, label=station.stationName, x=station.x, y=station.y)

