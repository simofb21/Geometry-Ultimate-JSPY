/*
Il seguente codice consente all' arduino di leggere i dati x e y di un joystick e di inviarli tramite seriale in formato JSON.
*/
int xAxisPin = 0; //  X pin Joystick
int yAxisPin = 1; // pin y joystick
int clickPin = 2; // pin click joystick
typedef struct {
  int x;
  int y;
  int click;
} Joystick;

void setup() {
  Serial.begin(9600); // inizializzo seriale
  pinMode(clickPin, INPUT); // imposta il pin click come input

}

void loop() {
    Joystick joystick;
  joystick.x = analogRead(xAxisPin); // leggo x 
  joystick.y = analogRead(yAxisPin); // leggo y
  joystick.click = digitalRead(clickPin); // leggo click

  Serial.print("{ \"X\" : ");
  Serial.print(joystick.x);
  Serial.print(", \"Y\" : ");
  Serial.print(joystick.y);
  Serial.print(", \"CLICK\" : ");
  Serial.print(joystick.click);
  Serial.println(" }");

  delay(200)
}
