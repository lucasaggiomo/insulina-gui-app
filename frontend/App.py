import tkinter as tk
from tkinter import ttk

class App(tk.Tk):

    # Costruttore che costruisce l'oggetto di tipo App
    def __init__(self): 
        super().__init__()

        # Size iniziale della finestra
        self.geometry("800x500")

        # Titolo finestra
        self.title("Fondamenti di Misure")

        # Non permettere il resize
        # self.resizable(0, 0)
        
        # Chiamo la funzione create_widgets - dichiarata successivamente
        self.create_widgets()

    # Funzione per la creazione dei frame nella grid Parameters
    def create_parameters_frame(self, parent):
        parameters_frame = tk.LabelFrame(parent, text="Parameters", bg="red") # creo un oggetto frame con etichetta Parameters
        
        #parameters_frame.grid_propagate(True)
        parameters_frame.columnconfigure(0, weight=1)
        parameters_frame.columnconfigure(1, weight=1)
        parameters_frame.columnconfigure(2, weight=1)
        parameters_frame.columnconfigure(3, weight=1)
        parameters_frame.columnconfigure(4, weight=1)
        parameters_frame.columnconfigure(5, weight=1)
        parameters_frame.columnconfigure(6, weight=1)
        
        parameters_frame.rowconfigure(0, weight=1)
        parameters_frame.rowconfigure(1, weight=1)

        frequency_label = tk.Label(parameters_frame, text="Frequency", anchor="e", height=2, width=10, bg="red")
        frequency_label.grid(column=0, row=0, sticky="nesw")
       
        frequency_start_label = tk.Label(parameters_frame, text="Start F", anchor="e", height=2, width=10, bg="red")
        frequency_start_label.grid(column=1, row=0, sticky="nesw")
        self.start_frequency = tk.DoubleVar()
        frequency_start_entry = tk.Entry(parameters_frame, textvariable=self.start_frequency, width=20)
        frequency_start_entry.grid(column=2, row=0, sticky="ew")

        frequency_stop_label = tk.Label(parameters_frame, text="Stop F", anchor="e", height=2, width=10, bg="red")
        frequency_stop_label.grid(column=3, row=0, sticky="nsw")
        self.stop_frequency = tk.DoubleVar()
        frequency_stop_entry = tk.Entry(parameters_frame, textvariable=self.stop_frequency, width=20)
        frequency_stop_entry.grid(column=4, row=0, sticky="w")

        frequency_points_label = tk.Label(parameters_frame, text="Points", anchor="e", height=2, width=10, bg="red")
        frequency_points_label.grid(column=5, row=0, sticky="nsw")
        self.points = tk.DoubleVar()
        frequency_points_entry = tk.Entry(parameters_frame, textvariable=self.points, width=20)
        frequency_points_entry.grid(column=6, row=0, sticky="w")
        
        voltage_label = tk.Label(parameters_frame, text="Voltage", anchor="e", height=2, width=10, bg="red")
        voltage_label.grid(column=0, row=1, sticky="nesw")
        self.voltage_value = tk.DoubleVar() # voltage_value appartiene all'oggetto self
        voltage_value_entry = tk.Entry(parameters_frame, textvariable=self.voltage_value, width=20)
        voltage_value_entry.grid(column=2, row=1, sticky="ew")
        
        return parameters_frame

    def create_dati_tab(self, tab_control):
        acquisizione_dati_frame = tk.Frame(tab_control)
        
        acquisizione_dati_frame.grid_propagate(False)

        # definisco le colonne
        acquisizione_dati_frame.columnconfigure(0, weight=1)
        acquisizione_dati_frame.columnconfigure(1, weight=1)

        # definisco le righe
        acquisizione_dati_frame.rowconfigure(0, weight=2)
        acquisizione_dati_frame.rowconfigure(1, weight=6)
        acquisizione_dati_frame.rowconfigure(2, weight=1)

        parameters_frame = self.create_parameters_frame(acquisizione_dati_frame)
        parameters_frame.grid(column=0, row=0, padx=5, pady=5, sticky="nsew") # creo il frame dei parametri

        # tabs_frame = tk.Frame(self, bg="yellow")
        # tabs_frame.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

        value_table = tk.LabelFrame(acquisizione_dati_frame, text="Tabella valori", bg="blue")
        value_table.grid(column=1, row=0, rowspan=3, padx=5, pady=5, sticky="nsew")

        graph_frame = tk.Frame(acquisizione_dati_frame, bg="green")
        graph_frame.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")

        progress_bar_frame = tk.Frame(acquisizione_dati_frame, bg="purple")
        progress_bar_frame.grid(column=0, row=2, padx=5, pady=5, sticky="nsew")
        
        return acquisizione_dati_frame
    
    def create_macchina_tab(self, tab_control):
        stato_macchina_frame = tk.Frame(tab_control)
        
        stato_macchina_frame.grid_propagate(False)

        # definisco le colonne
        stato_macchina_frame.columnconfigure(0, weight=1)
        stato_macchina_frame.columnconfigure(1, weight=1)
        stato_macchina_frame.columnconfigure(2, weight=1)

        # definisco le righe
        stato_macchina_frame.rowconfigure(0, weight=2)

        dati_macchina_frame = tk.Frame(stato_macchina_frame, bg="blue")
        dati_macchina_frame.grid(column=0, row=0, rowspan=3, padx=5, pady=5, sticky="nsew")

        logger_macchina_frame = tk.Frame(stato_macchina_frame, bg="green")
        logger_macchina_frame.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")

        errori_frame = tk.Frame(stato_macchina_frame, bg="purple")
        errori_frame.grid(column=2, row=0, padx=5, pady=5, sticky="nsew")
        
        return stato_macchina_frame
    
    def create_file_tab(self, tab_control):
        file_frame = tk.Frame(tab_control)
        
        file_frame.grid_propagate(False)

        # definisco le colonne
        file_frame.columnconfigure(0, weight=1)
        

        # definisco le righe
        file_frame.rowconfigure(0, weight=2)
        file_frame.rowconfigure(1, weight=2)

        export_excel_frame = tk.Frame(file_frame, bg="blue")
        export_excel_frame.grid(column=0, row=0, rowspan=3, padx=5, pady=5, sticky="nsew")

        export_pdf_frame = tk.Frame(file_frame, bg="green")
        export_pdf_frame.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")

       
        return file_frame

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

        dati_tab = self.create_dati_tab(tab_control)
        dati_tab.grid(row=0,column=0, sticky="nsew");

        macchina_tab = self.create_macchina_tab(tab_control)
        macchina_tab.grid(row=0,column=0, sticky="nsew");
        
        esporta_tab = self.create_file_tab(tab_control)
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