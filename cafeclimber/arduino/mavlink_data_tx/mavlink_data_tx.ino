#include "mavlink.h"
#include "xbee.h"
#include "typedef.h"

int ledPin = 13;
packet_t packet;
bool gps = false;
bool attitude = false;

XBee xbee = XBee();

void setup() {
  Serial.begin(57600);
  PixhawkSerial.begin(57600);
  XBeeSerial.begin(57600);
  xbee.setSerial(XBeeSerial);
  
  memset(&packet, 0, sizeof(packet_t));

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH); // Just to show power is on

  delay(5000); // Wait 5 seconds to allow XBee a chance to settle
}

void loop() {
  if (PixhawkSerial.available() > 0) {
    receive_message(&packet, &gps, &attitude);
  }

  if (gps && attitude) {
    Serial.println("######### Received full GPS / IMU data #########");
    send_packet(&xbee, &packet);
    gps = false;
    attitude = false;
  }
}
