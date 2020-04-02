# change from https://www.redblobgames.com/pathfinding/a-star/implementation.html#algorithm
from PQheap import heappush, _siftdown, heappop, _siftup

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item):
        heappush(self.elements, item)

    def get(self):
        return heappop(self.elements)
