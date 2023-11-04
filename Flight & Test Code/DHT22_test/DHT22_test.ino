#include <Wire.h>
#include <DHT.h>

#define DHTPIN 2 // D2
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

void setup()
{
  Serial.begin(115200);
  Wire.begin();
  delay(1000);

  dht.begin();
}

void loop()
{
  float dht_temperature, humidity;

  dht_temperature = dht.readTemperature();
  humidity = dht.readHumidity();

  // Displaying DHT22 Readings
  Serial.println("======== DHT22 Readings ========");
  Serial.print("Temperature: "); Serial.println(dht_temperature);
  Serial.print("Humidity: "); Serial.println(humidity);

  delay(1000);
}