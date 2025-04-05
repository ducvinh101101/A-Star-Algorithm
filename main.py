import heapq
import math


def heuristic(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def a_star_search(graph, coords, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0

    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic(coords[start], coords[goal])

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for neighbor, cost in graph[current]:
            tentative_g_score = g_score[current] + cost

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(coords[neighbor], coords[goal])
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None



coords = {
    'A': (0, 0),
    'B': (2, 4),
    'C': (5, 3),
    'D': (6, 1),
    'E': (8, 0)
}

graph = {
    'A': [('B', 4.5), ('C', 6)],
    'B': [('A', 4.5), ('C', 3)],
    'C': [('A', 6), ('B', 3), ('D', 2)],
    'D': [('C', 2), ('E', 3)],
    'E': [('D', 3)]
}


path = a_star_search(graph, coords, 'B', 'E')
print("Đường đi ngắn nhất:", path)
