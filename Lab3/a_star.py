import heapq
from graph import graph_weighted, heuristic


def a_star(graph, start, goal, heuristic):
    heap = [(heuristic[start], 0, [start])]
    visited = set()

    while heap:
        f, g, path = heapq.heappop(heap)
        node = path[-1]

        if node == goal:
            return path, g

        if node not in visited:
            visited.add(node)
            for neighbor, weight in graph[node]:
                new_g = g + weight
                new_f = new_g + heuristic[neighbor]
                new_path = list(path)
                new_path.append(neighbor)
                heapq.heappush(heap, (new_f, new_g, new_path))

    return None, float("inf")


if __name__ == "__main__":
    path, cost = a_star(graph_weighted, "A", "F", heuristic)
    print("A* Path:", path)
    print("A* Cost:", cost)
