#include "basic_rssi.hpp"

XBeeConnection::XBeeConnection(libxbee::XBee &parent, std::string type,
                               struct xbee_conAddress *address = NULL)
    : libxbee::ConCallback(parent, type, address){};

void XBeeConnection::xbee_conCallback(libxbee::Pkt **pkt)
{
    if ((*pkt)->size() > 0) {
        auto rssi = unsigned((*pkt)->getRssi());
        auto data = (*pkt)->getData().c_str();
        Packet packet(data);

        std::cout << packet << "," << rssi << std::endl;
        logfile << packet << "," << rssi << std::endl;
    }
}

/// Entry point for the BasicRSSI Program.
///
/// @param argc Number of arguments
/// @param argv Each argument as a string
///
/// @return Result of execution
int main(int argc, char **argv) {
    std::string device = DEFAULT_XBEE_PORT;
    int baudrate = DEFAULT_BAUDRATE;
    std::string log_file = generate_default_log_file_name();

    char ch;
    const struct option long_options[] = {
        {"help", no_argument, 0, 'h'},
        {"xbee", required_argument, 0, 'x'},
        {"baudrate", required_argument, 0, 'b'},
        {"file", required_argument, 0, 'f'},
        {NULL, 0, NULL, 0}};
    while ((ch = getopt_long(argc, argv, "h:x:b:f", long_options, NULL)) !=
           -1) {
        switch (ch) {
        case 'x': {
            device = optarg;
            break;
        }
        case 'b': {
            baudrate = atoi(optarg);
            // TODO: Check baudrate here
            break;
        }
        case 'f': {
            log_file = optarg;
            break;
        }
        case 'h': {
            usage();
            break;
        }
        default: {
            usage();
            break;
        }
        }
    }

    signal(SIGINT, sighandler);

    sigset_t mask;
    sigemptyset(&mask);
    sigaddset(&mask, SIGINT);

    logfile = std::ofstream(log_file);

    logfile << "lat,lon,alt,roll,pitch,yaw,rssi" << std::endl;

    try {
        libxbee::XBee xbee("xbee1", device, baudrate);
        {
            struct xbee_conAddress addr = {};
            memset(&addr, 0, sizeof(addr));
            addr.addr16_enabled = 1;
            unsigned char xbee_addr[2] = {0x43, 0x21};
            memcpy(addr.addr16, xbee_addr, 2);
            std::cout << "[MAIN] Starting XBee" << std::endl;
            XBeeConnection xbee_con(xbee, "16-bit Data", &addr);

            while(true) {
                if (sigprocmask(SIG_BLOCK, &mask, NULL) != 0) {
                    break;
                }
                if (sigprocmask(SIG_UNBLOCK, &mask, NULL) != 0) {
                    break;
                }
                usleep(1000000);
            }
        }

        //xbee_thread.join();

        return 0;
        
    }catch (xbee_err& err) {
        std::cerr << "[XBEE]: " << err << std::endl;
        return 1;
    }
    catch (std::exception &e) {
        std::cerr << "EXCEPTION: " << e.what() << std::endl;
        return 1;
    } catch (...) {
        std::cerr << "FATAL EXCEPTION" << std::endl;
    }

}

/*void start_xbee_thread(XBee::XBee xbee, std::string logfile_) {
    // TODO: Make this a CLI argument
    unsigned char addr[2] = {0x12, 0x34};
    xbee.connect(stop_thread, addr, logfile_);
    }*/

void usage() {
    printf("Usage: BasicRSSI [OPTIONS]\n");
    printf("Starts basicRSSI program with Pixhawk on specified ");
    printf("serial port at the specified baudrate\n\n");
    printf("Options:\n");
    printf("\t-h, --help\tDisplay this help text\n");
    printf("\t-x, --xbee\tThe device name of the xbee [default: "
           "/dev/ttyUSB0]\n");
    printf("\t-b, --baudrate\tThe baudrate of the XBee "
           "[default: 57600]\n\n");
    printf("\t-f, --file\t The file to output data. File is output "
           "in csv format. [default: RSSI_<date>_<time>.csv]");
    exit(EXIT_FAILURE);
}

void sighandler(int signo) {
    printf("\nRECEIVED QUIT REQUEST:%d\n\n", signo);
    //stop_thread = true;
    logfile.close();
    exit(EXIT_SUCCESS);
}

std::string generate_default_log_file_name() {
    auto t = std::time(nullptr);
    auto tm = *std::localtime(&t);

    std::ostringstream filename;
    filename << "RSSI_" << std::put_time(&tm, "%d-%m-%Y_%H-%M-%S") << ".csv";

    return filename.str();
}
