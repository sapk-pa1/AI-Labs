import heapq
from graph import graph_weighted


def ucs(graph, start, goal):
    heap = [(0, [start])]
    visited = set()

    while heap:
        cost, path = heapq.heappop(heap)
        node = path[-1]

        if node == goal:
            return path, cost

        if node not in visited:
            visited.add(node)
            for neighbor, weight in graph[node]:
                new_path = list(path)
                new_path.append(neighbor)
                heapq.heappush(heap, (cost + weight, new_path))

    return None, float("inf")


if __name__ == "__main__":

    path, cost = ucs(graph_weighted, "A", "F")
    print("UCS Path:", path)
    print("UCS Cost:", cost)
