'''
Codice di prova usato solo per leggere i dati da seriale e stampare a video , eseguito sul pc windows
'''
import serial

# lo usiamo da windows
# Configura la porta seriale : assicurati di usare la porta corretta per il tuo dispositivo Bluetooth , se si usa windows è com5, o com7 ecc
# se si usa linux o raspberry è /dev/ttyUSB0 o /dev/rfcomm0 ecc
ser = serial.Serial(
    port='COM5',  # così è da pc, sarà da cambiare con la porta seriale del raspberry
    baudrate=9600,
    timeout=1
)

print("i am currently listening your messages")

try:
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            print(f"Received: {data}")
            # legge da seriale e stampa a video

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    ser.close()