/*
Il seguente codice consente all' arduino di leggere i dati x e y di un joystick e di inviarli tramite seriale in formato JSON.
*/
int xAxisPin = 0; //  X pin Joystick
int yAxisPin = 1; // pin y joystick

typedef struct {
  int x;
  int y;
} Joystick;

void setup() {
  Serial.begin(9600); // inizializzo seriale
}

void loop() {
  Joystick joystick;
  joystick.x = analogRead(xAxisPin); // leggo x 
  joystick.y = analogRead(yAxisPin); //leggo y

  Serial.print("{ \"X\" : "); //stampo 
  Serial.print(joystick.x);
  Serial.print(", \"Y\" : ");
  Serial.print(joystick.y);
  Serial.println(" }");

  delay(200);
}
