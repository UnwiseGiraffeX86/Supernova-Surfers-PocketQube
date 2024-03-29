#include <Wire.h>
#include <MPU9250.h>
#include <Adafruit_BMP280.h>

MPU9250 mpu;
Adafruit_BMP280 bmp;

void setup()
{
  Serial.begin(115200);
  Wire.begin();
  delay(10000);

  // MPU9250 initialization
  if (!mpu.setup(0x68)) 
  { 
    while (1) 
    {
      Serial.println("MPU9250 not found!");
      delay(500);
    }
  }

  // BMP280 initialization
  if (!bmp.begin(0x76))
  {  
    while (1) 
    {
      Serial.println("BMP280 not found!");
      delay(500);
    }
  }
}

void loop()
{
  float temperature, pressure_hPa;
  mpu.update();
  mpu.update_mag();
  temperature = bmp.readTemperature()-4;
  pressure_hPa = bmp.readPressure() / 100.0; 

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
  delay(1000);
}