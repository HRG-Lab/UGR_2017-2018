#ifndef TYPEDEF_H
#define TYPEDEF_H

typedef struct packet_ {
  int32_t lat;
  int32_t lon;
  int32_t alt;

  float roll;
  float pitch;
  float yaw;
} packet_t;

#endif
