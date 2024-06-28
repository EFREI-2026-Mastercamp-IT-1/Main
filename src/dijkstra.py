import heapq
from datetime import timedelta

class GraphDijkstra:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [{} for _ in range(vertices)]

    def add_edge(self, u, v, weight, departure_time):
        if v not in self.graph[u]:
            self.graph[u][v] = []
        self.graph[u][v].append((weight, departure_time))

    def dijkstra(self, src, start_time):
        dist = [(float('inf'), None) for _ in range(self.V)]
        dist[src] = (0, start_time)
        pq = [(0, start_time, src)]
        parent = [-1] * self.V

        while pq:
            current_dist, current_time, u = heapq.heappop(pq)

            if current_dist > dist[u][0]:
                continue

            for v in self.graph[u]:
                for weight, departure_time in self.graph[u][v]:
                    if departure_time >= current_time:
                        wait_time = (departure_time - current_time).total_seconds()
                        new_dist = current_dist + weight + wait_time
                        new_time = departure_time + timedelta(seconds=weight)
                        if new_dist < dist[v][0]:
                            dist[v] = (new_dist, new_time)
                            parent[v] = u
                            heapq.heappush(pq, (new_dist, new_time, v))

        return dist, parent

    def shortest_path(self, src, dest, start_time):
        dist, parent = self.dijkstra(src, start_time)
        path = []
        if dist[dest][0] == float('inf'):
            return float('inf'), path, None

        current = dest
        while current != -1:
            path.insert(0, current)
            current = parent[current]

        return dist[dest][0], path, dist[dest][1]
