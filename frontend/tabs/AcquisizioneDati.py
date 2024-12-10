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

# per integrare il grafico in Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from frontend.image_manager import ImageManager
from frontend.style_manager import StyleManager
        
# definisce la classe AcquisizioneDati, che eredita da tk.Frame
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
    
    # costruttore che costruisce l'oggetto di tipo App
    def __init__(self, parent_frame, start_measurement_single_frequency, start_measurement_sweep_frequency, stop_measurement):
        super().__init__(parent_frame)
        
        # inizializza le funzioni da invocare per mandare i comandi al client (gestiti nella classe App)
        self.start_measurement_single_frequency = start_measurement_single_frequency
        self.start_measurement_sweep_frequency = start_measurement_sweep_frequency
        self.stop_board = stop_measurement
        
        self.is_measuring = False
        
        # crea i widget del tab AcquisizioneDati
        self.create_widgets()
    
    def create_widgets(self):
        self.grid_propagate(False)

        # colonne
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)

        # righe
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)

        # frame dell'inserimento dei parametri (voltaggio, frequenza, ...)
        parameters_frame = self.create_parameters_frame()
        parameters_frame.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

        # frame della tabella delle misurazioni
        self.value_table = self.create_tree_view()
        self.value_table.grid(column=1, row=0, rowspan=3, padx=10, pady=10, sticky="nsew")

        # frame del grafico 
        graph_frame = self.create_graph_frame()
        graph_frame.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")

        # frame dei bottoni start e stop (e trash)
        start_stop_frame = self.create_bottom_bar_frame()
        start_stop_frame.grid(column=0, row=2, padx=5, pady=0, sticky="nsew")

    # crea il frame della tabella delle misurazioni    
    def create_tree_view(self):
        value_table = ttk.Treeview(
            self,
            columns = ('index', 'temperatura'),
            show = 'headings'
        )
        value_table.grid_propagate(False)
        
        # heading delle colonne
        value_table.heading('index', text='Numero misura')
        value_table.heading('temperatura', text='Temperatura [°C]')
        
        # larghezza delle colonne
        value_table.column("index", width=150)
        value_table.column("temperatura", width=150)

        # inizializza il contatore delle misurazioni a 0
        self.numero_misurazioni = 0
        
        return value_table
    
    # crea il frame del grafico
    def create_graph_frame(self):
        graph_frame = tk.Frame(self)
        
        # definisce una riga e una colonna
        graph_frame.grid_rowconfigure(0, weight=1)
        graph_frame.grid_columnconfigure(0, weight=1)
    
        # la figura di Matplotlib
        self.fig, self.graph = plt.subplots(figsize=(4, 3))
        
        # inizializza il grafico
        self.init_graph()
        
        # inizializza due array per gestire i valori delle ascisse e delle ordinate
        self.x_data = []
        self.y_data = []

        # GRAFICO FREQUENZA - TENSIONE --- TASK PRECEDENTE
        # Imposta i titoli degli assi e del grafico
        # self.ax.set_title("Misurazione Frequenza e Tensione")
        # self.ax.set_xlabel("Frequenza (kHz)")
        # self.ax.set_ylabel("Tensione (mV)")
        
        # # Limiti predefiniti del grafico
        # self.ax.set_xlim(AcquisizioneDati.MIN_FREQUENCY, AcquisizioneDati.MAX_FREQUENCY)
        # self.ax.set_ylim(AcquisizioneDati.MIN_VOLTAGE, AcquisizioneDati.MAX_VOLTAGE)

        # aggiunge il grafico alla finestra Tkinter
        self.canvas = FigureCanvasTkAgg(master=graph_frame, figure=self.fig)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        return graph_frame
        
    # funzione per la creazione dei frame nella grid dei parametri
    def create_parameters_frame(self):
        # frame con titolo Parameters
        parameters_frame = tk.LabelFrame(self, text="Parameters")
                
        parameters_frame.grid_propagate(True)
        
        # definizione colonne
        parameters_frame.columnconfigure(0, weight=0)
        parameters_frame.columnconfigure(1, weight=1)
        parameters_frame.columnconfigure(2, weight=1)
        parameters_frame.columnconfigure(3, weight=1)
        parameters_frame.columnconfigure(4, weight=1)
        parameters_frame.columnconfigure(5, weight=1)
        parameters_frame.columnconfigure(6, weight=1)
       
        # definizione righe  
        parameters_frame.rowconfigure(0, weight=1)
        parameters_frame.rowconfigure(1, weight=1)
        parameters_frame.rowconfigure(2, weight=1)
        
        # bottoni per cambiare modalità (frequenza singola / frequenza sweep)
        self.toggle_frequency_mode_button = ttk.Button(
            parameters_frame,
            text="Frequenza singola",
            width = 20,
            padding = 10,
            style = StyleManager.MEDIUM_RED3_BUTTON_STYLE_NAME,
            command = self.toggle_frequency_mode_button_clicked
        )
        self.toggle_frequency_mode_button.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")
        
        # inizializza la modalità come frequenza singola
        self.current_frequency_mode = AcquisizioneDati.FREQUENZA_SINGOLA
        
        frequency_label = ttk.Label(
            parameters_frame,
            style = StyleManager.SMALL_BLUE_LABEL_STYLE_NAME,
            text = f"Frequency\n({AcquisizioneDati.MIN_FREQUENCY} kHz - {AcquisizioneDati.MAX_FREQUENCY} kHz)",
            anchor = "w",
            padding = (10,0,10,20)
        )
        frequency_label.grid(column=0, row=1, sticky="nesw")
       
        self.frequency_start_label = ttk.Label(
            parameters_frame,
            style = StyleManager.SMALL_BLUE_LABEL_STYLE_NAME,
            text = "Start F",
            anchor = "e", 
            width = 10
        )
        self.frequency_start_label.grid(column=1, row=1, sticky="nesw")

        # registra le funzioni di validazione per le entry dei parametri (uno per i double e uno per gli int)
        validate_double = (self.register(AcquisizioneDati.validate_double_number),  '%d', '%S', '%P')
        validate_int = (self.register(AcquisizioneDati.validate_int_number),  '%d', '%S', '%P')

        # definisce variabili e entry per i parametri
        self.start_frequency = tk.DoubleVar()
        
        self.frequency_start_entry = ttk.Entry(
            parameters_frame,
            style = StyleManager.ENTRY_BLUE_STYLE_NAME,
            font = StyleManager.small_font,     # il font per le entry va impostato separatamente dallo style
            textvariable = self.start_frequency,
            width = 15,
            validatecommand = validate_double, # funzione di validazione
            validate = "key"                   # la funzione si attiva ad ogni pressione di un tasto (key)
        )
        self.frequency_start_entry.grid(column=2, row=1, sticky="w")

        self.frequency_stop_label = ttk.Label(
            parameters_frame,
            style = StyleManager.SMALL_BLUE_LABEL_STYLE_NAME,
            text = "Stop F",
            anchor = "e",
            width = 10
        )
        
        self.stop_frequency = tk.DoubleVar()
        
        self.frequency_stop_entry = ttk.Entry(
            parameters_frame,
            style = StyleManager.ENTRY_BLUE_STYLE_NAME,
            font = StyleManager.small_font,     # il font per le entry va impostato separatamente dallo style
            textvariable = self.stop_frequency,
            width = 15,
            validatecommand = validate_double, # funzione di validazione
            validate = "key"                   # la funzione si attiva ad ogni pressione di un tasto (key)
        )

        self.frequency_points_label = ttk.Label(
            parameters_frame,
            style = StyleManager.SMALL_BLUE_LABEL_STYLE_NAME,
            text = "Points",
            anchor = "e",
            width = 10
        )
        
        self.frequency_points = tk.IntVar()
        
        self.frequency_points_entry = ttk.Entry(
            parameters_frame,
            style = StyleManager.ENTRY_BLUE_STYLE_NAME,
            font = StyleManager.small_font,     # il font per le entry va impostato separatamente dallo style
            textvariable = self.frequency_points,
            width = 15,
            validatecommand = validate_int,    # funzione di validazione
            validate = "key"                   # la funzione si attiva ad ogni pressione di un tasto (key)
        )
        
        voltage_label = ttk.Label(
            parameters_frame,
            style = StyleManager.SMALL_BLUE_LABEL_STYLE_NAME,
            text = f"Voltage\n({AcquisizioneDati.MIN_VOLTAGE} mV - {AcquisizioneDati.MAX_VOLTAGE} mV)",
            anchor = "w",
            padding = (10,0,10,20)
        )
        voltage_label.grid(column=0, row=2, sticky="nesw")
        
        self.numero_cicli_label = ttk.Label(
            parameters_frame,
            style = StyleManager.SMALL_BLUE_LABEL_STYLE_NAME,
            text = "Numero\ncicli",
            anchor = "e",
            width = 10
        )
        
        self.numero_cicli = tk.IntVar()
        
        self.numero_cicli_entry = ttk.Entry(
            parameters_frame,
            style = StyleManager.ENTRY_BLUE_STYLE_NAME,
            font = StyleManager.small_font,     # il font per le entry va impostato separatamente dallo style
            textvariable = self.numero_cicli,
            width = 15,
            validatecommand = validate_int,    # funzione di validazione
            validate = "key"                   # la funzione si attiva ad ogni pressione di un tasto (key)
        )
        
        self.voltage_value_label = ttk.Label(
            parameters_frame,
            style = StyleManager.SMALL_BLUE_LABEL_STYLE_NAME,
            text = "Voltage",
            anchor = "e", 
            width = 10
        )
        self.voltage_value_label.grid(column=1, row=2, sticky="nesw")
        
        self.voltage_value = tk.DoubleVar()     # voltage_value appartiene all'oggetto self
        
        voltage_value_entry = ttk.Entry(
            parameters_frame,
            style = StyleManager.ENTRY_BLUE_STYLE_NAME,
            font = StyleManager.small_font,     # il font per le entry va impostato separatamente dallo style
            textvariable = self.voltage_value,
            width = 15,
            validatecommand = validate_double,   # funzione di validazione
            validate = "key"                   # la funzione si attiva ad ogni pressione di un tasto (key)
        )
        voltage_value_entry.grid(column=2, row=2, sticky="w")
        
        # inizializza le posizioni nella griglia di StopF e Points (solo quelli che sono modificati al cambio della modalità di frequenza)
        self.init_parameters_grid()
        
        # inizializza i valori
        self.reset_parameters()
        
        # inizializza la modalità di frequenza
        self.show_single_frequency()
        
        return parameters_frame
    
    # FUNZIONI DI VALIDAZIONE: sono attivate per carattere inserito
    # - action indica quale azione c'è stato
    # - char è il nuovo carattere inserito (se c'è stato un inserimento)
    # queste funzioni restituiscono True se è accettata la modifica, False altrimenti (modifica scartata)
    @staticmethod
    def validate_double_number(action, char, new_value):
        # se l'azione è di cancellazione, accetta (l'azione sarà "0")
        if action == "0":
            return True

        # se il nuovo carattere inserito è un numero, accetta fino a 10 caratteri massimo
        if char.isdigit():
            return len(new_value) <= 10 or char == ""

        # se il carattere da inserire è un punto, lo inserisce solo se ce n'è solo uno
        if char == '.' and new_value.count('.') == 1:
            return True
        
        # altrimenti rifiuta
        return False
    
    @staticmethod
    def validate_int_number(action, char, new_value):
        # se l'azione è di cancellazione, accetta (l'azione sarà "0")
        if action == "0":
            return True
        
        # se il nuovo carattere inserito è un numero, accetta fino a 10 caratteri massimo
        if char.isdigit():
            return True
        
        # altrimenti rifiuta
        return False
    
    # crea la barra inferiore della schermata AcquisizioneDati, contenente:
    #   - la progress bar associata alla misurazione (FUNZIONE create_progress_bar_frame)
    #   - i bottoni di start, stop e cancellazione dati (FUNZIONE create_start_stop_frame)
    def create_bottom_bar_frame(self):
        bottom_bar_frame = ttk.Frame(self, height=50)

        # progress bar
        self.progress_value = tk.DoubleVar()

        progress_bar_frame = ttk.Progressbar(
            bottom_bar_frame,
            length=300,
            variable=self.progress_value
        )
        progress_bar_frame.pack(side="left", fill="both", pady=30, padx=20)

        # inizializza a 50 la progress bar
        self.progress_value.set(50)
        
        # bottoni di start, stop e cancellazione dati
        status_frame = self.create_start_stop_frame(bottom_bar_frame)
        status_frame.pack(side="right", fill="both")   # allinea sulla destra

        return bottom_bar_frame

    # funzione per la creazione dei frame start stop e cancellazione dati
    def create_start_stop_frame(self, parent):
        start_stop_frame = tk.Frame(parent, height=20)
        
        # riga
        start_stop_frame.rowconfigure(0, weight=1)
        
        # colonne (uniforma i bottoni)
        start_stop_frame.columnconfigure(0, weight=0, uniform="buttons")
        start_stop_frame.columnconfigure(1, weight=0, uniform="buttons")
        start_stop_frame.columnconfigure(2, weight=0, uniform="buttons")
        
        # bottone per iniziare la misurazione
        start_button = ttk.Button(
            start_stop_frame,
            style=StyleManager.MEDIUM_BLUE_BUTTON_STYLE_NAME,
            image=ImageManager.start_image,
            command=self.start_button_clicked
        )
        start_button.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")
        
        # bottone per terminare la misurazione
        stop_button = ttk.Button(
            start_stop_frame,
            style=StyleManager.MEDIUM_BLUE_BUTTON_STYLE_NAME,
            image=ImageManager.stop_image,
            command=self.stop_button_clicked
        )
        stop_button.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")
        
        # bottone per cancellare i dati delle misurazioni precedenti
        trash_button = ttk.Button(
            start_stop_frame,
            style=StyleManager.MEDIUM_BLUE_BUTTON_STYLE_NAME,
            image=ImageManager.trash_image,
            command=self.trash_button_clicked
        )
        trash_button.grid(column=2, row=0, padx=5, pady=5, sticky="nsew")
        
        return start_stop_frame
        
    # metodo che, dato in ingresso una variabile tkinter numerica (IntVar o DoubleVar), restituisce il valore associato
    # Inoltre solleva un errore qualora il valore della variabile non sia compresa nell'intervallo [min, max]
    @staticmethod
    def get_variable_value(variable: tk.Variable, min, max):
        value = variable.get()
        
        if value < min or value > max:
            raise ValueError('Il valore è al di fuori del range accettabile')
        
        return value
        
    # inizializza il grafico graph
    def init_graph(self):
        self.graph.set_title("Grafico misurazioni", fontsize = 17)
        self.graph.set_xlabel("Numero misurazione", fontsize = 13)
        self.graph.set_ylabel("Temperatura [°C]", fontsize = 13)

        self.graph.grid(True)
        
        # range di valori degli assi
        self.graph.set_xlim(1, 10)
        self.graph.set_ylim(0, 100)
        
    # aggiunge il punto "lettura" al grafico come valore sull'asse Y
    # il valore sull'asse X è dato dal numero della misurazione corrente (che viene incremnetato)
    def add_graph_point(self, lettura):
        # aggiunge il nuovo punto agli assi
        self.x_data.append(self.numero_misurazioni)
        self.y_data.append(lettura)

        # rimuove il grafico precedente
        self.graph.clear()
        
        self.init_graph()
        
        # disegna i punti (self.x_data contiene le ascisse e self.y_data contiene le ordinate) e li unisce con linee
        self.graph.plot(
            self.x_data,
            self.y_data,
            marker='o', color='b', linestyle='-', label="Temperatura"
        )

        # estende l'asse x se necessario
        if self.numero_misurazioni > self.graph.get_xlim()[1]:
            self.graph.set_xlim(1, self.numero_misurazioni + 1)

        # disegna il grafico
        self.canvas.draw()

    # agginuge il punto "lettura" alla tabella delle misurazioni
    def add_value_in_table(self, lettura):
        self.value_table.insert("", tk.END, values=(self.numero_misurazioni, lettura, 0))

    # cancella tutte le misurazioni (tabella e grafico)
    def cancel_data(self):
        print("Cancellazione dati...")
        
        # pulisce i dati nel grafico, mantenendo titolo e label
        self.graph.clear()  # Cancella il contenuto del grafico

        self.init_graph()

        # ridisegna il grafico vuoto
        self.canvas.draw()

        # resetta le liste dei dati
        self.x_data = []
        self.y_data = []
        
        # cancella tutte le righe dalla Treeview
        for row in self.value_table.get_children():
            self.value_table.delete(row)
            
        # azzera il contatore delle misurazioni
        self.numero_misurazioni = 0
            
        # resetta i parametri
        self.reset_parameters()
        
    # resetta i parametri ai valori di default (valori minimi)
    def reset_parameters(self):
        self.start_frequency.set(AcquisizioneDati.MIN_FREQUENCY)
        self.stop_frequency.set(AcquisizioneDati.MIN_FREQUENCY)
        self.frequency_points.set(AcquisizioneDati.MIN_POINTS)
        self.numero_cicli.set(AcquisizioneDati.MIN_CICLI)
        self.voltage_value.set(AcquisizioneDati.MIN_VOLTAGE)
        
    # ottiene i valori dei parametri inseriti e li stampa a video, verificando che siano negli intervalli di valori accettabili
    def get_parameters(self):
        # esegue questo blocco di codice in un try, in modo da gestire eventuali errori nel blocco except
        try:
            # legge i valori degli oggetti entry, verificando che siano compresi nell'intervallo giusto
            
            # legge solo la frequenza e il voltaggio sia se è in modalità singola che sweep
            startF = AcquisizioneDati.get_variable_value(
                variable = self.start_frequency,
                min = AcquisizioneDati.MIN_FREQUENCY,
                max = AcquisizioneDati.MAX_FREQUENCY
            )
            
            voltage = AcquisizioneDati.get_variable_value(
                variable = self.voltage_value,
                min = AcquisizioneDati.MIN_VOLTAGE,
                max = AcquisizioneDati.MAX_VOLTAGE
            )
            
            if self.current_frequency_mode == AcquisizioneDati.FREQUENZA_SINGOLA:
                print(f"La frequenza è: {startF} kHz")
                print(f"L'ampiezza del segnale di stimolazione è: {voltage} mV")    
            
                return (voltage, startF)
            else:
                # legge anche stopF, freqPoints e numeroCicli SOLO se è in modalità sweep
                stopF = AcquisizioneDati.get_variable_value(
                    variable = self.stop_frequency,
                    min = startF,
                    max = AcquisizioneDati.MAX_FREQUENCY
                )
                
                freqPoints = AcquisizioneDati.get_variable_value(
                    variable = self.frequency_points,
                    min = AcquisizioneDati.MIN_POINTS,
                    max = AcquisizioneDati.MAX_POINTS
                )
                
                numeroCicli = AcquisizioneDati.get_variable_value(
                    variable = self.numero_cicli,
                    min = AcquisizioneDati.MIN_CICLI,
                    max = AcquisizioneDati.MAX_CICLI
                )
            
                print(f"La frequenza iniziale è: {startF} kHz")
                print(f"La frequenza finale è: {stopF} kHz")
                print(f"Il numero di punti delle frequenze è: {freqPoints}")
                print(f"Il numero di cicli è: {numeroCicli}")
                print(f"L'ampiezza del segnale di stimolazione è: {voltage} mV")
                
                return (voltage, startF, stopF, freqPoints, numeroCicli)
        
        except (ValueError, tk.TclError):
            # cattura dell'eccezione per input non validi            
            messagebox.showerror(
                title = "Errore",
                message = "Controlla i parametri inseriti!"
            )
            
            # rilancia l'eccezione catturata nell'except (equivale a throw)
            raise

    # gestisce l'arrivo di una nuova lettura, aggiungendo il valore al grafico e alla tabella
    def handle_new_measurement(self, lettura):
        # verifica se la lettura è nel range 1 °C - 70 °C
        if lettura < 1 or lettura > 70:
            messagebox.showwarning(
                title="Avviso misurazione",
                message=f"Attenzione! Il valore ricevuto della lettura è {lettura} °C, al di fuori del range accettabile (1 - 70 °C)"
            )
            return
        
        # incrementa il numero di misurazioni
        self.numero_misurazioni += 1
        
        # aggiorna il grafico, aggiungendo il nuovo punto
        self.add_graph_point(lettura)
        
        # aggiorna la tabella, aggiungendo la nuova lettura
        self.add_value_in_table(lettura)
    
    # COMANDI BOTTONI
    def start_button_clicked(self):
        # verifica se sta già misurando
        if self.is_measuring:
            messagebox.showerror(
                title = "Errore",
                message = "Attenzione! Misurazione già in corso.")
            print("Messaggio di errore: Misurazione già in corso.")
            return

        try:
            # in base alla modalità, legge i parametri inseriti ed inizia la misurazione (invia alla board i parametri e il comando di inizio)
            if self.current_frequency_mode == AcquisizioneDati.FREQUENZA_SINGOLA:
                (voltage, frequenza) = self.get_parameters()
                
                is_measurement_started = self.start_measurement_single_frequency(voltage, frequenza)
            else:
                (voltage, startF, stopF, freqPoints, numeroCicli) = self.get_parameters()
                
                is_measurement_started = self.start_measurement_sweep_frequency(voltage, startF, stopF, freqPoints, numeroCicli)
                
            # verifica se l'invio è avvenuto correttamente
            if not is_measurement_started:
                return
            
            print("La misurazione è iniziata")
            self.is_measuring = True
        
        except (ValueError, tk.TclError):
            # cattura dell'eccezione per input non validi
            print("La misurazione non è iniziata a causa di errori")

    def stop_button_clicked(self):
        # verifica se non sta ancora misurando
        if not self.is_measuring:
            messagebox.showerror(
                title="Errore",
                message="La misurazione non è stata terminata perché non c'è alcuna misurazione in corso"
            )
            return
        
        # chiede conferma prima di interrompere
        has_to_stop = messagebox.askyesno(
            title="Interruzione misurazione",
            message="Sei sicuro di voler interrompere la misurazione?"
        )
        
        if(has_to_stop):
            # manda stop alla board per interrompere
            self.stop_board()
            self.is_measuring = False
            print("La misurazione è stata interrotta")
        else:
            print("L'interruzione è stata annullata")
    
    def trash_button_clicked(self):
        # chiede conferma prima di cancellare i dati
        has_to_cancel = messagebox.askyesno(
            title="Cancellazione dati",
            message="Sei sicuro di voler cancellare i dati?"
        )
        
        if(has_to_cancel):
            self.cancel_data()
            print("Le misurazioni sono state cancellate")
        else:
            print("La cancellazione è stata annullata")
    
    # cambia la modalità di frequenza (singola - sweep)
    def toggle_frequency_mode_button_clicked(self):
        # Se la modalità corrente è a singola frequenza, passa a quella sweep e viceversa
        if self.current_frequency_mode == AcquisizioneDati.FREQUENZA_SINGOLA:
            self.show_sweep_frequency()
        else:
            self.show_single_frequency()
        
    # imposta modalità a frequenza singola
    def show_single_frequency(self):
        print("Attivata modalità a singola frequenza")
        
        self.current_frequency_mode = AcquisizioneDati.FREQUENZA_SINGOLA
        self.toggle_frequency_mode_button.configure(text = "Frequenza singola")
        
        # nasconde gli elementi non relativi alla modalità a singola frequenza
        self.frequency_stop_label.grid_forget()
        self.frequency_stop_entry.grid_forget()
        self.frequency_points_label.grid_forget()
        self.frequency_points_entry.grid_forget()
        self.numero_cicli_label.grid_forget()
        self.numero_cicli_entry.grid_forget()
        
        # cambia il nome Start F in Frequency
        self.frequency_start_label.configure(text = "Frequency")
        
    # imposta modalità a frequenza sweep
    def show_sweep_frequency(self):
        print("Attivata modalità a frequenza sweep")
        
        self.current_frequency_mode = AcquisizioneDati.FREQUENZA_SWEEP
        self.toggle_frequency_mode_button.configure(text = "Frequenza sweep")
        
        # ripristina gli elementi relativi alla frequenza sweep
        self.init_parameters_grid()
        
        # cambia il nome Frequency in Start F
        self.frequency_start_label.configure(text = "StartF")
        
    # inizializza i parametri nella griglia (relativi alla frequenza sweep), per mostrarli a video
    def init_parameters_grid(self):
        self.frequency_stop_label.grid(column=3, row=1, sticky="nesw")
        self.frequency_stop_entry.grid(column=4, row=1, sticky="w")
        
        self.frequency_points_label.grid(column=5, row=1, sticky="nesw")
        self.frequency_points_entry.grid(column=6, row=1, sticky="w")

        self.numero_cicli_label.grid(column=5, row=2, sticky="nesw")
        self.numero_cicli_entry.grid(column=6, row=2, sticky="w")
        