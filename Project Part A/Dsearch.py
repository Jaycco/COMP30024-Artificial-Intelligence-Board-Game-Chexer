# change from https://www.redblobgames.com/pathfinding/a-star/implementation.html#algorithm
import heapq

# Dijkstra search, return cost_dictionary. ({piece coordianate: heuristic, ..}
def Dsearch(blocks, colour):

    # goals according to colour
    if colour == "red":
        goals = [[3, -3], [3, -2], [3, -1], [3, 0]]
    elif colour == "green":
        goals = [[-3, 3], [-2, 3], [-1, 3], [0, 3]]
    elif colour == "blue":
        goals = [[-3, 0], [-2, -1], [-1, -2], [0, -3]]
    frontier = PriorityQueue()
    cost_to_exit = {}

    # set cost of goal coordinates in cost_dictionary to 1. ({goal coordinate: 1, ..})
    for goal in goals:
        if goal not in blocks:
            frontier.put(tuple(goal), 1)
            cost_to_exit[tuple(goal)] = 1

    #
    while not frontier.empty():
        current = frontier.get()
        for next in neighbors(current, blocks, goals):
            next = tuple(next)
            current = tuple(current)

            # get new_cost of each next coordinate
            if next in cost_to_exit:
                new_cost = min(cost_to_exit[current] + 1, cost_to_exit[next])
            else:
                new_cost = cost_to_exit[current] + 1

            # use new_cost to update priority queue for each next coordinate
            if next not in cost_to_exit or new_cost < cost_to_exit[next]:
                cost_to_exit[next] = new_cost
                priority = new_cost
                frontier.put(next, priority)
    return cost_to_exit

# return all coordinates current coordinate can move or jump to
def neighbors(node, blocks, goals):
    dirs = [[0, -1], [1, -1], [1, 0], [0, 1], [-1, 1], [-1, 0]]
    result = []
    all_nodes = []
    ran = range(-3, +3 + 1)
    for qr in [(q, r) for q in ran for r in ran if -q - r in ran]:
        all_nodes.append(qr)
    # consider jump action is possible even there is no neighbor block piece
    for dir in dirs:
        neighbor = [node[0] + dir[0], node[1] + dir[1]]
        neighbor_jump = [neighbor[0] + dir[0], neighbor[1] + dir[1]]
        if tuple(neighbor) in all_nodes:
            if neighbor not in blocks and neighbor not in goals:
                result.append(neighbor)
        if tuple(neighbor_jump) in all_nodes:
            if neighbor_jump not in blocks and neighbor_jump not in goals:
                result.append(neighbor_jump)
    return result



class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]
