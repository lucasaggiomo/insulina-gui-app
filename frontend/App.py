# Progetto GUI misuratore d'insulina - A.A. 2024/2025 Corso di Laboratorio di Misure
# Autori:
# Saggiomo Luca
# Saccone Matteo
# Ponticelli Lorenzo
# Porcelli Nicola

# Importo la libreria tkinter
import tkinter as tk
from tkinter import ttk

# Importo altre classe 
from Tabs import *

class App(tk.Tk):

    # Costruttore che costruisce l'oggetto di tipo App
    def __init__(self): 
        super().__init__()

        # Size iniziale della finestra
        self.geometry("1100x600")
        self.minsize(width=900, height=400)

        # Titolo finestra
        self.title("Fondamenti di Misure")

        # Non permettere il resize
        # self.resizable(0, 0)
        
        # Chiamo la funzione create_widgets - dichiarata successivamente
        self.create_widgets()

    def create_widgets(self):
        self.grid_propagate(False)
        
        # definisco le colonne della finestra globale
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        
        # definisco le righe della finestra globale
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)

        tab_control = tk.Frame(self, bg="yellow")
        tab_control.grid(column=0, row=1, columnspan=4, sticky="nesw")

        tab_control.grid_propagate(False)
        
        tab_control.rowconfigure(0, weight=1)
        tab_control.columnconfigure(0, weight=1)

        dati_tab = AcquisizioneDati(tab_control)
        dati_tab.grid(row=0,column=0, sticky="nsew");
        dati_tab.progress_value = 50;

        macchina_tab = StatoMacchina(tab_control)
        macchina_tab.grid(row=0,column=0, sticky="nsew");
        
        esporta_tab = EsportazioneDati(tab_control)
        esporta_tab.grid(row=0,column=0, sticky="nsew");

        dati_tab.tkraise()

        dati_button = tk.Button(self, text="Acquisizione dati", command=dati_tab.tkraise)
        dati_button.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

        macchina_button = tk.Button(self, text="Stato macchina", command=macchina_tab.tkraise)
        macchina_button.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")
        
        esporta_button = tk.Button(self, text="Caricamento a file", command=esporta_tab.tkraise)
        esporta_button.grid(column=2, row=0, padx=5, pady=5, sticky="nsew")
        
        # frame bluetooth + batteria (stato della board)
        status_frame = tk.Frame(self, bg="darkgreen")
        status_frame.grid(column=3, row=0, padx=5, pady=5, sticky="nsew")
        
        # tab_control.add(dati_tab, text="Acquisizione dati")
        # tab_control.add(macchina_tab, text="Stato macchina")
        # tab_control.add(esporta_tab, text="Caricamento file")

if __name__ == "__main__":
    app = App() # invoco il costruttore
    app.mainloop() # funzione per eseguire il programma - la possiamo utilizzare in quanto si trova nella classe padre Tk