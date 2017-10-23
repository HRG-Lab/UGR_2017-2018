#include "xbee.hpp"

namespace XBee {
    XBeeConnection::XBeeConnection(libxbee::XBee &parent,
                            std::string type,
                            struct xbee_conAddress *address = NULL) :
        libxbee::ConCallback(parent, type, address) {};

    void XBeeConnection::xbee_conCallback(libxbee::Pkt **pkt) {
        BOOST_LOG_TRIVIAL(info) << "[XBEE] Packet Size: " << (*pkt)->size();
        if ((*pkt)->size() > 0) {
            BOOST_LOG_TRIVIAL(info) << "[XBEE] RSSI: -"
                                    << (int)(*pkt)->getRssi()
                                    << " dBm";
        }
    }
}
