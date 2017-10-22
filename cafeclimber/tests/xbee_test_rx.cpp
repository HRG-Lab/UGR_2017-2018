#include <iostream>
#include <string.h>
#include <unistd.h>

#include <xbeep.h>

class myConnection: public libxbee::ConCallback {
public:
    explicit myConnection(libxbee::XBee &parent,
                          std::string type,
                          struct xbee_conAddress *address = NULL) :
        libxbee::ConCallback(parent, type, address) {};

    void xbee_conCallback(libxbee::Pkt **pkt);

    std::string myData;
};

void myConnection::xbee_conCallback(libxbee::Pkt **pkt) {
    std::cout << "Callback!" << std::endl;
    if ((*pkt)->size() > 0) {
        std::cout << "[RX] Data: " << (*pkt)->getData() << std::endl;
        std::cout << "[RX] RSSI: -" << (int)(*pkt)->getRssi() << " dBm" << std::endl;
    }
}

int main(int argc, char* argv[]) {
    try {
        libxbee::XBee xbee("xbee1", "/dev/ttyUSB1", 57600);

        {
            struct xbee_conAddress addr = {};
            memset(&addr, 0, sizeof(addr));
            addr.addr64_enabled = 1;
            unsigned char addr64[] = {0x00, 0x13, 0xA2, 0x00,
                                      0x40, 0x9A, 0x7E, 0x0C};
            memcpy(addr.addr64, addr64, 8);
            myConnection xbee_con(xbee, "64-bit Data", &addr);

            for(;;) {
                usleep(1000000);
            }
        }

        usleep(1000000);
    } catch (xbee_err err) { std::cerr << "[XBEE]: " << err <<
        std::endl;
        return 1;
    }
}
