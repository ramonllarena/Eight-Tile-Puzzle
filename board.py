# a 2-D list that corresponds to the tiles in the goal state
GOAL_TILES = [['0', '1', '2'],
              ['3', '4', '5'],
              ['6', '7', '8']]

class Board:
    """ A class for objects that represent an Eight Puzzle board.
    """
    def __init__(self, digitstr):
        """ a constructor for a Board object whose configuration
            is specified by the input digitstr
            input: digitstr is a permutation of the digits 0-9
        """
        # check that digitstr is 9-character string
        # containing all digits from 0-9
        assert(len(digitstr) == 9)
        for x in range(9):
            assert(str(x) in digitstr)

        self.tiles = [[''] * 3 for x in range(3)]
        self.blank_r = -1
        self.blank_c = -1

        # Put your code for the rest of __init__ below.
        # Do *NOT* remove our code above.\
        for r in range(3):
            for c in range(3):
                self.tiles[r][c] = digitstr[(3 * r + c)]
                if '0' in self.tiles[r][c]:
                    self.blank_r = r
                    self.blank_c = c

    ### Method definitions below. ###
    def __repr__(self):
        """ returns a string representation of a Board object """
        s = ''
        for r in range(3):
            for c in range(3):
                if str(self.tiles[r][c]) == '0':
                    s += '_' + ' '
                else:
                    s += str(self.tiles[r][c]) + ' '
            s += '\n'
        return s
    
    def move_blank(self, direction):
        """ takes as input a string direction that specigies the
        direction in which the blank should move, and that attempts
        to modify the contents of the called Board object accordingly """
        if direction == 'up' or direction == 'down' or direction == 'left' or direction == 'right':
            if self.blank_r == 0 and direction == 'up':
                return False
            elif self.blank_r == 2 and direction == 'down':
                return False
            elif self.blank_c == 0 and direction == 'left':
                return False
            elif self.blank_c == 2 and direction == 'right':
                return False
            elif direction == 'up':
                self.tiles[self.blank_r][self.blank_c] = self.tiles[self.blank_r - 1][self.blank_c]
                self.tiles[self.blank_r - 1][self.blank_c] = '0'
                self.blank_r -= 1
                return True
            elif direction == 'down':
                self.tiles[self.blank_r][self.blank_c] = self.tiles[self.blank_r + 1][self.blank_c]
                self.tiles[self.blank_r + 1][self.blank_c] = '0'
                self.blank_r += 1
                return True
            elif direction == 'left':
                self.tiles[self.blank_r][self.blank_c] = self.tiles[self.blank_r][self.blank_c - 1]
                self.tiles[self.blank_r][self.blank_c - 1] = '0'
                self.blank_c -= 1
                return True
            elif direction == 'right':
                self.tiles[self.blank_r][self.blank_c] = self.tiles[self.blank_r][self.blank_c + 1]
                self.tiles[self.blank_r][self.blank_c + 1] = '0'
                self.blank_c += 1
                return True
        return False
    
    def digit_string(self):
        """ creates and returns a string of digits that corresponds
        to the current contents of the called Board object’s tiles
        attribute """
        s = ''
        for r in range(3):
            for c in range(3):
                s += str(self.tiles[r][c])
        return s
    
    def copy(self):
        """ returns a newly-constructed Board object that is a deep
        copy of the called object """
        board_copy = Board(self.digit_string())
        return board_copy
    
    def num_misplaced(self):
        """ counts and returns the number of tiles in the called Board
        object that are not where they should be in the goal state """
        count = 0
        for r in range(len(self.tiles)):
            for c in range(len(self.tiles[0])):
                if self.tiles[r][c] != '0':
                    if self.tiles[r][c] != GOAL_TILES[r][c]:
                        count += 1
        return count
    
    def num_misplaced_2(self):
        """ returns a new number as priority. If a number is not at the
        correct place, it will get the necessary value from the correct
        column and row """
        newpriority = 0
        for r in range(len(self.tiles)):
            for c in range(len(self.tiles[0])):
                board_tiles = self.tiles[r][c]
                if board_tiles != '0':
                    if board_tiles != GOAL_TILES[r][c]:
                        newpriority += abs(r - int(board_tiles) // 3)
                        newpriority += abs(c - int(board_tiles) % 3)
                    else:
                        None
        return newpriority
    
    def __eq__(self, other):
        """ returns True if the called object (self) and the argument (other)
        have the same values for the tiles attribute, and False otherwise """
        if self.tiles == other.tiles:
            return True
        else:
            return False
