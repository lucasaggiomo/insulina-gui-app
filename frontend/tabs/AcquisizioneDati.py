# Progetto GUI misuratore d'insulina - A.A. 2024/2025 Corso di Laboratorio di Misure
# Autori:
# Saggiomo Luca
# Saccone Matteo
# Romano Davide
# Ponticelli Lorenzo
# Porcelli Nicola

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg   # Per integrare il grafico in Tkinter
import matplotlib.pyplot as plt   # Matplotlib per creare il grafico

from frontend.image_manager import ImageManager
from frontend.style_manager import StyleManager
        
# Definisco la classe AcquisizioneDati, che eredita da tk.Frame
class AcquisizioneDati(tk.Frame):
    # Costanti della classe
    # kHz
    MIN_FREQUENCY = 1
    MAX_FREQUENCY = 100
    
    # mV
    MIN_VOLTAGE = 10
    MAX_VOLTAGE = 500
    
    MIN_POINTS = 1
    MAX_POINTS = 1000

    MIN_CICLI = 1
    MAX_CICLI = 1000
    
    FREQUENZA_SINGOLA = False
    FREQUENZA_SWEEP = True
    
    # Costruttore che costruisce l'oggetto di tipo App
    def __init__(self, parent_frame): 
        super().__init__(parent_frame)
        
        self.create_widgets()
    
    def create_widgets(self):
        self.grid_propagate(False)

        # definisco le colonne
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)

        # definisco le righe
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)

        parameters_frame = self.create_parameters_frame()
        parameters_frame.grid(column=0, row=0, padx=5, pady=5, sticky="nsew") # creo il frame dei parametri

        self.value_table = self.create_tree_view()
        self.value_table.grid(column=1, row=0, rowspan=3, padx=10, pady=10, sticky="nsew")

        graph_frame = self.create_graph_frame()
        graph_frame.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")

        start_stop_frame = self.create_bottom_bar_frame()
        start_stop_frame.grid(column=0, row=2, padx=5, pady=5, sticky="nsew")
    
    def create_tree_view(self):
        column_names = ('index', 'modulo', 'fase');
        
        value_table = ttk.Treeview(self,
                                   columns=column_names,
                                   show='headings')
        value_table.grid_propagate(False)
        
        value_table.heading('index', text='Numero misura')
        value_table.heading('modulo', text='Modulo [Ohm]')
        value_table.heading('fase', text='Fase [°]')
        
        # Definisce la larghezza delle colonne
        value_table.column("index", width=150)
        value_table.column("modulo", width=150)
        value_table.column("fase", width=150)

        self.numero_misurazioni = 0
        
        return value_table
    
    def create_graph_frame(self):
        # Creo il frame dove inserire il grafico
        graph_frame = tk.Frame(self)
        
        # Configura la griglia del frame per espandersi
        graph_frame.grid_rowconfigure(0, weight=1)  # Fa sì che la riga del grafico si espanda
        graph_frame.grid_columnconfigure(0, weight=1)  # Fa sì che la colonna del grafico si espanda
        
        # graph_frame.pack_propagate(False)

        # Inizializzo la figura di Matplotlib
        self.fig, self.ax = plt.subplots(figsize=(4, 3))
        
        AcquisizioneDati.init_graph(self.ax)
        
        # Inizializza due array per gestire i valori delle ascisse e delle ordinate
        self.x_data = []
        self.y_data = []

# region GRAFICO FREQUENZA - TENSIONE
        # Imposta i titoli degli assi e del grafico
        # self.ax.set_title("Misurazione Frequenza e Tensione")
        # self.ax.set_xlabel("Frequenza (kHz)")
        # self.ax.set_ylabel("Tensione (mV)")
        
        # # Limiti predefiniti del grafico
        # self.ax.set_xlim(AcquisizioneDati.MIN_FREQUENCY, AcquisizioneDati.MAX_FREQUENCY)
        # self.ax.set_ylim(AcquisizioneDati.MIN_VOLTAGE, AcquisizioneDati.MAX_VOLTAGE)
#endregion

        # Aggiungi il grafico alla finestra Tkinter
        self.canvas = FigureCanvasTkAgg(master=graph_frame, figure=self.fig)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=4, pady=4)  # Usa grid per il posizionamento

        return graph_frame
        
    # Funzione per la creazione dei frame nella grid Parameters
    def create_parameters_frame(self):
        parameters_frame = tk.LabelFrame(self, text="Parameters") # creo un oggetto frame con etichetta Parameters
                
        parameters_frame.grid_propagate(True)
        
        parameters_frame.columnconfigure(0, weight=0)
        parameters_frame.columnconfigure(1, weight=1)
        parameters_frame.columnconfigure(2, weight=1)
        parameters_frame.columnconfigure(3, weight=1)
        parameters_frame.columnconfigure(4, weight=1)
        parameters_frame.columnconfigure(5, weight=1)
        parameters_frame.columnconfigure(6, weight=1)
        
        parameters_frame.rowconfigure(0, weight=1)
        parameters_frame.rowconfigure(1, weight=1)
        parameters_frame.rowconfigure(2, weight=1)
        
        # Bottoni per cambiare modalità (frequenza singola / frequenza sweep)
        self.toggle_frequency_mode_button = ttk.Button(parameters_frame,
                                                       text="Frequenza singola",
                                                       width=20,
                                                       padding=10,
                                                       style=StyleManager.MEDIUM_RED_BUTTON_STYLE_NAME,
                                                       command=self.toggle_frequency_mode_button_clicked)
        self.toggle_frequency_mode_button.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")
        self.current_frequency_mode = AcquisizioneDati.FREQUENZA_SINGOLA
        
        frequency_label = ttk.Label(parameters_frame,
                                    style=StyleManager.SMALL_BLUE_LABEL_STYLE_NAME,
                                    text=f"Frequency\n({AcquisizioneDati.MIN_FREQUENCY} kHz - {AcquisizioneDati.MAX_FREQUENCY} kHz)",
                                    anchor="w",
                                    padding=(10,0,10,20))
        frequency_label.grid(column=0, row=1, sticky="nesw")
       
        self.frequency_start_label = ttk.Label(parameters_frame,
                                          style=StyleManager.SMALL_BLUE_LABEL_STYLE_NAME,
                                          text="Start F",
                                          anchor="e", 
                                          width=10)
        self.frequency_start_label.grid(column=1, row=1, sticky="nesw")

        # Registra le funzioni di validazione per le entry dei parametri (uno per i double e uno per gli int)
        vcmd_double = (self.register(AcquisizioneDati.validate_double_number),  '%d', '%S', '%P')
        vcmd_int = (self.register(AcquisizioneDati.validate_int_number),  '%d', '%S', '%P')

        self.start_frequency = tk.DoubleVar()
        
        self.frequency_start_entry = ttk.Entry(parameters_frame,
                                            style=StyleManager.ENTRY_BLUE_STYLE_NAME,
                                            textvariable=self.start_frequency,
                                            font=StyleManager.small_font,
                                            width=15,
                                            validate="key",
                                            validatecommand=vcmd_double)
        self.frequency_start_entry.grid(column=2, row=1, sticky="w")

        self.frequency_stop_label = ttk.Label(parameters_frame,
                                         style=StyleManager.SMALL_BLUE_LABEL_STYLE_NAME,
                                         text="Stop F",
                                         anchor="e",
                                         width=10)

        self.stop_frequency = tk.DoubleVar()
        
        self.frequency_stop_entry = ttk.Entry(parameters_frame,
                                         style=StyleManager.ENTRY_BLUE_STYLE_NAME,
                                         font=StyleManager.small_font,
                                         textvariable=self.stop_frequency,
                                         width=15,
                                         validate="key",
                                         validatecommand=vcmd_double)

        self.frequency_points_label = ttk.Label(parameters_frame,
                                           style=StyleManager.SMALL_BLUE_LABEL_STYLE_NAME,
                                           text="Points",
                                           anchor="e",
                                           width=10)
        
        self.frequency_points = tk.IntVar()
        
        self.frequency_points_entry = ttk.Entry(parameters_frame,
                                           style=StyleManager.ENTRY_BLUE_STYLE_NAME,
                                           font=StyleManager.small_font,
                                           textvariable=self.frequency_points,
                                           width=15,
                                           validate="key",
                                           validatecommand=vcmd_int)
        
        voltage_label = ttk.Label(parameters_frame,
                                  style=StyleManager.SMALL_BLUE_LABEL_STYLE_NAME,
                                  text=f"Voltage\n({AcquisizioneDati.MIN_VOLTAGE} mV - {AcquisizioneDati.MAX_VOLTAGE} mV)",
                                  anchor="w",
                                  padding=(10,0,10,20))
        voltage_label.grid(column=0, row=2, sticky="nesw")
        
        self.numero_cicli_label = ttk.Label(parameters_frame,
                                           style=StyleManager.SMALL_BLUE_LABEL_STYLE_NAME,
                                           text="Numero\ncicli",
                                           anchor="e",
                                           width=10)
        
        self.numero_cicli = tk.IntVar()
        
        self.numero_cicli_entry = ttk.Entry(parameters_frame,
                                           style=StyleManager.ENTRY_BLUE_STYLE_NAME,
                                           font=StyleManager.small_font,
                                           textvariable=self.numero_cicli,
                                           width=15,
                                           validate="key",
                                           validatecommand=vcmd_int)
        
        self.voltage_value_label = ttk.Label(parameters_frame,
                                            style=StyleManager.SMALL_BLUE_LABEL_STYLE_NAME,
                                            text="Voltage",
                                            anchor="e", 
                                            width=10)
        self.voltage_value_label.grid(column=1, row=2, sticky="nesw")
        
        self.voltage_value = tk.DoubleVar() # voltage_value appartiene all'oggetto self
        
        voltage_value_entry = ttk.Entry(parameters_frame,
                                        style=StyleManager.ENTRY_BLUE_STYLE_NAME,
                                        font=StyleManager.small_font,
                                        textvariable=self.voltage_value,
                                        width=15,
                                        validate="key",
                                        validatecommand=vcmd_double)
        voltage_value_entry.grid(column=2, row=2, sticky="w")
        
        # inizializza le posizioni nella griglia di StopF e Points (solo quelli che sono modificati al cambio della modalità di frequenza)
        self.init_parameters_grid()
        
        # inizializza i valori
        self.reset_parameters()
        
        # inizializza la modalità di frequenza
        self.show_single_frequency()
        
        return parameters_frame
    
    @staticmethod
    def validate_double_number(action, char, new_value):
        # Se l'azione è di cancellazione, permetti (l'azione sarà "0")
        if action == "0":
            return True

        # Se il nuovo carattere inserito è un numero, permetti
        if char.isdigit():
            return len(new_value) <= 10 or char == ""

        # Se il carattere da inserire è un punto, lo inserisce solo se ce n'è solo uno
        if char == '.' and new_value.count('.') == 1:
            return True
        # Altrimenti rifiuta
        return False
    
    @staticmethod
    def validate_int_number(action, char, new_value):
        # Se l'azione è di cancellazione, permetti (l'azione sarà "0")
        if action == "0":
            return True
        # Se il nuovo carattere inserito è un numero, permetti
        if char.isdigit():
            return True
        
        # Altrimenti rifiuta
        return False
    
    # Crea la barra inferiore della schermata AcquisizioneDati, contenente:
    #   - la progress bar associata alla misurazione (FUNZIONE create_progress_bar_frame)
    #   - i bottoni di start, stop e cancellazione dati  (FUNZIONE create_start_stop_frame)
    def create_bottom_bar_frame(self):
        bottom_bar_frame = ttk.Frame(self, height=50)
        # bottom_bar_frame.pack_propagate(True)

        # bottoni per cabiare schermata nel tab_manager
        progress_bar_frame = self.create_progress_bar_frame(bottom_bar_frame)
        progress_bar_frame.pack(side="left", fill="both", pady=30, padx=20)        # allinea sulla sinistra

        self.progress_value.set(50)
        
        
        # creo una entry per simulare l'input dalla board
        lettura_label = ttk.Label(bottom_bar_frame,
                                    style=StyleManager.SMALL_BLUE_LABEL_STYLE_NAME,
                                    text="Lettura simulata\n(1 Ohm - 500 Ohm):",
                                    anchor="w",
                                    padding=(10,0,10,0))
        lettura_label.pack(side="left", fill="both", padx=0, pady=0)
        
        self.lettura_impedenza = tk.DoubleVar()
        self.lettura_impedenza_entry = ttk.Entry(bottom_bar_frame,
                                          style=StyleManager.ENTRY_BLUE_STYLE_NAME,
                                          textvariable=self.lettura_impedenza,
                                          font=StyleManager.small_font,
                                          width=5)
        self.lettura_impedenza_entry.pack(side="left", fill="both", padx=0, pady=20)
        
        self.lettura_impedenza.set(1)   # inizializzo a 1
        
        
        # bottoni di start, stop e cancellazione dati
        status_frame = self.create_start_stop_frame(bottom_bar_frame)
        status_frame.pack(side="right", fill="both")   # allinea sulla destra

        return bottom_bar_frame

    def create_progress_bar_frame(self, parent):
        self.progress_value = tk.DoubleVar()
        progress_bar_frame = ttk.Progressbar(parent,
                                             length=300,
                                             variable=self.progress_value)
        return progress_bar_frame

    # Funzione per la creazione dei frame start stop...
    # NOME DA CAMBIARE EVENTUALMENTE
    def create_start_stop_frame(self, parent):
        start_stop_frame = tk.Frame(parent, height=20)
        
        # start_stop_frame.grid_propagate(True)
        
        # Definisco la riga
        start_stop_frame.rowconfigure(0, weight=1)
        
        # Definisco le colonne
        start_stop_frame.columnconfigure(0, weight=0, uniform="buttons")
        start_stop_frame.columnconfigure(1, weight=0, uniform="buttons")
        start_stop_frame.columnconfigure(2, weight=0, uniform="buttons")
        
        # Bottone per iniziare la misurazione
        start_button = ttk.Button(start_stop_frame,
                                  style=StyleManager.MEDIUM_BLUE_BUTTON_STYLE_NAME,
                                  image=ImageManager.start_image,
                                  command=self.start_button_clicked)
        start_button.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")
        
        # Bottone per terminare la misurazione
        stop_button = ttk.Button(start_stop_frame,
                                 style=StyleManager.MEDIUM_BLUE_BUTTON_STYLE_NAME,
                                 image=ImageManager.stop_image,
                                 command=self.stop_button_clicked)
        stop_button.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")
        
        # Bottone per cancellare i dati delle misurazioni precedenti
        trash_button = ttk.Button(start_stop_frame,
                                  style=StyleManager.MEDIUM_BLUE_BUTTON_STYLE_NAME,
                                  image=ImageManager.trash_image,
                                  command=self.trash_button_clicked)
        trash_button.grid(column=2, row=0, padx=5, pady=5, sticky="nsew")
        
        return start_stop_frame
        
    # Metodo che, dato in ingresso una variabile tkinter numerica (IntVar o DoubleVar), restituisce il valore associato
    # Solleva un errore talora il valore non sia compreso nell'intervallo [min, max]
    @staticmethod
    def get_variable_value(variable, min, max):
        value = variable.get()
        
        if value < min or value > max:
            raise ValueError('Il valore è al di fuori del range accettabile')
        
        return value
        
    @staticmethod
    def init_graph(graph):
        graph.set_title("Grafico misurazioni", fontsize=20)  
        graph.set_xlabel("Numero misurazione", fontsize=15, labelpad=2)     
        graph.set_ylabel("Ohm", fontsize=15, labelpad=2)

        graph.grid(True)
        
        graph.set_xlim(1, 10)
        graph.set_ylim(0, 600)
        
    def add_graph_point(self, lettura):
        # Aggiungi la nuova misurazione alle liste
        self.x_data.append(self.numero_misurazioni)
        self.y_data.append(lettura)

        # Rimuovi il grafico precedente
        self.ax.clear()
        
        AcquisizioneDati.init_graph(self.ax)
        
        # Disegna i punti (self.x_data contiene le ascisse e self.y_data contiene le ordinate) e li unisce con linee
        self.ax.plot(self.x_data,
                     self.y_data,
                     marker='o', color='b', linestyle='-', label="Resistenza")

        # Estendi gli assi se necessario
        if self.numero_misurazioni > self.ax.get_xlim()[1]:
            self.ax.set_xlim(1, self.numero_misurazioni + 1)

        if max(self.y_data) > self.ax.get_ylim()[1]:
            self.ax.set_ylim(1, max(self.y_data) + 50)  # Aggiungi un piccolo margine

        # Ridisegna il grafico
        self.canvas.draw()

    def add_value_in_table(self, lettura):
        self.value_table.insert("", tk.END, values=(self.numero_misurazioni, lettura, 0))

    def cancel_data(self):
        print("Cancellazione dati...")
        
        # puliscp i dati nel grafico, mantenendo titolo e label
        self.ax.clear()  # Cancella il contenuto del grafico

        AcquisizioneDati.init_graph(self.ax)

        # ridisegno il grafico vuoto
        self.canvas.draw()

        # resetto le liste dei dati
        self.x_data = []
        self.y_data = []
        
        # cancello tutte le righe dalla Treeview
        for row in self.value_table.get_children():
            self.value_table.delete(row)
            
        # azzero il contatore delle misurazioni
        self.numero_misurazioni = 0
            
        self.reset_parameters()
        
    def reset_parameters(self):
        self.start_frequency.set(AcquisizioneDati.MIN_FREQUENCY)
        self.stop_frequency.set(AcquisizioneDati.MIN_FREQUENCY)
        self.frequency_points.set(AcquisizioneDati.MIN_POINTS)
        self.numero_cicli.set(AcquisizioneDati.MIN_CICLI)
        self.voltage_value.set(AcquisizioneDati.MIN_VOLTAGE)

    def stop_measurement(self):
        print("Interruzione della misurazione...")
        
        
    # COMANDI BOTTONI
    
    def start_button_clicked(self):
        try:
            # Leggiamo i valori degli oggetti entry, verificando che siano compresi nell'intervallo giusto
            # Eseguiamo questo blocco di codice in un try, in modo da gestire eventuali errori nel blocco except

            startF = AcquisizioneDati.get_variable_value(self.start_frequency,
                                                         AcquisizioneDati.MIN_FREQUENCY,
                                                         AcquisizioneDati.MAX_FREQUENCY)
            
            voltage = AcquisizioneDati.get_variable_value(self.voltage_value,
                                                          AcquisizioneDati.MIN_VOLTAGE,
                                                          AcquisizioneDati.MAX_VOLTAGE)
            
            if self.current_frequency_mode == AcquisizioneDati.FREQUENZA_SINGOLA:
                # Legge solo la frequenza e il voltaggio se è in modalità singola
                print(f"La frequenza è: {startF} kHz")
                print(f"L'ampiezza del segnale di stimolazione è: {voltage} mV")
            else:
                # Legge stopF, freqPoints e numeroCicli SOLO se è in modalità sweep
                stopF = AcquisizioneDati.get_variable_value(self.stop_frequency,
                                                            startF,
                                                            AcquisizioneDati.MAX_FREQUENCY)
                
                freqPoints = AcquisizioneDati.get_variable_value(self.frequency_points,
                                                                AcquisizioneDati.MIN_POINTS,
                                                                AcquisizioneDati.MAX_POINTS)
                
                numeroCicli = AcquisizioneDati.get_variable_value(self.numero_cicli,
                                                                AcquisizioneDati.MIN_CICLI,
                                                                AcquisizioneDati.MAX_CICLI)
            
                print(f"La frequenza iniziale è: {startF} kHz")
                print(f"La frequenza finale è: {stopF} kHz")
                print(f"Il numero di punti delle frequenze è: {freqPoints}")
                print(f"Il numero di cicli è: {numeroCicli}")
                print(f"L'ampiezza del segnale di stimolazione è: {voltage} mV")
        
        
            print("La misurazione è iniziata")
            
            # Legge la misurazione (simulata) dalla entry
            lettura = AcquisizioneDati.get_variable_value(self.lettura_impedenza,
                                                          1,
                                                          500)
            self.numero_misurazioni += 1            # incremento il numero di misurazioni
            
            # Aggiorna il grafico, aggiungendo il nuovo punto
            self.add_graph_point(lettura)
            
            # Aggiorna la tabella, aggiungendo la nuova misurazione
            self.add_value_in_table(lettura)
        
        except (ValueError, tk.TclError):
            # Cattura dell'eccezione per input non validi
            # Gestione dell'errore mostrando una finestra di dialogo con un messaggio di errore
            
            messagebox.showerror("Errore", "Controlla i parametri inseriti!")
            print("La misurazione è stata interrotta per errori")
            
    def stop_button_clicked(self):
        has_to_stop = messagebox.askyesno(title="Interruzione misurazione",
                                          message="Sei sicuro di voler interrompere la misurazione?")
        if(has_to_stop):
            self.stop_measurement()
            print("La misurazione è stata interrotta")
        else:
            print("L'interruzione è stata annullata")
    
    def trash_button_clicked(self):
        has_to_cancel = messagebox.askyesno(title="Cancellazione dati",
                                            message="Sei sicuro di voler cancellare i dati?")
        if(has_to_cancel):
            self.cancel_data()
            print("Le misurazioni sono state cancellate")
        else:
            print("La cancellazione è stata annullata")
    
    def toggle_frequency_mode_button_clicked(self):        
        # Se la modalità corrente è a singola frequenza, passa a quella sweep e viceversa
        if self.current_frequency_mode == AcquisizioneDati.FREQUENZA_SINGOLA:
            self.show_sweep_frequency()
        else:
            self.show_single_frequency()
        
        
    def show_single_frequency(self):
        print("Attivata modalità a singola frequenza")
        
        self.current_frequency_mode = AcquisizioneDati.FREQUENZA_SINGOLA
        self.toggle_frequency_mode_button.configure(text = "Frequenza singola")
        
        # Nasconde gli elementi non relativi alla modalità a singola frequenza
        self.frequency_stop_label.grid_forget()
        self.frequency_stop_entry.grid_forget()
        self.frequency_points_label.grid_forget()
        self.frequency_points_entry.grid_forget()
        self.numero_cicli_label.grid_forget()
        self.numero_cicli_entry.grid_forget()
        
        # Elimina il nome di StartF
        self.frequency_start_label.configure(text = "Frequency")
        
    def show_sweep_frequency(self):
        print("Attivata modalità a frequenza sweep")
        
        self.current_frequency_mode = AcquisizioneDati.FREQUENZA_SWEEP
        self.toggle_frequency_mode_button.configure(text = "Frequenza sweep")
        
        # Ripristina gli elementi relativi alla frequenza sweep
        self.init_parameters_grid()
        
        # Ripristina la scritta "Start F"
        self.frequency_start_label.configure(text = "StartF")
        
    def init_parameters_grid(self):
        self.frequency_stop_label.grid(column=3, row=1, sticky="nesw")
        self.frequency_stop_entry.grid(column=4, row=1, sticky="w")
        
        self.frequency_points_label.grid(column=5, row=1, sticky="nesw")
        self.frequency_points_entry.grid(column=6, row=1, sticky="w")

        self.numero_cicli_label.grid(column=5, row=2, sticky="nesw")
        self.numero_cicli_entry.grid(column=6, row=2, sticky="w")
        