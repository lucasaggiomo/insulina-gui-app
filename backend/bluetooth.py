import asyncio
import threading
import tkinter as tk
from tkinter import scrolledtext
from bleak import BleakScanner
from bleak import BleakClient
from bleak.exc import BleakError
import datetime
import os
import sys

# esecuzione asincrona della scansione
def run_scan_thread(target_name, target_address, items, status_var):
   asyncio.run(start_scan(target_name, target_address, items, status_var))
   
# esecuzione asincrona nella connessione
def run_connection_thread(device_name, device_address, status_var):
    asyncio.run(connect_to_device(device_name, device_address, status_var))
    
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
            await communicate(client)
            return True
        else:
            status_var.set(f"Impossibile connettersi a {device_address}")
            return False
            
    except BleakError as e:
        status_var.set(f"Errore di connessione: {e}")
        return False
    
    except Exception as e:
        status_var.set(f"Errore inaspettato: {e}")
        return False
    
# UUID del servizio e della caratteristica
SERVICE_UUID = "D0611E78-BBB4-4591-A5F8-487910AE4366"
CHARACTERISTIC_UUID = "8667556C-9A37-4C91-84ED-54EE27D90049"

async def communicate(client):
    # Funzione di callback per le notifiche
    def notification_handler(sender, data):
        print(f"Notifica ricevuta: {data}")

    # Iscrizione alle notifiche
    await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
    
    # La stringa che vuoi inviare
    message = "Ciao, dispositivo BLE!"

    # Codifica la stringa in UTF-8 per ottenere una sequenza di byte
    command = message.encode('utf-8')

    # Invio del comando codificato in UTF-8
    await client.write_gatt_char(CHARACTERISTIC_UUID, command)
    print(f"Comando inviato: {message}")

    # Tempo di attesa per ricevere risposte (ad esempio 10 secondi)
    await asyncio.sleep(10)


# async def send_command(client, command):
#     try:
#         # Scrive il comando sulla caratteristica specifica
#         await client.write_gatt_char(UUID_COMANDO, command)
#     except BleakError as e:
#         print(f"Errore durante l'invio del comando: {e}")

# async def start_device(client):
#     # Comando specifico per avviare il dispositivo
#     command = b'\x01'  # Esempio: il byte 0x01 rappresenta "start"
#     await send_command(client, command)

# async def stop_device(client):
#     # Comando specifico per fermare il dispositivo
#     command = b'\x02'  # Esempio: il byte 0x02 rappresenta "stop"
#     await send_command(client, command)
