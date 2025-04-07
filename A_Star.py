from queue import PriorityQueue

with open("input.txt", "r") as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

start, goal = lines[0].split()
graph = {}
heuristic = {}

for line in lines[1:]:
    parts = line.split()
    node = parts[0]
    neighbors = []
    i = 1
    while i < len(parts) - 1:
        if parts[i].isalpha():
            neighbor = parts[i]
            cost = int(parts[i+1])
            neighbors.append((neighbor, cost))
            i += 2
        else:
            break
    h = int(parts[-1])
    graph[node] = neighbors
    heuristic[node] = h


class Node:
    def __init__(self, name, par=None, g=0, h=0):
        self.name = name
        self.par = par
        self.g = g
        self.h = h

    def __lt__(self, other):
        return self.g + self.h < other.g + other.h

def getPath(node):
    path = []
    while node:
        path.append(node.name)
        node = node.par
    return path[::-1]


def A_Star(start, goal):
    open_list = PriorityQueue()
    start_node = Node(start, None, 0, heuristic[start])
    open_list.put((start_node.g + start_node.h, start_node))
    visited = {}

    while not open_list.empty():
        _, current = open_list.get()

        if current.name == goal:
            return getPath(current)

        visited[current.name] = current.g

        for neighbor, cost in graph.get(current.name, []):
            g_new = current.g + cost
            h_new = heuristic.get(neighbor, 0)
            neighbor_node = Node(neighbor, current, g_new, h_new)

            if neighbor not in visited or g_new < visited[neighbor]:
                open_list.put((neighbor_node.g + neighbor_node.h, neighbor_node))
                visited[neighbor] = g_new
    return None

path = A_Star(start, goal)
if path:
    print("Đường đi ngắn nhất từ", start, "đến", goal, "là:")
    print(" -> ".join(path))
else:
    print("Không tìm thấy đường đi.")
