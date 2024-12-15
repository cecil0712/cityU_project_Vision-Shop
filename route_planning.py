import heapq
from program.database_connect import get_map

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

class Graph:
    def __init__(self, map_data):
        self.map_data = {k: tuple(v) for k, v in map_data.items()}
        self.grid = {v: k for k, v in self.map_data.items()}

    def neighbors(self, node):
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        results = []
        for dir in dirs:
            neighbor = (node[0] + dir[0], node[1] + dir[1])
            if neighbor in self.grid:
                results.append(neighbor)
        return results

    def cost(self, current, next):
        return 1

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far

def get_route(start,destination):
    graph = Graph(get_map())
    came_from, cost_so_far = a_star_search(graph, start, destination)

    # Print the path
    current = destination
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()

    return path

# test: print(get_route((0,0),(3,2)))