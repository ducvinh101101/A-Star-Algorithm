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

    with open("output.txt", "w", encoding="utf-8") as file:
        file.write(f"{'Duyệt điểm':<12} | {'Danh sách kề':<25} | {'g(x)':<6} | {'h(x)':<6} | Danh sách hàng đợi\n")
        file.write("-" * 90 + "\n")
        file.write(f"{'':<12} | {'':<25} | {'':<6} | {'':<6} | {start_node.name+":"+str(start_node.h)}\n")

        while not open_list.empty():
            _, current = open_list.get()
            visited[current.name] = current.g

            neighbors = graph.get(current.name, [])
            name_neighbor = [name for name, weight in neighbors]

            for neighbor, weight in neighbors:
                g_new = current.g + weight
                h_new = heuristic.get(neighbor,0)
                neighbor_node = Node(neighbor,current,g_new,h_new)

                if neighbor not in visited or g_new < visited[neighbor]:
                    open_list.put((neighbor_node.g + neighbor_node.h, neighbor_node))
                    visited[neighbor] = g_new

            g_current = current.g
            h_current = current.h

            queue_str = " | ".join(f"{node.name}:{f}" for f, node in open_list.queue)

            file.write(f"{current.name:<12} | {str(name_neighbor):<25} | {g_current:<6} | {h_current:<6} | {queue_str}\n")
            if current.name == goal:
                file.write("-" * 90 + "\n")
                file.write("Đã tìm thấy đường đi.\n")
                file.write(f"Chi phí:{current.g}\n")
                return getPath(current)

        file.write("-" * 90 + "\n")
        file.write("Không tìm thấy đường đi.\n")
    return None

path = A_Star(start, goal)
with open("output.txt", "a", encoding="utf-8") as file:
    if path:
        file.write(f"Đường đi ngắn nhất từ {start} đến {goal} là:\n")
        file.write(" -> ".join(path) + "\n")
    else:
        file.write("\nKhông tìm thấy đường đi.\n")

    # while not open_list.empty():
    #     _, current = open_list.get()
    #     print("Duyệt điểm:", current.name)
    #     if current.name == goal:
    #         return getPath(current)
    #     visited[current.name] = current.g
    #     name_neighbor = [name for name, weigth in graph.get(current.name, [])]
    #     print("Danh sách kề:", name_neighbor)
    #     for neighbor, cost in graph.get(current.name, []):
    #         g_new = current.g + cost
    #         h_new = heuristic.get(neighbor, 0)
    #         print(f'g({neighbor})=',g_new)
    #         print(f'f({neighbor})=', g_new+h_new)
    #         neighbor_node = Node(neighbor, current, g_new, h_new)
    #
    #         if neighbor not in visited or g_new < visited[neighbor]:
    #             open_list.put((neighbor_node.g + neighbor_node.h, neighbor_node))
    #             visited[neighbor] = g_new
    #
    #     print("Danh sách hàng đợi:")
    #     for f, node in open_list.queue:
    #         print(node.name, f)
    #     print("===================")
    # return None

# path = A_Star(start, goal)
# if path:
#     print("Đường đi ngắn nhất từ", start, "đến", goal, "là:")
#     print(" -> ".join(path))
# else:
#     print("Không tìm thấy đường đi.")
