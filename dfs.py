from graph import graph_unweighted


def dfs(graph, start, goal):
    stack = [[start]]
    visited = set()

    while stack:
        path = stack.pop()
        node = path[-1]

        if node == goal:
            return path

        if node not in visited:
            visited.add(node)
            for neighbor in reversed(graph[node]):
                new_path = list(path)
                new_path.append(neighbor)
                stack.append(new_path)

    return None


if __name__ == "__main__":
    print("DFS Path:", dfs(graph_unweighted, "A", "F"))
