# Progetto GUI misuratore d'insulina - A.A. 2024/2025 Corso di Laboratorio di Misure
# Autori:
# Saggiomo Luca
# Saccone Matteo
# Ponticelli Lorenzo
# Porcelli Nicola

import tkinter as tk
from tkinter import ttk

class StyleManager:
    custom_font = ("Helvetica", 15, "bold")
    foreground_color = "darkblue"

    # Definisco delle costanti per i nomi degli stili
    # (in modo da semplificare la modifica, senza dover modificare il nome dappertutto)
    CUSTOM_BUTTON_STYLE_NAME = "Custom.TButton"
    CUSTOM_LABEL_STYLE_NAME = "Custom.TLabel"
    
    @staticmethod
    def load_styles():
        style = ttk.Style()

        # Stile per bottoni
        style.configure(StyleManager.CUSTOM_BUTTON_STYLE_NAME,       # nome
                        font=StyleManager.custom_font,              # font
                        foreground=StyleManager.foreground_color,   # colore testo
                        padding=10
                        )
                
        style.configure(StyleManager.CUSTOM_LABEL_STYLE_NAME,       # nome
                        font=StyleManager.custom_font,              # font
                        foreground=StyleManager.foreground_color,   # colore testo
                        padding=(0,0,10,0)
                        )