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

from image_manager import ImageManager
from style_manager import StyleManager
        
# Definisco la classe AcquisizioneDati, che eredita da tk.Frame
class AcquisizioneDati(tk.Frame):
    # kHz
    MIN_FREQUENCY = 1
    MAX_FREQUENCY = 100
    
    # mV
    MIN_VOLTAGE = 10
    MAX_VOLTAGE = 500
    
    MIN_POINTS = 1
    MAX_POINTS = 1000
    
    # Costruttore che costruisce l'oggetto di tipo App
    def __init__(self, parent_frame): 
        super().__init__(parent_frame)
        
        self.create_widgets()
    
    def create_widgets(self):
        self.grid_propagate(False)

        # definisco le colonne
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # definisco le righe
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=6)
        self.rowconfigure(2, weight=0)

        parameters_frame = self.create_parameters_frame()
        parameters_frame.grid(column=0, row=0, padx=5, pady=5, sticky="nsew") # creo il frame dei parametri

        value_table = tk.LabelFrame(self, text="Tabella valori", bg="blue")
        value_table.grid(column=1, row=0, rowspan=3, padx=5, pady=5, sticky="nsew")

        graph_frame = tk.Frame(self, bg="green")
        graph_frame.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")

        start_stop_frame = self.create_bottom_bar_frame()
        start_stop_frame.grid(column=0, row=2, padx=5, pady=5, sticky="nsew")
    
    # Funzione per la creazione dei frame nella grid Parameters
    def create_parameters_frame(self):
        parameters_frame = tk.LabelFrame(self, text="Parameters") # creo un oggetto frame con etichetta Parameters
                
        parameters_frame.grid_propagate(True)
        parameters_frame.columnconfigure(0, weight=1)
        parameters_frame.columnconfigure(1, weight=1)
        parameters_frame.columnconfigure(2, weight=1)
        parameters_frame.columnconfigure(3, weight=1)
        parameters_frame.columnconfigure(4, weight=1)
        parameters_frame.columnconfigure(5, weight=1)
        parameters_frame.columnconfigure(6, weight=1)
        
        parameters_frame.rowconfigure(0, weight=1)
        parameters_frame.rowconfigure(1, weight=1)
        
        frequency_label = ttk.Label(parameters_frame,
                                    style=StyleManager.SMALL_LABEL_STYLE_NAME,
                                    text=f"Frequency\n({AcquisizioneDati.MIN_FREQUENCY} kHz - {AcquisizioneDati.MAX_FREQUENCY} kHz)",
                                    anchor="w",
                                    padding=(10,0,10,0))
        frequency_label.grid(column=0, row=0, sticky="nesw")
       
        frequency_start_label = ttk.Label(parameters_frame,
                                          style=StyleManager.SMALL_LABEL_STYLE_NAME,
                                          text="Start F",
                                          anchor="e", 
                                          width=10)
        frequency_start_label.grid(column=1, row=0, sticky="nesw")

        # Registra le funzioni di validazione per le entry dei parametri (uno per i double e uno per gli int)
        vcmd_double = (self.register(AcquisizioneDati.validate_double_number),  '%d', '%S', '%P')
        vcmd_int = (self.register(AcquisizioneDati.validate_int_number),  '%d', '%S', '%P')

        self.start_frequency = tk.DoubleVar()
        
        self.frequency_start_entry = ttk.Entry(parameters_frame,
                                          style=StyleManager.ENTRY_STYLE_NAME,
                                          textvariable=self.start_frequency,
                                          font=StyleManager.small_font,
                                          width=15,
                                          validate="key",
                                          validatecommand=vcmd_double)
        self.frequency_start_entry.grid(column=2, row=0, sticky="w")

        self.frequency_stop_label = ttk.Label(parameters_frame,
                                         style=StyleManager.SMALL_LABEL_STYLE_NAME,
                                         text="Stop F",
                                         anchor="e",
                                         width=10)
        self.frequency_stop_label.grid(column=3, row=0, sticky="nesw")
        
        self.stop_frequency = tk.DoubleVar()
        
        self.frequency_stop_entry = ttk.Entry(parameters_frame,
                                         style=StyleManager.ENTRY_STYLE_NAME,
                                         font=StyleManager.small_font,
                                         textvariable=self.stop_frequency,
                                         width=15,
                                         validate="key",
                                         validatecommand=vcmd_double)
        self.frequency_stop_entry.grid(column=4, row=0, sticky="w")

        self.frequency_points_label = ttk.Label(parameters_frame,
                                           style=StyleManager.SMALL_LABEL_STYLE_NAME,
                                           text="Points",
                                           anchor="e",
                                           width=10)
        self.frequency_points_label.grid(column=5, row=0, sticky="nesw")
        
        self.frequency_points = tk.IntVar()
        
        self.frequency_points_entry = ttk.Entry(parameters_frame,
                                           style=StyleManager.ENTRY_STYLE_NAME,
                                           font=StyleManager.small_font,
                                           textvariable=self.frequency_points,
                                           width=15,
                                           validate="key",
                                           validatecommand=vcmd_int)
        self.frequency_points_entry.grid(column=6, row=0, sticky="w")
        
        voltage_label = ttk.Label(parameters_frame,
                                  style=StyleManager.SMALL_LABEL_STYLE_NAME,
                                  text=f"Voltage\n({AcquisizioneDati.MIN_VOLTAGE} mV - {AcquisizioneDati.MAX_VOLTAGE} mV)",
                                  anchor="w",
                                  padding=(10,0,10,0))
        voltage_label.grid(column=0, row=1, sticky="nesw")
        
        self.voltage_value = tk.DoubleVar() # voltage_value appartiene all'oggetto self
        
        voltage_value_entry = ttk.Entry(parameters_frame,
                                        style=StyleManager.ENTRY_STYLE_NAME,
                                        font=StyleManager.small_font,
                                        textvariable=self.voltage_value,
                                        width=15,
                                        validate="key",
                                        validatecommand=vcmd_double)
        voltage_value_entry.grid(column=2, row=1, sticky="w")
        
        # inizializza i valori
        self.reset_parameters()
        
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
                                  style=StyleManager.MEDIUM_BUTTON_STYLE_NAME,
                                  image=ImageManager.start_image,
                                  command=self.start_button_clicked)
        start_button.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")
        
        # Bottone per terminare la misurazione
        stop_button = ttk.Button(start_stop_frame,
                                 style=StyleManager.MEDIUM_BUTTON_STYLE_NAME,
                                 image=ImageManager.stop_image,
                                 command=self.stop_button_clicked)
        stop_button.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")
        
        # Bottone per cancellare i dati delle misurazioni precedenti
        trash_button = ttk.Button(start_stop_frame,
                                  style=StyleManager.MEDIUM_BUTTON_STYLE_NAME,
                                  image=ImageManager.trash_image,
                                  command=self.trash_button_clicked)
        trash_button.grid(column=2, row=0, padx=5, pady=5, sticky="nsew")
        
        return start_stop_frame
        
    @staticmethod
    def get_double_value(variable, min, max):
        value = variable.get()
        
        if value < min or value > max:
            raise ValueError('Il valore è al di fuori del range accettabile')
        
        return value
        
    def start_button_clicked(self):
        try:
            # Leggiamo i valori degli oggetti entry, verificando che siano compresi nell'intervallo giusto
            startF = AcquisizioneDati.get_double_value(self.start_frequency,
                                                       AcquisizioneDati.MIN_FREQUENCY,
                                                       AcquisizioneDati.MAX_FREQUENCY)
            
            stopF = AcquisizioneDati.get_double_value(self.stop_frequency,
                                                      startF,
                                                      AcquisizioneDati.MAX_FREQUENCY)
            
            freqPoints = AcquisizioneDati.get_double_value(self.frequency_points,
                                                           AcquisizioneDati.MIN_POINTS,
                                                           AcquisizioneDati.MAX_POINTS)
            
            voltage = AcquisizioneDati.get_double_value(self.voltage_value,
                                                        AcquisizioneDati.MIN_VOLTAGE,
                                                        AcquisizioneDati.MAX_VOLTAGE)
            
            print(f"La frequenza iniziale è: {startF} kHz")
            print(f"La frequenza finale è: {stopF} kHz")
            print(f"Il numero di frequenze è: {freqPoints}")
            print(f"Il voltaggio è: {voltage} mV")
        
            print("La misurazione è iniziata")
        
        except (ValueError, tk.TclError):  # Eccezione per input non validi
        # Gestisci l'errore mostrando una finestra di dialogo con un messaggio di errore
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
            
    def cancel_data(self):
        print("Cancellazione dati...")
        
        self.reset_parameters()
        
    def reset_parameters(self):
        self.start_frequency.set(AcquisizioneDati.MIN_FREQUENCY)
        self.stop_frequency.set(AcquisizioneDati.MIN_FREQUENCY)
        self.frequency_points.set(AcquisizioneDati.MIN_POINTS)
        self.voltage_value.set(AcquisizioneDati.MIN_VOLTAGE)

    def stop_measurement(self):
        print("Interruzione della misurazione...")