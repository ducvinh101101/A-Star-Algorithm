from queue import PriorityQueue
from tabulate import tabulate

with open("test.txt", "r") as f:
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
            cost = float(parts[i + 1])
            neighbors.append((neighbor, cost))
            i += 2
        else:
            break
    h = float(parts[-1])
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
    rows = []

    rows.append(["", "", "", "", "", "", f"{start_node.name}:{start_node.h}"])

    while not open_list.empty():
        _, current = open_list.get()
        visited[current.name] = current.g

        neighbors = graph.get(current.name, [])
        name_neighbor = [name for name, weight in neighbors]
        kuv = []
        g_ = []
        h_ = []
        f_ = []

        for neighbor, weight in neighbors:
            g_new = current.g + weight
            h_new = heuristic.get(neighbor, 0)
            neighbor_node = Node(neighbor, current, g_new, h_new)
            kuv.append(weight)
            g_.append(g_new)
            h_.append(h_new)
            f_.append(g_new+h_new)
            if neighbor not in visited or g_new < visited[neighbor]:
                open_list.put((neighbor_node.g + neighbor_node.h, neighbor_node))
                visited[neighbor] = g_new

        queue_str = " | ".join(f"{node.name}:{f}" for f, node in open_list.queue[:3])
        if(current.name ==goal):
            queue_str = ""
        rows.append([
            current.name,
            "\n".join(name_neighbor),
            "\n".join(map(str, kuv)),
            "\n".join(map(str, g_)),
            "\n".join(map(str, h_)),
            "\n".join(map(str, f_)),
            queue_str + "| ..."
        ])
        if current.name == goal:

            with open("output.txt", "w", encoding="utf-8") as file:
                file.write(tabulate(rows, headers=["Duyệt điểm", "Danh sách kề","k(u,v)" , "g(v)", "h(v)", "f(v)", "Danh sách hàng đợi"], tablefmt="grid"))
                file.write("\n\nĐã tìm thấy đường đi.\n")
                file.write(f"Chi phí: {current.g}\n")
            return getPath(current)

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
