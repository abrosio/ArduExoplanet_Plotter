#include <Stepper.h>

// Numero di passi per una rotazione completa del motore (28BYJ-48 ha 2048 passi)
#define STEPS_PER_REV 2048

// Pin collegati al driver ULN2003AN
#define IN1 2
#define IN2 3
#define IN3 4
#define IN4 5

// Pin del potenziometro
#define POT_PIN A1

// Creazione oggetto Stepper
Stepper stepperMotor(STEPS_PER_REV, IN1, IN3, IN2, IN4);

// Variabile per velocità
int motorSpeed = 0; // Velocità iniziale in RPM
const int MAX_SPEED = 31; // Velocità massima in RPM

void setup() {
  // Imposta velocità iniziale del motore
  stepperMotor.setSpeed(motorSpeed);
}

void loop() {
  // Leggi il valore del potenziometro
  int potValue = analogRead(POT_PIN);

  // Mappa il valore del potenziometro (0-1023) alla velocità (0-MAX_SPEED)
  motorSpeed = map(potValue, 0, 1023, 0, MAX_SPEED);

  // Imposta la velocità del motore
  stepperMotor.setSpeed(motorSpeed);

  // Fai girare il motore solo se la velocità è maggiore di 0
  if (motorSpeed > 0) {
    stepperMotor.step(STEPS_PER_REV / 100); // Fa piccoli movimenti per un loop continuo
  }
}