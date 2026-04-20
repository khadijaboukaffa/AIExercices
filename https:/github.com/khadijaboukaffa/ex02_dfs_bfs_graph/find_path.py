graph = {
    "A": ["B", "C"],# A est connecté à B et C
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["G"],
    "F": [],
    "G": []
}

def bfs_path(graph, start, goal):
    """
    Cette fonction fait un parcours en largeur (BFS)
    à partir du noeud de départ.
    """
    # La file contient des chemins (liste de noeuds)
    queue = [[start]]
    print(' ----------- queue ----------')
    print(queue)

    # Liste des noeuds visités
    visited = []

    while queue:
        # On prend le premier chemin
        path = queue.pop(0)
        print(' -------------- path -----------')
        print(path)

        # On regarde le dernier noeud du chemin
        node = path[-1]
        print(' -------------- node -----------')
        print(node)

        # Si on a trouvé le but → on retourne le chemin
        if node == goal:
            return path

        # Si on n'a pas encore visité ce noeud
        if node not in visited:
            visited.append(node)

            # On explore les voisins
            for neighbor in graph[node]:
                # On crée un nouveau chemin
                print('------- meighbor------')
                print(neighbor)
                print('------- mew path ------')
                new_path = path + [neighbor]
                print(new_path)
                # On ajoute ce chemin à la file
                queue.append(new_path)
                print(' ------ queue after -----')
                print(queue)

    # Si aucun chemin trouvé
    return None


def dfs_path(graph, start, goal):
    # La pile contient des chemins complets
    stack = [[start]]

    # Liste des noeuds visités
    visited = []

    while stack:
        # On prend le dernier chemin ajouté
        path = stack.pop()

        # Le noeud courant = dernier noeud du chemin
        node = path[-1]

        # Si on a trouvé le but, on retourne le chemin
        if node == goal:
            return path

        # Si le noeud n'a pas encore été visité
        if node not in visited:
            visited.append(node)

            # On ajoute les voisins à la pile
            for neighbor in reversed(graph[node]):
                new_path = path + [neighbor]
                stack.append(new_path)

    # Si aucun chemin trouvé
    return None

"""""
trouver le chemin de A vers G bar BFS

"""
path = bfs_path(graph, "A", "G")
print("Path found with BFS:")
print(path)

"""""
path = bfs_path(graph, "A", "F")
print("Path found with BFS:")
print(path)

path = dfs_path(graph, "A", "G")

print("DFS path found:")
print(path)

path = dfs_path(graph, "A", "F")
print("Path found with DFS:")
print(path)
"""""