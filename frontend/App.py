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
        
        

        self.create_widgets()

    # Funzione per la creazione dei frame
    def create_parameters_frame(self):
        
        parameters_frame = tk.LabelFrame(self, text="Parameters", bg="red") # creo un oggetto frame con etichetta Parameters
        parameters_frame.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")
        parameters_frame.grid_propagate(False)
        parameters_frame.columnconfigure(0, weight=0)
        parameters_frame.columnconfigure(1, weight=0)
        parameters_frame.columnconfigure(2, weight=0)
        parameters_frame.columnconfigure(3, weight=0)
        parameters_frame.columnconfigure(4, weight=0)
        parameters_frame.columnconfigure(5, weight=1)
        parameters_frame.rowconfigure(0, weight=0)
        parameters_frame.rowconfigure(1, weight=0)

        frequency_label = tk.Label(parameters_frame, text="Frequency", anchor="e", height=2, width=10, bg="red")
        frequency_label.grid(column=0, row=0, sticky="nesw")
        self.frequency_var = tk.StringVar()
        frequency_entry = tk.Entry(parameters_frame, textvariable=self.frequency_var, width=20)
        frequency_entry.grid(column=1, row=0, sticky="ew")

        frequency_start_label = tk.Label(parameters_frame, text="Start F", anchor="e", height=2, width=10, bg="red")
        frequency_start_label.grid(column=2, row=0, sticky="nesw")
        self.start_frequency = tk.StringVar()
        frequency_start_entry = tk.Entry(parameters_frame, textvariable=self.start_frequency, width=20)
        frequency_start_entry.grid(column=3, row=0, sticky="ew")

        frequency_stop_label = tk.Label(parameters_frame, text="Stop F", anchor="e", height=2, width=10, bg="red")
        frequency_stop_label.grid(column=4, row=0, sticky="nsw")
        self.stop_frequency = tk.StringVar()
        frequency_stop_entry = tk.Entry(parameters_frame, textvariable=self.stop_frequency, width=20)
        frequency_stop_entry.grid(column=5, row=0, sticky="w")

        frequency_points_label = tk.Label(parameters_frame, text="Points", anchor="e", height=2, width=10, bg="red")
        frequency_points_label.grid(column=4, row=1, sticky="nsw")
        self.points = tk.StringVar()
        frequency_points_entry = tk.Entry(parameters_frame, textvariable=self.points, width=20)
        frequency_points_entry.grid(column=5, row=1, sticky="w")

    def create_widgets(self):
        self.grid_propagate(False)

        # definisco le colonne
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)

        # definisco le righe
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=6)
        self.rowconfigure(3, weight=1)

        self.create_parameters_frame()

        tabs_frame = tk.Frame(self, bg="yellow")
        tabs_frame.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

        status_frame = tk.Frame(self, bg="darkgreen")
        status_frame.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")

        value_table = tk.LabelFrame(self, text="Tabella valori", bg="blue")
        value_table.grid(column=1, row=1, rowspan=3, padx=5, pady=5, sticky="nsew")

        graph_frame = tk.Frame(self, bg="green")
        graph_frame.grid(column=0, row=2, padx=5, pady=5, sticky="nsew")

        tabs_frame = tk.Frame(self, bg="cyan")
        tabs_frame.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

        bar_frame = tk.Frame(self, bg="purple")
        bar_frame.grid(column=0, row=3, padx=5, pady=5, sticky="nsew")

    

if __name__ == "__main__":
    app = App()
    app.mainloop()