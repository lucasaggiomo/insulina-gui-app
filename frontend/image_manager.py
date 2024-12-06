# Progetto GUI misuratore d'insulina - A.A. 2024/2025 Corso di Laboratorio di Misure
# Autori:
# Saggiomo Luca
# Saccone Matteo
# Romano Davide
# Ponticelli Lorenzo
# Porcelli Nicola

import tkinter as tk

# gestione path per poter caricare le immagini correttamente
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# classe per gestire tutte le immagini del programma
class ImageManager:
    
    # carica tutte le immagini in variabili statiche della classe
    @staticmethod
    def load_images():
        ImageManager.battery_low_image = tk.PhotoImage(file='images/Battery_low.png').subsample(15,15)
        ImageManager.battery_medium_image = tk.PhotoImage(file='images/Battery_medium.png').subsample(15,15)
        ImageManager.battery_high_image = tk.PhotoImage(file='images/Battery_high.png').subsample(15,15)
        ImageManager.battery_max_image = tk.PhotoImage(file='images/Battery_max.png').subsample(15,15)
            
        ImageManager.bluetooth_image = tk.PhotoImage(file='images/Bluetooth.png').subsample(40,40)

        ImageManager.start_image = tk.PhotoImage(file='images/Start.png').subsample(25,25)
        ImageManager.stop_image = tk.PhotoImage(file='images/Stop.png').subsample(35,35)
        ImageManager.trash_image = tk.PhotoImage(file='images/Garbage.png').subsample(4,4)

        ImageManager.excel_image = tk.PhotoImage(file='images/Excel_logo_2k.png').subsample(30,30)
        ImageManager.pdf_image = tk.PhotoImage(file='images/Pdf_logo_white.png').subsample(30,30)

    # funzione che restituisce l'immagine della batteria in base alla percentuale
    def get_battery_image(percentage):
        # limita la percentuale tra 0 e 100
        percentage = max(0.0, min(percentage, 100.0))  

        if percentage < 25.0:
            return ImageManager.battery_low_image
        elif 25.0 <= percentage < 50:
            return ImageManager.battery_medium_image
        elif 50.0 <= percentage < 75:
            return ImageManager.battery_high_image
        else:
            return ImageManager.battery_max_image