void setup() {
  Serial.begin(9600);

  pinMode(2, OUTPUT);
  pinMode(4, OUTPUT);
  
  digitalWrite(2, HIGH);  // default OFF
  digitalWrite(4, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    String userInput = Serial.readStringUntil('\n');  // Read until newline
    userInput.trim();  // Remove extra whitespace and newline

    if (userInput == "pumpOn") {
      digitalWrite(2, LOW);  // Turn ON pump
      Serial.println("pumpOn");
    } 
    else if (userInput == "pumpOff") {
      digitalWrite(2, HIGH);  // Turn OFF pump
      Serial.println("pumpOff");
    }
  }
}
