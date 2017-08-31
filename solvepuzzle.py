"""
HOW FUCK IS THIS ASSIGNMENT!!!!!!!!!!!!!!!!!!!!!!!
"""

import argparse as ap

######## RUNNING THE CODE ####################################################
#   You can run this code from terminal by executing the following command
#   python solvepuzzle.py <puzzle> <procedure> <output_file> <flag>
#   for example: python solvepuzzle.py BBWEW A result 0
#   NOTE: THIS IS JUST ONE EXAMPLE INPUT DATA
###############################################################################


################## YOUR CODE GOES HERE ########################################

class Stack:
    """
    Stack object to be used as the data stucture for DLS.
    """

    def __init__(self):
        self.stack = []

    def __str__(self):
        string_to_print = ""
        for i in range(len(self.stack)-1, -1, -1):
            string_to_print += str(self.stack[i]) + ' '
        return string_to_print

    def pop(self):
        return self.stack.pop()

    def push(self, item):
        self.stack.append(item)

    def empty(self):
        return len(self.stack) == 0


class Node:
    """
    Node object to be used as the data structure DLS and A*.
    """
    # Static variable, recording the number of Node objects have been
    # generated.
    NO_OF_NODES = 0

    def __init__(self, parent, cost, heuristic, puzzle, operator, depth):
        # Set identifier for the node and increase `NO_OF_NODES`
        self.identifier = self.NO_OF_NODES
        Node.NO_OF_NODES += 1

        self.depth = depth

        # Children
        self.L1 = None
        self.L2 = None
        self.L3 = None
        self.R1 = None
        self.R2 = None
        self.R3 = None

        # Some numbers
        self.g = cost  # The cost of reaching this node
        self.h = heuristic  # The heuristic value h
        self.f = self.g + self.h

        # Parent
        self.parent = parent

        self.puzzle = puzzle
        self.operator = operator

    def __str__(self):
        return "N" + str(self.identifier)

    def __repr__(self):
        return "N" + str(self.identifier)

    def set_children(self, l1=None, l2=None, l3=None, r1=None, r2=None, r3=None):
        self.L1 = l1
        self.L2 = l2
        self.L3 = l3
        self.R1 = r1
        self.R2 = r2
        self.R3 = r3

    # Accessors
    def get_cost(self):
        return self.g
    def get_f(self):
        return self.f
    def get_h(self):
        return self.h
    def get_puzzle(self):
        return self.puzzle
    def get_depth(self):
        return self.depth
    def get_parent(self):
        return self.parent
    def get_operator(self):
        return self.operator

def check_L1(expand_node_puzzle):
    empty_index = expand_node_puzzle.index("E")
    return (empty_index-1 >= 0)

def check_L2(expand_node_puzzle):
    empty_index = expand_node_puzzle.index("E")
    return (empty_index-2 >= 0)

def check_L3(expand_node_puzzle):
    empty_index = expand_node_puzzle.index("E")
    return (empty_index-3 >= 0)

def check_R1(expand_node_puzzle):
    empty_index = expand_node_puzzle.index("E")
    return (empty_index+1 <= len(expand_node_puzzle)-1)

def check_R2(expand_node_puzzle):
    empty_index = expand_node_puzzle.index("E")
    return (empty_index+2 <= len(expand_node_puzzle)-1)

def check_R3(expand_node_puzzle):
    empty_index = expand_node_puzzle.index("E")
    return (empty_index+3 <= len(expand_node_puzzle)-1)

def get_l1_puzzle(expand_node_puzzle):
    new_puzzle = expand_node_puzzle[:]
    empty_index = expand_node_puzzle.index("E")
    # Swap new_puzzle[empty_index-1] and new_puzzle[empty_index]
    new_puzzle[empty_index] = new_puzzle[empty_index-1]
    new_puzzle[empty_index-1] = "E"
    return new_puzzle

def get_l2_puzzle(expand_node_puzzle):
    new_puzzle = expand_node_puzzle[:]
    empty_index = expand_node_puzzle.index("E")
    # Swap new_puzzle[empty_index-2] and new_puzzle[empty_index]
    new_puzzle[empty_index] = new_puzzle[empty_index-2]
    new_puzzle[empty_index-2] = "E"
    return new_puzzle

def get_l3_puzzle(expand_node_puzzle):
    new_puzzle = expand_node_puzzle[:]
    empty_index = expand_node_puzzle.index("E")
    # Swap new_puzzle[empty_index-3] and new_puzzle[empty_index]
    new_puzzle[empty_index] = new_puzzle[empty_index-3]
    new_puzzle[empty_index-3] = "E"
    return new_puzzle

def get_r1_puzzle(expand_node_puzzle):
    new_puzzle = expand_node_puzzle[:]
    empty_index = expand_node_puzzle.index("E")
    # Swap new_puzzle[empty_index+1] and new_puzzle[empty_index]
    new_puzzle[empty_index] = new_puzzle[empty_index+1]
    new_puzzle[empty_index+1] = "E"
    return new_puzzle

def get_r2_puzzle(expand_node_puzzle):
    new_puzzle = expand_node_puzzle[:]
    empty_index = expand_node_puzzle.index("E")
    # Swap new_puzzle[empty_index+2] and new_puzzle[empty_index]
    new_puzzle[empty_index] = new_puzzle[empty_index+2]
    new_puzzle[empty_index+2] = "E"
    return new_puzzle

def get_r3_puzzle(expand_node_puzzle):
    new_puzzle = expand_node_puzzle[:]
    empty_index = expand_node_puzzle.index("E")
    # Swap new_puzzle[empty_index+3] and new_puzzle[empty_index]
    new_puzzle[empty_index] = new_puzzle[empty_index+3]
    new_puzzle[empty_index+3] = "E"
    return new_puzzle

def check_puzzle_solved(expanded_node_puzzle):
    """
    This function is to determine whether the white tiles are all to
    the left of black tiles.
    """
    white_count = expanded_node_puzzle.count("W")
    white_found = 0
    for i in range(len(expanded_node_puzzle)):
        if expanded_node_puzzle[i] == "E":
            continue
        if expanded_node_puzzle[i] == "B":
            if white_found == white_count:
                return True
            else:
                return False
        if expanded_node_puzzle[i] == "W":
            white_found += 1

def find_solution(expand_node):
    """
    This function is to backtrack and find the sequence of moves to be
    performed to get from the starting configuration to the goal
    configuration.
    """
    operator = Stack()
    generated_puzzle = Stack()
    cost = Stack()
    current_node = expand_node
    while current_node.get_parent() is not None:
        operator.push(current_node.get_operator())
        generated_puzzle.push(current_node.get_puzzle())
        cost.push(current_node.get_cost())
        current_node = current_node.get_parent()
    operator.push("start")
    generated_puzzle.push(current_node.get_puzzle())
    cost.push(current_node.get_cost())

    solution = ""
    while not operator.empty():
        solution += "{:<5} {} {}\n".format(
            str(operator.pop()),
            ''.join(generated_puzzle.pop()),
            str(cost.pop())
        )
    print(solution)
    return solution

def diagnostic_generate_string(new_node):
    """
    This function is to generate the string for diagnosing of a node
    who is generated.
    """
    return "\nNode {} is GENERATED:\nOperator: {}\nIdentifier: {}\nParent: {}\ng: {}, h: {}, f: {}\n".format(
            str(new_node),
            new_node.get_operator(),
            str(new_node),
            str(new_node.get_parent()),
            new_node.get_cost(),
            new_node.get_h(),
            new_node.get_f()
        )

def DLS(puzzle, bound, diagnostic, flag):
    open_list = Stack()  # The nodes that haven't been visited
    closed_list = []  # The nodes that have been visited
    diagnostic_count = 0

    root = Node(None, 0, 0, puzzle, None, 0)  # Root node with cost 0
    open_list.push(root)
    while not open_list.empty():
        # DEBUG:
        # print("haha")
        # print(open_list)
        # for node in open_list.stack:
        #     print(str(node), node.get_puzzle())
        expand_node = open_list.pop()
        closed_list.append(expand_node)
        expand_node_cost = expand_node.get_cost()
        expand_node_puzzle = expand_node.get_puzzle()
        expand_node_depth = expand_node.get_depth()

        if check_puzzle_solved(expand_node_puzzle):
            return find_solution(expand_node)
        if expand_node_depth >= bound:
            continue

        diagnostic_order_of_expansion = []
        diagnostic_generate = ""

        l1, l2, l3, r1, r2, r3 = None, None, None, None, None, None
        # The priority of the children to pop up should be "R2, L2,
        # R1, L1, R3, L3", because it's a stack, the order we push in
        # should be the revise.
        if check_L3(expand_node_puzzle):
            new_puzzle = get_l3_puzzle(expand_node_puzzle)
            l3 = Node(
                expand_node,
                expand_node_cost+2,
                0,
                new_puzzle,
                "L3",
                expand_node_depth+1
            )
            open_list.push(l3)
            if diagnostic_count < flag:
                diagnostic_order_of_expansion.append(str(l3))
                diagnostic_generate += diagnostic_generate_string(l3)
        if check_R3(expand_node_puzzle):
            new_puzzle = get_r3_puzzle(expand_node_puzzle)
            r3 = Node(
                expand_node,
                expand_node_cost+2,
                0,
                new_puzzle,
                "R3",
                expand_node_depth+1
            )
            open_list.push(r3)
            if diagnostic_count < flag:
                diagnostic_order_of_expansion.append(str(r3))
                diagnostic_generate += diagnostic_generate_string(r3)
        if check_L1(expand_node_puzzle):
            new_puzzle = get_l1_puzzle(expand_node_puzzle)
            l1 = Node(
                expand_node,
                expand_node_cost+1,
                0,
                new_puzzle,
                "L1",
                expand_node_depth+1
            )
            open_list.push(l1)
            if diagnostic_count < flag:
                diagnostic_order_of_expansion.append(str(l1))
                diagnostic_generate += diagnostic_generate_string(l1)
        if check_R1(expand_node_puzzle):
            new_puzzle = get_r1_puzzle(expand_node_puzzle)
            r1 = Node(
                expand_node,
                expand_node_cost+1,
                0,
                new_puzzle,
                "R1",
                expand_node_depth+1
            )
            open_list.push(r1)
            if diagnostic_count < flag:
                diagnostic_order_of_expansion.append(str(r1))
                diagnostic_generate += diagnostic_generate_string(r1)
        if check_L2(expand_node_puzzle):
            new_puzzle = get_l2_puzzle(expand_node_puzzle)
            l2 = Node(
                expand_node,
                expand_node_cost+1,
                0,
                new_puzzle,
                "L2",
                expand_node_depth+1
            )
            open_list.push(l2)
            if diagnostic_count < flag:
                diagnostic_order_of_expansion.append(str(l2))
                diagnostic_generate += diagnostic_generate_string(l2)
        if check_R2(expand_node_puzzle):
            new_puzzle = get_r2_puzzle(expand_node_puzzle)
            r2 = Node(
                expand_node,
                expand_node_cost+1,
                0,
                new_puzzle,
                "R2",
                expand_node_depth+1
            )
            open_list.push(r2)
            if diagnostic_count < flag:
                diagnostic_order_of_expansion.append(str(r2))
                diagnostic_generate += diagnostic_generate_string(r2)
        expand_node.set_children(l1, l2, l3, r1, r2, r3)

        # Set up diagnostic mode information
        if diagnostic_count < flag:
            diagnostic_expand = "Node {} is EXPANDED:\nIdentifier: {}\nOrder of expansion: {}\ng: {}, f: {}\nOPEN list: {}\nCLOSED list: {}\n".format(
                str(expand_node),
                str(expand_node),
                ', '.join(diagnostic_order_of_expansion),
                expand_node.get_cost(),
                expand_node.get_f(),
                str(open_list),
                ', '.join([str(node) for node in closed_list])
            )
            diagnostic.append(diagnostic_expand + diagnostic_generate)
            diagnostic_count += 1

def graphsearch(puzzle, flag, procedure_name):
    solution = "start BBBWWWE 0" + "\n" + "2L BBBWEWW 1" + "\n" + "2L BBEWBWW 2" + "\n" + "3R BBWWBEW 4"
    if procedure_name == "DLS":
        bound = 20  # you have to determine its value
        diagnostic = [] # The list stored the detail of nodes of expanation
        solution = DLS(list(puzzle), bound, diagnostic, flag)
    elif procedure_name == "A":
        print("your code for A/A* goes here")
    else:
        print("invalid procedure name")

    if flag > 0:
        for i in range(flag):
            print(diagnostic[i])

    return solution

###############################################################################
########### DO NOT CHANGE ANYTHING BELOW ######################################
###############################################################################

def write_to_file(file_name, solution):
    file_handle = open(file_name, 'w')
    file_handle.write(solution)

def main():
    # create a parser object
    parser = ap.ArgumentParser()

    # specify what arguments will be coming from the terminal/commandline
    parser.add_argument("puzzle_string", help= "comprises a sequence of symbols, can be B, W, E", type= str)
    parser.add_argument("procedure_name", help="specifies the type of algorithm to be applied, can be BK, DLS, A", type=str)
    parser.add_argument("output_file_name", help="specifies the name of the output file", type=str)
    parser.add_argument("flag", help="specifies the number of steps that should be printed", type=int)

    # get all the arguments
    arguments = parser.parse_args()

##############################################################################
# these print statements are here to check if the arguments are correct.
# print("The puzzle is " + arguments.puzzle_string)
# print("The procedure_name is " + arguments.procedure_name)
# print("The output_file_name is " + arguments.output_file_name)
# print("The flag is " + str(arguments.flag))
##############################################################################

    # Extract the required arguments
    puzzle = arguments.puzzle_string
    procedure_name = arguments.procedure_name
    output_file_name = arguments.output_file_name
    flag = arguments.flag

    solution_string = "" # contains solution
    write_flag = 0 # to control access to output file

    # take a decision based upon the procedure name
    if procedure_name == "DLS" or procedure_name == "A":
        solution_string = graphsearch(puzzle, flag, procedure_name)
        write_flag = 1
    else:
        print("invalid procedure name")

    # call function write to file only in case we have a solution
    if write_flag == 1:
        write_to_file(output_file_name, solution_string)

if __name__ == "__main__":
    main()
