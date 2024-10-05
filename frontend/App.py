# Progetto GUI misuratore d'insulina - A.A. 2024/2025 Corso di Laboratorio di Misure
# Autori:
# Saggiomo Luca
# Saccone Matteo
# Ponticelli Lorenzo
# Porcelli Nicola

# Importo la libreria tkinter
import tkinter as tk
from tkinter import ttk

# Importo altre classi
from tabs import *
from image_manager import ImageManager

class App(tk.Tk):

    # Costruttore che costruisce l'oggetto di tipo App
    def __init__(self): 
        super().__init__()

        # Size iniziale della finestra
        self.geometry("1100x700")
        self.minsize(width=1100, height=600)

        # Titolo finestra
        self.title("Fondamenti di Misure")

        # Carico tutte le immagini dell'applicazione con la classe ImageManager
        ImageManager.load_images()

        # Definisco gli stili utilizzati
        App.create_styles()
                
        # Chiamo la funzione create_widgets - dichiarata successivamente
        self.create_widgets()
        
    # region FUNZIONI STATICHE [#region per dire a VScode di compattare il codice]
    # Sezione delle funzioni statiche (senza "self" come parametro e con "@staticmethod"), che non accedono alle proprietà dell'oggetto

    # Crea gli stili dell'applicazione
    @staticmethod
    def create_styles():
        # Definisco delle variabili comuni a tutti gli stili
        App.custom_font = ("Helvertica", 15, "bold")
        App.foreground_color = "darkblue"

        # Creazione di uno stile personalizzato
        style = ttk.Style()
        
        # Definisco uno stile personalizzato per i bottoni
        # Nota: il nome dello stile deve terminare con TButton
        style.configure("Custom.TButton",                   # nome
                        font=App.custom_font,                   # font
                        foreground=App.foreground_color,        # colore testo
                        padding=10
                        )
        
        style.configure("Custom.TLabel",                    # nome
                        font=App.custom_font,                   # font
                        foreground=App.foreground_color,        # colore testo
                        padding=(0,0,10,0)
                        )
        
    #endregion

    # region FUNZIONI DI ISTANZA (non statiche) [#region per dire a VScode di compattare il codice]

    # Funzione per creare tutti i widgets della finestra
    def create_widgets(self):
        # frame della barra superiore del programma (bottoni per cambiare la schermata e informazioni sulla board)
        top_bar_frame = self.create_top_bar_frame()
        top_bar_frame.pack(side="top", fill="both")

        # frame contenente il tab corrente (AcquisizioneDati, StatoMacchina o EsportazioneDati)
        tab_manager = self.create_tab_manager_frame()
        tab_manager.pack(side="bottom", fill="both", expand=True)


    # Crea la barra superiore del programma, contenente:
    #   - i bottoni per cambiare schermata nel tab_manager (FUNZIONE create_switch_tab_buttons)
    #   - informazioni sullo stato della board (bluetooth + batteria) (FUNZIONE create_board_status_frame)
    def create_top_bar_frame(self):
        top_bar_frame = ttk.Frame(self, height=50)

        # bottoni per cabiare schermata nel tab_manager
        giovanni = self.create_switch_tab_buttons(top_bar_frame)
        giovanni.pack(side="left", fill="both")        # allinea sulla sinistra
        
        # frame bluetooth + batteria (stato della board) 
        status_frame = self.create_board_status_frame(top_bar_frame)
        status_frame.pack(side="right", fill="both")   # allinea sulla destra

        return top_bar_frame

    # Crea i bottoni per cambiare schermata nel tab_manager
    def create_switch_tab_buttons(self, parent):
        switch_tab_buttons = ttk.Frame(parent)

        switch_tab_buttons.grid_propagate(True)

        # Definisco la riga della topbar
        switch_tab_buttons.rowconfigure(0, weight=1)

        # Definisco le colonne della topbar        
        switch_tab_buttons.columnconfigure(0, weight=0)
        switch_tab_buttons.columnconfigure(1, weight=0)
        switch_tab_buttons.columnconfigure(2, weight=0)

        # Bottone per mostrare la schermata dell'acquisizione dati
        show_dati_button = ttk.Button(switch_tab_buttons,
                                      text="Acquisizione dati",
                                      width=20,
                                      padding=10,
                                      style="Custom.TButton",
                                      command=self.show_dati_button_clicked)
        show_dati_button.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

        # Bottone per mostrare la schermata dello stato macchina
        show_macchina_button = ttk.Button(switch_tab_buttons,
                                          text="Stato macchina",
                                          width=20,
                                          padding=10,
                                          style="Custom.TButton",
                                          command=self.show_macchina_button_clicked)
        show_macchina_button.grid(column=1, row=0, padx=5, pady=5, sticky="nswe")
        
        # Bottone per mostrare la schermata dell'esportazione dati
        show_esporta_button = ttk.Button(switch_tab_buttons,
                                         text="Esporta dati",
                                         width=20,
                                         padding=10,
                                         style="Custom.TButton",
                                         command=self.show_esporta_button_clicked)
        show_esporta_button.grid(column=2, row=0, padx=5, pady=5, sticky="nswe")

        return switch_tab_buttons
    
    # Creazione del Frame bluetooth + batteria (stato della board) 
    def create_board_status_frame(self, parent):
        status_frame = ttk.Frame(parent)
        
        status_frame.grid_propagate(True)
        
        # definisco la riga
        status_frame.rowconfigure(0, weight=1)
        
        # definisco le colonne
        status_frame.columnconfigure(0, weight=0)
        status_frame.columnconfigure(1, weight=0)
        
        bluetooth_button = ttk.Button(status_frame,
                                      image=ImageManager.bluetooth_image,
                                      compound="right",
                                      command=self.bluetooth_button_clicked)
        bluetooth_button.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")
        
        self.battery_percentage_string = tk.StringVar(value="100 %")
        self.battery_percentage_value = 100.0
        # chiama un'ipotetica funzione che legge la percentuale di batteria
        self.battery_label = ttk.Label(status_frame,
                                       style="Custom.TLabel",
                                       compound="left",
                                       textvariable=self.battery_percentage_string)
        self.update_battery_percentage()
        self.battery_label.grid(column=2, row=0, padx=5, pady=5, sticky="nsew")
        
        return status_frame

    # Crea il frame che contiene i tre tabs (AcquisizioneDati, StatoMacchina e EsportazioneDati)
    def create_tab_manager_frame(self):
        tab_manager = tk.Frame(self, bg="red", width=100)

        tab_manager.grid_propagate(False)
        
        # Definisco la riga dello status bar
        tab_manager.rowconfigure(0, weight=1)

        # Definisco la colonna dello status bar
        tab_manager.columnconfigure(0, weight=1)

        self.dati_tab = AcquisizioneDati(tab_manager)
        self.dati_tab.grid(row=0,column=0, sticky="nsew");
        self.dati_tab.progress_value = 50;

        self.macchina_tab = StatoMacchina(tab_manager)
        self.macchina_tab.grid(row=0,column=0, sticky="nsew");
        
        self.esporta_tab = EsportazioneDati(tab_manager)
        self.esporta_tab.grid(row=0,column=0, sticky="nsew");

        self.dati_tab.tkraise()
        
        return tab_manager
    

    # Aggiorna la percentuale di batteria
    def update_battery_percentage(self):
        newPercentage = self.read_board_battery_percentage()
        self.battery_percentage_value = newPercentage
        self.battery_percentage_string.set(f"{newPercentage} %")
        
        self.battery_label.configure(image = ImageManager.get_battery_image(newPercentage))
            
    # Questo metodo legge la percentuale di batteria della board
    def read_board_battery_percentage(self):
        return 74.0      # percentuale fittizia
        
    # EVENTI BOTTONI
    def show_dati_button_clicked(self):
        self.dati_tab.tkraise()
        print("Schermata Acquisizione Dati selezionata")

    def show_macchina_button_clicked(self):
        self.macchina_tab.tkraise()
        print("Schermata Stato Macchina selezionata")
        
    def show_esporta_button_clicked(self):
        self.esporta_tab.tkraise()
        print("Schermata Esportazione Dati selezionata")
        
    def bluetooth_button_clicked(self):
        print("Bottone bluetooth clickato")
        
    #endregion
        
if __name__ == "__main__":
    app = App() # invoco il costruttore
    app.mainloop() # funzione per eseguire il programma - la possiamo utilizzare in quanto si trova nella classe padre Tk