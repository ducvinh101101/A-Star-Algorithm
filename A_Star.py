from queue import PriorityQueue

from tabulate import tabulate

with open('input.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]
start, goal = lines[0].split()
graph = {}
heuristic = {}

for line in lines[1:]:
    parts = line.split()
    node = parts[0]
    neighbors = []
    i = 1
    while i <len(parts) - 1:
        if parts[i].isalpha():
            neighbor = parts[i]
            cost = float(parts[i+1])
            neighbors.append((neighbor, cost))
            i += 2
        else:
            break
    graph[node] = neighbors
    h = float(parts[-1])
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
    rows = []

    rows.append(["", "", "", "", "", "", f"{start_node.name}:{start_node.h}"])

    while not open_list.empty():
        _, current = open_list.get()
        visited[current.name] = current.g

        neighbors = graph.get(current.name, [])
        if current.name == goal:
            rows.append([current.name, "TTKT", "", "", "", "", ""])
            with open("output.txt", "w", encoding="utf-8") as file:
                file.write(tabulate(rows, headers=["Duyệt điểm", "Danh sách kề","k(u,v)" , "g(v)", "h(v)", "f(v)", "Danh sách hàng đợi"], tablefmt="grid"))
                file.write("\nChi phí: " + str(current.g))
            return getPath(current)
        name_neighbor = []
        kuv = []
        _g = []
        _h = []
        _f = []
        for name, weight in neighbors:
            name_neighbor.append(name)
            g = current.g + weight
            h = heuristic[name]
            neighbor_node = Node(name, current, g, h)
            f = g + h
            _g.append(g)
            _h.append(h)
            _f.append(f)
            kuv.append(weight)
            if name not in visited or g < visited[name]:
                open_list.put((f, neighbor_node))
                visited[name] = g
        queue_str = " | ".join(f"{node.name}:{f}" for f, node in open_list.queue)
        rows.append([
            current.name,
            "\n".join(name_neighbor),
            "\n".join(map(str, kuv)),
            "\n".join(map(str, _g)),
            "\n".join(map(str, _h)),
            "\n".join(map(str, _f)),
            queue_str
        ])

    with open("output.txt", "w", encoding="utf-8") as file:
        file.write(tabulate(rows, headers=["Duyệt điểm", "Danh sách kề", "k(u,v)" , "g(v)", "h(v)", "f(v)", "Danh sách hàng đợi"], tablefmt="grid"))
        file.write("\n\nKhông tìm thấy đường đi.\n")
    return None

path = A_Star(start, goal)
with open("output.txt", "a", encoding="utf-8") as file:
    if path:
        file.write(f"\nĐường đi ngắn nhất từ {start} đến {goal} là:\n")
        file.write(" -> ".join(path) + "\n")
    else:
        file.write("\nKhông tìm thấy đường đi.\n")