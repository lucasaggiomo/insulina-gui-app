# Progetto GUI misuratore d'insulina - A.A. 2024/2025 Corso di Laboratorio di Misure
# Autori:
# Saggiomo Luca
# Saccone Matteo
# Romano Davide
# Ponticelli Lorenzo
# Porcelli Nicola

# Importo la libreria tkinter
import tkinter as tk
from tkinter import ttk

# Importo altre classi
import frontend as ft
import backend as bk

from frontend.tabs import *
from frontend.image_manager import ImageManager  # importo la classe ImageManager dal modulo (cioè file) image_manager.py per la gestione delle immagini
from frontend.style_manager import StyleManager  # importo la classe StyleManager dal modulo style_manager.py per la gestione degli stili
import matplotlib.pyplot as plt   # Matplotlib per creare il grafico
from backend.bluetooth import BLEClient
from tkinter import messagebox
import threading
import asyncio


class App(tk.Tk):

    # Costruttore che costruisce l'oggetto di tipo App
    def __init__(self): 
        super().__init__()
        
        # Imposta il protocollo per la chiusura della finestra
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Ottiene la risoluzione dello schermo
        self.screen_width = self.winfo_screenwidth() # width of the screen
        self.screen_height = self.winfo_screenheight() # height of the screen
        
        # Imposta la finestra al 80% della larghezza e al 80% dell'altezza dello schermo
        window_width = int(self.screen_width * 0.7)
        window_height = int(self.screen_height * 0.7)
        
        # Calcola le posizioni x e y della finestra
        x = int((self.screen_width - window_width) / 2)
        y = int((self.screen_height - window_height) / 2)

        # Imposta la geometria della finestra (dimensioni e posizione)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Imposta la dimensione mini
        self.minsize(width=1200, height=700)
        
        # Titolo finestra
        self.title("Fondamenti di Misure")

        # Carico tutte le immagini dell'applicazione con la classe ImageManager
        ImageManager.load_images()

        # Carico tutti gli stili dell'applicazione con la classe StyleManager
        StyleManager.load_styles()
    
        # Chiamo la funzione create_widgets - dichiarata successivamente
        self.create_widgets()

    def on_closing(self):
        plt.close('all')  # Chiude tutte le figure matplotlib aperte
        
        if self.BLEclient:
            # manda stop alla board
            self.BLEclient.run_async_task(
                self.BLEclient.disconnect_sequence()
            )
            
        # Chiude la finestra tkinter
        self.destroy()

    # Funzione per creare tutti i widgets della finestra
    def create_widgets(self):
        # frame della barra superiore del programma (bottoni per cambiare la schermata e informazioni sulla board)
        top_bar_frame = self.create_top_bar_frame()
        top_bar_frame.pack(side="top", fill="x")

        # frame contenente il tab corrente (AcquisizioneDati, StatoMacchina o EsportazioneDati)
        tab_manager = self.create_tab_manager_frame()
        tab_manager.pack(side="bottom", fill="both", expand=True)

    # Crea la barra superiore del programma, contenente:
    #   - i bottoni per cambiare schermata nel tab_manager (FUNZIONE create_switch_tab_buttons)
    #   - informazioni sullo stato della board (bluetooth + batteria) (FUNZIONE create_board_status_frame)
    def create_top_bar_frame(self):
        top_bar_frame = ttk.Frame(self, height=50)

        # bottoni per cabiare schermata nel tab_manager
        tab_buttons_frame = self.create_switch_tab_buttons(top_bar_frame)
        tab_buttons_frame.pack(side="left", fill="both")        # allinea sulla sinistra
        
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
        self.show_dati_button = ttk.Button(switch_tab_buttons,
                                      text="Acquisizione dati",
                                      width=20,
                                      padding=10,
                                      style=StyleManager.BIG_BLUE_BUTTON_STYLE_NAME,
                                      command=self.show_dati_button_clicked)
        self.show_dati_button.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

        # Bottone per mostrare la schermata dello stato macchina
        self.show_macchina_button = ttk.Button(switch_tab_buttons,
                                          text="Stato macchina",
                                          width=20,
                                          padding=10,
                                          style=StyleManager.BIG_BLUE_BUTTON_STYLE_NAME,
                                          command=self.show_macchina_button_clicked)
        self.show_macchina_button.grid(column=1, row=0, padx=5, pady=5, sticky="nswe")
        
        # Bottone per mostrare la schermata dell'esportazione dati
        self.show_esporta_button = ttk.Button(switch_tab_buttons,
                                         text="Esporta dati",
                                         width=20,
                                         padding=10,
                                         style=StyleManager.BIG_BLUE_BUTTON_STYLE_NAME,
                                         command=self.show_esporta_button_clicked)
        self.show_esporta_button.grid(column=2, row=0, padx=5, pady=5, sticky="nswe")

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
        
        # variabile che indica se la finestra di bluetooth è aperta
        # permette di prevenire l'apertura multipla di più finestre bluetooth
        self.is_bluetooth_window_open = False
        bluetooth_button = ttk.Button(status_frame,
                                      width=10,
                                      image=ImageManager.bluetooth_image,
                                      compound="right",
                                      command=self.bluetooth_button_clicked)
        bluetooth_button.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")
        
        self.battery_percentage_string = tk.StringVar()
        self.battery_percentage_value = 100.0
        # chiama un'ipotetica funzione che legge la percentuale di batteria
        self.battery_label = ttk.Label(status_frame,
                                       style=StyleManager.MEDIUM_BLUE_LABEL_STYLE_NAME,
                                       compound="left",
                                       textvariable=self.battery_percentage_string)
        self.update_battery_percentage(100.0)
        self.battery_label.grid(column=2, row=0, padx=5, pady=5, sticky="nsew")
        
        return status_frame
            
    # Crea il frame che contiene i tre tabs (AcquisizioneDati, StatoMacchina e EsportazioneDati)
    def create_tab_manager_frame(self):
        tab_manager = tk.Frame(self)

        tab_manager.grid_propagate(False)
        
        # Definisco la riga dello status bar
        tab_manager.rowconfigure(0, weight=1)

        # Definisco la colonna dello status bar
        tab_manager.columnconfigure(0, weight=1)

        self.dati_tab = AcquisizioneDati(tab_manager,
                                         self.start_board,
                                         self.stop_board)
        self.dati_tab.grid(row=0,column=0, sticky="nsew")
        self.dati_tab.progress_value = 50
        
        # creo un oggetto BLEclient
        self.BLEclient = BLEClient(self.dati_tab.handle_new_measurement,
                                   self.update_battery_percentage)
        self.BLEclient.start_event_loop()

        self.macchina_tab = StatoMacchina(tab_manager)
        self.macchina_tab.grid(row=0,column=0, sticky="nsew")
        
        self.esporta_tab = EsportazioneDati(tab_manager)
        self.esporta_tab.grid(row=0,column=0, sticky="nsew")

        # imposta Acquisizione Dati come schermata iniziale
        self.show_dati_button_clicked()
        
        return tab_manager

    # Aggiorna la percentuale di batteria
    def update_battery_percentage(self, new_percentage):
        self.battery_percentage_value = new_percentage
        self.battery_percentage_string.set(f"{new_percentage} %")
        
        self.battery_label.configure(image = ImageManager.get_battery_image(new_percentage))
    
    # SEZIONE BLUETOOTH
    def bluetooth_button_clicked(self):
        # esce dalla funzione se la finestra risulta già aperta
        if self.is_bluetooth_window_open:
            return
        
        self.is_bluetooth_window_open = True
        print("Bottone bluetooth clickato")
        
        # definisce flag booleani
        self.is_connecting = False
        self.is_scanning = False
        
        bluetooth_window = tk.Toplevel(self)  # Crea una nuova finestra
        bluetooth_window.title("Ricerca bluetooth")
        
        bluetooth_window_width = 500
        bluetooth_window_height = 700
        
        # Calcola le posizioni x e y della finestra
        x = int((self.screen_width - bluetooth_window_width) / 2)
        y = int((self.screen_height - bluetooth_window_height) / 2)
        
        # Imposta la dimensione della finestra e la posizione
        bluetooth_window.geometry(f"{bluetooth_window_width}x{bluetooth_window_height}+{x}+{y}")
        bluetooth_window.minsize(width=400, height=400)
        
        # Imposto che alla chiusura della finestra la variabile is_bluetooth_window_open sia impostata a False
        bluetooth_window.protocol("WM_DELETE_WINDOW", lambda: self.on_bluetooth_window_closing(bluetooth_window))

        # Aggiungo un'etichetta nella nuova finestra
        
        # Aggiungo un pulsante per chiudere la nuova finestra
        self.scan_button = ttk.Button(bluetooth_window,
                                      text="Ricerca",
                                      style=StyleManager.MEDIUM_BLUE_BUTTON_STYLE_NAME,
                                      command=self.scan_button_click)
        self.scan_button.pack(side=tk.TOP, pady=(50,10))

        self.scan_stauts_var = tk.StringVar(value="Clicca il tasto \"Ricerca\" per cercare la tua board")
        status_label = ttk.Label(bluetooth_window,
                                 textvariable=self.scan_stauts_var,
                                 justify=tk.CENTER,
                                 style=StyleManager.SMALL_BLUE_LABEL_STYLE_NAME)
        status_label.pack(side=tk.TOP, pady=(0, 10))
              
        # definisco il frame della tabella, contenente:
        # - la tabella nella riga 0 e colonna 0
        # - la barra di scorrimento nella riga 0 e colonna 1  
        devices_list_frame = tk.Frame(bluetooth_window)
        devices_list_frame.grid_propagate(False)
        
        # riga
        devices_list_frame.rowconfigure(0, weight=1)

        # colonne
        devices_list_frame.columnconfigure(0, weight=1)
        devices_list_frame.columnconfigure(1, weight=0)
        
        # Creo una tabella con due colonne
        self.devices_tree = ttk.Treeview(devices_list_frame,
                                         columns=("name", "address"),
                                         show="headings")
        self.devices_tree.grid_configure(row=0, column=0, sticky="nwes")
        
        # Imposto le intestazioni delle colonne
        self.devices_tree.heading("name", text="Nome Dispositivo", anchor=tk.CENTER)
        self.devices_tree.heading("address", text="Indirizzo", anchor=tk.CENTER)

        # Definisco la larghezza delle colonne (opzionale)
        self.devices_tree.column("name", anchor=tk.W, width=150)
        self.devices_tree.column("address", anchor=tk.W, width=200)
        
        # definisco la scrollbar
        vertical_scrollbar = ttk.Scrollbar(devices_list_frame,
                                           orient="vertical",
                                           command=self.devices_tree.yview)
        vertical_scrollbar.grid_configure(row=0, column=1, sticky="wns")

        self.devices_tree.configure(yscrollcommand=vertical_scrollbar.set)

        self.aggiorna_bluetooth_treeview()

        # Posiziona il frame della tabella nella finestra
        devices_list_frame.pack(expand=True, fill=tk.BOTH, padx=20)
                
        self.connect_button = ttk.Button(bluetooth_window,
                                 text="Connetti",
                                 style=StyleManager.MEDIUM_BLUE_BUTTON_STYLE_NAME,
                                 command=self.connect_to_device_click)
        self.connect_button.pack(side=tk.TOP, pady=10)
        
        # inizialmente il bottone di connessione è disabilitato
        self.connect_button.config(state=tk.DISABLED)
        
        # self.connection_status_var = tk.StringVar(value="Seleziona un dispositivo e clicca\n\"Connetti\" per instaurare la connessione")
        # connection_status_label = ttk.Label(bluetooth_window,
        #                                     textvariable=self.connection_status_var,
        #                                     justify=tk.CENTER,
        #                                     style=StyleManager.SMALL_BLUE_LABEL_STYLE_NAME)
        # connection_status_label.pack(side=tk.TOP, pady=(0, 10))
        
        self.BLEclient.status_var = self.scan_stauts_var

    # rimuove tutti gli elementi esistenti nella tabella dei dispositivi bluetooth
    def reset_bluetooth_treeview(self):
        for item in self.devices_tree.get_children():
            self.devices_tree.delete(item)
            
    # aggiorna la tabella dei dispositivi bluetooth
    def aggiorna_bluetooth_treeview(self):
        # resetta la treeview
        self.reset_bluetooth_treeview()

        # Inserisce i nuovi dati dalla lista self.devices
        for device in self.BLEclient.devices_found:
            self.devices_tree.insert("", tk.END, values=(device.name or "Sconosciuto", device.address))
            
    def on_bluetooth_window_closing(self, bluetooth_window):
        self.is_bluetooth_window_open = False
        bluetooth_window.destroy()
        
    # avvia la scansione dei dispositivi BLE nelle vicinanze
    # ed esegue on_scan_complete al termine, per aggiornare la tabella
    def scan_button_click(self):
        # esce se sta già connettendo
        if self.is_scanning:
            return
        
        # imposta che sta effettuando la scansione e disabilita il bottone per scansionare (per impedire scansioni multiple)
        # disabilita anche il bottone per connettersi
        self.is_scanning = True
        self.scan_button.config(state=tk.DISABLED)
        self.connect_button.config(state=tk.DISABLED)
        
        # resetta la tabella dei dispositivi trovati in precedenza
        self.reset_bluetooth_treeview()
        
        # effettua la scansione in maniera asincrona (quindi non bloccante per il programma)
        self.BLEclient.run_async_task(
            self.BLEclient.start_scan(callback=self.on_scan_complete,
                                      on_error=self.reset_flags)
        )
        
    # funzione eseguita al termine della scansione:
    # - aggiorna la tabella dei dispositivi trovati
    # - abilita nuovamente il bottone per scansionare e imposta la variabile is_scanning a False
    # - abilita il bottone per connettere
    def on_scan_complete(self):
        self.aggiorna_bluetooth_treeview()
        self.reset_flags()
        
    def reset_flags(self):
        self.is_scanning = False
        self.is_connecting = False
        self.scan_button.config(state=tk.NORMAL)
        self.connect_button.config(state=tk.NORMAL)
            
    def connect_to_device_click(self):
        print(f"is_scanning = {self.is_scanning}, is_connecting = {self.is_connecting}")
        
        # esce se sta già connettendo o se sta scansionando
        if self.is_scanning or self.is_connecting:
            return
        
        # preleva l'elemento selezionato
        selected_item = self.devices_tree.selection()
        if not selected_item:
            self.scan_stauts_var.set("Non hai selezionato un dispositivo.\nSeleziona un dispositivo e clicca \"Connetti\" per connetterti")
            return
        
        # imposta che sta effettuando la connesione e disabilita il bottone per connettere (per impedire connessioni multiple)
        self.is_connecting = True
        self.scan_button.config(state=tk.DISABLED)
        self.connect_button.config(state=tk.DISABLED)
        
        # ottiene il nome e l'indirizzo del dispositivo selezionato
        device_info = self.devices_tree.item(selected_item, "values")
        device_name = device_info[0]     # Il nome è nella prima colonna
        device_address = device_info[1]  # L'indirizzo è nella seconda colonna
        
        print(f"Dispositivo selezionato:\nnome: {device_name}, indirizzo MAC: {device_address}")
        
        # Avvia la connessione in modo asincrono
        self.BLEclient.run_async_task(
            self.BLEclient.connect_to_device(device_name,
                                             device_address,
                                             on_success=self.on_connect_success,
                                             on_error=self.reset_flags)
        )
    
    # funzione eseguita al termine della connessione:
    # - abilita nuovamente il bottone per scansionare e imposta la variabile is_connecting a False
    # - invia la richiesta di notifiche per la batteria alla board
    def on_connect_success(self):
        self.connect_button.config(state=tk.NORMAL)
        self.is_connecting = False
        # self.connect_button.config(state=tk.DISABLED)
        self.start_battery_level_notify()

    def start_board(self):
        if not self.BLEclient.is_connected:
            messagebox.showerror(title="Misurazione non iniziata",
                                 message="Non hai effettuato la connessione con una board.\nClicca sul bottone con il simbolo del bluetooth per collegare una board.")
            return False
        
        print("Mando start alla board")
        
        # manda un comando di start alla board
        self.BLEclient.run_async_task(
            self.BLEclient.start_board()
        )
        
        return True
        
    def stop_board(self):
        if not self.BLEclient.is_connected:
            messagebox.showerror(title="Misurazione non terminata",
                                 message="Non hai effettuato la connessione con una board.\nClicca sul bottone con il simbolo del bluetooth per collegare una board.")
            return False
        
        print("Mando stop alla board")
        
        # manda un comando di start alla board
        self.BLEclient.run_async_task(
            self.BLEclient.stop_board()
        )
        
        return True
        
    def start_battery_level_notify(self):
        if self.BLEclient is None or not self.BLEclient.is_connected:
            return False
        
        print("Mando la richiesta di ricezione delle notifiche sulla percentuale di batteria della board")
        
        self.BLEclient.run_async_task(
            self.BLEclient.start_battery_level_notify()
        )
        
        return True
    
    def stop_battery_level_notify(self):
        if not self.BLEclient:
            messagebox.showerror(title="Misurazione non terminata",
                                 message="Non hai effettuato la connessione con una board.\nClicca sul bottone con il simbolo del bluetooth per collegare una board.")
            return False
        
        print("Interrompo la ricezione della percentuale di batteria della board")
        
        self.BLEclient.run_async_task(
            self.BLEclient.stop_battery_level_notify()
        )
    
    # EVENTI BOTTONI
    def show_dati_button_clicked(self):
        self.dati_tab.tkraise()
        
        self.show_dati_button.configure(style = StyleManager.BIG_GREEN_BUTTON_STYLE_NAME)
        self.show_macchina_button.configure(style = StyleManager.BIG_BLUE_BUTTON_STYLE_NAME)
        self.show_esporta_button.configure(style = StyleManager.BIG_BLUE_BUTTON_STYLE_NAME)
        
        print("Schermata Acquisizione Dati selezionata")

    def show_macchina_button_clicked(self):
        self.macchina_tab.tkraise()
        
        self.show_macchina_button.configure(style = StyleManager.BIG_GREEN_BUTTON_STYLE_NAME)
        self.show_dati_button.configure(style = StyleManager.BIG_BLUE_BUTTON_STYLE_NAME)
        self.show_esporta_button.configure(style = StyleManager.BIG_BLUE_BUTTON_STYLE_NAME)
        
        print("Schermata Stato Macchina selezionata")
        
    def show_esporta_button_clicked(self):
        self.esporta_tab.tkraise()
        
        self.show_esporta_button.configure(style = StyleManager.BIG_GREEN_BUTTON_STYLE_NAME)
        self.show_macchina_button.configure(style = StyleManager.BIG_BLUE_BUTTON_STYLE_NAME)
        self.show_dati_button.configure(style = StyleManager.BIG_BLUE_BUTTON_STYLE_NAME)
        
        print("Schermata Esportazione Dati selezionata")


if __name__ == "__main__":
    app = App() # invoco il costruttore
    app.mainloop() # funzione per eseguire il programma - la possiamo utilizzare in quanto si trova nella classe padre Tk
