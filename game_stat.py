#se hai fumato troppo, ricordati che devono necessariamente restituire liste.PUNTO.

class GameStat:

    
        


    
    def __init__(self, board):

        self.control_board = board
        self._rev_board = self.rev_board
        self._diag1 = self.diag1
        self._diag2 = self.diag2
    
    
    
   
       
   
    @property
    def rev_board(self):
        
        return [[self.control_board[c][r] for c in range(3)] for r in range(3)]
   
    @property
    def diag1(self):

        return [self.control_board[i][i] for i in range(3)]

    @property
    def diag2(self):
        
        return [self.control_board[i][2 - i] for i in range(3)]
    
    


    def is_full(self):
        
        return all((None not in row) for row in self.control_board)    

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



