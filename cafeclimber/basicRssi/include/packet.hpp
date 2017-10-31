#ifndef PACKET_H
#define PACKET_H

#include <iostream>
#include <stdint.h>
#include <string.h>
#include <unistd.h>

typedef struct packet_ {
    int32_t lat;
    int32_t lon;
    int32_t alt;

    float roll;
    float pitch;
    float yaw;
} packet_t;

class Packet {
 public:
    Packet() = delete;
    explicit Packet(const char *data);

    friend std::ostream& operator<<(std::ostream& os, const Packet& pkt);

 private:
    packet_t packet;
};

#endif // PACKET_H
