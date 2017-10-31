#ifndef XBEE_H
#define XBEE_H

#include <XBee.h>
#include "typedef.h"

#define XBeeSerial Serial3

void send_packet(XBee *xbee, packet_t *packet);

#endif
