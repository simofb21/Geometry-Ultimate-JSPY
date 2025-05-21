//script per il gioco che viene eseguito nel browser
// variabili globali per x e y
let x = 0;
let y = 0;
let cliccato = 0;
let snakeSize = 25;
let joystick = true;
let nemici = [];
gameOver = false;
let punteggio = 0;
class Nemico {
    constructor(x, y, size) {
        this.x = x;
        this.y = y;
        this.size = size;
    }
}

// inizializzo randomicamente i nemici
for (let i = 0; i < 10; i++) {
    let x = snakeSize;
    let y = snakeSize;
    let div = window.innerWidth / snakeSize;
    x *= Math.floor(Math.random() * div);
    div = window.innerHeight / snakeSize;
    y *= Math.floor(Math.random() * div);
    nemici.push(new Nemico(x, y, snakeSize));
}

document.addEventListener('keydown', getPositionWasd);

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

async function getPositionWasd(event) { //se va in errore ottengo da wasd
    switch (event.key) {
        case 's':
            y += snakeSize;
            break;
        case 'a':
            x -= snakeSize;
            break;
        case 'w':
            y -= snakeSize;
            break;
        case 'd':
            x += snakeSize;
            break;
        case 'Space':
            cliccato = 1;
            default:
            return;
            
    }
}
async function getPositionJoystick() { //ottengo dal joystick
    try {
        const response = await fetch('http://192.168.1.7:5000/get_position'); // richiesta GET al server
        if (!response.ok) {
            throw new Error('Errore nella richiesta: ' + response.status);
        }
        const data = await response.json(); // converto la risposta in JSON
        

        if (data.x >= 500 && data.x <= 600 && data.y >= 500 && data.y <= 600) {
             // tai fermo
        } else if (data.y <= 100) {
            y -= snakeSize; // vai su
        } else if (data.y >= 900) {
            y += snakeSize; // vai giù
        } else if (data.x >= 800) {
            x += snakeSize; // vai avanti
        } else if (data.x <= 100) {
            x -= snakeSize; // vai indietro
        }

        joystick = true;
    } catch (error) {
        joystick = false;
    }
}

function drawSnake() {
    ctx.clearRect(0, 0, canvas.width, canvas.height); //pulisco il canvas
    ctx.fillStyle = 'green';
    ctx.fillRect(x, y, snakeSize, snakeSize); //disegno
}

function drawEnemies() {
    ctx.fillStyle = 'red';
    nemici.forEach(nemico => {
        ctx.fillRect(nemico.x, nemico.y, nemico.size, nemico.size);
    });
}

function moveSnake() {
    if (joystick)
        getPositionJoystick();
    //altrimenti premendo da tastiera userà wasd  . la funzione getPositionWasd viene chiamata quando avviene l' evento
    if (x < 0) x = canvas.width - snakeSize;
    if (x >= canvas.width) x = 0;
    if (y < 0) y = canvas.height - snakeSize;
    if (y >= canvas.height) y = 0;
}

function moveEnemies() {
    nemici.forEach(nemico => {
        const direction = Math.floor(Math.random() * 4);

        switch (direction) {
            case 0: // su
                nemico.y -= snakeSize;
                break;
            case 1: // giu
                nemico.y += snakeSize;
                break;
            case 2: // sx
                nemico.x -= snakeSize;
                break;
            case 3: // dx
                nemico.x += snakeSize;
                break;
        }
        //controllo 
        if (nemico.x < 0) nemico.x = canvas.width - nemico.size;
        if (nemico.x >= canvas.width) nemico.x = 0;
        if (nemico.y < 0) nemico.y = canvas.height - nemico.size;
        if (nemico.y >= canvas.height) nemico.y = 0;
    });
}
function checkCollision() {
    nemici.forEach(nemico => {
        if (x < nemico.x + nemico.size &&
            x + snakeSize > nemico.x &&
            y < nemico.y + nemico.size &&
            y + snakeSize > nemico.y) {
            gameOver = true;
        }
    });
}
function gameLoop() {
    if(gameOver){
        document.getElementById('gameOver').style.display = 'block';
        document.getElementById('gameCanvas').style.display = 'none';
        document.getElementById('score').innerHTML = punteggio;
        const email = document.getElementById('emailInput').value;
        const data = {
            punteggio: punteggio,
            email: email
        };
         const emailInput = document.getElementById('emailInput');
         if(emailInput){
            fetch('http://IPSERVER:5000/send_email', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
         }  


    }
    moveSnake();
    console.log(x, y);
    drawSnake();
    moveEnemies();
    drawEnemies();
    checkCollision();
}

setInterval(gameLoop, 100); //ogni 100ms chiama gameLoop