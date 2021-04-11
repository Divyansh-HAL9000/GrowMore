#include <Arduino.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>


#define LDR_PIN A5
#define MAX_ADC_READING 1023
#define ADC_REF_VOLTAGE 5
#define REF_RESISTANCE 5000
#define LUX_CALC_SCALAR 12518931
#define LUX_CALC_EXPONENT -1.405

// Set DHT pin:
#define DHTPIN 2
// Set DHT type, uncomment whatever type you're using!
//#define DHTTYPE DHT11   // DHT 11 
#define DHTTYPE DHT22   // DHT 22  (AM2302)
//#define DHTTYPE DHT21   // DHT 21 (AM2301)

// Initialize DHT sensor for normal 16mhz Arduino:
DHT dht = DHT(DHTPIN, DHTTYPE);


void get_temp();
void get_humidity();
void get_brightness();

void setup() {
  pinMode(LDR_PIN, INPUT);
  pinMode(13, OUTPUT);
  Serial.begin(9600);
  pinMode(A0, INPUT);
  dht.begin();
}

bool gtcalled = false;
float temperature = 0.0;

void loop() {
  gtcalled = false;
  temperature = 0.0;
  if (Serial.read()) {

    get_temp();
    get_brightness();
    get_humidity();
    Serial.flush();
    delay(4000);
  }
}

void get_temp() {
  gtcalled = true;
  int reading = analogRead(A0);
  // Convert the reading into voltage
  float voltage = reading * (5000 / 1024.0);
  // Convert the voltage into the temperature in degree Celsius:
  temperature += 0.2 * voltage / 10;
  // Print the temperature in the Serial Monitor:
}

void get_brightness() {
  int rawData = analogRead(LDR_PIN);
  // MAX_ADC_READING is 1023 and ADC_REF_VOLTAGE is 5
  float resistorVoltage = (float)rawData / MAX_ADC_READING * ADC_REF_VOLTAGE;
  float ldrVoltage = ADC_REF_VOLTAGE - resistorVoltage;
  float ldrResistance = ldrVoltage/resistorVoltage * REF_RESISTANCE;  // REF_RESISTANCE is 5 kohm
  float ldrLux = LUX_CALC_SCALAR * pow(ldrResistance, LUX_CALC_EXPONENT);  
  Serial.print("{\"B\":\"");
  Serial.print(ldrLux*4.17);
  Serial.print("\",");
}

void get_humidity() {
  float h = dht.readHumidity();
  // Read the temperature as Celsius:
  float t = dht.readTemperature();
  if (gtcalled) {
    temperature += 0.8*t;
  } else {
    temperature += t;
  }
  // Read the temperature as Fahrenheit:
  float f = dht.readTemperature(true);
  // Check if any reads failed and exit early (to try again):

  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Compute heat index in Fahrenheit (default):
 // float hif = dht.computeHeatIndex(f, h);
  // Compute heat index in Celsius:
 // float hic = dht.computeHeatIndex(t, h, false);
  Serial.print("\"T\":\"");
  Serial.print(temperature);
  Serial.print("\",");
  Serial.print("\"H\":\"");
  Serial.print(h);
  Serial.println("\"}");
/*
  Serial.print("Temperature: ");
  Serial.print(t);
  Serial.print(" \xC2\xB0");
  Serial.print("C | ");
  Serial.print(f);
  Serial.print(" \xC2\xB0");
  Serial.print("F ");
  Serial.print("Heat index: ");
  Serial.print(hic);
  Serial.print(" \xC2\xB0");
  Serial.print("C | ");
  Serial.print(hif);
  Serial.print(" \xC2\xB0");
  Serial.println("F");
*/
}