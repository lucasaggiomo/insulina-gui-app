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
async def start_scan(target_name, target_address, display_box):
   display_box.insert(tk.END, "Checking Bluetooth adapter status...\n")
   display_box.see(tk.END)
 
 
   # Check Bluetooth permissions and adapter status on Linux/macOS
   if sys.platform == "linux" or sys.platform == "darwin":
       check_bluetooth_permissions(display_box)
 
 
   try:
       # Increase the scanning timeout to give the adapter more time to detect devices
       devices = await BleakScanner.discover(timeout=10)  # Scanning for 10 seconds
       display_box.insert(tk.END, "Scanning for Bluetooth devices...\n")
       display_box.see(tk.END)
 
 
       if devices:
           for device in devices:
               log_device(device)  # Log all devices detected
               display_device(device, display_box)  # Show all devices in display box
 
 
               # Check if it matches filter criteria
               if matches_filter(device, target_name, target_address):
                   display_box.insert(tk.END, f"Matched Device: {device.name or 'Unknown'}, Address: {device.address}\n")
                   display_box.see(tk.END)
 
 
       else:
           display_box.insert(tk.END, "No devices found.\n")
           display_box.see(tk.END)
 
 
       display_box.insert(tk.END, "Scan complete.\n")
       display_box.see(tk.END)
 
 
   except BleakError as e:
       display_box.insert(tk.END, f"Bluetooth error: {e}\n")
       display_box.see(tk.END)
   except Exception as e:
       display_box.insert(tk.END, f"Unexpected error: {e}\n")
       display_box.see(tk.END)
 
 
# Function to display the discovered devices in the text box
def display_device(device, display_box):
   device_name = device.name or "Unknown"
   display_box.insert(tk.END, f"Found Device - Name: {device_name}, Address: {device.address}, RSSI: {device.rssi} dBm\n")
   display_box.see(tk.END)
 
 
# Function to log the discovered devices to a file
def log_device(device):
   device_name = device.name or "Unknown"
   with open("bluetooth_scan_log.txt", "a") as log_file:
       log_entry = f"{datetime.datetime.now()} - Name: {device_name}, Address: {device.address}, RSSI: {device.rssi} dBm\n"
       log_file.write(log_entry)
 
 
# Function to check if a device matches the given filter
def matches_filter(device, target_name, target_address):
   return ((target_name.lower() in (device.name or "").lower()) if target_name else True) and \
          ((target_address.lower() in device.address.lower()) if target_address else True)
 
 
# Function to check and grant Bluetooth permissions on Linux/macOS
def check_bluetooth_permissions(display_box):
   if sys.platform == "linux":
       # Check if Bluetooth is blocked
       rfkill_output = os.popen("rfkill list bluetooth").read()
       if "Soft blocked: yes" in rfkill_output or "Hard blocked: yes" in rfkill_output:
           display_box.insert(tk.END, "Bluetooth is blocked. Attempting to unblock...\n")
           os.system("sudo rfkill unblock bluetooth")
           os.system("sudo hciconfig hci0 up")
           display_box.insert(tk.END, "Bluetooth unblocked.\n")
           display_box.see(tk.END)
   elif sys.platform == "darwin":
       # macOS-specific check (usually requires system-level permissions)
       display_box.insert(tk.END, "Ensure Bluetooth permissions are granted in System Preferences > Security & Privacy > Privacy > Bluetooth.\n")
       display_box.see(tk.END)
 
 
# Function to run asyncio in a thread
def run_scan_thread(target_name, target_address, list_box):
   asyncio.run(start_scan(target_name, target_address, list_box))
 
 
# # Setting up the Tkinter GUI
# root = tk.Tk()
# root.title("Bluetooth Scanner - The Pycodes")
 
 
# # Label for name filter
# name_label = tk.Label(root, text="Filter by Device Name:")
# name_label.grid(column=0, row=0)
 
 
# # Entry for name filter
# name_filter = tk.Entry(root, width=40)
# name_filter.grid(column=1, row=0)
 
 
# # Label for address filter
# address_label = tk.Label(root, text="Filter by Device Address:")
# address_label.grid(column=0, row=1)
 
 
# # Entry for address filter
# address_filter = tk.Entry(root, width=40)
# address_filter.grid(column=1, row=1)
 
 
# # Button to start scanning
# scan_button = tk.Button(root, text="Start Scan", command=scan_button_click)
# scan_button.grid(column=0, row=2, columnspan=2)
 
 
# # Scrolled text box to display the scan results
# display_box = scrolledtext.ScrolledText(root, width=60, height=20)
# display_box.grid(column=0, row=3, columnspan=2)
 
 
