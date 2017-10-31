#include "packet.hpp"

const float PI = 3.14159;

Packet::Packet(const char* data)
{
    memcpy(&packet, data, sizeof(packet_t));
}

std::ostream& operator<<(std::ostream& os, const Packet& pkt)
{
    os << pkt.packet.lat << "," << pkt.packet.lon << "," << pkt.packet.alt << ","
       << pkt.packet.roll * (180.0 / PI) << ","
       << pkt.packet.pitch * (180.0 / PI)<< ","
       << pkt.packet.yaw * (180.0 / PI);
    return os;
}
