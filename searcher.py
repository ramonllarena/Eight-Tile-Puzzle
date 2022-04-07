#
# searcher.py (Final project)
#
# classes for objects that perform state-space search on Eight Puzzles  
#
# name: Ramon Llarena
# email: llar011@bu.edu
#
# If you worked with a partner, put their contact info below:
# partner's name:
# partner's email:
#

import random
from state import *

class Searcher:
    """ A class for objects that perform random state-space
        search on an Eight Puzzle.
        This will also be used as a superclass of classes for
        other state-space search algorithms.
    """
    ### Add your Searcher method definitions here. ###

    def __init__(self, depth_limit):
        """ a constructor for a Searcher object """
        self.states = []
        self.num_tested = 0
        self.depth_limit = depth_limit

    def add_state(self, new_state):
        """ takes a single State object called new_state and adds
        it to the Searcher‘s list of untested states """
        self.states += [new_state]
        
    def should_add(self, state):
        """ takes a State object called state and returns True if
        the called Searcher should add state to its list of
        untested states, and False otherwise """
        if self.depth_limit != -1 and state.num_moves > self.depth_limit:
            return False
        elif state.creates_cycle() == True:
            return False
        else:
            return True
        
    def add_states(self, new_states):
        """ takes a list State objects called new_states, and that
        processes the elements of new_states one at a time """
        for s in new_states:
            if self.should_add(s) == True:
                self.add_state(s)

    def next_state(self):
        """ chooses the next state to be tested from the list of 
        untested states, removing it from the list and returning it
        """
        s = random.choice(self.states)
        self.states.remove(s)
        return s
    
    def find_solution(self, init_state):
        """ performs a full state-space search that begins at the
        specified initial state init_state and ends when the goal state
        is found or when the Searcher runs out of untested states """
        self.add_state(init_state)
        while self.states:
            s = self.next_state()
            self.num_tested += 1
            if s.is_goal():
                return s
            else:
                self.add_states(s.generate_successors())
        else:
            return None
    
    def __repr__(self):
        """ returns a string representation of the Searcher object
            referred to by self.
        """
        # You should *NOT* change this method.
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        if self.depth_limit == -1:
            s += 'no depth limit'
        else:
            s += 'depth limit = ' + str(self.depth_limit)
        return s


### Add your BFSeacher and DFSearcher class definitions below. ###
class BFSearcher(Searcher):
    """ performs breadth-first search (BFS) instead of random search """
    def next_state(self):
        """ rather than choosing at random from the list of untested states,
        this version of next_state should follow FIFO (first-in first-out)
        ordering – choosing the state that has been in the list the longest """
        s = self.states[0]
        self.states.remove(s)
        return s
    
class DFSearcher(Searcher):
    """ performs depth-first search (DFS) instead of random search """
    def next_state(self):
        """ follow LIFO (last-in first-out) ordering – choosing the state
        that was most recently added to the list """
        s = self.states[-1]
        self.states.remove(s)
        return s

def h0(state):
    """ a heuristic function that always returns 0 """
    return 0

### Add your other heuristic functions here. ###
def h1(state):
    """ computes and returns an estimate of how many additional moves are
    needed to get from state to the goal state """
    return state.board.num_misplaced() * 1

def h2(state):
    """ computes and returns a new estimate of how many additional moves are
    needed to get from state to the goal state """
    return state.board.num_misplaced_2() * 1

class GreedySearcher(Searcher):
    """ A class for objects that perform an informed greedy state-space
        search on an Eight Puzzle.
    """
    ### Add your GreedySearcher method definitions here. ###
    def __init__(self, heuristic):
        """ constructor for a new GreedySearcher object """
        super(GreedySearcher, self).__init__(-1)
        self.heuristic = heuristic
        
    def __repr__(self):
        """ returns a string representation of the GreedySearcher object
            referred to by self.
        """
        # You should *NOT* change this method.
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        s += 'heuristic ' + self.heuristic.__name__
        return s

    def priority(self, state):
        """ computes and returns the priority of the specified state,
        based on the heuristic function used by the searcher """
        return -1 * self.heuristic(state)
    
    def add_state(self, state):
        """ rather than simply adding the specified state to the list
        of untested states, the method should add a sublist that is a
        [priority, state] pair, where priority is the priority of state
        that is determined by calling the priority method """
        self.states += [[self.priority(state), state]]
        
    def next_state(self):
        """ overrides (i.e., replaces) the next_state method that is
        inherited from Searcher. This version of next_state should choose
        one of the states with the highest priority """
        temp = self.states[0][0]
        max_idx = 0
        for idx in range(len(self.states)):
            if self.states[idx][0] > temp:
                temp = self.states[idx][0]
                max_idx = idx
        s = self.states[max_idx][1]
        self.states.remove(self.states[max_idx])
        return s
    
class AStarSearcher(GreedySearcher):
    """ class for searcher objects that performs A* search """
    def priority(self, state):
        return -1 * (self.heuristic(state) + state.num_moves)