# Progetto GUI misuratore d'insulina - A.A. 2024/2025 Corso di Laboratorio di Misure
# Autori:
# Saggiomo Luca
# Saccone Matteo
# Ponticelli Lorenzo
# Porcelli Nicola

import tkinter as tk
from tkinter import ttk

from image_manager import ImageManager
from style_manager import StyleManager

# Definisco la classe EsportazioneDati, che eredita da tk.Frame
class EsportazioneDati(tk.Frame):
    
    # Costruttore che costruisce l'oggetto di tipo App
    def __init__(self, parent_frame): 
        super().__init__(parent_frame)
        
        self.create_widgets()
    
    # Definisco la funzione per creare i widgets nel Frame
    def create_widgets(self):
        # self.grid_propagate(True)

        # # definisco le colonne
        # self.columnconfigure(0, weight=0)
        # self.columnconfigure(1, weight=1)
        
        # # definisco le righe
        # self.rowconfigure(0, weight=0)
        # self.rowconfigure(1, weight=0)
        # self.rowconfigure(2, weight=5)

        export_excel_frame = ttk.Button(self,
                                        style=StyleManager.CUSTOM_BUTTON_STYLE_NAME,
                                        text="Esporta dati su Excel",
                                        image=ImageManager.excel_image,
                                        compound="left",                         # mostra l'immagine alla sinistra del testo
                                        command=self.esporta_dati_excel_clicked) # funzione invocata al click del bottone
                                        
        # export_excel_frame.grid(column=0, row=0, padx=5, pady=5, sticky="nswe")
        export_excel_frame.pack(fill="both")

        export_pdf_frame = ttk.Button(self,
                                      style=StyleManager.CUSTOM_BUTTON_STYLE_NAME,
                                      text="Esporta dati su Pdf",
                                      image=ImageManager.pdf_image,
                                      compound="left",                          # mostra l'immagine alla sinistra del testo
                                      command=self.esporta_dati_pdf_clicked)    # funzione invocata al click del bottone
        # export_pdf_frame.grid(column=0, row=1, padx=5, pady=5, sticky="nswe")
        export_pdf_frame.pack(fill="both")

    # EVENTI BOTTONI
    def esporta_dati_excel_clicked(self):
        print("Esportazione dati su excel in corso...")

    def esporta_dati_pdf_clicked(self):
        print("Esportazione dati su pdf in corso...")
    
