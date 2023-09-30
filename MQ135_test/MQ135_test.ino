const int MQ135Pin = A0;  // Assuming the MQ135 sensor is connected to the A0 analog pin
const int CALIBRATION_TIME = 30000;  // 30 seconds in milliseconds
int baseline = 0;

void setup() {
  Serial.begin(9600);   // Start serial communication at 9600 baud rate
  delay(10000);
  
  Serial.println("Calibrating...");

  // Calibration period
  int sum = 0;
  int count = 0;
  unsigned long startTime = millis();
  
  while (millis() - startTime < CALIBRATION_TIME) {
    sum += analogRead(MQ135Pin);
    count++;
    delay(100);  // Read every 100ms during calibration
  }

  // Calculate average reading during calibration
  baseline = sum / count;
  Serial.println("Calibration complete!");
  Serial.print("Baseline value: ");
  Serial.println(baseline);
}

void loop() {
  int mq135Value = analogRead(MQ135Pin);  // Read the value from MQ135 sensor

  Serial.print("MQ135 Analog Value: ");
  Serial.println(mq135Value);
  
  // If you wish to see the difference between the actual reading and the baseline
  Serial.print("Difference from Baseline: ");
  Serial.println(mq135Value - baseline);

  delay(1000);  // Wait for 1 second
}
