graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["G"],
    "F": [],
    "G": []
}


def dfs(graph, start):
    visited = []
    stack = [start]

    while stack:
        node = stack.pop()

        if node not in visited:
            visited.append(node)

            for neighbor in reversed(graph[node]):
                stack.append(neighbor)

    return visited


def bfs(graph, start):
    visited = []
    queue = [start]
    
    while queue:
        node = queue.pop(0)

        if node not in visited:
            visited.append(node)

            for neighbor in graph[node]:
                queue.append(neighbor)

    return visited


print("DFS visit order:")
print(dfs(graph, "A"))

print()

print("BFS visit order:")
print(bfs(graph, "A"))