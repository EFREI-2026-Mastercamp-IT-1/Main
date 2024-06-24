class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.edges = []

    def add_edge(self, u, v, w):
        self.edges.append((u, v, w))

    def find(self, parent, i):

        if parent[i] == i:
            return i
        parent[i] = self.find(parent, parent[i])
        return parent[i]

    def union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    def kruskal(self):
        result = []
        self.edges.sort(key=lambda edge: edge[2])
        
        parent = list(range(self.V))
        
        rank = [0] * self.V
        for u, v, w in self.edges:
            x = self.find(parent, u)
            y = self.find(parent, v)
            if x != y:
                result.append((u, v))
                self.union(parent, rank, x, y)
                if len(result) == self.V - 1:
                    break
        return result
