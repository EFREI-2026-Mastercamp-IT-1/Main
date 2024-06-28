import heapq
from datetime import timedelta

class GraphDijkstra:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v, weight, departure_time):
        if u not in self.graph:
            self.graph[u] = {}
        if v not in self.graph[u]:
            self.graph[u][v] = []
        self.graph[u][v].append((weight, departure_time))

    def dijkstra(self, src, start_time):
        dist = {node: (float('inf'), None) for node in self.graph}
        dist[src] = (0, start_time)
        pq = [(0, start_time, src)]
        parent = {node: None for node in self.graph}

        while pq:
            current_dist, current_time, u = heapq.heappop(pq)

            if current_dist > dist[u][0]:
                continue

            for v in self.graph.get(u, {}):
                for weight, departure_time in self.graph[u][v]:
                    if departure_time >= current_time:
                        wait_time = departure_time - current_time
                        new_dist = current_dist + weight + wait_time
                        new_time = departure_time + timedelta(seconds=weight)
                        if new_dist < dist[v][0]:
                            dist[v] = (new_dist, new_time)
                            parent[v] = u
                            heapq.heappush(pq, (new_dist, new_time, v))

        return dist, parent

    def shortest_path(self, src, dest, start_time):
        dist, parent = self.dijkstra(src, start_time)
        if dest not in dist:
            return float('inf'), [], None

        path = []
        current = dest
        while current is not None:
            path.insert(0, current)
            current = parent[current]

        return dist[dest][0], path, dist[dest][1]