#include <Wire.h>
#include <MPU9250.h>
#include <Adafruit_BMP280.h>
#include <DHT.h>



#define DHTPIN 2     // D2 on ESP32
#define DHTTYPE DHT22
#define BUZZER_PIN 8  // D8 on ESP32
#define LED_PIN 9     // D9 on ESP32



const int mq135Pin = A2; 
int baseline = 0; // Variable to store the baseline value for MQ-135
const int mq131Pin = A0;
int baselineMQ131 = 0; // Variable to store the baseline value for MQ-131
const int calibrationTime = 30000; // Calibration time in milliseconds (e.g., 30 seconds)

MPU9250 mpu;
Adafruit_BMP280 bmp;
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  Wire.begin();

  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);


 

  if (!mpu.setup(0x68)) {  // MPU9250 initialization
    while (1) {
      Serial.println("MPU9250 not found!");
      delay(500);
    }
  }

  if (!bmp.begin(0x76)) {  // BMP280 initialization
    while (1) {
      Serial.println("BMP280 not found!");
      delay(500);
    }
  }


  dht.begin();
  calibrateSensor(); // MQ-135 calibration
  calibrateMQ131();  // MQ-131 calibration
  
  

  // Blink LED and Buzzer 3 times after initialization
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(167);  // 1/6 of a second
    digitalWrite(LED_PIN, LOW);
    delay(167);  // 1/6 of a second
  }
  tone(BUZZER_PIN, 1000,1000);
 
}

void loop() {
  // MPU9250, BMP280, DHT22, MQ-135, and MQ-131 readings
  float temperature, pressure_hPa, dht_temperature, humidity;
  mpu.update();
  temperature = bmp.readTemperature()-4;
  pressure_hPa = bmp.readPressure() / 100.0;  // Convert to hectopascals
  dht_temperature = dht.readTemperature();
  humidity = dht.readHumidity();

  // Displaying MPU9250 Readings
  Serial.println("======== MPU9250 Readings ========");
  Serial.print("Accel X: "); Serial.println(mpu.getAcc(0));
  Serial.print("Accel Y: "); Serial.println(mpu.getAcc(1));
  Serial.print("Accel Z: "); Serial.println(mpu.getAcc(2));

  Serial.print("Gyro X: "); Serial.println(mpu.getGyro(0));
  Serial.print("Gyro Y: "); Serial.println(mpu.getGyro(1));
  Serial.print("Gyro Z: "); Serial.println(mpu.getGyro(2));

  Serial.print("Mag X: "); Serial.println(mpu.getMag(0));
  Serial.print("Mag Y: "); Serial.println(mpu.getMag(1));
  Serial.print("Mag Z: "); Serial.println(mpu.getMag(2));

  // Displaying BMP280 Readings
  Serial.println("======== BMP280 Readings ========");
  Serial.print("Temperature: "); Serial.println(temperature);
  Serial.print("Pressure: "); Serial.println(pressure_hPa);

  // Displaying DHT22 Readings
  Serial.println("======== DHT22 Readings ========");
  Serial.print("Temperature: "); Serial.println(dht_temperature);
  Serial.print("Humidity: "); Serial.println(humidity);

  // MQ-135 Readings
  int mq135Value = analogRead(mq135Pin);
  int relativeValue = mq135Value - baseline;

  // Displaying MQ-135 Readings
  Serial.println("======== MQ-135 Readings ========");
  Serial.print("MQ-135 Sensor Value: "); Serial.println(mq135Value);
  Serial.print("Relative Value: "); Serial.println(relativeValue);
  Serial.println("==================================");

  // MQ-131 Readings
  int mq131Value = analogRead(mq131Pin);
  int relativeValueMQ131 = mq131Value - baselineMQ131;

  // Displaying MQ-131 Readings
  Serial.println("======== MQ-131 Readings ========");
  Serial.print("MQ-131 Sensor Value: "); Serial.println(mq131Value);
  Serial.print("Relative Value MQ-131: "); Serial.println(relativeValueMQ131);
  Serial.println("==================================");

  

  delay(40);  // Update all sensors 25 times a second
}

void calibrateSensor() {
  // MQ-135 calibration function
  Serial.println("Calibration started...");
  long sum = 0;
  long startTime = millis();

  // Read and sum up the sensor values during the calibration period
  while (millis() - startTime < calibrationTime) {
    sum += analogRead(mq135Pin);
    delay(10);
  }

  // Calculate the average value to determine the baseline
  baseline = sum / (calibrationTime / 10);
  Serial.print("Calibration completed. Baseline value: ");
  Serial.println(baseline);
}

void calibrateMQ131() {
  // MQ-131 calibration function
  Serial.println("MQ-131 Calibration started...");
  long sumMQ131 = 0;
  long startTime = millis();

  while (millis() - startTime < calibrationTime) {
    sumMQ131 += analogRead(mq131Pin);
    delay(10);
  }

  baselineMQ131 = sumMQ131 / (calibrationTime / 10);
  Serial.print("Calibration completed. Baseline value MQ-131: ");
  Serial.println(baselineMQ131);
}
