from tkinter import *
from tkinter.font import Font
from random import shuffle
from ai import *


class Gui:

    def __init__(self, root):
        
        self.root= root
        self.game_fonts= {
                            1: Font(family= "Retro Gaming", size= 28, weight= "bold"),
                            2: Font(family= "Retro Gaming", size= 24, weight= "bold"),
                            3: Font(family= "Retro Gaming", size= 20, weight= "bold"),
                            4: ("Arial", 40, "bold")
                         }
              
        self.gui_init()
        
    #WIDGETS 

    def control_board_init(self):
       
        self.control_board = [[None, None, None], [None, None, None], [None, None, None]]

    def main_widg_init(self):
                
        self.main_strings = ["play", "quit"]
        self.main_frame = Frame(self.root, bg = "black")
        self.game_title = Label(self.main_frame, bg = "black", fg = "white", pady = 60, text = "Tic Tac Toe", font = self.game_fonts[1])
        self.sub_frame= Frame(self.main_frame, pady = 5, bg = "black")  
        self.main_menu= {
                            index: Label(self.main_frame, bg = "black", fg = "white", pady = 20, 
                                         text = string, font = self.game_fonts[2]) 
                                         for index, string in enumerate(self.main_strings)
                        }
        self.sub_menu=  {
                            (0, col): Label(self.sub_frame, bg = "black", fg = "white", pady = 20, padx = 20, text= string,
                                      font = self.game_fonts[3]) for col, string in enumerate(("easy", "medium", "hard"))
                        }
            
    def board_widg_init(self):    
        
        self.control_board_init()
        self.game_frame= Frame(self.root, pady = 5, bg = "black")  
        self.cells= {        
                        pos: Canvas(self.game_frame, height =160, width = 160, bg = "black") 
                        for pos in ((row, col) for row in range(3) for col in range(3))
                    }
        self.winner_label= Label(self.root, pady= 60, font = self.game_fonts[1], bg = "black", fg = "white")
        
    def end_widg_init(self):
        
        self.end_strings = ["play again", "main menu", "quit"]
        self.end_menu =  {
                            index: Label(self.root, bg = "black", fg = "white", pady = 20, 
                                        text = string, font = self.game_fonts[2]) 
                                        for index, string in enumerate(self.end_strings)
                        }
        
    def quit_widg(self) :

        self.farewell = Label(self.root, bg = "black", fg = "white", pady = 200, text = "Bye Bye", font = self.game_fonts[1])
        #widgets iterator to grid pack
    #gui initializer 
    def gui_init(self):
        self.main_widg_init()
        self.packer(self.main_frame)
        self.packer(self.game_title)
        self.packer(self.main_menu)
        self.enter_leave_binder(self.main_menu)
        self.events_binder("main")
    #board initializer
    def board_init(self):   
        
        self.control_board_init() 
        self.board_widg_init()
        self.grid_packer(self.cells)
        self.packer(self.game_frame)
        self.events_binder("cells")
        self.game_Ai = GameAi(self.control_board, self.mode)
    #end menu initializer
    def end_menu_init(self):        
        self.end_widg_init()
        self.packer(self.winner_label)
        self.root.after(500, lambda: self.packer(self.end_menu))
        self.enter_leave_binder(self.end_menu)
        self.events_binder("end")

    def quit(self):
        self.root_reset()
        self.quit_widg()
        self.packer(self.farewell)
        self.root.after(2500, self.root.destroy)    
    #CLASS METHODS  
    #recognizes single or widgets dicts and packs them
    def packer(self, widg):

        if type(widg) is not dict:
            widg.pack()       
        else:
            for key in widg:
                widg[key].pack()  
    #puts game board's cells in the grid
    def grid_packer(self, to_grid):

        for pos in to_grid:
            to_grid[pos].grid(row= pos[0], column= pos[1])             
    #does the animations bindings
    def enter_leave_binder(self, menu):

        if type(menu) is not dict:
            menu.bind("<Leave>", lambda event: menu.pack_forget())
            
            return
    
        for pos in menu:  
                    
            menu[pos].bind("<Enter>", lambda event, index = menu[pos]: self.enter_leave(index))
            menu[pos].bind("<Leave>", lambda event, index = menu[pos]: self.enter_leave(index, False))
    #binds all labels and canvases
    def events_binder(self, menu):

        if menu == "main":

            self.main_menu[0].bind("<Button-1>", lambda event: self.choice_menu())
            self.main_menu[1].bind("<Button-1>", lambda event: self.choice_selector(self.main_frame, "quit"))

        elif menu == "sub":

            self.sub_menu[(0, 0)].bind("<Button-1>", lambda event: self.choice_selector(self.main_frame, "easy")) 
            self.sub_menu[(0, 1)].bind("<Button-1>", lambda event: self.choice_selector(self.main_frame, "medium"))
            self.sub_menu[(0, 2)].bind("<Button-1>", lambda event: self.choice_selector(self.main_frame, "hard")) 
        
        elif menu == "cells":

            for pos in self.cells:
                self.cells[pos].bind("<Button-1>", lambda event, index= pos: self.player_choice(index))

        elif menu == "end":

            self.end_menu[0].bind("<Button-1>", lambda event: self.play_again())
            self.end_menu[1].bind("<Button-1>", lambda event:self.back_to_menu())
            self.end_menu[2].bind("<Button-1>", lambda event: self.quit())

    def play_again(self):

        self.root_reset()      
        self.root.after(500, self.board_init)       
    
    def root_reset(self):

        for container in self.root.winfo_children():

            container.destroy()

    #difficulty selection   
    def choice_selector(self, menu, mode):
        
        self.widg_remover(menu)      

        if any((mode == "easy", mode == "medium", mode == "hard")):
            self.mode = mode
            self.board_init()  
                
        else:
            self.quit()
        
    #it captures player's choice and pass it to insert()
    def player_choice(self, index):
        
        self.insert(index, "X")
        if self.game_Ai.find_avalaible():
            cpu_choice = self.game_Ai.ai_choice()
            self.insert(cpu_choice, "O")
            
    #given player's symbol insert it in the grid 
    def insert(self, index, player):

        self.cells[index].create_text(80, 80, text = player, font = self.game_fonts[4], fill = "white")
        self.cells[index].unbind("<Button-1>")
        self.control_board[index[0]][index[1]] = player
        self.status = GameStat(self.control_board)
        if self.status.game_status():
            self.game_over()

    def game_over(self):        
            
            self.cells_unbind()
            winner = self.status.game_status()
            if winner in "XO":
                winner = "You win" if winner == "X" else "CPU wins"
            self.winner_label.config(text = winner)
            self.game_frame.after(1000, lambda: self.widg_remover(self.game_frame, True))
            self.root.after(1800, self.end_menu_init)
            
    def cells_unbind(self):

        for cell in self.cells:
            self.cells[cell].unbind("<Button-1>")
    
    def back_to_menu(self):

        self.root_reset()
        self.gui_init()

    #animations
    
    #modifies text on "<Enter>/<Leave>" events
    def enter_leave(self, index, enter= True):
        
        string= index.cget("text")
        string= string.replace("*", "")

        if enter:            
            index.config(text = "*" + string + "*")
        else:
            index.config(text = string) 
    
    #opens the difficulty choice menu
    def choice_menu(self):
        
        self.main_menu[1].pack_forget()
        self.enter_leave_binder(self.sub_frame)
        self.enter_leave_binder(self.sub_menu)
        self.grid_packer(self.sub_menu)
        self.events_binder("sub")
        self.packer(self.sub_frame)
        self.main_menu[1].pack()
    
    #removes widgets from a container
    def widg_remover(self, container, rand= False):

        widg = container.winfo_children()
        
        if rand:
            shuffle(widg)
        if not widg:                       
            container.destroy()
            
            return
        
        container.after(200, widg[-1].destroy())
        
        return self.widg_remover(container)
           
    
        





        

        
    


        



            
            
            
        
          
            
                
    
    

            






