import heapq
from collections import deque

class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []
            return True
        return False

    def add_edge(self, u, v, cost=0):
        if u in self.graph and v in self.graph:
            if not any(neighbor == v for neighbor, c in self.graph[u]):
                self.graph[u].append((v, cost))
                self.graph[v].append((u, cost))
                return True
        return False

    def display(self):
        print("\n--- Current Graph Adjacency List ---")
        for node, neighbors in self.graph.items():
            print(f"{node} -> {neighbors}")

    def get_heuristic(self, goal):
        heuristic = {}
        print(f"\n--- Enter Heuristics (Goal: {goal}) ---")
        for node in self.graph:
            if node == goal:
                heuristic[node] = 0
            else:
                while True:
                    try:
                        val = input(f"Enter Heuristic value for node '{node}': ")
                        heuristic[node] = int(val)
                        break
                    except ValueError:
                        print("Invalid input! Please enter an integer.")
        return heuristic

    def astar(self, start, goal):
        if start not in self.graph or goal not in self.graph:
            print("Start or Goal node not in graph.")
            return

        h_table = self.get_heuristic(goal)
        frontier = []
        heapq.heappush(frontier, (h_table[start], 0, start, [start]))

        explored = []
        iteration = 1
        print("\nIter | Fringe (Node : f) | Explored")
        print("-" * 50)

        while frontier:
            fringe_view = [(n, f) for (f, g, n, p) in sorted(frontier)]
            print(f"{iteration:>4} | {fringe_view} | {explored}")

            f, g, node, path = heapq.heappop(frontier)
            if node in explored: continue
            explored.append(node)

            if node == goal:
                print("\nTotal Cost (g):", g)
                print("Optimized Path:", " -> ".join(map(str, path)))
                return

            for child, cost in self.graph[node]:
                if child not in explored:
                    new_g = g + cost
                    new_f = new_g + h_table[child]
                    heapq.heappush(frontier, (new_f, new_g, child, path + [child]))
            iteration += 1
        print("Goal not reachable")

def setup_graph(g):
    nodes_input = input("Enter all nodes: ").split()
    for n in nodes_input:
        g.add_node(n)

    print("\nEnter edges in format. Type 'done' to finish.")
    while True:
        entry = input("Edge (u v cost): ").strip()
        if entry.lower() == 'done': break
        try:
            u, v, cost = entry.split()
            if g.add_edge(u, v, int(cost)):
                print(f"Edge {u}-{v} added.")
            else:
                print("Error: Ensure nodes exist and edge is not a duplicate.")
        except ValueError:
            print("Invalid format! Use: node1 node2 cost")

g = Graph()
setup_graph(g)
while True:
    print("\n--- MENU ---")
    print("1  Display Graph\n2  A* Search\n3  Reset Graph\n4  Exit")
    ch = input("Enter choice: ")

    if ch == '1':
        g.display()
    elif ch == '2':
        g.astar(input("Start: "), input("Goal: "))
    elif ch == '3':
        g = Graph()
        setup_graph(g)
    elif ch == '4':
        print("End"); break
    else:
        print("Invalid choice")
