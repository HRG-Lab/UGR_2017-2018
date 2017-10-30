#ifndef BASIC_RSSI_HPP
#define BASIC_RSSI_HPP

#include <atomic>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <fstream>
#include <future>
#include <getopt.h>
#include <inttypes.h>
#include <iomanip>
#include <iostream>
#include <memory>
#include <mutex>
#include <signal.h>
#include <sstream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <time.h>
#include <thread>
#include <unistd.h>

#include <xbeep.h>

const std::string DEFAULT_XBEE_PORT = "/dev/ttyUSB0";
const int DEFAULT_BAUDRATE = 57600;

static std::ofstream logfile; 

void usage();
std::string generate_default_log_file_name();
void sighandler(int signo);
//void start_xbee_thread(XBee::XBee xbee, std::string logfile_);

class XBeeConnection: public libxbee::ConCallback {
public:
    explicit XBeeConnection(libxbee::XBee &parent,
                            std::string type,
                            struct xbee_conAddress *address);
    
    void xbee_conCallback(libxbee::Pkt **pkt);
    void reset(void);
};


#endif
