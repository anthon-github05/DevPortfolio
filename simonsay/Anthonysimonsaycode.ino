#include <EEPROM.h> 

const int startButtonPin = A2, buzzerPin = 6, buttonPins[4] = {A2, A3, A4, A5}, ledPins[4] = {2, 3, 4, 5}; // 5=led green, 4=led red, 3=led yellow, 2=led blue
int sequence[31], currentStep = 0, playerStep = 0;
bool gameRunning = false;
const int tones[4] = {659, 261, 220, 165}; // Frequencies for each button: Mi3, Do3, La2, Mi2
const int errorTone = 130; // Frequency for error sound: Do1

//initialize the start button and pin
void setup() {
  pinMode(startButtonPin, INPUT_PULLUP);
  for (int i = 0; i < 4; i++) {
    pinMode(buttonPins[i], INPUT_PULLUP);
    pinMode(ledPins[i], OUTPUT);
  }
  pinMode(buzzerPin, OUTPUT);

  
  unsigned int seed = EEPROM.read(0) + 1;
  if (seed > 255) seed = 0; 
  EEPROM.write(0, seed);


  randomSeed(seed);
}

void loop() {
  // Check if the start button is pressed
  if (digitalRead(startButtonPin) == LOW && !gameRunning) {
    gameRunning = true;
    startGame();
  }

  if (gameRunning) {
    checkPlayerInput();
  }
}
// startgame + jingle + sequence
void startGame() {
  // Play a jingle
  playJingle();
  delay(300); // Wait for 3 seconds after the jingle
  // Initialize the sequence with one random step
  sequence[0] = random(0, 4);
  currentStep = 0;
  playerStep = 0;
  
  // Play the first step of the sequence
  playSequence();
}

// play a jingle
void playJingle() {
  for (int i = 0; i < 4; i++) {
    digitalWrite(ledPins[i], HIGH);
    tone(buzzerPin, tones[i], 200); // Different tone for each LED
    delay(200);
    digitalWrite(ledPins[i], LOW);
    delay(100); // Short delay between steps
  }
}

void playErrorTone() {
  // Play song for error and leds blink 3 times
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 4; j++) {
      digitalWrite(ledPins[j], HIGH);
    }
    tone(buzzerPin, errorTone, 300); // erreur musicale-note Do1
    delay(300);
    for (int j = 0; j < 4; j++) {
      digitalWrite(ledPins[j], LOW);
    }
    delay(300);
  }
}

void playVictoryJingle() {
  // Play a victory tone sequence with each LED lighting up one at a time
  for (int i = 0; i < 4; i++) {
    digitalWrite(ledPins[i], HIGH);
    tone(buzzerPin, tones[i], 300); // Different tone for each LED
    delay(300);
    digitalWrite(ledPins[i], LOW);
    delay(150); // Short delay between steps
  }
}
// function playsequence
void playSequence() {
  for (int i = 0; i <= currentStep; i++) {
    playStep(sequence[i]);
  }
}

void playStep(int step) {
  digitalWrite(ledPins[step], HIGH);
  tone(buzzerPin, tones[step], 200); // Play the tone for the step
  delay(200);
  digitalWrite(ledPins[step], LOW);
  delay(100); // Short delay after the step
}

// function check + sequence + conditions + win and loose
void checkPlayerInput() {
  for (int i = 0; i < 4; i++) {
    if (digitalRead(buttonPins[i]) == LOW) {
      if (i == sequence[playerStep]) {
        playStep(i);
        playerStep++;
        if (playerStep > currentStep) {
          if (currentStep == 31) { // Victory condition after 31 steps
            playVictoryJingle();
            gameRunning = false;
          } else {
            currentStep++;
            sequence[currentStep] = random(0, 4);
            playerStep = 0;
            delay(500); // Short delay before playing the next sequence
            playSequence();
          }
        }
      } else {
        playErrorTone(); // Play the error song 
        delay(500); // short delay
        startGame(); // Rrestart the game + 1 sequence
      }
      delay(300); // Debounce delay
    }
  }
}
