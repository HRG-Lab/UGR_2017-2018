#include "xbee.h"

void send_packet(XBee *xbee, packet_t *packet) {
  Serial.println("send_packet()");
  uint8_t payload[sizeof(packet_t)];
  memcpy(&payload, packet, sizeof(packet_t));

  Tx16Request tx = Tx16Request(0x1234, payload, sizeof(payload));
  TxStatusResponse txStatus = TxStatusResponse();
  xbee->send(tx);

  if (xbee->readPacket(2000)) {
    if(xbee->getResponse().getApiId() == TX_STATUS_RESPONSE) {
      xbee->getResponse().getTxStatusResponse(txStatus);
      if(txStatus.getStatus() == SUCCESS) {
        Serial.println("Packet sent succesfully");
        memset(packet, 0, sizeof(packet_t)); // Resets packet to 0
      }
    }
  } else {
    Serial.println("XBee is not configured properly. Failed to send packet");
  }

  delay(500);
}

