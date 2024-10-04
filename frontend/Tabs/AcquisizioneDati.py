# Progetto GUI misuratore d'insulina - A.A. 2024/2025 Corso di Laboratorio di Misure
# Autori:
# Saggiomo Luca
# Saccone Matteo
# Ponticelli Lorenzo
# Porcelli Nicola

import tkinter as tk
from tkinter import ttk

# Definisco la classe AcquisizioneDati, che eredita da tk.Frame
class AcquisizioneDati(tk.Frame):
    
    # Costruttore che costruisce l'oggetto di tipo App
    def __init__(self, parent_frame): 
        super().__init__(parent_frame)
        
        self.create_images()
        self.create_widgets()
        
    def create_images(self):
        self.start_image = tk.PhotoImage(file='Images/Start_icon_1.png').subsample(13,13)
        self.stop_image = tk.PhotoImage(file='Images/Bottoni_stop.png').subsample(8,8)
        self.trash_image = tk.PhotoImage(file='Images/Trash_icon.png').subsample(30,30)
    
    def create_widgets(self):
        self.grid_propagate(False)

        # definisco le colonne
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)

        # definisco le righe
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=6)
        self.rowconfigure(2, weight=1)

        parameters_frame = self.create_parameters_frame()
        parameters_frame.grid(column=0, row=0, padx=5, pady=5, sticky="nsew") # creo il frame dei parametri

        value_table = tk.LabelFrame(self, text="Tabella valori", bg="blue")
        value_table.grid(column=1, row=0, rowspan=3, padx=5, pady=5, sticky="nsew")

        graph_frame = tk.Frame(self, bg="green")
        graph_frame.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")

        start_stop_frame = self.create_start_stop_frame()
        start_stop_frame.grid(column=0, row=2, padx=5, pady=5, sticky="nsew")
    
    # Funzione per la creazione dei frame nella grid Parameters
    def create_parameters_frame(self):
        parameters_frame = tk.LabelFrame(self, text="Parameters", bg="red") # creo un oggetto frame con etichetta Parameters
        
        #parameters_frame.grid_propagate(True)
        parameters_frame.columnconfigure(0, weight=1)
        parameters_frame.columnconfigure(1, weight=1)
        parameters_frame.columnconfigure(2, weight=1)
        parameters_frame.columnconfigure(3, weight=1)
        parameters_frame.columnconfigure(4, weight=1)
        parameters_frame.columnconfigure(5, weight=1)
        parameters_frame.columnconfigure(6, weight=1)
        
        parameters_frame.rowconfigure(0, weight=1)
        parameters_frame.rowconfigure(1, weight=1)

        frequency_label = tk.Label(parameters_frame, text="Frequency", anchor="e", height=2, width=10, bg="red")
        frequency_label.grid(column=0, row=0, sticky="nesw")
       
        frequency_start_label = tk.Label(parameters_frame, text="Start F", anchor="e", height=2, width=10, bg="red")
        frequency_start_label.grid(column=1, row=0, sticky="nesw")
        self.start_frequency = tk.DoubleVar()
        frequency_start_entry = tk.Entry(parameters_frame, textvariable=self.start_frequency, width=15)
        frequency_start_entry.grid(column=2, row=0, sticky="w")

        frequency_stop_label = tk.Label(parameters_frame, text="Stop F", anchor="e", height=2, width=10, bg="red")
        frequency_stop_label.grid(column=3, row=0, sticky="nesw")
        self.stop_frequency = tk.DoubleVar()
        frequency_stop_entry = tk.Entry(parameters_frame, textvariable=self.stop_frequency, width=15)
        frequency_stop_entry.grid(column=4, row=0, sticky="w")

        frequency_points_label = tk.Label(parameters_frame, text="Points", anchor="e", height=2, width=10, bg="red")
        frequency_points_label.grid(column=5, row=0, sticky="nesw")
        self.points = tk.DoubleVar()
        frequency_points_entry = tk.Entry(parameters_frame, textvariable=self.points, width=15)
        frequency_points_entry.grid(column=6, row=0, sticky="w")
        
        voltage_label = tk.Label(parameters_frame, text="Voltage", anchor="e", height=2, width=10, bg="red")
        voltage_label.grid(column=0, row=1, sticky="nesw")
        self.voltage_value = tk.DoubleVar() # voltage_value appartiene all'oggetto self
        voltage_value_entry = tk.Entry(parameters_frame, textvariable=self.voltage_value, width=15)
        voltage_value_entry.grid(column=2, row=1, sticky="w")
        
        return parameters_frame
    
    # Funzione per la creazione dei frame start stop...
    # NOME DA CAMBIARE EVENTUALMENTE
    def create_start_stop_frame(self):
        start_stop_frame = tk.Frame(self)
        
        start_stop_frame.grid_propagate(False)
        
        # Definisco la riga
        start_stop_frame.rowconfigure(0, weight=1)
        
        # Definisco le colonne
        start_stop_frame.columnconfigure(0, weight=1)
        start_stop_frame.columnconfigure(1, weight=1)
        start_stop_frame.columnconfigure(2, weight=1)
        start_stop_frame.columnconfigure(3, weight=1)
        
        # Progress Bar
        self.progress_value = tk.DoubleVar()
        progress_bar_frame = ttk.Progressbar(start_stop_frame, length=100, variable=self.progress_value)
        progress_bar_frame.grid(column=0, row=0, padx=5, pady=5, sticky="w")
        
        start_button = ttk.Button(start_stop_frame, image=self.start_image, compound="right", width=25)
        start_button.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")
        
        stop_button = tk.Button(start_stop_frame, image=self.stop_image, compound="right", width=25)
        stop_button.grid(column=2, row=0, padx=5, pady=5, sticky="nsew")
        
        trash_button = tk.Button(start_stop_frame, image=self.trash_image, compound="right", width=25)
        trash_button.grid(column=3, row=0, padx=5, pady=5, sticky="nsew")
        
        return start_stop_frame