# Progetto GUI misuratore d'insulina - A.A. 2024/2025 Corso di Laboratorio di Misure
# Autori:
# Saggiomo Luca
# Saccone Matteo
# Romano Davide
# Ponticelli Lorenzo
# Porcelli Nicola

import tkinter as tk
from tkinter import ttk

class StyleManager:
    big_font = ("Helvetica", 18, "bold")
    medium_font = ("Helvetica", 15, "bold")
    small_font = ("Helvetica", 13, "bold")
    
    foreground_color = "darkblue"

    # Definisco delle costanti per i nomi degli stili
    # (in modo da semplificare la modifica, senza dover modificare il nome dappertutto)
    BIG_BUTTON_STYLE_NAME = "Big.TButton"
    MEDIUM_BUTTON_STYLE_NAME = "Medium.TButton"
    
    CUSTOM_LABELBUTTON_STYLE_NAME = "Custom2.TLabel"
    
    # Label
    BIG_LABEL_STYLE_NAME = "Big.TLabel"
    MEDIUM_LABEL_STYLE_NAME = "Medium.TLabel"
    SMALL_LABEL_STYLE_NAME = "Small.TLabel"
    
    SMALL_TREE_VIEW_STYLE_NAME = "Small.TreeView"
    
    # Entry
    ENTRY_STYLE_NAME = "Custom.TEntry"
    
    @staticmethod
    def load_styles():
        style = ttk.Style()

        # BOTTONI
        style.configure(StyleManager.BIG_BUTTON_STYLE_NAME,         # nome
                        font=StyleManager.big_font,                 # font
                        foreground=StyleManager.foreground_color,   # colore testo
                        padding=10
                        )
        style.configure(StyleManager.MEDIUM_BUTTON_STYLE_NAME,      # nome
                        font=StyleManager.medium_font,              # font
                        foreground=StyleManager.foreground_color,   # colore testo
                        padding=10
                        )
                
        # LABEL
        style.configure(StyleManager.BIG_LABEL_STYLE_NAME,          # nome
                        font=StyleManager.big_font,                 # font
                        foreground=StyleManager.foreground_color,   # colore testo
                        padding=(0,0,10,0)
                        )
        style.configure(StyleManager.MEDIUM_LABEL_STYLE_NAME,          # nome
                        font=StyleManager.medium_font,                 # font
                        foreground=StyleManager.foreground_color,   # colore testo
                        padding=(0,0,10,0)
                        )
        style.configure(StyleManager.SMALL_LABEL_STYLE_NAME,        # nome
                        font=StyleManager.small_font,               # font
                        foreground=StyleManager.foreground_color,   # colore testo
                        padding=(0,0,10,0)
                        )

        # ENTRY
        style.configure(StyleManager.ENTRY_STYLE_NAME,              # nome
                        font=StyleManager.medium_font,               # font
                        foreground=StyleManager.foreground_color,   # colore testo
                        padding=10
                        )
        
        # TREE VIEW
        style.configure(StyleManager.SMALL_TREE_VIEW_STYLE_NAME,          # nome
                        font=StyleManager.medium_font,                 # font
                        foreground=StyleManager.foreground_color,   # colore testo
                        padding=(0,0,10,0)
                )
        
        style.configure("Treeview.Heading",
                        font=StyleManager.small_font,
                        foreground=StyleManager.foreground_color)
        
        style.configure("Treeview",
                        font=StyleManager.small_font,
                        foreground=StyleManager.foreground_color)
        
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