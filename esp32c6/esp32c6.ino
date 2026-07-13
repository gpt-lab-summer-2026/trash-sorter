// Auto-sweep servo control for ESP32-C6-DevKitC-1  (NO ESP32Servo library, no joystick)
// Arduino-ESP32 core 3.x API: ledcAttach() / ledcWrite()
// Both servos sweep smoothly between (base - deflect) and (base + deflect), back and forth.
// Button on GPIO2 pauses / resumes the sweep.
// Set Tools > USB CDC On Boot > Enabled for Serial output.

#define button 2
#define servo1_pin 11
#define servo2_pin 10 

#define SERVO_FREQ 50
#define SERVO_RES  12

// --- Center + travel (same idea as before: base +/- deflect) ---
#define BASE_US     1300   // center position (us)
#define DEFLECT_US  700    // swing each side of base; ~11.1 us/deg -> 889 ~= 80 deg

// --- Absolute safe limits: never command beyond these ---
#define SERVO_US_ABS_MIN 400
#define SERVO_US_ABS_MAX 2600

// --- Sweep speed ---
#define STEP_US      8     // us change per update (bigger = faster)
#define UPDATE_MS    20    // ms between updates
#define NUDGE_US     50

int servo1_current_pos = BASE_US;
int servo2_current_pos = BASE_US;

int Mode = 0, flag = 0;

int lo() { return (BASE_US - DEFLECT_US < SERVO_US_ABS_MIN) ? SERVO_US_ABS_MIN : BASE_US - DEFLECT_US; }
int hi() { return (BASE_US + DEFLECT_US > SERVO_US_ABS_MAX) ? SERVO_US_ABS_MAX : BASE_US + DEFLECT_US; }

uint32_t usToDuty(uint32_t us) {
  return (uint32_t)((uint64_t)us * ((1UL << SERVO_RES) - 1) / 20000UL);
}

int clampUs(int us) {
  if (us < lo()) us = lo();
  if (us > hi()) us = hi();
  return us;
}

void writeUs(int pin, int us) {
  ledcWrite(pin, usToDuty(clampUs(us)));
}

void testFunc() {
  if (Serial.available() > 0) {
    char cmd = Serial.read();

    if (cmd == 'p') {
      Mode = !Mode;
      Serial.print("Mode = "); Serial.println(Mode);
    }
    else if (cmd == 'w') {                 // servo2 up
      servo2_current_pos = clampUs(servo2_current_pos - NUDGE_US);
      writeUs(servo2_pin, servo2_current_pos);
    }
    else if (cmd == 's') {                 // servo2 down
      servo2_current_pos = clampUs(servo2_current_pos + NUDGE_US);
      writeUs(servo2_pin, servo2_current_pos);
    }
    else if (cmd == 'a') {                 // servo1 up
      servo1_current_pos = clampUs(servo1_current_pos + NUDGE_US);
      writeUs(servo1_pin, servo1_current_pos);
    }
    else if (cmd == 'd') {                 // servo1 down
      servo1_current_pos = clampUs(servo1_current_pos - NUDGE_US);
      writeUs(servo1_pin, servo1_current_pos);
    }
    else if (cmd == 'b') {                 // both to base
      servo1_current_pos = BASE_US;
      servo2_current_pos = BASE_US;
      writeUs(servo1_pin, servo1_current_pos);
      writeUs(servo2_pin, servo2_current_pos);
    }
    else if (cmd == 'S') {                 // absolute position: "S<us1>,<us2>\n"
      String line = Serial.readStringUntil('\n');
      int commaIdx = line.indexOf(',');
      if (commaIdx <= 0) return;
      servo1_current_pos = clampUs(line.substring(0, commaIdx).toInt());
      servo2_current_pos = clampUs(line.substring(commaIdx + 1).toInt());
      writeUs(servo1_pin, servo1_current_pos);
      writeUs(servo2_pin, servo2_current_pos);
    }
    else {
      return;  // ignore newlines / unknown keys
    }

    Serial.print("s1="); Serial.print(servo1_current_pos);
    Serial.print(" s2="); Serial.println(servo2_current_pos);
  }
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("Boot");

  pinMode(button, INPUT_PULLUP);

  bool ok1 = ledcAttach(servo1_pin, SERVO_FREQ, SERVO_RES);
  bool ok2 = ledcAttach(servo2_pin, SERVO_FREQ, SERVO_RES);
  Serial.print("ledcAttach servo1 = "); Serial.println(ok1);
  Serial.print("ledcAttach servo2 = "); Serial.println(ok2);

  // set motor to base point
  writeUs(servo1_pin, BASE_US);
  writeUs(servo2_pin, BASE_US);
  delay(700);
}

void loop() {
  testFunc();
}

/*
void loop() {
  // button toggles pause / resume, button from pc
  if (digitalRead(button) == LOW) {
    if (flag == 0) { flag = 1; Mode = !Mode; delay(100); }
  } else {
    flag = 0;
  }

  // press button -> go to that direction to-do:


  if (Mode == 0) {            // sweeping
    pos += dir * STEP_US;
    if (pos >= sweepMax()) { pos = sweepMax(); dir = -1; }
    if (pos <= sweepMin()) { pos = sweepMin(); dir =  1; }

    writeUs(servo1_pin, pos);
    writeUs(servo2_pin, pos);

    Serial.print("pos="); Serial.println(pos);
  }

  delay(UPDATE_MS);
}
*/
