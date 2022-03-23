//XC4444 PIR Sensor Module
//VCC and GND are connected to VCC and GND on the arduino
//Out is connected to a digital IO pin on the Arduino
//pin defines- pin 13 is connected to onboard LED

//sudo chmod a+rw /dev/ttyACM0

#include <SPI.h>
#include <Ethernet.h>
#include <PubSubClient.h>

#define MOTIONSENSOR1 7
#define MOTIONSENSOR2 21
#define MOTIONSENSOR3 22
#define MOTIONSENSOR4 23
#define MOTIONSENSOR5 24
#define MOTIONSENSOR6 25
#define MOTIONSENSOR7 26
#define MOTIONSENSOR8 27
#define MOTIONSENSOR9 28

// Function prototypes
void subscribeReceive(char* topic, byte* payload, unsigned int length);
 
// Set your MAC address and IP address here
byte mac[] = { 0xDE, 0xA2, 0xDA, 0x1F, 0xAF, 0xD5};
IPAddress ip(10, 30, 10, 60);
 
// Make sure to leave out the http and slashes!
const char* server = "test.mosquitto.org";
 
// Ethernet and MQTT related objects
EthernetClient ethClient;
PubSubClient mqttClient(ethClient);

void setup() {

  Serial.begin(9600);

  // Start the ethernet connection
  Ethernet.begin(mac, ip);              
  
  // Ethernet takes some time to boot!
  delay(3000);

  // Set the MQTT server to the server stated above ^
  mqttClient.setServer(server, 1883);   
 
  // Attempt to connect to the server with the ID
  if (mqttClient.connect("steo/hayball")) 
  {
    Serial.println("Connection Successful");
 
    // Establish the subscribe event
    mqttClient.setCallback(subscribeReceive);
  } 
  else 
  {
    Serial.println("Connection Failed");
  }
  
  pinMode(MOTIONSENSOR1,INPUT); //set PIRPIN as input
}

void loop()
{
  // This is needed at the top of the loop!
  mqttClient.loop();
 
  // Ensure that we are subscribed to the topic
  mqttClient.subscribe("/sound_demo/data/hayball-ard");

  // Collect sensor data
  bool pir; //variable to hold input state
  pir=digitalRead(MOTIONSENSOR1); //read input

  Serial.println(pir);

  char message = char(pir);
  
  // Attempt to publish a value to the topic
  if(mqttClient.publish("/sound_demo/data/hayball-ard", "hello"))
  {
    Serial.println("Publish message success");
  }
  else
  {
    Serial.println("Could not send message :(");
  }
  
  // Dont overload the server!
  delay(4000);
}

void subscribeReceive(char* topic, byte* payload, unsigned int length)
{
  // Print the topic
  Serial.print("Topic: ");
  Serial.println(topic);
 
  // Print the message
  Serial.print("Message: ");
  for(int i = 0; i < length; i ++)
  {
    Serial.print(char(payload[i]));
  }
 
  // Print a newline
  Serial.println("");
}
