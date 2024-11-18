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
from screeninfo import get_monitors
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

        # Ottieni la risoluzione dello schermo
        screen_width = get_monitors()[0].width
        screen_height = get_monitors()[0].height

        # Imposta la finestra al 80% della larghezza e al 80% dell'altezza dello schermo
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)

        # Imposta la geometria della finestra
        self.geometry(f"{window_width}x{window_height}")
        
        self.minsize(width=1300, height=800)
        
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
        
        # self.stop_board(write_message = False)
        
        if self.BLEclient:
            self.BLEclient.run_async_task(self.BLEclient.disconnect_from_device())
            self.BLEclient.stop_event_loop()
            
        self.destroy()     # Chiude la finestra tkinter


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
        
        bluetooth_window = tk.Toplevel(self)  # Crea una nuova finestra
        bluetooth_window.title("Ricerca bluetooth")
        bluetooth_window.geometry("500x800")  # Imposta la dimensione della finestra
        bluetooth_window.minsize(width=400, height=400)
        
        # Imposto che alla chiusura della finestra la variabile is_bluetooth_window_open sia impostata a False
        bluetooth_window.protocol("WM_DELETE_WINDOW", lambda: self.on_bluetooth_window_closing(bluetooth_window))

        # Aggiungo un'etichetta nella nuova finestra
        
        # Aggiungo un pulsante per chiudere la nuova finestra
        scan_button = ttk.Button(bluetooth_window,
                                 text="Ricerca",
                                 style=StyleManager.MEDIUM_BLUE_BUTTON_STYLE_NAME,
                                 command=self.scan_button_click)
        scan_button.pack(side=tk.TOP, pady=(50,10))

        self.scan_var = tk.StringVar(value="Clicca il tasto Ricerca per cercare la tua board")
        status_label = ttk.Label(bluetooth_window,
                                 textvariable=self.scan_var,
                                 justify=tk.CENTER,
                                 style=StyleManager.SMALL_BLUE_LABEL_STYLE_NAME)
        status_label.pack(side=tk.TOP)
                
        # Creo una tabella con due colonne
        self.devices_tree = ttk.Treeview(bluetooth_window,
                                         columns=("name", "address"),
                                         show="headings")
        
        # Imposto le intestazioni delle colonne
        self.devices_tree.heading("name", text="Nome Dispositivo", anchor=tk.W)
        self.devices_tree.heading("address", text="Indirizzo", anchor=tk.W)

        # Definisco la larghezza delle colonne (opzionale)
        self.devices_tree.column("name", anchor=tk.W, width=150)
        self.devices_tree.column("address", anchor=tk.W, width=200)

        self.aggiorna_bluetooth_treeview()

        # Posiziona la Treeview nella finestra
        self.devices_tree.pack(expand=True, fill=tk.BOTH, padx=20)
                
        self.connect_button = ttk.Button(bluetooth_window,
                                 text="Connetti",
                                 style=StyleManager.MEDIUM_BLUE_BUTTON_STYLE_NAME,
                                 command=self.connect_to_device_click)
        self.connect_button.pack(side=tk.TOP, pady=10)
        
        self.connection_status_var = tk.StringVar(value="Seleziona un dispositivo e clicca\n\"Connetti\" per instaurare la connessione")
        connection_status_label = ttk.Label(bluetooth_window,
                                            textvariable=self.connection_status_var,
                                            justify=tk.CENTER,
                                            style=StyleManager.SMALL_BLUE_LABEL_STYLE_NAME)
        connection_status_label.pack(side=tk.TOP, pady=(0, 10))
        
        self.BLEclient.status_var = self.connection_status_var

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
        
    def on_scan_complete(self):
        self.reset_bluetooth_treeview()
        self.aggiorna_bluetooth_treeview()
        
    # avvia la scansione dei dispositivi BLE nelle vicinanze
    # ed esegue on_scan_complete al termine, per aggiornare la tabella
    def scan_button_click(self):
        self.BLEclient.run_async_task(
            self.BLEclient.start_scan(callback=self.on_scan_complete)
        )
        
    def on_connect_success(self):
        self.connect_button.config(state=tk.DISABLED)
        # self.disconnect_button.config(state=tk.NORMAL)
            
    def connect_to_device_click(self):
        selected_item = self.devices_tree.selection()
        if not selected_item:
            self.update_status("Seleziona un dispositivo per connetterti.")
            return
        
        # ottiene il nome e l'indirizzo del dispositivo selezionato
        device_info = self.devices_tree.item(selected_item, "values")
        device_name = device_info[0]     # Il nome è nella prima colonna
        device_address = device_info[1]  # L'indirizzo è nella seconda colonna
        
        print(f"Dispositivo selezionato:\nnome: {device_name}, indirizzo MAC: {device_address}")
        
        # Avvia la connessione in modo asincrono
        self.BLEclient.run_async_task(
            self.BLEclient.connect_to_device(device_name,
                                             device_address,
                                             on_success=self.on_connect_success)
        )

    def start_board(self):
        if not self.BLEclient.is_connected:
            messagebox.showerror(title="Misurazione non iniziata",
                                 message="Non hai effettuato la connessione con una board.\nClicca sul bottone con il simbolo del bluetooth per collegare una board.")
            return False
        
        print("Mando start alla board")
        
        # Crea un loop asincrono permanente
        self.measurement_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.measurement_loop)
        
        # Avvia il ciclo di eventi in un thread separato
        threading.Thread(target=self.measurement_loop.run_forever, daemon=True).start()
        
        # Usa create_task per avviare start_board senza chiudere il loop
        self.measurement_loop.create_task(self.BLEclient.start_board())
        
        return True
        
    def stop_board(self):
        if not self.BLEclient.is_connected:
            messagebox.showerror(title="Misurazione non terminata",
                                 message="Non hai effettuato la connessione con una board.\nClicca sul bottone con il simbolo del bluetooth per collegare una board.")
            return False
        
        print("Mando stop alla board")
        
        self.measurement_loop.stop()
        asyncio.run(self.BLEclient.stop_board())
        
        return True
        
    def start_battery_level_notify(self):
        if self.BLEclient.is_connected:
            return False
        
        print("Mando la richiesta di ricezione delle notifiche sulla percentuale di batteria della board")
        
        # Crea un loop asincrono permanente
        self.battery_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.battery_loop)
        
        # Avvia il ciclo di eventi in un thread separato
        threading.Thread(target=self.battery_loop.run_forever, daemon=True).start()
        
        # Usa create_task per avviare start_battery_level_notify senza chiudere il loop
        self.battery_loop.create_task(self.BLEclient.start_battery_level_notify())
        
        return True
    
    def stop_battery_level_notify(self):
        if self.clientBLE is None:
            messagebox.showerror(title="Misurazione non terminata",
                                 message="Non hai effettuato la connessione con una board.\nClicca sul bottone con il simbolo del bluetooth per collegare una board.")
            return False
        
        print("Interrompo la ricezione della percentuale di batteria della board")
        
        self.battery_loop.stop()
        asyncio.run(self.BLEclient.stop_battery_level_notify())
    
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
