
class GameStat:
    
    def __init__(self, board):

        self.control_board = board
        self._rev_board = self.rev_board
        self._diag1 = self.diag1
        self._diag2 = self.diag2
          
    # rev_board returns a reversed version of the game board. It's a simple zip implementation
    @property
    def rev_board(self):
        
        return [[self.control_board[c][r] for c in range(3)] for r in range(3)]
    
    # diag1 returns the diagonal from upper-left to lower-right corner
    @property
    def diag1(self):

        return [self.control_board[i][i] for i in range(3)]
    
    # diag1 returns the diagonal from lower-left to upper-right corner
    @property
    def diag2(self):
        
        return [self.control_board[i][2 - i] for i in range(3)]
    
    # is_full checks for not None values. Returns a boolean
    def is_full(self):
        
        return all((None not in row) for row in self.control_board)    

    # checks for a winner. If there's one returns winner's symble, if board is
    # full and there's no winner returns "Tie" string. It none of these conditions is met
    # it returns None
    def game_status(self):
             
        for row in self.control_board:
            if row[0] == row[1] == row[2] != None:
                return row[0]
        
        for col in self.rev_board:
            if col[0] == col[1] == col[2] != None:
                
                return col[0]

        if self.diag1[0] == self.diag1[1] == self.diag1[2] != None:
            
            return self.diag1[0]
        
        if self.diag2[0] == self.diag2[1] == self.diag2[2] != None:

            return self.diag2[0]
        
        if self.is_full():

            return "Tie"



