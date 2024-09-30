import tkinter as tk
from tkinter import ttk

class App(tk.Tk):

    # Costruttore che costruisce l'oggetto di tipo App
    def __init__(self): 
        super().__init__()

        # Size iniziale della finestra
        self.geometry("800x500")

        # Titolo finestra
        self.title("Fondamenti di Misure")

        # Non permettere il resize
        # self.resizable(0, 0)
        
        
        # Chiamo la funzione create_widgets - dichiarata successivamente
        self.create_widgets()

    # Funzione per la creazione dei frame nella grid Parameters
    def create_parameters_frame(self):
        
        parameters_frame = tk.LabelFrame(self, text="Parameters", bg="red") # creo un oggetto frame con etichetta Parameters
        
        parameters_frame.grid(column=0, row=1, padx=5, pady=5, sticky="nsew") # creo il frame dei parametri
        
        #parameters_frame.grid_propagate(True)
        parameters_frame.columnconfigure(0, weight=1)
        parameters_frame.columnconfigure(1, weight=1)
        parameters_frame.columnconfigure(2, weight=1)
        parameters_frame.columnconfigure(3, weight=1)
        parameters_frame.columnconfigure(4, weight=1)
        parameters_frame.columnconfigure(5, weight=1)
        parameters_frame.columnconfigure(6, weight=1)
        
        
        
        parameters_frame.rowconfigure(0, weight=0)
        parameters_frame.rowconfigure(1, weight=0)

        frequency_label = tk.Label(parameters_frame, text="Frequency", anchor="e", height=2, width=10, bg="red")
        frequency_label.grid(column=0, row=0, sticky="nesw")
       
        
        frequency_start_label = tk.Label(parameters_frame, text="Start F", anchor="e", height=2, width=10, bg="red")
        frequency_start_label.grid(column=1, row=0, sticky="nesw")
        self.start_frequency = tk.StringVar()
        frequency_start_entry = tk.Entry(parameters_frame, textvariable=self.start_frequency, width=20)
        frequency_start_entry.grid(column=2, row=0, sticky="ew")

        frequency_stop_label = tk.Label(parameters_frame, text="Stop F", anchor="e", height=2, width=10, bg="red")
        frequency_stop_label.grid(column=3, row=0, sticky="nsw")
        self.stop_frequency = tk.StringVar()
        frequency_stop_entry = tk.Entry(parameters_frame, textvariable=self.stop_frequency, width=20)
        frequency_stop_entry.grid(column=4, row=0, sticky="w")

        frequency_points_label = tk.Label(parameters_frame, text="Points", anchor="e", height=2, width=10, bg="red")
        frequency_points_label.grid(column=5, row=0, sticky="nsw")
        self.points = tk.StringVar()
        frequency_points_entry = tk.Entry(parameters_frame, textvariable=self.points, width=20)
        frequency_points_entry.grid(column=6, row=0, sticky="w")
        
        voltage_label = tk.Label(parameters_frame, text="Voltage", anchor="e", height=2, width=10, bg="red")
        voltage_label.grid(column=0, row=1, sticky="nsw")
        self.voltage_value = tk.DoubleVar() # voltage_value appartiene all'oggetto self
        voltage_value_entry = tk.Entry(parameters_frame, textvariable=self.voltage_value, bg="white", width=20)
        voltage_value_entry.grid(column=2, row=1)

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
    app = App() # invoco il costruttore
    app.mainloop() # funzione per eseguire il programma - la possiamo utilizzare in quanto si trova nella classe padre Tk