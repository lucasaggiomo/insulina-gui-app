# Progetto GUI misuratore d'insulina - A.A. 2024/2025 Corso di Laboratorio di Misure
# Autori:
# Saggiomo Luca
# Saccone Matteo
# Ponticelli Lorenzo
# Porcelli Nicola

import tkinter as tk
from tkinter import ttk

# Definisco la classe EsportazioneDati, che eredita da tk.Frame
class EsportazioneDati(tk.Frame):
    
    # Costruttore che costruisce l'oggetto di tipo App
    def __init__(self, parent_frame): 
        super().__init__(parent_frame)
        
        self.create_widgets()
    
    # Definisco la funzione per creare i widgets nel Frame
    def create_widgets(self):
        self.grid_propagate(False)

        # definisco le colonne
        self.columnconfigure(0, weight=1)
        
        # definisco le righe
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=2)

        export_excel_frame = tk.Button(self, text="Esporta dati su Excel")
        export_excel_frame.grid(column=0, row=0, rowspan=3, padx=5, pady=5, sticky="new")

        export_pdf_frame = tk.Button(self, text="Esporta dati su Pdf")
        export_pdf_frame.grid(column=0, row=1, padx=5, pady=5, sticky="new")