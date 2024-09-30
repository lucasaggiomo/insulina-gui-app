import tkinter as tk
from tkinter import ttk

class App(tk.Tk):

    def __init__(self):
        super().__init__()

        # Size iniziale
        self.geometry("700x500")

        # Titolo finestra
        self.title("Fondamenti di Misure")

        # Non permettere il resize
        # self.resizable(0, 0)
        
        

if __name__ == "__main__":
    app = App()
    app.mainloop()