#include "mavlink.h"

void receive_message(packet_t *packet, bool *got_gps, bool *got_attitude) {
  Serial.println("receive_message()");
  uint8_t recv_byte;
  mavlink_message_t msg;
  memset(&msg, 0, sizeof(mavlink_message_t));
  mavlink_status_t status;

  recv_byte = PixhawkSerial.read();

  mavlink_parse_char(MAVLINK_COMM_1, recv_byte, &msg, &status);

  switch(msg.msgid) {
    case MAVLINK_MSG_ID_HEARTBEAT: {
      Serial.println("MAVLINK_MSG_ID_HEARTBEAT");
      break;
    }
    case MAVLINK_MSG_ID_ATTITUDE: {
      Serial.println("MAVLINK_MSG_ID_ATTITUDE");
      mavlink_attitude_t attitude;
      mavlink_msg_attitude_decode(&msg, &attitude);

      packet->roll = attitude.roll;
      packet->pitch = attitude.pitch;
      packet->yaw = attitude.yaw;
      
      *got_attitude = true;
      break;
    }
    case MAVLINK_MSG_ID_GLOBAL_POSITION_INT: {
      Serial.println("MAVLINK_MSG_ID_GLOBAL_POSITION_INT");
      mavlink_global_position_int_t gps;
      mavlink_msg_global_position_int_decode(&msg, &gps);

      packet->lat = gps.lat;
      packet->lon = gps.lon;
      packet->alt = gps.alt;
      
      *got_gps = true;
      break;
    }
    default: {
      break;
    }
  }
}


