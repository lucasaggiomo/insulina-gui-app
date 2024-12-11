# Progetto GUI misuratore d'insulina - A.A. 2024/2025 Corso di Laboratorio di Misure
# Autori:
# Saggiomo Luca
# Saccone Matteo
# Romano Davide
# Ponticelli Lorenzo
# Porcelli Nicola

from tkinter import ttk

# classe per gestire tutte le immagini del programma
class StyleManager:
    # FONT
    big_font = ("Helvetica", 18, "bold")
    medium_font = ("Helvetica", 15, "bold")
    small_font = ("Helvetica", 13, "bold")
    
    # COLORI
    foreground_blue_color = "darkblue"
    foreground_red_color = "red"
    foreground_red3_color = "red3"
    foreground_green_color = "green"
    foreground_darkgreen_color = "darkgreen"

    # NOMI DEGLI STILI
    # (costanti utilizzate per semplificare la modifica del nome dello stile, senza dover modificare il nome dappertutto)
    
    # Bottoni (terminano con ".TButton")
    BIG_BLUE_BUTTON_STYLE_NAME = "BigBlue.TButton"
    MEDIUM_BLUE_BUTTON_STYLE_NAME = "MediumBlue.TButton"
    
    BIG_GREEN_BUTTON_STYLE_NAME = "BigGreen.TButton"
    MEDIUM_GREEN_BUTTON_STYLE_NAME = "MediumGreen.TButton"
    
    MEDIUM_RED3_BUTTON_STYLE_NAME = "MediumRed3.TButton"
    
    MEDIUM_RED_BUTTON_STYLE_NAME = "MediumRed.TButton"
    
    # Label (terminano con ".TLabel")
    BIG_BLUE_LABEL_STYLE_NAME = "BigBlue.TLabel"
    MEDIUM_BLUE_LABEL_STYLE_NAME = "MediumBlue.TLabel"
    SMALL_BLUE_LABEL_STYLE_NAME = "SmallBlue.TLabel"
    
    # TreeView (terminano con ".TreeView")
    SMALL_TREE_VIEW_STYLE_NAME = "Small.TreeView"
    
    # Entry (terminano con ".TEntry")
    ENTRY_BLUE_STYLE_NAME = "CustomBlue.TEntry"
    
    # carica tutti gli stili in variabili statiche della classe
    @staticmethod
    def load_styles():
        style = ttk.Style()

        # BOTTONI
        style.configure(
            StyleManager.BIG_BLUE_BUTTON_STYLE_NAME,            # nome
            font=StyleManager.big_font,                         # font
            foreground=StyleManager.foreground_blue_color,      # colore testo
            padding=10
        )
        
        style.configure(
            StyleManager.MEDIUM_BLUE_BUTTON_STYLE_NAME,         # nome
            font=StyleManager.medium_font,                      # font
            foreground=StyleManager.foreground_blue_color,      # colore testo
            padding=10
        )
        
        style.configure(
            StyleManager.BIG_GREEN_BUTTON_STYLE_NAME,           # nome
            font=StyleManager.big_font,                         # font
            foreground=StyleManager.foreground_green_color,     # colore testo
            padding=10
        )
        
        style.configure(
            StyleManager.MEDIUM_RED_BUTTON_STYLE_NAME,          # nome
            font=StyleManager.medium_font,                      # font
            foreground=StyleManager.foreground_red_color,       # colore testo
            padding=10
        )
        
        style.configure(
            StyleManager.MEDIUM_GREEN_BUTTON_STYLE_NAME,        # nome
            font=StyleManager.medium_font,                      # font
            foreground=StyleManager.foreground_green_color,     # colore testo
            padding=10
        )
                     
        style.configure(
            StyleManager.MEDIUM_RED3_BUTTON_STYLE_NAME,         # nome
            font=StyleManager.medium_font,                      # font
            foreground=StyleManager.foreground_red3_color,      # colore testo
            padding=10
        )
           
        # LABEL
        style.configure(
            StyleManager.BIG_BLUE_LABEL_STYLE_NAME,             # nome
            font=StyleManager.big_font,                         # font
            foreground=StyleManager.foreground_blue_color,      # colore testo
            padding=(0,0,10,0)
        )
        
        style.configure(
            StyleManager.MEDIUM_BLUE_LABEL_STYLE_NAME,          # nome
            font=StyleManager.medium_font,                      # font
            foreground=StyleManager.foreground_blue_color,      # colore testo
            padding=(0,0,10,0)
        )
        
        style.configure(
            StyleManager.SMALL_BLUE_LABEL_STYLE_NAME,           # nome
            font=StyleManager.small_font,                       # font
            foreground=StyleManager.foreground_blue_color,      # colore testo
            padding=(0,0,10,0)
        )

        # ENTRY
        style.configure(
            StyleManager.ENTRY_BLUE_STYLE_NAME,                 # nome
            font=StyleManager.medium_font,                      # font
            foreground=StyleManager.foreground_blue_color,      # colore testo
            padding=10
        )
        
        # TREE VIEW
        style.configure(
            StyleManager.SMALL_TREE_VIEW_STYLE_NAME,            # nome
            font=StyleManager.medium_font,                      # font
            foreground=StyleManager.foreground_blue_color,      # colore testo
            padding=(0,0,10,0)
        )
        
        # stile globale per gli heading delle colonne delle tabelle
        style.configure(
            "Treeview.Heading",
            font=StyleManager.small_font,
            foreground=StyleManager.foreground_blue_color
        )
        
        # stile globale per le righe delle tabelle
        style.configure(
            "Treeview",
            font=StyleManager.small_font,
            foreground=StyleManager.foreground_blue_color
        )