import asyncio
import threading
from bleak import BleakScanner
from bleak import BleakClient
from bleak.exc import BleakError
import datetime
import struct

# NOTA: implementare bluetooth come classe

# funzione di log
def log_message(message, status_var = None):
    print(message)
    if status_var:
        status_var.set(message)

# esecuzione asincrona della scansione
def run_scan_thread(target_name, target_address, items, status_var):
   asyncio.run(start_scan(target_name, target_address, items, status_var))
   
# esecuzione asincrona nella connessione
def run_connection_thread(device_name, device_address, status_var):
    return asyncio.run(connect_to_device(device_name, device_address, status_var))
    
# Function to start scanning for Bluetooth devices
async def start_scan(target_name, target_address, items, status_var):
    try:
        log_message("Scansione in corso...", status_var)
        
        # Increase the scanning timeout to give the adapter more time to detect devices
        devices = await BleakScanner.discover(timeout=10)
 
        if devices:
           for device in devices:
                add_device(device, items)
 
                # # Controlla se rispetta i filtri
                # if matches_filter(device, target_name, target_address):
                #     print(f"Matched Device: {device.name or 'Sconosciuto'}, Address: {device.address}\n")
        else:
            log_message("Nessun dispositivo trovato", status_var)
 
        log_message("Scansione completata.\nPremi Ricerca per rifare la scansione", status_var)
 
    except BleakError as e:
        log_message(f"Bluetooth error: {e}\nControlla se il bluetooth è attivo", status_var)

    except Exception as e:
        log_message(f"Unexpected error: {e}\nControlla se il bluetooth è attivo", status_var)

# aggiunge il device alla lista
def add_device(device, devices):
    devices.append(
        {'name': device.name or "Sconosciuto", 'address': device.address}
    )
   
    device_name = device.name or "Sconosciuto"
    log_entry = f"{datetime.datetime.now()} - Name: {device_name}, Address: {device.address}, RSSI: {device.rssi} dBm"
    log_message(log_entry)

# verifica se il device corrisponde ai filtri target_name e target_address
def matches_filter(device, target_name, target_address):
   return ((target_name.lower() in (device.name or "").lower()) if target_name else True) and \
          ((target_address.lower() in device.address.lower()) if target_address else True)

async def connect_to_device(device_name, device_address, status_var):
    try:
        log_message(f"Connessione a {device_name}...", status_var)
        
        # effettua la connessione
        client = BleakClient(device_address)
        await client.connect()
            
        # Controlla se ci si è connessi correttamente
        if client.is_connected:
            print("Connesso a {device_name}")
            log_message(f"Connesso a {device_name}", status_var)
            return client
        
        # caso in cui non è conneso
        log_message(f"Impossibile connettersi a {device_address}", status_var)
        return None
            
    except BleakError as e:
        log_message(f"Errore di connessione: {e}", status_var)
        return None
    
    except Exception as e:
        log_message(f"Errore inaspettato: {e}", status_var)
        return None
    
# UUID del servizio e della caratteristica
SERVICE_UUID = "26e29ec9-3491-4d42-b816-d081936e2edc"
COMMAND_CHARACTERISTIC_UUID = "9b3c81d8-57b1-4a8a-b8df-0e56f7ca51c2"
MEASUREMENT_NOTIFICATION_CHARACTERISTIC_UUID = "9fbf120d-6301-42d9-8c58-25e699a21dbd"
BATTERY_LEVEL_NOTIFICATION_CHARACTERISTIC_UUID = "00002a19-0000-1000-8000-00805f9b34fb"

# funzione da eseguire per gestire l'arrivo di una nuova lettura
# questa variabile (che va inteso come un "puntatore a funzione") va inizializzata nella classe dell'App
new_measurement_callback = None

# funzione da eseguire per gestire l'arrivo di una nuova percentuale di batteria
# questa variabile (che va inteso come un "puntatore a funzione") va inizializzata nella classe dell'App
update_battery_level_callback = None

# Funzione di callback per gestire le notifiche
def notification_text_handler(sender, data):
    testo_ricevuto = data.decode('utf-8')  # Decodifica i byte come stringa UTF-8
    print(f"Testo ricevuto: {testo_ricevuto}")
    
    # invoca la funzione da eseguire per gestire l'arrivo di una nuova lettura
    if new_measurement_callback:
        new_measurement_callback(testo_ricevuto)
    else:
        print("Nessuna funzione di callback assegnata per gestire le notifiche.")
    
def notification_float_handler(sender, data):
    # Decodifica i dati come float a 4 byte (usa "d" per double, che è 8 byte)
    numero = struct.unpack('<f', data)[0]  # '<f' indica un float in formato little-endian
    print(f"Numero float ricevuto: {numero}")
    
    # invoca la funzione da eseguire per gestire l'arrivo di una nuova lettura
    if new_measurement_callback:
        new_measurement_callback(numero)
    else:
        print("Nessuna funzione di callback assegnata per gestire le notifiche.")
        
def notification_handler_new(sender, data):    
    print(f"Data: {data}")
    print(f"type of data: {type(data)}")
    
    valore = struct.unpack('>i', data)[0]
    print(f"Numero int ricevuto: {valore}")
    
    # invoca la funzione da eseguire per gestire l'arrivo di una nuova lettura
    if new_measurement_callback:
        new_measurement_callback(valore)
    else:
        print("Nessuna funzione di callback assegnata per gestire le notifiche.")
        
def notification_battery_level(sender, data):
    valore = struct.unpack('>i', data)[0]
    if valore < 0 or valore > 100:
        print(f"Errore! La percentuale di batteria era {valore} %")
        return
        
    print(f"Percentuale della batteria: {valore}")
    
    # invoca la funzione da eseguire per gestire l'arrivo di una nuova percentuale
    if update_battery_level_callback:
        update_battery_level_callback(valore)
    else:
        print("Nessuna funzione di callback assegnata per gestire le notifiche.")

# Iscrive il client alle notifiche del server (per ricevere i dati)
async def start_measurement_notify(client):
    # ad ogni notifica ricevuta sulla caratteristica con uuid MEASUREMENT_NOTIFICATION_CHARACTERISTIC_UUID,
    # viene eseguita la funzione notification_float_handler
    await client.start_notify(MEASUREMENT_NOTIFICATION_CHARACTERISTIC_UUID,
                              notification_float_handler)
    print("Notifiche sulla misurazione attivate")
    
# Interrompe la ricezione delle notifiche
async def stop_measurement_notify(client):
    await client.stop_notify(MEASUREMENT_NOTIFICATION_CHARACTERISTIC_UUID)
    print("Notifiche sulla misurazione fermate")
    
async def start_battery_level_notify(client):
    # ad ogni notifica ricevuta sulla caratteristica con uuid BATTERY_LEVEL_NOTIFICATION_CHARACTERISTIC_UUID,
    # viene eseguita la funzione 
    print("safdisaid")
    await client.start_notify(BATTERY_LEVEL_NOTIFICATION_CHARACTERISTIC_UUID,
                              notification_battery_level)
    print("Notifiche sulla percentuale di batteria attivate")
    
async def stop_battery_level_notify(client):
    # ad ogni notifica ricevuta sulla caratteristica con uuid BATTERY_LEVEL_NOTIFICATION_CHARACTERISTIC_UUID,
    # viene eseguita la funzione 
    await client.stop_notify(BATTERY_LEVEL_NOTIFICATION_CHARACTERISTIC_UUID)
    print("Notifiche sulla percentuale di batteria attivate")

# SEZIONE COMANDI

# Costanti
START_COMMAND = "start"
STOP_COMMAND = "stop"

# invia al server il comando di start e si mette in ascolto per le notiche
async def start_board(client):
    await send_command(client, START_COMMAND)
    await start_measurement_notify(client)

# invia al server il comando di stop e interrompe l'ascolto per le notiche
async def stop_board(client):
    await stop_measurement_notify(client)
    await send_command(client, STOP_COMMAND)

# funzione generica per inviare il comando "command"
async def send_command(client, command):
    try:
        # Scrive il comando sulla caratteristica specifica
        await client.write_gatt_char(COMMAND_CHARACTERISTIC_UUID, command.encode("utf-8"))
        print(f"Comando {command} inviato")
    except BleakError as e:
        print(f"Errore durante l'invio del comando: {e}")