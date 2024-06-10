from classes import *

def create_nodes(stops_list):
    nodes = []
    for stop in stops_list:
        nodes.append(Node(
            id=stop.stop_id,
            label=stop.stop_name,
            x=float(stop.stop_lon),
            y=float(stop.stop_lat)
        ))
    return nodes

def create_edges(pathways_list):
    edges = []
    for pathway in pathways_list:
        edges.append(Edge(
            id=pathway.pathway_id,
            source=pathway.from_stop_id,
            target=pathway.to_stop_id,
            label=pathway.signposted_as
        ))
    return edges
