// Define the pin where the limit switch is connected
const int limitSwitchPin = 2;

// Variables to store the previous state and the last debounced state
int previousSwitchState = HIGH;
int lastDebouncedState = HIGH;
unsigned long debounceTime = 80; // Debounce time in milliseconds

void setup() {
  // Initialize serial communication
  Serial.begin(9600);

  // Set the limit switch pin as an input with internal pull-up resistor enabled
  pinMode(limitSwitchPin, INPUT_PULLUP);
}

void loop() {
  // Read the current state of the switch
  int switchState = digitalRead(limitSwitchPin);

  // Check if the state has changed
  if (switchState != previousSwitchState) {
    // Record the time of the state change
    unsigned long currentTime = millis();

    // If the time since the last state change is greater than the debounce time
    if (currentTime - lastDebouncedState > debounceTime) {
      if (switchState == LOW) {
        // The switch is pressed
        Serial.println("Switch Released");
      } else {
        // The switch is released
        Serial.println("Switch Pressed");
      }

      // Update the last debounced state
      lastDebouncedState = currentTime;
    }
  }

  // Update the previous switch state
  previousSwitchState = switchState;
}
