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
from backend import bluetooth
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
    
        self.clientBLE = None
                
        # Chiamo la funzione create_widgets - dichiarata successivamente
        self.create_widgets()

    def on_closing(self):
        plt.close('all')  # Chiude tutte le figure matplotlib aperte
        
        # self.stop_board(write_message = False)
        
        # if self.clientBLE:
        #     threading.Thread(asyncio.run(self.clientBLE.disconnect())).start()
        
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
        
        # inizializzo le funzioni riguardanti le notifiche
        bluetooth.new_measurement_callback = lambda lettura: self.dati_tab.handle_new_measurement(lettura)
        bluetooth.update_battery_level_callback = lambda lettura: self.update_battery_percentage(lettura)

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
    def scanning_devices(self):
        target_name = ""
        target_address = ""
    
        # svuoto la lista
        self.devices = []
        self.reset_bluetooth_treeview()
        
        # attivo la scansione dei dispositivi
        scan_thread = threading.Thread(target=bluetooth.run_scan_thread,
                                       args=(target_name, target_address, self.devices, self.status_text))
        scan_thread.start()
        scan_thread.join()
        
        # aggiorno la lista
        self.aggiorna_bluetooth_treeview()
        # nomi_dispositivi = [f'{device['name']}: {device['address']}' for device in self.devices]
        # self.devices_list_variable.set(nomi_dispositivi)
    
    def connecting_to_device(self, device_name, device_address):
        # crea un thread che invoca la funzione "bluetooth.run_connection_thread(device_name, device_address, self.connection_status_text))"
        # e poi assegna il risultato di questa funzione all'attributo self.clientBLE
        connection_thread = threading.Thread(target=lambda:
                                setattr(self, 'clientBLE',
                                        bluetooth.run_connection_thread(device_name, device_address, self.connection_status_text)))
        
        connection_thread.start()
        connection_thread.join()
        
        self.start_battery_level_notify()        
    
    def reset_bluetooth_treeview(self):
        # Rimuove tutti gli elementi esistenti dalla Treeview
        for item in self.devices_tree.get_children():
            self.devices_tree.delete(item)
            
    def aggiorna_bluetooth_treeview(self):
        # resetta la treeview
        self.reset_bluetooth_treeview()

        # Inserisce i nuovi dati dalla lista self.devices
        for device in self.devices:
            self.devices_tree.insert("", tk.END, values=(device["name"], device["address"]))
            
    def on_bluetooth_window_closing(self, bluetooth_window):
        self.is_bluetooth_window_open = False
        bluetooth_window.destroy()
    
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

        self.status_text = tk.StringVar(value="Clicca il tasto Ricerca per cercare la tua board")
        status_label = ttk.Label(bluetooth_window,
                                 textvariable=self.status_text,
                                 justify=tk.CENTER,
                                 style=StyleManager.SMALL_BLUE_LABEL_STYLE_NAME)
        status_label.pack(side=tk.TOP)
        
        self.devices = []
        
        # Creo una Treeview con due colonne
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
                
        scan_button = ttk.Button(bluetooth_window,
                                 text="Connetti",
                                 style=StyleManager.MEDIUM_BLUE_BUTTON_STYLE_NAME,
                                 command=self.connect_device_click)
        scan_button.pack(side=tk.TOP, pady=10)
        
        self.connection_status_text = tk.StringVar(value="Seleziona un dispositivo e clicca\n\"Connetti\" per instaurare la connessione")
        connection_status_label = ttk.Label(bluetooth_window,
                                            textvariable=self.connection_status_text,
                                            justify=tk.CENTER,
                                            style=StyleManager.SMALL_BLUE_LABEL_STYLE_NAME)
        connection_status_label.pack(side=tk.TOP, pady=(0, 10))
            
    def scan_button_click(self):
        # ricerca i dispositivi in maniera concorrente
        scanner = threading.Thread(target=self.scanning_devices)
        scanner.start()
        
    def connect_device_click(self):
        selected_item = self.devices_tree.selection()
        if not selected_item:
            self.connection_status_text.set("Nessun dispositivo selezionato\nSeleziona un dispositivo e clicca\n\"Connetti\" per instaurare la connessione")
            return

        # Ottieni l'indirizzo del dispositivo selezionato
        device_info = self.devices_tree.item(selected_item, "values")
        device_name = device_info[0]     # Il nome è nella prima colonna
        device_address = device_info[1]  # L'indirizzo è nella seconda colonna
        
        connection = threading.Thread(target=self.connecting_to_device,
                                      args=(device_name, device_address))
        connection.start()
        
        print(f"Dispositivo selezionato:\nnome: {device_name}, indirizzo MAC: {device_address}")

    def start_board(self):
        if self.clientBLE is None:
            messagebox.showerror(title="Misurazione non iniziata",
                                 message="Non hai effettuato la connessione con una board.\nClicca sul bottone con il simbolo del bluetooth per collegare una board.")
            return False
        
        print("Mando start alla board")
        
        # Crea un loop asincrono permanente
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        # Avvia il ciclo di eventi in un thread separato
        threading.Thread(target=self.loop.run_forever, daemon=True).start()
        
        # Usa create_task per avviare start_board senza chiudere il loop
        self.loop.create_task(bluetooth.start_board(self.clientBLE))
        
        return True
        
    def stop_board(self, write_message = True):
        if self.clientBLE is None:
            if write_message:
                messagebox.showerror(title="Misurazione non terminata",
                                    message="Non hai effettuato la connessione con una board.\nClicca sul bottone con il simbolo del bluetooth per collegare una board.")
            return False
        
        if write_message:
            print("Mando stop alla board")
        
        
        self.loop.stop()
        asyncio.run(bluetooth.stop_board(self.clientBLE))
        
        return True
        
    def start_battery_level_notify(self):
        if self.clientBLE is None:
            # messagebox.showerror(title="Misurazione non iniziata",
            #                     message="Non hai effettuato la connessione con una board.\nClicca sul bottone con il simbolo del bluetooth per collegare una board.")
            return False
        
        print("Mando la richiesta di ricezione delle notifiche sulla percentuale di batteria della board")
        
        # Crea un loop asincrono permanente
        self.battery_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.battery_loop)
        
        # Avvia il ciclo di eventi in un thread separato
        threading.Thread(target=self.battery_loop.run_forever, daemon=True).start()
        
        # Usa create_task per avviare start_battery_level_notify senza chiudere il loop
        self.battery_loop.create_task(bluetooth.start_battery_level_notify(self.clientBLE))
        
        return True
    
    def stop_battery_level_notify(self):
        if self.clientBLE is None:
            messagebox.showerror(title="Misurazione non terminata",
                                    message="Non hai effettuato la connessione con una board.\nClicca sul bottone con il simbolo del bluetooth per collegare una board.")
            return False
        
        print("Interrompo la ricezione della percentuale di batteria della board")
        
        self.battery_loop.stop()
        asyncio.run(bluetooth.stop_battery_level_notify(self.clientBLE))
    
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
