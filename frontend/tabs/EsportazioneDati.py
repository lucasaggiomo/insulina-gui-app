# Progetto GUI misuratore d'insulina - A.A. 2024/2025 Corso di Laboratorio di Misure
# Autori:
# Saggiomo Luca
# Saccone Matteo
# Romano Davide
# Ponticelli Lorenzo
# Porcelli Nicola

import tkinter as tk
from tkinter import ttk

from frontend.image_manager import ImageManager
from frontend.style_manager import StyleManager

# definisce la classe EsportazioneDati, che eredita da tk.Frame
class EsportazioneDati(tk.Frame):
    
    def __init__(self, parent_frame): 
        super().__init__(parent_frame)
        
        self.create_widgets()
    
    # definisce la funzione per creare i widgets nel tab
    def create_widgets(self):
        export_excel_frame = ttk.Button(
            self,
            style=StyleManager.MEDIUM_BLUE_BUTTON_STYLE_NAME,
            text="Esporta dati su Excel",
            image=ImageManager.excel_image,
            compound="left",                            # mostra l'immagine alla sinistra del testo
            command=self.esporta_dati_excel_clicked
        )
        export_excel_frame.pack(fill="both")

        export_pdf_frame = ttk.Button(
            self,
            style=StyleManager.MEDIUM_BLUE_BUTTON_STYLE_NAME,
            text="Esporta dati su Pdf",
            image=ImageManager.pdf_image,
            compound="left",                            # mostra l'immagine alla sinistra del testo
            command=self.esporta_dati_pdf_clicked
        )
        export_pdf_frame.pack(fill="both")

    # EVENTI BOTTONI
    def esporta_dati_excel_clicked(self):
        print("Esportazione dati su excel in corso...")

    def esporta_dati_pdf_clicked(self):
        print("Esportazione dati su pdf in corso...")
    
