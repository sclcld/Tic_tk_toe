from gui import *

root = Tk()
root.geometry("500x500")
root.config(bg = "black")
root.title("Tk tac toe")
root.resizable(False, False)
gui = Gui(root)
root.mainloop()