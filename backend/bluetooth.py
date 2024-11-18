import asyncio
import threading
from bleak import BleakScanner
from bleak import BleakClient
from bleak.exc import BleakError
import datetime
import struct

# NOTA: implementare bluetooth come classe
class BLEClient:
    
    # UUID della board
    SERVICE_UUID = "26e29ec9-3491-4d42-b816-d081936e2edc"
    COMMAND_CHARACTERISTIC_UUID = "9b3c81d8-57b1-4a8a-b8df-0e56f7ca51c2"
    MEASUREMENT_NOTIFICATION_CHARACTERISTIC_UUID = "9fbf120d-6301-42d9-8c58-25e699a21dbd"
    BATTERY_LEVEL_NOTIFICATION_CHARACTERISTIC_UUID = "00002a19-0000-1000-8000-00805f9b34fb"
    
    # COMANDI
    START_COMMAND = "start"
    STOP_COMMAND = "stop"
    
    def __init__(self, new_measurement_callback, update_battery_level_callback):
        # funzione da eseguire per gestire l'arrivo di una nuova lettura
        # questa variabile (che va inteso come un "puntatore a funzione") va inizializzata nella classe dell'App
        self.new_measurement_callback = new_measurement_callback

        # funzione da eseguire per gestire l'arrivo di una nuova percentuale di batteria
        # questa variabile (che va inteso come un "puntatore a funzione") va inizializzata nella classe dell'App
        self.update_battery_level_callback = update_battery_level_callback
        
        self.main_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.main_loop)
        
        # oggetto BleakClient utilizzato per la connessione
        self.client = None
        
        # altre variabili sulla connessione
        self.is_connected = False
        self.devices_found = []
        
    # esegue una coroutine nel loop principale della classe
    def run_async_task(self, coro):
        return asyncio.run_coroutine_threadsafe(coro, self.main_loop)
    
    # esegue la scansione dei dispositivi BLE nelle vicinanze
    async def start_scan(self, callback=None):
        try:
            self.log_message("Scansione in corso...")
            
            # effettua una scansione per "stimeout" secondi e trova i dispositivi BLE nelle vicinanze, inserendoli nella variabile self.devices_found
            self.devices_found = await BleakScanner.discover(timeout=3)
    
            if self.devices_found:
                # stampa nel terminale i dispositivi trovati
                self.log_devices_in_terminal()
        
                # # Controlla se rispetta i filtri
                # if matches_filter(device, target_name, target_address):
                #     print(f"Matched Device: {device.name or 'Sconosciuto'}, Address: {device.address}\n")
                
                # Esegue la funzione di callback per mostrare i dispositivi 
                if callback:
                    callback()
            else:
                self.log_message("Nessun dispositivo trovato")

        except BleakError as e:
            self.log_message(f"Bluetooth error: {e}\nControlla se il bluetooth è attivo")

        except Exception as e:
            self.log_message(f"Unexpected error: {e}\nControlla se il bluetooth è attivo")

    # si connette al dispositivo con indirizzo device_address
    # al termine della connessione, in caso di successo esegue la funzione on_success
    async def connect_to_device(self, device_name, device_address, on_success=None):
        """Connetti al dispositivo specificato."""
        try:
            self.log_message(f"Connessione a {device_name} in corso...")
            
            # effettua la connessione
            self.client = BleakClient(device_address)
            await self.client.connect()
            
            # Controlla se ci si è connessi correttamente
            if self.client.is_connected:
                self.is_connected = True
                self.log_message(f"Connesso a {device_name}")
                
                # esegue la funzione da eseguire in caso di successo (se è non nulla)
                if on_success:
                    on_success()
            else:
                # caso in cui non si è connesso
                self.log_message(f"Impossibile connettersi a {device_address}")
                return
                    
        except BleakError as e:
            self.log_message(f"Errore di connessione: {e}")
        
        except Exception as e:
            self.log_message(f"Errore inaspettato: {e}")

    # si disconnette dal dispositivo a cui è attualmente connesso (qualora fosse connesso a qualcuno)
    # ed esegue la funzione on_success in caso di successo
    async def disconnect_from_device(self, on_success=None):
        if self.client and self.client.is_connected:
            self.log_message(f"Disconnessione in corso...")

            await self.client.disconnect()
            
            self.log_message(f"Disconnesso")
            
            if on_success:
                on_success()

    # FUNZIONI PER LA GESTIONE DEL LOOP PRINCIPALE DELLA CLASSE
    
    # esegue il loop principale della classe in un thread separato da quello del chiamante
    def start_event_loop(self):
        threading.Thread(target=self.main_loop.run_forever, daemon=True).start()

    # interrompe il loop principale della classe
    def stop_event_loop(self):
        self.main_loop.call_soon_threadsafe(self.main_loop.stop)
        self.main_loop.stop()
    
    # funzione di log
    def log_message(self, message):
        print(message)
        if self.status_var:
            self.status_var.set(message)
            
    # effettua il log dei dispositivi trovati nella console
    def log_devices_in_terminal(self):
        for device in self.devices_found:
            print(f"Nome: {device.name or "Sconosciuto"}, Indirizzo: {device.address}")
   
    # FUNZIONI DI CALLBACK PER GESTIRE LA RICEZIONE DELLE NOTIFICHE
    
    def notification_text_handler(self, sender, data):
        testo_ricevuto = data.decode('utf-8')  # Decodifica i byte come stringa UTF-8
        print(f"Testo ricevuto: {testo_ricevuto}")
        
        # invoca la funzione da eseguire per gestire l'arrivo di una nuova lettura
        if self.new_measurement_callback:
            self.new_measurement_callback(testo_ricevuto)
        else:
            print("Nessuna funzione di callback assegnata per gestire le notifiche.")
        
    def notification_float_handler(self, sender, data):
        # Decodifica i dati come float a 4 byte (usa "d" per double, che è 8 byte)
        numero = struct.unpack('<f', data)[0]  # '<f' indica un float in formato little-endian
        print(f"Numero float ricevuto: {numero}")
        
        # invoca la funzione da eseguire per gestire l'arrivo di una nuova lettura
        if self.new_measurement_callback:
            self.new_measurement_callback(numero)
        else:
            print("Nessuna funzione di callback assegnata per gestire le notifiche.")
            
    def notification_handler_new(self, sender, data):    
        print(f"Data: {data}")
        print(f"type of data: {type(data)}")
        
        valore = struct.unpack('>i', data)[0]
        print(f"Numero int ricevuto: {valore}")
        
        # invoca la funzione da eseguire per gestire l'arrivo di una nuova lettura
        if self.new_measurement_callback:
            self.new_measurement_callback(valore)
        else:
            print("Nessuna funzione di callback assegnata per gestire le notifiche.")
            
    def notification_battery_level(self, sender, data):
        valore = struct.unpack('>i', data)[0]
        if valore < 0 or valore > 100:
            print(f"Errore! La percentuale di batteria era {valore} %")
            return
            
        print(f"Percentuale della batteria: {valore}")
        
        # invoca la funzione da eseguire per gestire l'arrivo di una nuova percentuale
        if self.update_battery_level_callback:
            self.update_battery_level_callback(valore)
        else:
            print("Nessuna funzione di callback assegnata per gestire le notifiche.")


    # FUNZIONI CHE COMUNICANO CON IL SERVER
    
    async def start_measurement_notify(self):
        # ad ogni notifica ricevuta sulla caratteristica con uuid MEASUREMENT_NOTIFICATION_CHARACTERISTIC_UUID,
        # viene eseguita la funzione notification_float_handler
        await self.client.start_notify(BLEClient.MEASUREMENT_NOTIFICATION_CHARACTERISTIC_UUID,
                                       self.notification_float_handler)
        print("Notifiche sulla misurazione attivate")
        
    # Interrompe la ricezione delle notifiche
    async def stop_measurement_notify(self):
        await self.client.stop_notify(BLEClient.MEASUREMENT_NOTIFICATION_CHARACTERISTIC_UUID)
        print("Notifiche sulla misurazione fermate")
        
    async def start_battery_level_notify(self):
        # ad ogni notifica ricevuta sulla caratteristica con uuid BATTERY_LEVEL_NOTIFICATION_CHARACTERISTIC_UUID,
        # viene eseguita la funzione 
        await self.client.start_notify(BLEClient.BATTERY_LEVEL_NOTIFICATION_CHARACTERISTIC_UUID,
                                  self.notification_battery_level)
        print("Notifiche sulla percentuale di batteria attivate")
        
    async def stop_battery_level_notify(self):
        # ad ogni notifica ricevuta sulla caratteristica con uuid BATTERY_LEVEL_NOTIFICATION_CHARACTERISTIC_UUID,
        # viene eseguita la funzione 
        await self.client.stop_notify(BLEClient.BATTERY_LEVEL_NOTIFICATION_CHARACTERISTIC_UUID)
        print("Notifiche sulla percentuale di batteria attivate")


    # SEZIONE COMANDI

    # invia al server il comando di start e si mette in ascolto per le notiche
    async def start_board(self):
        await self.send_command(BLEClient.START_COMMAND)
        await self.start_measurement_notify()

    # invia al server il comando di stop e interrompe l'ascolto per le notiche
    async def stop_board(self):
        await self.stop_measurement_notify()
        await self.send_command(BLEClient.STOP_COMMAND)

    # funzione generica per inviare il comando "command"
    async def send_command(self, command):
        try:
            # Scrive il comando sulla caratteristica specifica
            await self.client.write_gatt_char(BLEClient.COMMAND_CHARACTERISTIC_UUID, command.encode("utf-8"))
            print(f"Comando {command} inviato")
        except BleakError as e:
            print(f"Errore durante l'invio del comando: {e}")
            
            
    # verifica se il device corrisponde ai filtri target_name e target_address
    @staticmethod
    def matches_filter(device, target_name, target_address):
        return ((target_name.lower() in (device.name or "").lower()) if target_name else True) and \
                ((target_address.lower() in device.address.lower()) if target_address else True)