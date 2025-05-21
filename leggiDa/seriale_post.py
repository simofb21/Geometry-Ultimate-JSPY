'''
Questo script viene eseguito sul pc : legge i dati inviati tramite seriale da Arduino e li invia a un server Flask in esecuzione su un altro computer.
I dati devono essere in formato JSON e devono contenere le chiavi "X" e "Y" per rappresentare le coordinate.
L' invio avviene tramite una richiesta POST al server Flask contente x,y in formato json.
'''
import serial
import requests
import json

ser = serial.Serial(
    port='COM5',  # Cambia con la porta corretta
    baudrate=9600,
    timeout=1
)

url = "http://10.0.98.30:5000/update_position"  # Cambia con l'IP corretto

print("i am currently listening your messages")

def send_position(x, y):
    """
    Invia posizione con POST a /update_position
    """
    data = {
        "x": x,
        "y": y,
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

def send_click(click):
    """
    Invia click con POST a /update_position
    """
    data = {"click": click}
    try:
        response = requests.post(url, json=data)
        if response.status_code == 204:
            print("Click aggiornato con successo")
        else:
            print(f"Errore: {response.status_code}")
    except requests.ConnectionError as e:
        print(f"Connection error: {e}")
    except requests.Timeout as e:
        print(f"Request timed out: {e}")

try:
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            print(f"Received: {data}")
            try:
                position = json.loads(data)
                if "X" in position and "Y" in position and "CLICK" in position:
                    x = position["X"]
                    y = position["Y"]
                    click = position["CLICK"]
                    print(f"X: {x}, Y: {y}, CLICK: {click}")
                    send_position(x, y)  # invia sempre posizione
                    send_click(click)  # invia click solo se click == 1
                else:
                    print(f"Invalid data format: {data}")
            except json.JSONDecodeError:
                print(f"Error decoding JSON: {data}")
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    ser.close()