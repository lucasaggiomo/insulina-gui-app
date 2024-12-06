# Progetto GUI misuratore d'insulina - A.A. 2024/2025 Corso di Laboratorio di Misure
# Autori:
# Saggiomo Luca
# Saccone Matteo
# Romano Davide
# Ponticelli Lorenzo
# Porcelli Nicola

# importa tkinter e matplotlib
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# matplotlib per creare il grafico
import matplotlib.pyplot as plt

# importa altri moduli dal frontend
from frontend.tabs import *
from frontend.image_manager import ImageManager  # importo la classe ImageManager dal modulo image_manager.py per la gestione delle immagini
from frontend.style_manager import StyleManager  # importo la classe StyleManager dal modulo style_manager.py per la gestione degli stili

# importa il bluetooth dal backend
from backend.bluetooth import BLEClient

# definisce la classe App, che eredita da tk.Frame
class App(tk.Tk):

    # costruttore che costruisce l'oggetto di tipo App
    def __init__(self): 
        super().__init__()
                
        # imposta il protocollo per la chiusura della finestra
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # ottiene la risoluzione dello schermo
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        
        # imposta la finestra al 80% della larghezza e al 80% dell'altezza dello schermo
        window_width = int(self.screen_width * 0.8)
        window_height = int(self.screen_height * 0.8)
        
        # calcola le posizioni x e y della finestra
        x = int((self.screen_width - window_width) / 2)
        y = int((self.screen_height - window_height) / 2)

        # imposta la geometria della finestra (dimensioni e posizione) e imposta titolo e dimensione minima
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.minsize(width=1200, height=700)
        self.title("Fondamenti di Misure")

        # carica tutte le immagini dell'applicazione con la classe ImageManager
        ImageManager.load_images()

        # carica tutti gli stili dell'applicazione con la classe StyleManager
        StyleManager.load_styles()
    
        # crea tutti i widget che compongono la finestra
        self.create_widgets()

    # procedura eseguita alla chiusura della finestra
    def on_closing(self):
        # verifica se sta effettuando una misurazione
        if self.dati_tab.is_measuring:
            messagebox.showwarning(
                title="Misurazione in corso",
                message="Attenzione! Una misurazione è in corso!\nAttendi la sua terminazione oppure interrompila prima di chiudere l'applicazione"
            )
            return
        
        # chiude tutte le figure matplotlib aperte
        plt.close('all')
        
        # se connesso si disconnette dalla board
        if self.BLEclient:
            self.BLEclient.run_async_task(
                self.BLEclient.disconnect_sequence()
            )
            
        # chiude la finestra tkinter
        self.destroy()

    # funzione per creare tutti i widgets della finestra
    def create_widgets(self):
        # frame della barra superiore del programma (bottoni per cambiare la schermata e informazioni sulla board)
        top_bar_frame = self.create_top_bar_frame()
        top_bar_frame.pack(side="top", fill="x")

        # frame contenente il tab corrente (AcquisizioneDati, StatoMacchina o EsportazioneDati)
        tab_manager = self.create_tab_manager_frame()
        tab_manager.pack(side="bottom", fill="both", expand=True)

    # crea la barra superiore del programma, contenente:
    #   - i bottoni per cambiare schermata nel tab_manager (FUNZIONE create_switch_tab_buttons)
    #   - informazioni sullo stato della board (bluetooth + batteria) (FUNZIONE create_board_status_frame)
    def create_top_bar_frame(self):
        top_bar_frame = ttk.Frame(self, height=50)

        # bottoni per cabiare schermata nel tab_manager
        tab_buttons_frame = self.create_switch_tab_buttons(top_bar_frame)
        tab_buttons_frame.pack(side="left", fill="both")        # allinea sulla sinistra
        
        # frame bluetooth + batteria (stato della board) 
        status_frame = self.create_board_status_frame(top_bar_frame)
        status_frame.pack(side="right", fill="both")            # allinea sulla destra

        return top_bar_frame

    # crea i bottoni per cambiare schermata nel tab_manager
    def create_switch_tab_buttons(self, parent):
        switch_tab_buttons = ttk.Frame(parent)

        switch_tab_buttons.grid_propagate(True)

        # definisce la riga della topbar
        switch_tab_buttons.rowconfigure(0, weight=1)

        # definisce le colonne della topbar        
        switch_tab_buttons.columnconfigure(0, weight=0)
        switch_tab_buttons.columnconfigure(1, weight=0)
        switch_tab_buttons.columnconfigure(2, weight=0)

        # bottone per mostrare il tab Acquisizione Dati
        self.show_dati_button = ttk.Button(
            switch_tab_buttons,
            text="Acquisizione dati",
            width=20,
            padding=10,
            style=StyleManager.BIG_BLUE_BUTTON_STYLE_NAME,
            command=self.show_dati_button_clicked
        )
        self.show_dati_button.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

        # bottone per mostrare il tab Stato Macchina
        self.show_macchina_button = ttk.Button(
            switch_tab_buttons,
            text="Stato macchina",
            width=20,
            padding=10,
            style=StyleManager.BIG_BLUE_BUTTON_STYLE_NAME,
            command=self.show_macchina_button_clicked
        )
        self.show_macchina_button.grid(column=1, row=0, padx=5, pady=5, sticky="nswe")
        
        # bottone per mostrare il tab Esportazione Dati
        self.show_esporta_button = ttk.Button(
            switch_tab_buttons,
            text="Esporta dati",
            width=20,
            padding=10,
            style=StyleManager.BIG_BLUE_BUTTON_STYLE_NAME,
            command=self.show_esporta_button_clicked
        )
        self.show_esporta_button.grid(column=2, row=0, padx=5, pady=5, sticky="nswe")

        return switch_tab_buttons
    
    # crreazione del Frame bluetooth + batteria (stato della board)
    def create_board_status_frame(self, parent):
        status_frame = ttk.Frame(parent)
        
        status_frame.grid_propagate(True)
        
        # definisce la riga
        status_frame.rowconfigure(0, weight=1)
        
        # definisce le colonne
        status_frame.columnconfigure(0, weight=0)
        status_frame.columnconfigure(1, weight=0)
        
        # variabile che indica se la finestra di bluetooth è aperta
        # permette di prevenire l'apertura multipla di più finestre bluetooth
        self.is_bluetooth_window_open = False
        bluetooth_button = ttk.Button(
            status_frame,
            width=10,
            image=ImageManager.bluetooth_image,
            compound="right",
            command=self.bluetooth_button_clicked
        )
        bluetooth_button.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")
        
        # gestione batteria
        self.battery_percentage_string = tk.StringVar()
        self.battery_percentage_value = 100.0
        self.battery_label = ttk.Label(
            status_frame,
            style=StyleManager.MEDIUM_BLUE_LABEL_STYLE_NAME,
            compound="left",
            textvariable=self.battery_percentage_string
        )
        self.battery_label.grid(column=2, row=0, padx=5, pady=5, sticky="nsew")
        
        # imposta inizialmente a 100 %
        self.update_battery_percentage(100.0)
        
        return status_frame
            
    # crea il frame che contiene i tre tabs (AcquisizioneDati, StatoMacchina e EsportazioneDati)
    def create_tab_manager_frame(self):
        tab_manager = tk.Frame(self)

        tab_manager.grid_propagate(False)
        
        # definisce la riga dello status bar
        tab_manager.rowconfigure(0, weight=1)

        # definisce la colonna dello status bar
        tab_manager.columnconfigure(0, weight=1)

        self.dati_tab = AcquisizioneDati(
            tab_manager,
            self.start_measurement_single_frequency,
            self.start_measurement_sweep_frequency,
            self.stop_measurement
        )
        self.dati_tab.grid(row=0,column=0, sticky="nsew")
        
        # crea un oggetto BLEclient, assegnando i callback per gestire la ricezione di una nuova misura e del livello di batteria
        self.BLEclient = BLEClient(
            new_measurement_callback = self.dati_tab.handle_new_measurement,
            update_battery_level_callback = self.update_battery_percentage
        )
        self.BLEclient.start_event_loop()

        self.macchina_tab = StatoMacchina(tab_manager)
        self.macchina_tab.grid(row=0,column=0, sticky="nsew")
        
        self.esporta_tab = EsportazioneDati(tab_manager)
        self.esporta_tab.grid(row=0,column=0, sticky="nsew")

        # imposta Acquisizione Dati come schermata iniziale (simulando la pressione del bottone)
        self.show_dati_button_clicked()
        
        return tab_manager

    # aggiorna la percentuale di batteria
    def update_battery_percentage(self, new_percentage):
        self.battery_percentage_value = new_percentage
        self.battery_percentage_string.set(f"{new_percentage} %")
        
        # aggiorna l'immagine in base alla percentuale
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
        
        # crea una nuova finestra
        bluetooth_window = tk.Toplevel(self)
        bluetooth_window.title("Ricerca bluetooth")
        
        # imposta dimensioni e posizione (al centro) della finestra
        bluetooth_window_width = 700
        bluetooth_window_height = 700
        x = int((self.screen_width - bluetooth_window_width) / 2)
        y = int((self.screen_height - bluetooth_window_height) / 2)
        
        bluetooth_window.geometry(f"{bluetooth_window_width}x{bluetooth_window_height}+{x}+{y}")
        bluetooth_window.minsize(width=400, height=400)
        
        # imposta che alla chiusura della finestra la variabile is_bluetooth_window_open viene impostata a False
        bluetooth_window.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.on_bluetooth_window_closing(bluetooth_window)
        )

        # aggiunge un pulsante per scansionare i dispositivi
        self.scan_button = ttk.Button(
            bluetooth_window,
            text="Ricerca",
            style=StyleManager.MEDIUM_BLUE_BUTTON_STYLE_NAME,
            command=self.scan_button_click
        )
        self.scan_button.pack(side=tk.TOP, pady=(50,10))

        self.scan_status_var = tk.StringVar(
            value="Clicca il tasto \"Ricerca\" per effettuare una scansione\ndei dispositivi BLE nelle vicinanze"
        )
        status_label = ttk.Label(
            bluetooth_window,
            textvariable=self.scan_status_var,
            justify=tk.CENTER,
            style=StyleManager.SMALL_BLUE_LABEL_STYLE_NAME
        )
        status_label.pack(side=tk.TOP, pady=(0, 10))
        
        self.connected_device_var = tk.StringVar()
        self.connected_device_label = ttk.Label(
            bluetooth_window,
            textvariable=self.connected_device_var,
            justify=tk.CENTER,
            style=StyleManager.SMALL_BLUE_LABEL_STYLE_NAME
        )
        self.connected_device_label.pack(side=tk.TOP, pady=(0,10))

        if self.BLEclient.is_connected:
            self.connected_device_var.set(f"Sei connesso al dispositivo: {self.BLEclient.connected_device_name}, {self.BLEclient.connected_device_address}")
        else:
            self.connected_device_var.set(f"Non sei connesso ad alcun dispositivo")
            
        # definisce il frame della tabella, contenente:
        # - la tabella nella riga 0 e colonna 0
        # - la barra di scorrimento nella riga 0 e colonna 1
        devices_list_frame = self.create_devices_list_frame(bluetooth_window)

        # posiziona il frame della tabella nella finestra
        devices_list_frame.pack(expand=True, fill=tk.BOTH, padx=20)
        
        # definisce il bottone per la connessione
        self.connect_button = ttk.Button(
            bluetooth_window,
            text="Connetti",
            style=StyleManager.MEDIUM_BLUE_BUTTON_STYLE_NAME,
            command=self.connect_to_device_click
        )
        self.connect_button.pack(side=tk.TOP, pady=10)
        
        # imposta la variabile di stato dell'oggetto BLEclient
        self.BLEclient.status_var = self.scan_status_var
        
    # crea il frame contenente la tabella dei dispositivi trovati
    def create_devices_list_frame(self, parent):
        devices_list_frame = tk.Frame(parent)
        devices_list_frame.grid_propagate(False)
        
        # riga
        devices_list_frame.rowconfigure(0, weight=1)

        # colonne
        devices_list_frame.columnconfigure(0, weight=1)
        devices_list_frame.columnconfigure(1, weight=0)
        
        # crea una tabella con due colonne
        self.devices_tree = ttk.Treeview(
            devices_list_frame,
            columns=("name", "address"),
            show="headings"
        )
        self.devices_tree.grid_configure(row=0, column=0, sticky="nwes")
        
        # imposta le intestazioni delle colonne
        self.devices_tree.heading("name", text="Nome Dispositivo", anchor=tk.W)
        self.devices_tree.heading("address", text="Indirizzo", anchor=tk.W)

        # definisce larghezza delle colonne
        self.devices_tree.column("name", anchor=tk.W, width=100)
        self.devices_tree.column("address", anchor=tk.W)
        
        # definisce la scrollbar verticale
        vertical_scrollbar = ttk.Scrollbar(
            devices_list_frame,
            orient="vertical",
            command=self.devices_tree.yview
        )
        vertical_scrollbar.grid_configure(row=0, column=1, sticky="wns")

        self.devices_tree.configure(yscrollcommand=vertical_scrollbar.set)

        # aggiorna la tabella in base ai dispositivi trovati
        # (la prima volta sarà vuota, ma permette di mostrare di nuovo i
        # dispositivi trovati in precedenza se la finestra viene chiusa e riaperta)
        self.aggiorna_bluetooth_treeview()
        
        return devices_list_frame

    # funzione eseguita alla chiusura della finestra di bluetooth
    def on_bluetooth_window_closing(self, bluetooth_window):
        self.is_bluetooth_window_open = False
        bluetooth_window.destroy()
    
    # rimuove tutti gli elementi esistenti nella tabella dei dispositivi bluetooth
    def reset_bluetooth_treeview(self):
        for item in self.devices_tree.get_children():
            self.devices_tree.delete(item)
            
    # aggiorna la tabella dei dispositivi bluetooth
    def aggiorna_bluetooth_treeview(self):
        # resetta la treeview
        self.reset_bluetooth_treeview()

        # inserisce i nuovi dati dalla lista self.devices
        for device in self.BLEclient.devices_found:
            # ignora i dispositivi senza nome
            if not device.name:
                continue

            # inserisce il dispositivo nella tabella     
            self.devices_tree.insert("", tk.END, values=(device.name, device.address))
        
    # avvia la scansione dei dispositivi BLE nelle vicinanze
    # ed aggiorna la tabella (con on_scan_complete)
    def scan_button_click(self):
        # esce se è stato già premuto il tasto di scansione
        if self.is_scanning:
            return
        
        # imposta che sta effettuando la scansione,
        # disabilita il bottone per scansionare (per impedire scansioni multiple)
        # e disabilita il bottone per connettersi
        self.is_scanning = True
        self.scan_button.config(state=tk.DISABLED)
        self.connect_button.config(state=tk.DISABLED)
        
        # resetta la tabella dei dispositivi trovati in precedenza
        self.reset_bluetooth_treeview()
        
        # effettua la scansione in maniera asincrona (quindi non bloccante per il programma)
        self.BLEclient.run_async_task(
            self.BLEclient.start_scan(
                on_scan_complete = self.on_scan_complete,
                on_error = self.reset_flags
            )
        )
        
    # funzione eseguita al termine della scansione:
    # - aggiorna la tabella dei dispositivi trovati
    # - abilita nuovamente il bottone per scansionare e imposta la variabile is_scanning a False
    # - abilita il bottone per connettere
    def on_scan_complete(self):
        self.aggiorna_bluetooth_treeview()
        self.reset_flags()
    
    # connette il dispositivo selezionato
    def connect_to_device_click(self):
        # esce se sta già connettendo o se sta scansionando
        if self.is_scanning or self.is_connecting:
            return
        
        # preleva l'elemento selezionato dalla tabella
        selected_item = self.devices_tree.selection()
        if not selected_item:
            self.scan_status_var.set("Non hai selezionato un dispositivo.\nSeleziona un dispositivo e clicca \"Connetti\" per connetterti")
            return

        # ottiene il nome e l'indirizzo del dispositivo selezionato
        device_info = self.devices_tree.item(selected_item, "values")
        device_name = device_info[0]     # Il nome è nella prima colonna
        device_address = device_info[1]  # L'indirizzo è nella seconda colonna
        
        print(f"Dispositivo selezionato:\nnome: {device_name}, indirizzo MAC: {device_address}")
        
        # controlla se non ci si è già connessi allo stesso dispositivo
        if device_address == self.BLEclient.connected_device_address:
            messagebox.showinfo(
                title="Avviso",
                message=f"Sei già connesso al dispositivo {device_name}, {device_address}"
            )
            return
        
        # imposta che sta effettuando la connesione e disabilita il bottone per connettere (per impedire connessioni multiple)
        self.is_connecting = True
        self.scan_button.config(state=tk.DISABLED)
        self.connect_button.config(state=tk.DISABLED)
        
        # Avvia la connessione in modo asincrono
        self.BLEclient.run_async_task(
            self.BLEclient.connect_to_device(
                device_name,
                device_address,
                on_success = self.on_connect_success,
                on_error = self.reset_flags,
                on_disconnect = self.on_device_disconnected
            )
        )
    
    # riabilita i bottoni per la scansione e connessione e imposta a False le relative flags
    def reset_flags(self):
        self.is_scanning = False
        self.is_connecting = False
        self.scan_button.config(state=tk.NORMAL)
        self.connect_button.config(state=tk.NORMAL)
        
    # funzione eseguita al termine della connessione:
    # - abilita nuovamente il bottone per scansionare e imposta la variabile is_connecting a False
    # - invia la richiesta di notifiche per il livello della batteria alla board
    # - imposta la variabile di stato sulla connessione
    def on_connect_success(self):
        self.reset_flags()
        # self.connect_button.config(state=tk.DISABLED)
        self.start_battery_level_notify()
        self.connected_device_var.set(f"Sei connesso al dispositivo: {self.BLEclient.connected_device_name}, {self.BLEclient.connected_device_address}")

    # funzione eseguita quando il device precedentemente connesso si disconnette
    def on_device_disconnected(self):
        # interrompe la misurazione qualora fosse in esecuzione
        if self.dati_tab.is_measuring:
            messagebox.showerror(
                title="Disconnessione imprevista",
                message = "Attenzione! Il dispositivo si è connesso e la misurazione è stata interrotta bruscamente!"
            )
            self.dati_tab.is_measuring = False
            
        self.connected_device_var.set(f"Non sei connesso ad alcun dispositivo")
        print("Il dispositivo si è disconnesso")

    # FUNZIONI RIGUARDANTI LA MISURAZIONE
    
    # inizia misurazione a frequenza singola
    # restituisce True se il comando è stato inviato, False altrimenti
    def start_measurement_single_frequency(self, voltage, frequency):
        # verifica la connessione con il client
        if not self.BLEclient.is_connected:
            messagebox.showerror(
                title="Misurazione non iniziata",
                message="Non hai effettuato la connessione con una board.\nClicca sul bottone con il simbolo del bluetooth per collegare una board."
            )
            return False
        
        print("Mando alla board il comando di inizio misurazione a singola frequenza, con i parametri inseriti")
        
        # manda un comando di start a singola frequenza alla board
        self.BLEclient.run_async_task(
            self.BLEclient.start_measurement_single_frequency(voltage, frequency)
        )
        
        return True
        
    # inizia misurazione a frequenza sweep
    # restituisce True se il comando è stato inviato, False altrimenti
    def start_measurement_sweep_frequency(self, voltage, startF, stopF, freqPoints, numeroCicli):
        # verifica la connessione con il client
        if self.BLEclient is None or not self.BLEclient.is_connected:
            messagebox.showerror(
                title="Misurazione non iniziata",
                message="Non hai effettuato la connessione con una board.\nClicca sul bottone con il simbolo del bluetooth per collegare una board."
            )
            return False
        
        print("Mando alla board il comando di inizio misurazione a frequenza sweep, con i parametri inseriti")
        
        # manda un comando di start a frequenza sweep alla board
        self.BLEclient.run_async_task(
            self.BLEclient.start_measurement_sweep_frequency(voltage, startF, stopF, freqPoints, numeroCicli)
        )
        
        return True
        
    # inizia misurazione a frequenza sweep
    # restituisce True se il comando è stato inviato, False altrimenti
    def stop_measurement(self):
        # verifica la connessione con il client
        if self.BLEclient is None or not self.BLEclient.is_connected:
            messagebox.showerror(title="Misurazione non terminata",
                                 message="Non hai effettuato la connessione con una board.\nClicca sul bottone con il simbolo del bluetooth per collegare una board.")
            return False
        
        print("Mando stop alla board")
        
        # manda un comando di start alla board
        self.BLEclient.run_async_task(
            self.BLEclient.stop_measurement()
        )
        
        return True
        
    # abilita la ricezione delle notifiche per il livello di batteria
    # restituisce True se il comando è stato inviato, False altrimenti
    def start_battery_level_notify(self):
        # verifica la connessione con il client
        if self.BLEclient is None or not self.BLEclient.is_connected:
            return False
        
        print("Mando la richiesta di ricezione delle notifiche sulla percentuale di batteria della board")
        
        self.BLEclient.run_async_task(
            self.BLEclient.start_battery_level_notify()
        )
        
        return True
    
    # disabilita la ricezione delle notifiche per il livello di batteria
    # restituisce True se il comando è stato inviato, False altrimenti
    def stop_battery_level_notify(self):
        # verifica la connessione con il client
        if self.BLEclient is None:
            messagebox.showerror(title="Misurazione non terminata",
                                 message="Non hai effettuato la connessione con una board.\nClicca sul bottone con il simbolo del bluetooth per collegare una board.")
            return False
        
        print("Interrompo la ricezione della percentuale di batteria della board")
        
        self.BLEclient.run_async_task(
            self.BLEclient.stop_battery_level_notify()
        )
    
    # EVENTI BOTTONI DEI TAB (Acquisizione Dati, Stato Macchina ed Esportazione Macchina)
    # tutte queste funzioni mettono in primo piano il tab corrispondente e aggiornano i colori dei bottoni
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
    # costruttore di App
    app = App()
    
    # invocazione del mainloop di Tkinter
    app.mainloop()