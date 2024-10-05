import tkinter as tk
from tkinter import ttk

class StyleManager:
    custom_font = ("Helvetica", 15, "bold")
    foreground_color = "darkblue"
    
    @staticmethod
    def load_styles():
        style = ttk.Style()

        # Stile per bottoni
        style.configure("Custom.TButton",                           # nome
                        font=StyleManager.custom_font,              # font
                        foreground=StyleManager.foreground_color,   # colore testo
                        padding=10
                        )
                
        style.configure("Custom.TLabel",                            # nome
                        font=StyleManager.custom_font,              # font
                        foreground=StyleManager.foreground_color,   # colore testo
                        padding=(0,0,10,0)
                        )