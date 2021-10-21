import random
import sys
from read import readInput
from write import writeOutput
from copy import deepcopy
import pdb

from host import GO


class QLearningPlayer():
    def __init__(self):
        pass

    def get_input(self, go, piece_type):
        pass


'''
implementation notes

start building the tree after a few turns so the choices actually have an effect
depth: 4, branching factor: 10
steps:
-get current state
-build the tree as a member variable
-once the tree has been built to a certain depth, score all the nodes
-(alpha beta step: prune the nodes that do not need to be evaluated)
-choose the node of the root that has the highest evaluation

evaluation function for each state according to a strategy
- number of stones on the center
- number of stones on the edges
- number of stones on the board for each player - score function
other strategies
- do not place stones on the edges on your first turn
change the depth and branching factors depending on the time you have left
e.g. search more when you have time; search less when you have less



questions
-since we have go = GO(N), is it okay to use the member functions of go?
-in get_input, we use go.size
'''


class Node:
    def __init__(self, data):
        self.state = data
        self.move = [-1, -1]
        self.score = 0
        self.children = []

    def addChild(self, node):
        self.children.append(node)


class MinimaxPlayer():
    def __init__(self):
        self.type = 'minimax'
        self.num_moves = 0
        self.minimax_tree = Node(0)  # make a node with the current state
        self.piece_type = 0

    def write_num_moves(self, num_moves):
        f = open("num_moves.txt", "w")
        f.write(str(num_moves))

    '''
    get num moves
    increment it
    write it
    '''

    def get_num_moves(self):
        # Using readlines()
        file = open('num_moves.txt', 'r')
        lines = file.readlines()

        num_moves = 0
        for line in lines:
            num_moves = int(line.strip())
            break

        return num_moves

    '''
    Get one input.

    :param go: Go instance.
    :param piece_type: 1('X') or 2('O').
    :return: (row, column) coordinate of input.
    '''

    def get_input(self, go, piece_type):

        # determine the number of moves that've been played
        num_moves_previous = 0
        num_moves_current = 0
        num_moves = 0
        for i in range(go.size):
            for j in range(go.size):
                if go.previous_board[i][j] != 0:
                    num_moves_previous += 1
                if go.board[i][j] != 0:
                    num_moves_current += 1
        if num_moves_previous == 0 and num_moves_current == 0:
            self.write_num_moves(num_moves)
        elif num_moves_previous == 0:
            num_moves += 1
            self.write_num_moves(num_moves)
        else:
            num_moves = self.get_num_moves()
            num_moves += 1  # account for the opponent's move
            self.write_num_moves(num_moves)

        print("get input, move number ", num_moves + 1)

        possible_placements = []
        for i in range(go.size):
            for j in range(go.size):
                if go.valid_place_check(i, j, piece_type, test_check=True):
                    possible_placements.append((i, j))

        if not possible_placements:
            return "PASS"
        else:
            num_moves += 1
            self.write_num_moves(num_moves)
            '''
            decrease depth as players make more moves
            repeat tree building at every turn
            '''
            #if num_moves == 21 or num_moves == 22 and :  # could go first or second
            if num_moves >= 20:
                # if you go last, you would only need to make a tree of depth 2 (1 for current state)
                print("building minimax tree")
                # self.build_minimax_tree(go, piece_type, 1)
                root = Node(go)
                # root is at depth 0 because the build function builds to depth_max - 1
                if piece_type == 2:  # O, num_moves == even
                    #depth_max = 4  # exits when depth == depth_max
                    depth_max = 24 - num_moves + 2
                    depth_start = 1
                    self.build_minimax_tree_recursive(
                        root, piece_type, depth_max, depth_start)
                    maxNode = self.read_minimax_tree_recursive(
                        root, True, depth_max, depth_start)
                    print("max evaluation: ", maxNode.move, "move: ", maxNode.move)
                    return maxNode.move
                else:
                    #depth_max = 5
                    depth_max = 24 - num_moves + 2
                    depth_start = 1
                    self.build_minimax_tree_recursive(
                        root, piece_type, depth_max, depth_start)
                    maxNode = self.read_minimax_tree_recursive(
                        root, True, depth_max, depth_start)
                    print("max evaluation: ", maxNode.move, "move: ", maxNode.move)
                    return maxNode.move

            else:
                return random.choice(possible_placements)

    def read_minimax_tree_recursive(self, root, isMax, depth_max, depth):
        print("minimax tree read recursive called, move: ", root.move)
        pdb.set_trace()
        if depth == depth_max:
            return root

        if isMax:
            maxNode = Node(0)
            maxNode.score = -100  # negative infinity

            for node in root.children:
                maxNodeChild = self.read_minimax_tree_recursive(
                    node, False, depth_max, depth+1)
                if maxNodeChild.score >= maxNode.score:
                    maxNode = node

            print("max's score", maxNode.score)
            return maxNode

        else:
            minNode = Node(0)
            minNode.score = +100  # negative infinity

            for node in root.children:
                minNodeChild = self.read_minimax_tree_recursive(
                    node, True, depth_max, depth+1)
                if minNodeChild.score <= minNode.score:
                    minNode = node

            print("min's score", minNode.score)
            return minNode

    # this will always be in the perspective of my_player
    # if it's a terminal state, win: +1, loss: 0, draw: 0.5

    def evaluate(self, node, piece_type):
        if len(node.children) == 0:
            if node.state.judge_winner() == piece_type:
                return 1
            elif node.state.judge_winner() == (3-piece_type):
                return 0
            elif node.state.judge_winner() == 0:
                return 0.5

    def build_minimax_tree_recursive(self, root, piece_type, depth_max, depth):
        if depth == depth_max:  # maximum depth to explore
            return root

        current_state = deepcopy(root.state)
        branching_factor = 4 #observation
        num_branches = 0
        for i in range(current_state.size):
            for j in range(current_state.size):
                if current_state.valid_place_check(i, j, piece_type, test_check=True):
                    num_branches += 1
                    if num_branches >= branching_factor:
                        pass
                    else:
                        next_state = deepcopy(current_state)
                        next_state.place_chess(i, j, piece_type)
                        next_state.remove_died_pieces(3-piece_type)
                        child = Node(next_state)
                        child.move = [i, j]
                        # pass the node to check if it has any children
                        print("depth", depth, ", move", i, j, "piece type", piece_type)
                        if (self.get_num_moves()+(depth-1)) == 24:  # evaluate the state if it's terminal
                            # evaluate in the perspective of the player
                            child.score = self.evaluate(child, self.piece_type)
                            print("evaluation ", child.score)
                        root.addChild(child)

                        self.build_minimax_tree_recursive(
                            child, 3-piece_type, depth_max, depth+1)


class RandomPlayer():
    def __init__(self):
        self.type = 'random'

    def get_input(self, go, piece_type):
        '''
        Get one input.

        :param go: Go instance.
        :param piece_type: 1('X') or 2('O').
        :return: (row, column) coordinate of input.
        '''

        possible_placements = []
        for i in range(go.size):
            for j in range(go.size):
                if go.valid_place_check(i, j, piece_type, test_check=True):
                    possible_placements.append((i, j))

        if not possible_placements:
            return "PASS"
        else:
            return random.choice(possible_placements)


if __name__ == "__main__":
    N = 5
    piece_type, previous_board, board = readInput(N)
    go = GO(N)
    go.set_board(piece_type, previous_board, board)
    # player = RandomPlayer()
    player = MinimaxPlayer()
    player.piece_type = piece_type
    action = player.get_input(go, piece_type)
    writeOutput(action)
