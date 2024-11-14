import asyncio
import threading
from bleak import BleakScanner
from bleak import BleakClient
from bleak.exc import BleakError
import datetime
import struct

# esecuzione asincrona della scansione
def run_scan_thread(target_name, target_address, items, status_var):
   asyncio.run(start_scan(target_name, target_address, items, status_var))
   
# esecuzione asincrona nella connessione
def run_connection_thread(device_name, device_address, status_var):
    return asyncio.run(connect_to_device(device_name, device_address, status_var))
    
    
# Function to start scanning for Bluetooth devices
async def start_scan(target_name, target_address, items, status_var):
    try:
        print("Scansione in corso...\n")
        status_var.set("Scansione in corso...")
        
        # Increase the scanning timeout to give the adapter more time to detect devices
        devices = await BleakScanner.discover(timeout=10)  # Scanning for 10 seconds
 
        if devices:
           for device in devices:
                log_device(device)
                add_device(device, items)
 
                # # Controlla se rispetta i filtri
                # if matches_filter(device, target_name, target_address):
                #     print(f"Matched Device: {device.name or 'Sconosciuto'}, Address: {device.address}\n")
 
        else:
            print("Nessun dispositivo trovato\n")
            status_var.set("Nessun dispositivo trovato")
 
        print("Scansione completata.\n")
        status_var.set("Scansione completata.\nPremi Ricerca per rifare la scansione")
 
    except BleakError as e:
        print(f"Bluetooth error: {e}\n")
        status_var.set(f"Bluetooth error: {e}\nControlla se il bluetooth è attivo")
    except Exception as e:
        print(f"Unexpected error: {e}\n")
        status_var.set(f"Unexpected error: {e}\nControlla se il bluetooth è attivo")
 
# aggiunge il device alla lista
def add_device(device, devices):
   devices.append(
       {'name': device.name or "Sconosciuto", 'address': device.address}
   )
 
 
# logger in console
def log_device(device):
    device_name = device.name or "Sconosciuto"
    log_entry = f"{datetime.datetime.now()} - Name: {device_name}, Address: {device.address}, RSSI: {device.rssi} dBm\n"
    print(log_entry)
 
 
# verifica se il device corrisponde ai filtri target_name e target_address
def matches_filter(device, target_name, target_address):
   return ((target_name.lower() in (device.name or "").lower()) if target_name else True) and \
          ((target_address.lower() in device.address.lower()) if target_address else True)

async def connect_to_device(device_name, device_address, status_var):
    try:
        status_var.set(f"Connessione a {device_name}...")
        
        # effettua la connessione
        client = BleakClient(device_address)
        await client.connect()
            
        # Controlla se ci si è connessi correttamente
        if client.is_connected:
            status_var.set(f"Connesso a {device_name}")
            return client
        
        # caso in cui non è conneso
        status_var.set(f"Impossibile connettersi a {device_address}")
        return None
            
    except BleakError as e:
        status_var.set(f"Errore di connessione: {e}")
        return None
    
    except Exception as e:
        status_var.set(f"Errore inaspettato: {e}")
        return None
    
# UUID del servizio e della caratteristica
SERVICE_UUID = "26e29ec9-3491-4d42-b816-d081936e2edc"
COMMAND_CHARACTERISTIC_UUID = "9b3c81d8-57b1-4a8a-b8df-0e56f7ca51c2"
NOTIFICATION_CHARACTERISTIC_UUID = "9fbf120d-6301-42d9-8c58-25e699a21dbd"

# funzione da eseguire per gestire l'arrivo di una nuova lettura
# questa variabile (che va inteso come un "puntatore a funzione") va inizializzata nella classe dell'App
notification_function_callback = None

# Funzione di callback per gestire le notifiche
def notification_text_handler(sender, data):
    testo_ricevuto = data.decode('utf-8')  # Decodifica i byte come stringa UTF-8
    print(f"Testo ricevuto: {testo_ricevuto}")
    
    # invoca la funzione da eseguire per gestire l'arrivo di una nuova lettura
    if notification_function_callback:
        notification_function_callback(testo_ricevuto)
    else:
        print("Nessuna funzione di callback assegnata per gestire le notifiche.")
    
def notification_float_handler(sender, data):
    # Decodifica i dati come float a 4 byte (usa "d" per double, che è 8 byte)
    numero = struct.unpack('<f', data)[0]  # '<f' indica un float in formato little-endian
    print(f"Numero float ricevuto: {numero}")
    
    # invoca la funzione da eseguire per gestire l'arrivo di una nuova lettura
    if notification_function_callback:
        notification_function_callback(numero)
    else:
        print("Nessuna funzione di callback assegnata per gestire le notifiche.")
        
def notification_handler_new(sender, data):
    # Controlla che i dati siano di 4 byte (FLOAT 32)
    if len(data) == 4:
        # Decodifica i dati IEEE-11073 FLOAT 32
        
        print(f"Data: {data}")
        print(f"type of data: {type(data)}")
        
        valore = struct.unpack('>i', data)[0]
        print(f"Numero FLOAT 32 IEEE-11073 ricevuto: {valore}")
        
        # invoca la funzione da eseguire per gestire l'arrivo di una nuova lettura
        if notification_function_callback:
            notification_function_callback(valore)
        else:
            print("Nessuna funzione di callback assegnata per gestire le notifiche.")

    else:
        print("Dati di lunghezza inattesa per FLOAT 32 IEEE-11073")
        
# Iscrive il client alle notifiche del server (per ricevere i dati)
async def start_notify(client):
    # ad ogni notifica ricevuta sulla caratteristica con uuid NOTIFICATION_CHARACTERISTIC_UUID,
    # viene eseguita la funzione notification_float_handler
    await client.start_notify(NOTIFICATION_CHARACTERISTIC_UUID,
                              notification_handler_new)
    print("Notifiche attivate")
    
# Interrompe la ricezione delle notifiche
async def stop_notify(client):
    await client.stop_notify(NOTIFICATION_CHARACTERISTIC_UUID)
    print("Notifiche fermate")

# SEZIONE COMANDI

# Costanti
START_COMMAND = "start"
STOP_COMMAND = "stop"

# invia al server il comando di start e si mette in ascolto per le notiche
async def start_board(client):
    await send_command(client, START_COMMAND)
    await start_notify(client)

# invia al server il comando di stop e interrompe l'ascolto per le notiche
async def stop_board(client):
    await stop_notify(client)
    await send_command(client, STOP_COMMAND)

# funzione generica per inviare il comando "command"
async def send_command(client, command):
    try:
        # Scrive il comando sulla caratteristica specifica
        await client.write_gatt_char(COMMAND_CHARACTERISTIC_UUID, command.encode("utf-8"))
        print(f"Comando {command} inviato")
    except BleakError as e:
        print(f"Errore durante l'invio del comando: {e}")