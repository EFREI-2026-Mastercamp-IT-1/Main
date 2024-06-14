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

def create_edges(transfer_list , stops_list):
    edges = []
    print(stops_list)
    for transfer in transfer_list:
        
        if transfer[0] in [stop[0] for stop in stops_list] and transfer[1] in [stop[0] for stop in stops_list]:
            edges.append(Edge(
                source=transfer[0],
                target=transfer[1],
                time = transfer[2]
            ))
    return edges

