#include <ArduinoJson.h>
#include <SoftwareSerial.h>
#include "SIM800L.h"
#include "DHT.h"


#define DeviceID "ddb-001"
#define SIM800_RX_PIN 7
#define SIM800_TX_PIN 8
#define SIM800_RST_PIN 9

#define echoPin 3 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 4

#define DHTPIN 2
#define DHTTYPE DHT11 

int smokeA0 = A5;
int sensorThres = 400;

long duration; // variable for the duration of sound wave travel
int distance; // variable for the distance measurement

float humi;
float temp;

float gas;


const char APN[] = "INTERNET";
const char URL[] = "http://esrl.israfil.xyz/api/";
const char CONTENT_TYPE[] = "application/json";
char PAYLOAD[300];

SIM800L* sim800l;

DHT dht(DHTPIN, DHTTYPE);

void messureDisance(){
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)  
}

void readDHT(){
  delay(2000);
  humi = dht.readHumidity();
  temp = dht.readTemperature();
}

void readGas(){
  float analogSensor = analogRead(smokeA0);

  gas = analogSensor;
  delay(100);
}

void sendData (){
    messureDisance();
    readDHT();
    readGas();
    
    StaticJsonBuffer<300> jBuff;   //Declaring static JSON buffer
    JsonObject & jEn = jBuff.createObject(); 

    jEn["device"] = DeviceID;
    jEn["height"] = distance;
    jEn["gas"] = gas;
    jEn["temp"] = temp;  
    jEn["humidity"] = humi;   
    jEn.prettyPrintTo(PAYLOAD, sizeof(PAYLOAD));
    Serial.println(PAYLOAD);
}

void setup() {

  pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin, INPUT);
  pinMode(smokeA0, INPUT);

  dht.begin();
  
  Serial.begin(115200);
  while(!Serial);

  
  SoftwareSerial* serial = new SoftwareSerial(SIM800_RX_PIN, SIM800_TX_PIN);
  serial->begin(9600);
  delay(1000);
   
  
  sim800l = new SIM800L((Stream *)serial, SIM800_RST_PIN, 200, 512);

  setupModule();
}
 
void loop() { 
  
  bool connected = false;
  for(uint8_t i = 0; i < 5 && !connected; i++) {
    delay(1000);
    connected = sim800l->connectGPRS();
  }

  
  if(connected) {
    Serial.print(F("GPRS connected with IP "));
    Serial.println(sim800l->getIP());
  } else {
    Serial.println(F("GPRS not connected !"));
    Serial.println(F("Reset the module."));
    sim800l->reset();
    setupModule();
    return;
  }

  Serial.println(F("Start HTTP POST..."));
  
  sendData();
  
  uint16_t rc = sim800l->doPost(URL, CONTENT_TYPE, PAYLOAD, 10000, 10000);
   
   if(rc == 200) {
    // Success, output the data received on the serial
    Serial.print(F("HTTP POST successful ("));
    Serial.print(sim800l->getDataSizeReceived());
    Serial.println(F(" bytes)"));
    Serial.print(F("Received : "));
    Serial.println(sim800l->getDataReceived());
  } else {
    // Failed...
    Serial.print(F("HTTP POST error "));
    Serial.println(rc);
  }
  delay(1000);

  // Close GPRS connectivity (5 trials)
  bool disconnected = sim800l->disconnectGPRS();
  for(uint8_t i = 0; i < 5 && !connected; i++) {
    delay(1000);
    disconnected = sim800l->disconnectGPRS();
  }
  
  if(disconnected) {
    Serial.println(F("GPRS disconnected !"));
  } else {
    Serial.println(F("GPRS still connected !"));
  }

  // Go into low power mode
  bool lowPowerMode = sim800l->setPowerMode(MINIMUM);
  if(lowPowerMode) {
    Serial.println(F("Module in low power mode"));
  } else {
    Serial.println(F("Failed to switch module to low power mode"));
  }

  // End of program... wait...
  //while(1);
}

void setupModule() {
    // Wait until the module is ready to accept AT commands
  while(!sim800l->isReady()) {
    Serial.println(F("Problem to initialize AT command, retry in 1 sec"));
    delay(1000);
  }
  
  Serial.println(F("Setup Complete!"));

  // Wait for the GSM signal
  uint8_t signal = sim800l->getSignal();
  while(signal <= 0) {
    delay(1000);
    signal = sim800l->getSignal();
  }
  Serial.print(F("Signal OK (strenght: "));
  Serial.print(signal);
  Serial.println(F(")"));
  delay(1000);

  // Wait for operator network registration (national or roaming network)
  NetworkRegistration network = sim800l->getRegistrationStatus();
  while(network != REGISTERED_HOME && network != REGISTERED_ROAMING) {
    delay(1000);
    network = sim800l->getRegistrationStatus();
  }
  Serial.println(F("Network registration OK"));
  delay(1000);

  // Setup APN for GPRS configuration
  bool success = sim800l->setupGPRS(APN);
  while(!success) {
    success = sim800l->setupGPRS(APN);
    delay(5000);
  }
  Serial.println(F("GPRS config OK"));
}
