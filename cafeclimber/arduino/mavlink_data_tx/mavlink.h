#ifndef MAVLINK_ARDUINO_H
#define MAVLINK_ARDUINO_H

#define PixhawkSerial Serial2

#include "Arduino.h"
#include "typedef.h"
#include "/home/rdcampbell/Arduino/libraries/c_library_v1/common/mavlink.h"

void receive_message(packet_t *packet, bool *got_gps, bool *got_attitude);

#endif // MAVLINK_ARDUINO_H
