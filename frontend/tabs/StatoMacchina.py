# Progetto GUI misuratore d'insulina - A.A. 2024/2025 Corso di Laboratorio di Misure
# Autori:
# Saggiomo Luca
# Saccone Matteo
# Romano Davide
# Ponticelli Lorenzo
# Porcelli Nicola

import tkinter as tk
from tkinter import ttk

from image_manager import ImageManager
from style_manager import StyleManager

# Definisco la classe StatoMacchina, che eredita da tk.Frame
class StatoMacchina(tk.Frame):
    
    # Costruttore che costruisce l'oggetto di tipo App
    def __init__(self, parent_frame): 
        super().__init__(parent_frame)
        
        self.create_widgets()
        
    def create_widgets(self):
        self.grid_propagate(False)

        # definisco le colonne
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        # definisco le righe
        self.rowconfigure(0, weight=2)

        dati_macchina_frame = tk.Frame(self, bg="blue")
        dati_macchina_frame.grid(column=0, row=0, rowspan=3, padx=5, pady=5, sticky="nsew")

        logger_macchina_frame = tk.Frame(self, bg="green")
        logger_macchina_frame.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")

        errori_frame = tk.Frame(self, bg="purple")
        errori_frame.grid(column=2, row=0, padx=5, pady=5, sticky="nsew")