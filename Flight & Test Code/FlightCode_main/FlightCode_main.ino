#include <Wire.h>
#include <MPU9250.h>
#include <Adafruit_BMP280.h>
#include <DHT.h>
#include <SPI.h>
#include <SD.h>

#define DHTPIN 2      //
#define DHTTYPE DHT22
#define BUZZER_PIN 8  // D8 
const int CS = 5;    // D5

const int mq135Pin = A2; 
int baseline = 0; // Variable to store the baseline value for MQ-131
const int mq131Pin = A0;
int baselineMQ131 = 0; // Variable to store the baseline value for MQ-131
const int calibrationTime = 3000; // Calibration time in milliseconds

MPU9250 mpu;
Adafruit_BMP280 bmp;
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  Wire.begin();

  pinMode(BUZZER_PIN, OUTPUT);

 // SD Card Initialization
  if (!SD.begin(CS))
  {
    Serial.println("Initialization failed!");
    return;
  }

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

  tone(BUZZER_PIN, 1000,1000);
 
}

void loop() {
  // MPU9250, BMP280, DHT22, MQ-135, and MQ-131 readings
  float temperature, pressure_hPa, dht_temperature, humidity;
  mpu.update();
  mpu.update_mag();
  temperature = bmp.readTemperature()-4;
  pressure_hPa = bmp.readPressure() / 100.0;  // Convert to hectopascals
  dht_temperature = dht.readTemperature();
  humidity = dht.readHumidity();

 // MQ-135 Readings
  int mq135Value = analogRead(mq135Pin);
  int relativeValue = mq135Value - baseline;

  // MQ-131 Readings
  int mq131Value = analogRead(mq131Pin);
  int relativeValueMQ131 = mq131Value - baselineMQ131;

  File MPU = SD.open("MPU.txt", FILE_WRITE);

  if (MPU) 
  {
    MPU.print(mpu.getAcc(0));
    MPU.print(" ");
    MPU.print(mpu.getAcc(1));
    MPU.print(" ");
    MPU.print(mpu.getAcc(2));
    MPU.print(" ");
    MPU.print(mpu.getGyro(0));
    MPU.print(" ");
    MPU.print(mpu.getGyro(1));
    MPU.print(" ");
    MPU.print(mpu.getGyro(2));
    MPU.print(" ");
    MPU.print(mpu.getMag(0));
    MPU.print(" ");
    MPU.print(mpu.getMag(1));
    MPU.print(" ");
    MPU.print(mpu.getMag(2));
    MPU.println();
    MPU.close();
  }

  File BMP = SD.open("BMP.txt", FILE_WRITE);

  if (BMP) 
  {
    BMP.print(temperature);
    BMP.print(" ");
    BMP.print(pressure_hPa);
    BMP.println();
    BMP.close();
  }

  File DHT = SD.open("DHT.txt", FILE_WRITE);

  if(DHT)
  {
    DHT.print(humidity);
    DHT.println();
    DHT.close();
  }

  File MQ135 = SD.open("MQ135.txt", FILE_WRITE);

  if(MQ135)
  {
    MQ135.println(relativeValue);
    MQ135.close();
  }

  File MQ131 = SD.open("MQ131.txt", FILE_WRITE);
  
  if(MQ131)
  {
    MQ131.println(relativeValueMQ131);
    MQ131.close();
  }
  
  delay(50);  // Update all sensors 20 times a second
}

void calibrateSensor() {
  // MQ-135 calibration function
  Serial.println("Calibration started...");
  long sum = 0;
  long startTime = millis();

  while (millis() - startTime < calibrationTime) {
    sum += analogRead(mq135Pin);
    delay(10);
  }

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
