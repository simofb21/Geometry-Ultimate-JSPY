'''
server flask in esecuzione su raspberry, che riceve x, y da arduino via post, aggiorna  la pagina get_position , dove andrà js a leggere x,y
'''
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
current_position = {"x": 0, "y": 0}

@app.route('/')
def home(): 
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 