#matrice_adjacence = np.array([[0, 1, 0, 1, 0, 0],
#                    [0, 0, 1, 0, 0, 0],
#                    [0, 0, 0, 0, 0, 1],
#                    [0, 0, 1, 0, 1, 0],
#                    [0, 0, 0, 0, 0, 1],
#                    [0, 0, 0, 0, 0, 0]])
#
#matrice_couts = np.array([[0, 0, 0, 0, 0, 0],
#                      [0, 0, 9, 0, 0, 0],
#                      [0, 0, 0, 0, 0, 2],
#                      [0, 0, 4, 0, 4, 0],
#                      [0, 0, 0, 0, 0, 7],
#                      [0, 0, 0, 0, 0, 0]])

def dijkstra(matrice_adjacencee, matrice_coutss, start, end):
    # Nombre de nœuds dans le graphe
    n = len(matrice_adjacencee)
    
    # Initialiser les distances à l'infini et les parents pour reconstruire le chemin
    dist = [float('inf')] * n
    dist[start] = 0
    parent = [-1] * n
    
    # Initialiser les nœuds visités
    visited = [False] * n
    
    # Fonction pour trouver le nœud avec la plus petite distance
    def min_distance():
        min_dist = float('inf')
        min_index = -1
        for i in range(n):
            if not visited[i] and dist[i] < min_dist:
                min_dist = dist[i]
                min_index = i
        return min_index
    
    # Itération sur tous les nœuds
    for _ in range(n):
        # Trouver le nœud avec la plus petite distance
        u = min_distance()
        
        # Marquer le nœud comme visité
        visited[u] = True
        
        # Mise à jour des distances des nœuds voisins
        for v in range(n):
            # Vérifier s'il y a une arête entre u et v et si v n'a pas été visité
            if matrice_adjacencee[u][v] == 1 and not visited[v]:
                # Vérifier si une nouvelle distance trouvée est plus courte
                if dist[u] + matrice_coutss[u][v] < dist[v]:
                    # Mise à jour de la distance et du parent de v
                    dist[v] = dist[u] + matrice_coutss[u][v]
                    parent[v] = u
    
    # Reconstruct the shortest path
    path = []
    node = end
    while node != -1:
        path.insert(0, node)
        node = parent[node]
    
    # If the start node is not in the path, the end node is unreachable
    if path[0] != start:
        return []
    
    # Return the path
    return path

#print(dijkstra(matrice_adjacence, matrice_couts, 0, 5))
