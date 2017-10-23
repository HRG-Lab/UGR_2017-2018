#include <boost/log/core.hpp>
#include <boost/log/expressions.hpp>
#include <boost/log/trivial.hpp>
#include <iostream>
#include <memory>
#include <string.h>
#include <unistd.h>

#include <xbeep.h>

namespace XBee {
    class XBeeConnection: public libxbee::ConCallback {
    public:
        explicit XBeeConnection(libxbee::XBee &parent,
                                std::string type,
                                struct xbee_conAddress *address);

        void xbee_conCallback(libxbee::Pkt **pkt);

        std::string myData;
    };
}
