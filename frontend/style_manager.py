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
    CUSTOM_LABELBUTTON_STYLE_NAME = "Custom2.TLabel"
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

        # Definisco uno stile per la label che appare come un bottone
        style.configure(StyleManager.CUSTOM_LABELBUTTON_STYLE_NAME,
                        relief="raised",  # Effetto di contorno "bottone"
                        borderwidth=2,     # Spessore del contorno
                        padding=(10, 5),   # Padding interno
                        background="white", # Colore di sfondo
                        foreground="darkblue", # Colore del testo
                        font=("Helvetica", 12, "bold")) # Font della label
        
        # Opzionale: Stile attivo se desideri un effetto al passaggio del mouse
        style.map(StyleManager.CUSTOM_LABELBUTTON_STYLE_NAME,
                  background=[("active", "#e0eef9")],  # Colore di sfondo attivo
                  foreground=[("active", "blue")])     # Colore del testo attivo