
## Lab Exercise 3: Graph Search – BFS, DFS, UCS and A*

---

## Objective

In this lab, students will implement and compare four fundamental **search algorithms** used in Artificial Intelligence:

- Breadth-First Search (BFS)  
- Depth-First Search (DFS)  
- Uniform Cost Search (UCS)  
- A* Search  

By the end of this lab, students will understand:

- How different search strategies explore a state space  
- The difference between uninformed and informed search  
- How path cost and heuristics influence search behavior  
- Why some algorithms guarantee shortest paths and others do not  
- How search algorithms are used for planning and navigation  

---

## Background Theory (Simplified)

### What is Search in AI?

Search is the process of finding a sequence of actions that transforms an initial state into a goal state.

Examples:

- Finding a route on Google Maps  
- Solving a maze  
- Game playing  
- Robot navigation  

A problem consists of:

- **Initial State**  
- **Actions**  
- **Goal State**  
- **Cost (optional)**  

---

### Types of Search Algorithms

| Algorithm | Strategy | Uses Cost? | Uses Heuristic? | Guarantees Shortest Path? |
|------------|-----------|-------------|------------------|----------------------------|
| BFS | Level-by-level | ❌ | ❌ | ✅ (unweighted) |
| DFS | Go deep first | ❌ | ❌ | ❌ |
| UCS | Lowest path cost | ✅ | ❌ | ✅ |
| A* | Cost + Heuristic | ✅ | ✅ | ✅ (if heuristic is admissible) |

---

## Scenario Description

You will simulate a small **map of connected locations** represented as a graph.

- Each node represents a city (or room).  
- Each edge represents a road (or corridor).  
- Some roads have different travel costs.  

Your task is to find a path from a **Start node** to a **Goal node** using different search strategies.

## Graph Definition

### Unweighted Graph (For BFS and DFS)
![Unweighted Graph](resources/graph_unweighted.png)

```python 
graph_unweighted = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}
```

### Weighted Graph (For UCS)
```python
graph_weighted = {
    'A': [('B', 1), ('C', 4)],
    'B': [('D', 5), ('E', 2)],
    'C': [('F', 3)],
    'D': [],
    'E': [('F', 1)],
    'F': []
}
```
![Unweighted Graph](resources/graph_weighted.png)

### Heuristics Function (A*)

```python 
heuristic = {
    'A': 4,
    'B': 2,
    'C': 2,
    'D': 6,
    'E': 1,
    'F': 0
}
```
![Heuristic Graph](resources/graph_with_heuristics.png)