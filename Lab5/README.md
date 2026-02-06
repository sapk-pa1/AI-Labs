# Wumpus World AI: Knowledge-Based Agent Simulation

This project implements a fully functional **Artificial Intelligence Agent** capable of solving the classic "Wumpus World" problem. It demonstrates core AI concepts including Knowledge Representation, Propositional Logic, Search Algorithms, and Intelligent Agent Design.


---

## 📌 Project Overview

**The Wumpus World** is a cave consisting of a 4x4 grid of rooms surrounded by walls. The agent starts at `[0,0]` and must navigate the cave to find the **Gold**, avoiding deadly **Pits** and the **Wumpus** monster.

### Key Features
* **Environment Simulation:** A 4x4 grid with randomized hazards (Pits, Wumpus, Gold).
* **PEAS Implementation:** Full implementation of Performance, Environment, Actuators, and Sensors.
* **Inference Engine:** A logical agent that deduces safe moves based on percepts (Breeze, Stench).
* **Pathfinding:** Uses Breadth-First Search (BFS) to plan routes to safety or objectives.
* **Scoring System:** Tracks performance based on steps taken, arrows used, and gold retrieval.

---

## 🚀 How to Run

### Prerequisites
* Python 3.x

### Installation
1.  Clone this repository or copy the source code into a file named `simulation.py`.
2.  Run the simulation directly from your terminal:

```bash
python simulation.py
```

📝 Future Improvements
Advanced Inference: Implement a SAT solver to deduce Pit locations even when risks exist (probabilistic reasoning).

Optimized Planning: Use A* search instead of BFS to minimize movement costs.

UI Visualization: Create a graphical interface using pygame or tkinter.

👤 Author
Name: Pawan Sapkota Sharma

Course: Artificial Intelligence 