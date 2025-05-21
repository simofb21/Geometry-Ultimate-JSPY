'''
server flask in esecuzione su raspberry, che riceve x, y,click da arduino via post, aggiorna  la pagina get_position , dove andrà js a leggere x,y
'''
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
current_position = {"x": 0, "y": 0}
cliccato  = 0

@app.route('/')
def home(): 
    return render_template('index.html')

@app.route('/send_click', methods=['POST']) #se richieste post a send click
def send_click():
    data = request.get_json()
    if data and "click" in data:
        cliccato = data["click"] #aggiorna il click a quello ricevuto
        print(f"Click: {cliccato}")

@app.route('/isCliccato', methods=['GET']) #se richieste get a is cliccato
def isCliccato():
    return jsonify({"cliccato": cliccato}) #restituisce il click corrente in formato json
@app.route('/update_position', methods=['POST']) # se richieste post  a update position
def update_position():
    data = request.get_json()
    if data and "x" in data and "y" in data: #aggiorna x,y a quelle ricevute
        current_position["x"] = data["x"]
        current_position["y"] = data["y"]
        return "", 204 # ok
    return "Bad Request", 400 #problemi

@app.route('/get_position', methods=['GET'])
def get_position():
    return jsonify(current_position) #mostra le coordinate correnti . ci accedo alla risorsa tramite richiesta get,quindi posso farlo anche da browser

@app.route('/send_email',methods=['POST'])
def send_email():
    data = request.get_json().get('email') #prendo l'email dal json ricevuto
    punteggio = request.get_json().get('punteggio') #prendo il punteggio dal json ricevuto
    # Dati di accesso e destinatario
    gmail_user = 'simofusar@gmail.com'
    app_password = 'opab crhv rhun szki'
    to_email = data

    # Composizione del messaggio
    subject = 'Punteggio ottenuto su Geometry Ultimate JSPY'
    body = 'Dunque , hai richiesto di sapere il tuo punteggio per mail , eccolo\nIl tuo punteggio è: ' + str(punteggio) + '\n\nGrazie per aver giocato a Geometry Ultimate JSPY!'

    # Creazione messaggio
    message = MIMEMultipart()
    message['From'] = gmail_user
    message['To'] = to_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    try:
        # Connessione al server SMTP di Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Crittografia TLS
        server.login(gmail_user, app_password)
        server.send_message(message)
        print('Email inviata con successo!')
    except Exception as e:
        print('Errore durante l\'invio:', e)
    finally:
        server.quit()


    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 