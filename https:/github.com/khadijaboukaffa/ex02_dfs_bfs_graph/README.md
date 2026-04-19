# Exercise 2 - DFS and BFS Graph Search

## 📌 Description

This project implements two fundamental graph search algorithms:

* **Depth-First Search (DFS)**
* **Breadth-First Search (BFS)**

The goal is to understand how these algorithms explore a graph and how they can be used to find a path between two nodes.

---

## 🧠 Concepts Learned

* Graph representation using Python dictionary
* DFS (Depth-First Search) using a **stack (LIFO)**
* BFS (Breadth-First Search) using a **queue (FIFO)**
* Difference between exploring **deep vs level-by-level**
* Finding a **path** between two nodes

---

## 📊 Graph Structure

```text
        A
       / \
      B   C
     / \   \
    D   E   F
         \
          G
```

---

## ⚙️ Algorithms

### 🔹 DFS (Depth-First Search)

* Explores as far as possible before backtracking
* Uses a **stack**
* May not return the shortest path

---

### 🔹 BFS (Breadth-First Search)

* Explores level by level
* Uses a **queue**
* Guarantees the shortest path (if all edges have equal cost)

---

## 🧪 Example Output

```text
DFS path:
['A', 'B', 'E', 'G']

BFS path:
['A', 'B', 'E', 'G']
```

---

## ▶️ How to Run

```bash
python3 graph_search.py
```

---

## 📁 Project Structure

```text
ex02_dfs_bfs_graph/
├── graph_search.py
└── README.md
```

---

## 💡 What I Learned

* DFS goes deep first, BFS explores neighbors first
* BFS is better for shortest path problems
* Storing **paths instead of nodes** allows retrieving the full solution
* Understanding stacks vs queues is key in search algorithms

---

## 🚀 Possible Improvements

* Add visualization of the graph
* Measure execution time of DFS vs BFS
* Extend to weighted graphs
* Implement A* search algorithm

---
