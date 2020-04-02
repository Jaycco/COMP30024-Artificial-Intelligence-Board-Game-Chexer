"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching
Authors:
"""

import sys
import json
from State import State
from PriorityQueue import PriorityQueue
from Dsearch import Dsearch


def main():

    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: Search for and output winning sequence of moves
    # ...

    # {'colour': 'red', 'pieces': [[0, 0], [0, -1], [-2, 1]], 'blocks': [[-1, 0], [-1, 1], [1, 1], [3, -1]]}
    board_dict = {}

    for i in data.get("pieces"):
        board_dict[tuple(i)] = "red"
    for i in data.get("blocks"):
        board_dict[tuple(i)] = "Block"


    # run dijkstra
    D_cost_so_far = Dsearch(data.get("blocks"), data.get("colour"))

    # A*, initialize start, goal and run
    start = State(data.get("colour"), data.get("pieces"), data.get("blocks"), 0)
    goal = State(data.get("colour"), [], data.get("blocks"), 0)
    a_star_search(start, goal, D_cost_so_far)

# change from https://www.redblobgames.com/pathfinding/a-star/implementation.html#algorithm
def a_star_search(start, goal, D_cost_so_far):

    frontier = PriorityQueue()
    frontier.put(start)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    while not frontier.empty():
        current = frontier.get()
        if current == goal:
            break
        for next in current.successors():
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                next.priority = new_cost + next.heuristic(D_cost_so_far)
                frontier.put(next)
                came_from[next] = current

    # find path
    current = goal
    path = []
    while current != start:
        path.append(current.pieces)
        current = came_from[current]
    path.append(start.pieces)
    path.reverse()

    # print result
    last = path[0]
    cur_piece = 0
    last_piece = 0
    actionNo = 0
    for cur in path:

        # print exit if length of path change
        if len(cur) < len(last):
            for piece_i in range(0, len(last)):
                if last[piece_i] not in cur:
                    last_piece = last[piece_i]
            print('EXIT from {0}.'.format(tuple(last_piece)))
            actionNo += 1
        else:
            for piece_i in range(0, len(cur)):
                if cur[piece_i] not in last:
                    cur_piece = cur[piece_i]
            for piece_i in range(0, len(last)):
                if last[piece_i] not in cur:
                    last_piece = last[piece_i]
            # print move if hexa distance is 1, jump if hexa distance is 2
            if type(cur_piece) != type(0):
                if hexe_distance(last_piece,cur_piece) > 1:
                    print('JUMP from {0} to {1}.'.format(tuple(last_piece), tuple(cur_piece)))
                    actionNo += 1
                else:
                    print('MOVE from {0} to {1}.'.format(tuple(last_piece), tuple(cur_piece)))
                    actionNo += 1
        last = cur


def hexe_distance(g, n):
    (x1, y1) = g
    (x2, y2) = n
    return (abs(x1 - x2)
            + abs(x1 + y1 - x2 - y2)
            + abs(y1 - y2)) / 2




def print_board(board_dict, message="", debug=False, **kwargs):
    """
    Helper function to print a drawing of a hexagonal board's contents.
    Arguments:
    * `board_dict` -- dictionary with tuples for keys and anything printable
    for values. The tuple keys are interpreted as hexagonal coordinates (using
    the axial coordinate system outlined in the project specification) and the
    values are formatted as strings and placed in the drawing at the corres-
    ponding location (only the first 5 characters of each string are used, to
    keep the drawings small). Coordinates with missing values are left blank.
    Keyword arguments:
    * `message` -- an optional message to include on the first line of the
    drawing (above the board) -- default `""` (resulting in a blank message).
    * `debug` -- for a larger board drawing that includes the coordinates
    inside each hex, set this to `True` -- default `False`.
    * Or, any other keyword arguments! They will be forwarded to `print()`.
    """

    # Set up the board template:
    if not debug:
        # Use the normal board template (smaller, not showing coordinates)
        template = """# {0}
#           .-'-._.-'-._.-'-._.-'-.
#          |{16:}|{23:}|{29:}|{34:}|
#        .-'-._.-'-._.-'-._.-'-._.-'-.
#       |{10:}|{17:}|{24:}|{30:}|{35:}|
#     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
#    |{05:}|{11:}|{18:}|{25:}|{31:}|{36:}|
#  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
# |{01:}|{06:}|{12:}|{19:}|{26:}|{32:}|{37:}|
# '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#    |{02:}|{07:}|{13:}|{20:}|{27:}|{33:}|
#    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#       |{03:}|{08:}|{14:}|{21:}|{28:}|
#       '-._.-'-._.-'-._.-'-._.-'-._.-'
#          |{04:}|{09:}|{15:}|{22:}|
#          '-._.-'-._.-'-._.-'-._.-'"""
    else:
        # Use the debug board template (larger, showing coordinates)
        template = """# {0}
#              ,-' `-._,-' `-._,-' `-._,-' `-.
#             | {16:} | {23:} | {29:} | {34:} |
#             |  0,-3 |  1,-3 |  2,-3 |  3,-3 |
#          ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#         | {10:} | {17:} | {24:} | {30:} | {35:} |
#         | -1,-2 |  0,-2 |  1,-2 |  2,-2 |  3,-2 |
#      ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#     | {05:} | {11:} | {18:} | {25:} | {31:} | {36:} |
#     | -2,-1 | -1,-1 |  0,-1 |  1,-1 |  2,-1 |  3,-1 |
#  ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
# | {01:} | {06:} | {12:} | {19:} | {26:} | {32:} | {37:} |
# | -3, 0 | -2, 0 | -1, 0 |  0, 0 |  1, 0 |  2, 0 |  3, 0 |
#  `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-'
#     | {02:} | {07:} | {13:} | {20:} | {27:} | {33:} |
#     | -3, 1 | -2, 1 | -1, 1 |  0, 1 |  1, 1 |  2, 1 |
#      `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-'
#         | {03:} | {08:} | {14:} | {21:} | {28:} |
#         | -3, 2 | -2, 2 | -1, 2 |  0, 2 |  1, 2 | key:
#          `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' ,-' `-.
#             | {04:} | {09:} | {15:} | {22:} |   | input |
#             | -3, 3 | -2, 3 | -1, 3 |  0, 3 |   |  q, r |
#              `-._,-' `-._,-' `-._,-' `-._,-'     `-._,-'"""

    # prepare the provided board contents as strings, formatted to size.
    ran = range(-3, +3+1)
    cells = []
    for qr in [(q,r) for q in ran for r in ran if -q-r in ran]:
        if qr in board_dict:
            cell = str(board_dict[qr]).center(5)
        else:
            cell = "     " # 5 spaces will fill a cell
        cells.append(cell)

    # fill in the template to create the board drawing, then print!
    board = template.format(message, *cells)
    print(board, **kwargs)


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
