const int ldrPin = A0;  // Pin analogico per LDR e potenziometro combinati

int bias = 0;  // Bias dinamico che si aggiorna automaticamente

void setup() {
  Serial.begin(9600);   // Inizializza la comunicazione seriale
  
  // Inizializza il bias con il valore iniziale dell'LDR
  bias = analogRead(ldrPin);
}

void loop() {
  // Legge il valore di luminosità combinato con il potenziometro
  int ldrValue = analogRead(ldrPin);

  // Calcola il valore invertito della luminosità
  int invertedLdrValue = 1023 - ldrValue;

  // Calcola la variazione rispetto al bias
  int differenceFromBias = invertedLdrValue - (1023 - bias);

  // Se il valore è diverso da 0, riporta gradualmente il bias
  if (differenceFromBias != 0) {
    bias = ldrValue;  // Aggiorna il bias al valore corrente
  }

  // Stampa la variazione sul monitor seriale per il plotter
  Serial.println(differenceFromBias);

  delay(110);  // Riduce la frequenza di campionamento
}
