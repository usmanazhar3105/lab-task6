import math
import heapq

# Task 3 hospital graph used by the Streamlit application.
locations = {
    "Pharmacy": (0, 0),
    "Main_Corridor": (2, 1),
    "Patient_Wing": (1, 4),
    "Nursing_Station": (4, 2),
    "Laboratory": (5, 5),
    "Emergency_Ward": (8, 6)
}

hospital_graph = {
    "Pharmacy": {"Main_Corridor": 2.2, "Patient_Wing": 4.1},
    "Main_Corridor": {"Nursing_Station": 2.2},
    "Patient_Wing": {"Laboratory": 5.0},
    "Nursing_Station": {"Laboratory": 3.2, "Emergency_Ward": 6.0},
    "Laboratory": {"Emergency_Ward": 3.2},
    "Emergency_Ward": {}
}

def heuristic(current, goal):
    x1, y1 = locations[current]
    x2, y2 = locations[goal]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def gbfs(start, goal):
    frontier = [(heuristic(start, goal), start)]
    came_from = {start: None}
    explored = set()

    while frontier:
        _, current = heapq.heappop(frontier)

        if current in explored:
            continue

        explored.add(current)

        if current == goal:
            break

        for neighbor in hospital_graph[current]:
            if neighbor not in explored:
                if neighbor not in came_from:
                    came_from[neighbor] = current
                heapq.heappush(
                    frontier,
                    (heuristic(neighbor, goal), neighbor)
                )

    if goal not in came_from:
        return None, None

    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()

    cost = 0
    for i in range(len(path) - 1):
        cost += hospital_graph[path[i]][path[i + 1]]

    return path, cost

def a_star(start, goal):
    frontier = [(heuristic(start, goal), 0, start)]
    came_from = {start: None}
    g_cost = {start: 0}
    explored = set()

    while frontier:
        _, current_g, current = heapq.heappop(frontier)

        if current in explored:
            continue
        if current_g > g_cost.get(current, float("inf")):
            continue

        explored.add(current)

        if current == goal:
            break

        for neighbor, cost in hospital_graph[current].items():
            tentative_g = current_g + cost

            if tentative_g < g_cost.get(neighbor, float("inf")):
                g_cost[neighbor] = tentative_g
                came_from[neighbor] = current
                f_value = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(
                    frontier,
                    (f_value, tentative_g, neighbor)
                )

    if goal not in came_from:
        return None, None

    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()

    return path, g_cost[goal]
