import pygatt
import time
from uuid import UUID

# Costanti per il servizio e le caratteristiche BLE
SERVICE_UUID = UUID("12345678-1234-5678-1234-56789abcdef0")
CHARACTERISTIC_UUID = UUID("12345678-1234-5678-1234-56789abcdef1")

# Configurazione dell'adattatore BLE
adapter = pygatt.GATTToolBackend()

# Funzione di callback per la lettura della caratteristica
def handle_read(characteristic):
    print("Client ha letto il valore.")
    # Restituisce un valore simulato; può essere modificato per i test
    return b"Valore di test"

# Funzione di callback per la scrittura nella caratteristica
def handle_write(characteristic, value):
    print(f"Client ha scritto il valore: {value}")
    # Si può anche impostare una risposta specifica a seconda del valore ricevuto

def start_ble_server():
    try:
        adapter.start()
        print("Server BLE in ascolto...")

        # Crea il dispositivo e configura servizi e caratteristiche
        device = adapter.add_device(name="SimulatoreBLE")
        device.add_service(SERVICE_UUID)

        # Aggiungi la caratteristica leggibile e scrivibile
        device.add_characteristic(
            CHARACTERISTIC_UUID,
            properties=["read", "write"],
            read_callback=handle_read,
            write_callback=handle_write,
        )

        # Mantieni il server in esecuzione
        while True:
            time.sleep(1)

    finally:
        adapter.stop()
        print("Server BLE terminato.")

# Avvio del server
if __name__ == "__main__":
    start_ble_server()