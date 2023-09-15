from random import choice


class GameStat:

#this class analyses the control board given from the GUI class. 

    def __init__(self, board):

        self.control_board = board
        self._rev_board = self.rev_board
        self._diag1 = self.diag1
        self._diag2 = self.diag2

    #rev_board returns a reversed game board. It's a simple implementation of a zip function  
    @property
    def rev_board(self):
        
        return [[self.control_board[c][r] for c in range(3)] for r in range(3)]
 
    #diag1 returns the diagonal from the top left to the lower right 
    @property
    def diag1(self):

        return [self.control_board[i][i] for i in range(3)]
    
    #diag2 returns diagonal from the lower left to the top right corner 
    @property
    def diag2(self):
        
        return [self.control_board[i][2 - i] for i in range(3)]
    
    #is_full checks if there's a None value it the board's row. Returns a Bool
    def is_full(self):
        
        return all((None not in row) for row in self.control_board)    
    
    #game_status checks for a winner on the board and diagonals. If there' s a winner, it returns 
    # the winner's symbol. If the board is full and there is no winner, it returns the string 'Tie'.
    # If none of these conditions are met, it returns None."
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


#Class Ai takes control board and mode from GUI. 
class GameAi:

    def __init__(self, control_board, mode):

        self.mode = mode
        self.control_board = control_board
                
    #find_avalaible checks for empty positions in the game grid. 
    def find_avalaible(self):

        return [
              (r, c) for r, row in enumerate(self.control_board)
                for c, col in enumerate(row) if not col
                ]
    
    #ai_choice calls "easy", "medium" and "hard" modes
    def ai_choice(self):

        cpu_choice = ()

        if self.mode == "easy":            
            cpu_choice = self.random_choice()
        elif self.mode == "medium" :            
            cpu_choice = self.medium()
        else:
            cpu_choice = self.hard() 
                   
        return cpu_choice    
    
    #random_choice returns a randomly choose couple(Tuple) of coords. 
    def random_choice(self):

        return choice(self.find_avalaible())
    
    #medium checks for an eventual opponent's move and fills the winning cell 
    #If there's no risk it calls random_choice method
    def medium(self):      
        
        if self.defend():
            return self.defend()
        
        return self.random_choice()
    
    #it's not hard for real.
    #hard works like medium but starts checking for winning moves.
    def hard(self):
       
        if self.attack():
            return self.attack()
        
        self.medium()
    
    #Both methods defend and attack return only a couple of coords.     
    #defend simulates every opponent's possible move. Uses class game_stat for winner's checking.
    def defend(self):
        
        cpu_choice = ()
        for move in self.find_avalaible():
            row, col = move
            self.control_board[row][col] = "X"                        
            checker = GameStat(self.control_board)
            if checker.game_status() == "X":
                cpu_choice = move
            self.control_board[row][col] = None
        
        return cpu_choice
    
    #attack simulates every cpu's possible move. Uses class game_stat for winner's checking.
    def attack(self):
        
        cpu_choice = ()
        for move in self.find_avalaible():
            row, col = move                             
            checker = GameStat(self.control_board)
            if checker.game_status() == "O":
                cpu_choice = move
            self.control_board[row][col] = None
                   
        return cpu_choice            

    
    
        
    