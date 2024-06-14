from classes import *

def create_nodes(stops_list):
    nodes = []
    for stop in stops_list:
        nodes.append(Node(
            id=stop[0],
            label=stop[1],
            x=stop[2],
            y=stop[3]
        ))
    return nodes

def create_edges(transfer_list, stops_list):
    edges = []
    for transfer in transfer_list:
        source_id = transfer[0]
        target_id = transfer[1]
        time = transfer[2]
        
        if any(stop[0] == source_id for stop in stops_list) and any(stop[0] == target_id for stop in stops_list):
            edges.append(Edge(
                source=source_id,
                target=target_id,
                time=time
            ))
    return edges
