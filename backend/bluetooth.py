import asyncio
import threading
import tkinter as tk
from tkinter import scrolledtext
from bleak import BleakScanner, BleakClient, BleakError
import datetime

# Variabili globali
loop = asyncio.new_event_loop()

# Funzione per avviare l'event loop in un thread separato
def start_event_loop():
    asyncio.set_event_loop(loop)
    loop.run_forever()

# Avvia l'event loop in un thread
threading.Thread(target=start_event_loop, daemon=True).start()

# Funzione per avviare la scansione in un thread
def run_scan_thread(target_name, target_address, items, status_var):
    loop.call_soon_threadsafe(asyncio.create_task, start_scan(target_name, target_address, items, status_var))

# Funzione per avviare la connessione in un thread
def run_connection_thread(device_name, device_address, status_var):
    loop.call_soon_threadsafe(asyncio.create_task, connect_to_device(device_name, device_address, status_var))

# Funzione per avviare la scansione dei dispositivi Bluetooth
async def start_scan(target_name, target_address, items, status_var):
    try:
        status_var.set("Scansione in corso...")
        devices = await BleakScanner.discover(timeout=10)  # Scansione per 10 secondi

        if devices:
            for device in devices:
                log_device(device)
                add_device(device, items)

        else:
            status_var.set("Nessun dispositivo trovato")

        status_var.set("Scansione completata.\nPremi Ricerca per rifare la scansione")
    except BleakError as e:
        status_var.set(f"Errore Bluetooth: {e}")
    except Exception as e:
        status_var.set(f"Errore inaspettato: {e}")

# Aggiunge il dispositivo alla lista
def add_device(device, devices):
    devices.append({'name': device.name or "Sconosciuto", 'address': device.address})

# Logger in console
def log_device(device):
    device_name = device.name or "Sconosciuto"
    log_entry = f"{datetime.datetime.now()} - Nome: {device_name}, Indirizzo: {device.address}, RSSI: {device.rssi} dBm\n"
    print(log_entry)

async def connect_to_device(device_name, device_address, status_var):
    try:
        status_var.set(f"Connessione a {device_name}...")
        client = BleakClient(device_address)
        await client.connect()

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
    def notification_handler(sender, data):
        print(f"Notifica ricevuta: {data}")

    await client.start_notify(CHARACTERISTIC_UUID, notification_handler)

    message = "Ciao, dispositivo BLE!"
    command = message.encode('utf-8')

    await client.write_gatt_char(CHARACTERISTIC_UUID, command)
    print(f"Comando inviato: {message}")

    await asyncio.sleep(10)  # Tempo di attesa per ricevere risposte