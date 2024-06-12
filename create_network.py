from classes import *

def create_nodes(stops_list):
    nodes = []
    for stop in stops_list:
        nodes.append(Node(
            id=stop[0],
            label=stop[2],
            x=stop[4],
            y=stop[5]
        ))
    return nodes

def create_edges(pathways_list):
    edges = []
    for pathway in pathways_list:
        edges.append(Edge(
            source=pathway[0],
            target=pathway[1],
            label= "",
            time = pathway[2]
        ))
    return edges

