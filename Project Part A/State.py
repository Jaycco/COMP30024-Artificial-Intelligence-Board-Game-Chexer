import math

class State:
    def __init__(self, colour, pieces, blocks, action):
        self.colour = colour
        self.pieces = pieces
        self.blocks = blocks
        self.priority = 0
        if self.colour == "red":
            self.goals = [[3, -3], [3, -2], [3, -1], [3, 0]]
        elif self.colour == "green":
            self.goals = [[-3, 3], [-2, 3], [-1, 3], [0, 3]]
        elif self.colour == "blue":
            self.goals = [[-3, 0], [-2, -1], [-1, -2], [0, -3]]
        self.action = action

    def __eq__(self, other):
        return sorted(self.pieces) == sorted(other.pieces) and sorted(self.blocks) == sorted(other.blocks)
        # piece equals

    def __hash__(self):
        s_pieces = sorted(self.pieces)
        s_blocks = sorted(self.blocks)
        pieces_tuple = tuple(tuple(x) for x in s_pieces)
        blocks_tuple = tuple(tuple(x) for x in s_blocks)
        my_tuple = (pieces_tuple, blocks_tuple)
        return hash(my_tuple)

    def successors(self):
        dirs = [[0, -1], [1, -1], [1, 0], [0, 1], [-1, 1], [-1, 0]]
        result = []
        all_nodes = []
        index_of_piece = 0
        ran = range(-3, +3 + 1)
        for qr in [[q, r] for q in ran for r in ran if -q - r in ran]:
            all_nodes.append(qr)

        # find successor states of each piece in pieces, only return one state(exit action) if any piece is in goal hex
        for piece in self.pieces:
            if piece in self.goals:
                state_blocks = self.blocks.copy()
                state_pieces = self.pieces.copy()
                state_colour = self.colour
                state_pieces.pop(index_of_piece)
                state_next = State(state_colour, state_pieces, state_blocks, 0)
                result = {state_next}
                return result
            else:
                for dir in dirs:
                    successor = [piece[0] + dir[0], piece[1] + dir[1]]
                    if successor in all_nodes:
                        if successor in self.pieces or successor in self.blocks:
                            successor_jump = [successor[0] + dir[0], successor[1] + dir[1]]
                            if successor_jump not in self.pieces and successor_jump not in self.blocks and \
                                    successor_jump in all_nodes:
                                state_blocks = self.blocks.copy()
                                state_pieces = self.pieces.copy()
                                state_colour = self.colour
                                state_pieces.pop(index_of_piece)
                                state_pieces.append(successor_jump)
                                state_next = State(state_colour, state_pieces, state_blocks, "jump")
                                result.append(state_next)
                        else:
                            state_blocks = self.blocks.copy()
                            state_pieces = self.pieces.copy()
                            state_colour = self.colour
                            state_pieces.pop(index_of_piece)
                            state_pieces.append(successor)
                            state_next = State(state_colour, state_pieces, state_blocks, "move")
                            result.append(state_next)
            index_of_piece += 1
        return result

    # return cost of moving from coordianate g to coordianate n
    def hexe_distance(self, g, n):
        (x1, y1) = g
        (x2, y2) = n
        return (abs(x1 - x2)
                + abs(x1 + y1 - x2 - y2)
                + abs(y1 - y2)) / 2

    # return total heuristic of pieces given in the cost_dictionary({piece coordianate: heuristic, ..})
    def heuristic(self, cost_dictionary):
        total = 0
        for piece in self.pieces:
            total += cost_dictionary[tuple(piece)]
        return total