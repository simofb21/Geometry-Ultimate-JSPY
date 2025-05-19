'''
Questo script viene eseguito sul pc : legge i dati inviati tramite seriale da Arduino e li invia a un server Flask in esecuzione su un altro computer.
I dati devono essere in formato JSON e devono contenere le chiavi "X" e "Y" per rappresentare le coordinate.
L' invio avviene tramite una richiesta POST al server Flask contente x,y in formato json.
'''
import serial
import requests
import json
# lo usiamo da windows
#codice che funziona in questo modo : comunicazione via seriale tra arduino e pc , e pc comunica con raspberry via post
# quindi il pc legge i dati da arduino e li manda al raspberry via post

# Configura la porta seriale : assicurati di usare la porta corretta per il tuo dispositivo Bluetooth , se si usa windows è com5, o com7 ecc
# se si usa linux o raspberry è /dev/ttyUSB0 o /dev/rfcomm0 ecc
ser = serial.Serial(
    port='COM5',  #così è da pc , sarebbe da cambiare con la porta seriale del raspberry
    baudrate=9600,        
    timeout=1            
)

url = "http://10.0.98.30:5000/update_position"  # da cambiare con ip raspberry a scuola

print("i am currently listening your messages")
        
def send_position(x, y):
    """
   invio posizione con post a pagina update position
    """
    data = {
        "x": x,
        "y": y
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 204:
            print("Posizione aggiornata con successo")
        else:
            print(f"Errore: {response.status_code}")
    except requests.ConnectionError as e: 
        print(f"Connection error: {e}")
    except requests.Timeout as e:
        print(f"Request timed out: {e}")

try:
    while True:
        if ser.in_waiting > 0: # controlla se ci sono dati in arrivo sulla porta seriale
            data = ser.readline().decode('utf-8').strip()
            print(f"Received: {data}")
            #legge da seriale e stampa a video 
            try:
                position = json.loads(data) #se ha ricevuto una x e una y ...
                if "X" in position and "Y" in position:
                    x = position["X"]
                    y = position["Y"]
                    send_position(x, y)  # mette in json i dati e li invia al server
                else:
                    print(f"Invalid data format: {data}")
            except json.JSONDecodeError:
                print(f"Error decoding JSON: {data}")
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    ser.close()