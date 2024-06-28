class GraphDijkstra:

    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]

    def minDistance(self, dist, sptSet):
        min = float('inf')
        min_index = -1

        for v in range(self.V):
            if dist[v] < min and not sptSet[v]:
                min = dist[v]
                min_index = v

        return min_index

    def dijkstra(self, src):
        dist = [float('inf')] * self.V
        dist[src] = 0
        sptSet = [False] * self.V
        parent = [-1] * self.V  # To store the path

        for cout in range(self.V):
            u = self.minDistance(dist, sptSet)
            sptSet[u] = True

            for v in range(self.V):
                if (self.graph[u][v] > 0 and
                        not sptSet[v] and
                        dist[v] > dist[u] + self.graph[u][v]):
                    dist[v] = dist[u] + self.graph[u][v]
                    parent[v] = u

        return dist, parent

    def shortest_path(self, src, dest):
        dist, parent = self.dijkstra(src)
        path = []
        if dist[dest] == float('inf'):
            return float('inf'), path

        current = dest
        while current != -1:
            path.insert(0, current)
            current = parent[current]

        return dist[dest], path

