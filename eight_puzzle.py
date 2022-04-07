from searcher import *
from timer import *

def create_searcher(algorithm, param):
    """ a function that creates and returns an appropriate
        searcher object, based on the specified inputs. 
        inputs:
          * algorithm - a string specifying which algorithm the searcher
              should implement
          * param - a parameter that can be used to specify either
            a depth limit or the name of a heuristic function
        Note: If an unknown value is passed in for the algorithm parameter,
        the function returns None.
    """
    searcher = None
    
    if algorithm == 'random':
        searcher = Searcher(param)
        
    elif algorithm == 'BFS':
        searcher = BFSearcher(param)
    elif algorithm == 'DFS':
        searcher = DFSearcher(param)
    elif algorithm == 'Greedy':
        searcher = GreedySearcher(param)
    elif algorithm == 'A*':
        searcher = AStarSearcher(param)
    else:  
        print('unknown algorithm:', algorithm)

    return searcher

def eight_puzzle(init_boardstr, algorithm, param):
    """ a driver function for solving Eight Puzzles using state-space search
        inputs:
          * init_boardstr - a string of digits specifying the configuration
            of the board in the initial state
          * algorithm - a string specifying which algorithm you want to use
          * param - a parameter that is used to specify either a depth limit
            or the name of a heuristic function
    """
    init_board = Board(init_boardstr)
    init_state = State(init_board, None, 'init')
    searcher = create_searcher(algorithm, param)
    if searcher == None:
        return

    soln = None
    timer = Timer(algorithm)
    timer.start()
    
    try:
        soln = searcher.find_solution(init_state)
    except KeyboardInterrupt:
        print('Search terminated.')

    timer.end()
    print(str(timer) + ', ', end='')
    print(searcher.num_tested, 'states')

    if soln == None:
        print('Failed to find a solution.')
    else:
        print('Found a solution requiring', soln.num_moves, 'moves.')
        show_steps = input('Show the moves (y/n)? ')
        if show_steps == 'y':
            soln.print_moves_to()
            
def process_file(filename, algorithm, param):
    """ opens the file with the specified filename for reading, and
    uses a loop to process the file one line at a time """
    file = open(filename, 'r')
    puzzles_solved = 0
    total_moves = 0
    total_states = 0
    for line in file:
        line = line[:-1]
        puzzle = line
        init_board = Board(puzzle)
        init_state = State(init_board, None, 'init')
        searcher = create_searcher(algorithm, param)
        soln = None
        try:
            soln = searcher.find_solution(init_state)
        except KeyboardInterrupt:
            print(puzzle + ':', 'search terminated, ', end='')

        if soln == None:
            print('no solution')
        else:
            puzzles_solved += 1
            total_moves += soln.num_moves
            total_states += searcher.num_tested
            print(puzzle + ':', str(soln.num_moves), 'moves,', searcher.num_tested, 'states tested')
    print()
    print('solved', puzzles_solved, 'puzzles')
    if puzzles_solved != 0:
        print('averages:', round((total_moves / puzzles_solved), 1), 'moves,', round((total_states / puzzles_solved), 3), 'states tested')
    file.close()
