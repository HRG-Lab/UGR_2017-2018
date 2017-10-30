#include <XBee.h>

#define XBeeSerial Serial3
#define PixhawkSerial Serial2

XBee xbee = XBee();

uint8_t payload[24]; //12 bytes for GPS and 12 bytes for Attitude

TxStatusResponse txStatus = TxStatusResponse();

int statusLed = 13;
bool gps = false;
bool attitude;

void receiveMessage();
void flashLed(int pin, int times, int wait);


void setup() {
  Serial.begin(57600);
  PixhawkSerial.begin(57600);
  XBeeSerial.begin(57600);
  xbee.setSerial(XBeeSerial);

  pinMode(statusLed, OUTPUT);
  
  delay(5000); // Wait 5 seconds
}

void loop() {
  while(!gps && !attitude) {
    if(PixhawkSerial.available() > 0) {
      receiveMessage();
   }
  }
  gps = false;
  attitude = false;
  
  Tx16Request tx = Tx16Request(0x1234, payload, sizeof(payload));
  xbee.send(tx);

  if (xbee.readPacket(2000)) {
    if(xbee.getResponse().getApiId() == TX_STATUS_RESPONSE) {
      xbee.getResponse().getTxStatusResponse(txStatus);
      if(txStatus.getStatus() == SUCCESS) {
        flashLed(statusLed, 2, 50);
      }
    }
  } else {
    Serial.println("XBee not working properly");
  }
  delay(500);
}

void receiveMessage() {
    uint8_t recv_byte;
  mavlink_message_t msg;
  mavlink_status_t status;

  recv_byte = PixhawkSerial.read();

  mavlink_parse_char(MAVLINK_COMM_1, recv_byte, &msg, &status);
  digitalWrite(ledPin, HIGH);

  switch(msg.msgid) {
    case MAVLINK_MSG_ID_HEARTBEAT: {
      Serial.println("MAVLINK_MSG_ID_HEARTBEAT");
      mavlink_heartbeat_t heartbeat;
      mavlink_msg_heartbeat_decode(&msg, &heartbeat);
      break;
    }
    case MAVLINK_MSG_ID_GLOBAL_POSITION_INT: {
      Serial.println("MAVLINK_MSG_ID_GLOBAL_POSITION_INT");
      mavlink_global_position_int_t gps;
      mavlink_msg_global_position_int_decode(&msg, &gps);

      memcpy(payload[0], &gps.lat, sizeof(gps.lat));
      memcpy(payload[4], &gps.lon, sizeof(gps.lon));
      memcpy(payload[8], &gps.alt, sizeof(gps.alt));

      gps = true;
      
      Serial.print("[GPS]\tLAT: ");
      Serial.print(gps.lat);
      Serial.print("\tLON: ");
      Serial.print(gps.lon);
      Serial.print("\tBOOT: ");
      Serial.println(gps.time_boot_ms);
      break;
    }
    case MAVLINK_MSG_ID_ATTITUDE: {
      Serial.println("MAVLINK_MSG_ID_ATTITUDE");
      mavlink_attitude_t attitude;
      mavlink_msg_attitude_decode(&msg, &attitude);

      memcpy(payload[12], &attitude.roll, sizeof(attitude.roll));
      memcpy(payload[16], &attitude.pitch, sizeof(attitude.pitch));
      memcpy(payload[20], &attitude.yaw, sizeof(attitude.yaw));
      
      Serial.print("[ATT]\tROLL: ");
      Serial.print(attitude.roll);
      Serial.print("\tPITCH: ");
      Serial.print(attitude.pitch);
      Serial.print("\tYAW: ");
      Serial.println(attitude.yaw);
      break;
    }
   default: {
      break;
    }
  }
}


void flashLed(int pin, int times, int wait) {
  for (int i = 0; i < times; i++) {
      digitalWrite(pin, HIGH);
      delay(wait);
      digitalWrite(pin, LOW);
      
      if (i + 1 < times) {
        delay(wait);
      }
  }
}
