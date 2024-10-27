import asyncio
import threading
import tkinter as tk
from tkinter import scrolledtext
from bleak import BleakScanner
from bleak.exc import BleakError
import datetime
import os
import sys
 
 
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
 
# esecuzione asincrona della scansione
def run_scan_thread(target_name, target_address, items, status_var):
   asyncio.run(start_scan(target_name, target_address, items, status_var))