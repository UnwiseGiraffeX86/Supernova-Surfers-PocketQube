#include <SPI.h>
#include <SD.h>

const int chipSelect = 5; // CS pin is on D10

void setup() {
  Serial.begin(9600);
  Serial.println("Starting to cum");
  delay(1000);
  // Check if SD card module is properly connected
  if (!SD.begin(chipSelect)) {
    Serial.println("Initialization failed!");
    return;
  }
  Serial.println("Initialization done.");

  // Write to the SD card
  File myFile = SD.open("test.txt", FILE_WRITE);
  if (myFile) {
    myFile.println("This is a test message.");
    myFile.close();
    Serial.println("Write done.");
  } else {
    Serial.println("Error opening test.txt for writing");
  }

  // Read from the SD card
  myFile = SD.open("test.txt");
  if (myFile) {
    Serial.println("test.txt content:");
    while (myFile.available()) {
      Serial.write(myFile.read());
    }
    myFile.close();
  } else {
    Serial.println("Error opening test.txt for reading");
  }
}

void loop() {
}
