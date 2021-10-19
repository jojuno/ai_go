import random
import sys
from read import readInput
from write import writeOutput
from copy import deepcopy

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
        self.minimax_tree = Node(0) #make a node with the current state

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

        #determine the number of moves that've been played
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
            num_moves += 1 #account for the opponent's move
            self.write_num_moves(num_moves)

        
        print("get input, move number ", num_moves + 1)

        possible_placements = []
        for i in range(go.size):
            for j in range(go.size):
                if go.valid_place_check(i, j, piece_type, test_check = True):
                    possible_placements.append((i,j))

        if not possible_placements:
            return "PASS"
        else:
            num_moves += 1
            self.write_num_moves(num_moves)
            if num_moves == 10 or num_moves == 11: #could go first or second
                print("building minimax tree")
                #self.build_minimax_tree(go, piece_type, 1)
                root = Node(go)
                self.build_minimax_tree_recursive(root, piece_type, 2, 0) #root is at depth 0 because the build function builds to depth_max - 1
                #read the tree
                #choose the max value
                #return self.read_minimax_tree(piece_type)
                return random.choice(possible_placements) #placeholder
            else:
                return random.choice(possible_placements)

    '''
    def add_children(self, node, piece_type): #exclude depth for now
        current_state = deepcopy(node.data) #make a deep copy of the current state
        parent = Node(current_state) #go instead of go.board so you can leverage the member functions
        for i in range(current_state.size):
            for j in range(current_state.size):
                if current_state.valid_place_check(i, j, piece_type, test_check = True):
                    next_state = deepcopy(current_state)
                    next_state.place_chess(i, j, piece_type)
                    next_state.remove_died_pieces(3-piece_type)
                    child = Node(next_state)
                    parent.addChild(child)
        return parent
    
    def build_minimax_tree_3(self, go, piece_type, depth):
        current_state = deepcopy(go) #make a deep copy of the current state
        root = Node(current_state) #go instead of go.board so you can leverage the member functions
        for level in range(depth):
            if level == 0:
                root = self.add_children(self, root, piece_type)
    '''

    #this will always be in the perspective of my_player
    def evaluate(self, state):
        pass


    def build_minimax_tree_recursive(self, root, piece_type, depth_max, depth):
        print("minimax tree recursive called")
        if depth == depth_max: #maximum depth to explore
            return root

        current_state = deepcopy(root.state)
        for i in range(current_state.size):
            for j in range(current_state.size):
                if current_state.valid_place_check(i, j, piece_type, test_check = True):
                    next_state = deepcopy(current_state)
                    next_state.place_chess(i, j, piece_type)
                    next_state.remove_died_pieces(3-piece_type)
                    child = Node(next_state)
                    child.move = [i, j]
                    child.score = self.evaluate(child.state)
                    root.addChild(child)
                    print("depth", depth, ", move", i, j)
                    self.build_minimax_tree_recursive(root, 3-piece_type, depth_max, depth+1)
        


    '''
    def build_minimax_tree_2(self, go, piece_type, depth):
        #add current state as root
        #add possible states as children
        #state, action to get to that state, and evaluation score
        current_state = deepcopy(go) #make a deep copy of the current state
        root = Node(current_state) #go instead of go.board so you can leverage the member functions

        for level in range(depth):
            if level == 0:
                for i in range(current_state.size):
                    for j in range(current_state.size):
                        if current_state.valid_place_check(i, j, piece_type, test_check = True):
                            next_state = deepcopy(current_state)
                            next_state.place_chess(i, j, piece_type)
                            next_state.remove_died_pieces(3-piece_type)
                            child = Node(next_state)
                            root.addChild(child)
            elif level == 1: 
                for possible_state in root.children:
                    for i in range(possible_state.size):
                        for j in range(possible_state.size):
                            if possible_state.valid_place_check(i, j, 3-piece_type, test_check = True): #min's turn
                                next_state = deepcopy(possible_state)
                                next_state.place_chess(i, j, 3-piece_type)
                                next_state.remove_died_pieces(piece_type) #remove max's stones
                                child = Node(next_state)
                                possible_state.addChild(child)
            elif level == 2:
                for possible_state in 
    '''

    '''
    read a minimax tree that's built for the entire game
    '''
    '''
    def read_minimax_tree(self, piece_type):
        max_evaluation = -1
        move = [-1, -1]
        if piece_type == 1: #X
            f = open("minimax_tree_x.txt", "r")
            lines = f.readlines()
        elif piece_type == 2:
            f = open("minimax_tree_o.txt", "r")
            lines = f.readlines()
        for line_num in range(len(lines)):
            line = lines[line_num].split()
            print(line)
            if line[0] == "evaluation":
                evaluation = float(line[1])
                if evaluation > max_evaluation:
                    max_evaluation = evaluation
                    move_x = lines[line_num+1].split()[1]
                    move_y = lines[line_num+1].split()[2]
                    move = [move_x, move_y]
        print("best move: ", str(move[0]), str(move[1]))
        return move
    '''

    '''
    build a minimax tree for the entire game
    according to the TA, this combines minimax and q-learning
    '''
    '''
    #current state is at depth 0
    def build_minimax_tree(self, go, max, depth):
        if max == 1:
            f = open("minimax_tree_x.txt", "w")
        elif max == 2:
            f = open("minimax_tree_o.txt", "w")
        
        piece_type = max
        
        possible_go = GO(5)
        original_stdout = sys.stdout
        #continue building until you run into a terminal state
        parent = 0
        node_number = 0
        for level in range(depth):
            max_evaluation = 0
            max_evaluation_move = []
            if parent == 0:
                node_number = 1
            f.write("depth " + str(depth) + "\n")
            f.write("node number " + str(node_number) + ", parent number " + str(parent) + "\n")
            
            sys.stdout = f
            go.visualize_board()
            print("starting state")
            parent = node
            
            for i in range(go.size):
                for j in range(go.size):
                    if go.valid_place_check(i, j, piece_type, test_check = True):
                        possible_go.board = deepcopy(go.board)
                        possible_go.place_chess(i, j, piece_type)
                        possible_go.remove_died_pieces(3-piece_type)
                        possible_go.visualize_board()
                        node_number += 1
                        evaluation = possible_go.judge_winner()
                        if evaluation == piece_type:
                            evaluation = 1
                        elif evaluation == 2:
                            evaluation = 0
                        else:
                            evaluation = 0.5
                        f.write("node number " + str(node_number) + ", parent number " + str(parent) + "\n")
                        f.write("evaluation " + str(evaluation) + "\n")
                        print("move:", i, j)
        sys.stdout = original_stdout
    '''

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
                if go.valid_place_check(i, j, piece_type, test_check = True):
                    possible_placements.append((i,j))

        if not possible_placements:
            return "PASS"
        else:
            return random.choice(possible_placements)

            
        

if __name__ == "__main__":
    N = 5
    piece_type, previous_board, board = readInput(N)
    go = GO(N)
    go.set_board(piece_type, previous_board, board)
    #player = RandomPlayer()
    player = MinimaxPlayer()
    action = player.get_input(go, piece_type)
    writeOutput(action)