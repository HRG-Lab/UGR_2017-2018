#include "basic_rssi.hpp"

/// Entry point for the BasicRSSI Program.
///
/// This program starts a loop, waits for GPS lock from the pixhawk
/// and then begins logging data. The data is logged to the specified csv file.
///
/// @param argc Number of arguments
/// @param argv Each argument as a string
///
/// @return Result of execution
int main(int argc, char **argv) {
    char *device = DEFAULT_SERIAL_PORT;
    int baudrate = DEFAULT_BAUDRATE;
    char *log_level = DEFAULT_LOGLEVEL;
    const char *log_file = generate_default_log_file_name();

    char ch;
    const struct option long_options[] = {
        {"help", no_argument, 0, 'h'},
        {"device", required_argument, 0, 'd'},
        {"baudrate", required_argument, 0, 'b'},
        {"file", required_argument, 0, 'f'},
        {"loglevel", required_argument, 0, 'l'},
        {NULL, 0, NULL, 0}};
    while ((ch = getopt_long(argc, argv, "d:b:f:l:h", long_options, NULL)) !=
           -1) {
        switch (ch) {
        case 'd': {
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
        case 'l': {
            log_level = optarg;
            break;
        }
        case 'h': {
            print_help();
            break;
        }
        default: { print_help(); }
        }
    }

    set_log_level(log_level);
    signal(SIGINT, sighandler);

    sigset_t mask;
    sigemptyset(&mask);
    sigaddset(&mask, SIGINT);

    try {
        uint64_t start_time = 0;
        uint64_t end_time = 0;
        pixhawk_interface =
            std::make_unique<Pixhawk::PixhawkInterface>(device, baudrate);

        std::ofstream log(log_file);
        log << "\"Latitude\",\"Longitude\",\"Altitude\","
            << "\"X Velocity\",\"Y Velocity\",\"Z Velocity\"\"Heading\""
            << "\"Roll\",\"Pitch\",\"Yaw\","
            << "\"Roll Speed\",\"Pitch Speed\",\"Yaw Speed\","
            << "\"RSSI\"" << std::endl;

        // TODO: Wait for GPS Lock

        while (true) {
            start_time = get_time_usec();

            if (sigprocmask(SIG_BLOCK, &mask, NULL) != 0) {
                break;
            }

            auto read_fut =
                std::async(std::launch::async,
                           &Pixhawk::PixhawkInterface::read_gps_imu_rssi,
                           pixhawk_interface.get());
            auto msg = read_fut.get();
            if (!msg.complete) {
                BOOST_LOG_TRIVIAL(warning) << "Ignoring incomplete packet";
                end_time = get_time_usec();
                usleep(100000 - (end_time - start_time)); // Poll at 10 Hz
                continue;
            }
            log << msg << std::endl;
            end_time = get_time_usec();
            usleep(100000 - (end_time - start_time)); // Poll at 10 Hz
        }
    } catch (SerialPort::SerialPortException &e) {
        BOOST_LOG_TRIVIAL(fatal)
            << "SERIAL PORT EXCEPTION: " << e.what() << std::endl;
    } catch (Pixhawk::PixhawkException &e) {
        BOOST_LOG_TRIVIAL(fatal)
            << "PIXHAWK EXCEPTION:     " << e.what() << std::endl;
    } catch (std::exception &e) {
        BOOST_LOG_TRIVIAL(fatal)
            << "Unhandled Exception:   " << e.what() << std::endl;
    }
}

void print_help() {
    printf("Usage: BasicRSSI [OPTIONS]\n");
    printf("Starts datalogger program with Pixhawk on specified ");
    printf("serial port at the specified baudrate\n\n");
    printf("Options:\n");
    printf("\t-h, --help\tDisplay this help text\n");
    printf("\t-d, --device\tThe device id for the Pixhawk [default: "
           "/dev/ttyUSB0]\n");
    printf("\t-b, --baudrate\tThe baudrate for communicating with the "
           "Pixhawk [default: 57600]\n\n");
    printf("\t-f, --file\t The file to output data. File is output "
           "in csv format. [default: RSSI_<date>_<time>.csv]");
    printf("\t-l --loglevel\tThe level of debugging output:\n");
    printf("\t\t\t{trace, debug, info, warning, error, fatal}\n\t\t\t[default: "
           "warning]\n");
    exit(EXIT_FAILURE);
}

void sighandler(int signo) {
    printf("\nRECEIVED QUIT REQUEST:%d\n\n", signo);
    pixhawk_interface->close();
    exit(EXIT_SUCCESS);
}

/// Sets the log level for Boost's log library based on the string passed to it
///
/// @param log_string desired log level
void set_log_level(const char *log_string) {
    auto desired_log_level = boost::log::trivial::warning;

    if (strncmp(log_string, "trace", 5) == 0 ||
        strncmp(log_string, "t", 1) == 0) {
        desired_log_level = boost::log::trivial::trace;
    } else if (strncmp(log_string, "debug", 5) == 0 ||
               strncmp(log_string, "d", 1) == 0) {
        desired_log_level = boost::log::trivial::debug;
    } else if (strncmp(log_string, "info", 4) == 0 ||
               strncmp(log_string, "i", 1) == 0) {
        desired_log_level = boost::log::trivial::info;
    } else if (strncmp(log_string, "warning", 7) == 0 ||
               strncmp(log_string, "w", 1) == 0) {
        desired_log_level = boost::log::trivial::warning;
    } else if (strncmp(log_string, "error", 5) == 0 ||
               strncmp(log_string, "e", 1) == 0) {
        desired_log_level = boost::log::trivial::error;
    } else if (strncmp(log_string, "fatal", 5) == 0 ||
               strncmp(log_string, "f", 1) == 0) {
        desired_log_level = boost::log::trivial::fatal;
    } else {
        BOOST_LOG_TRIVIAL(warning)
            << "Unrecognized log level. Defaulting to warning";
        desired_log_level = boost::log::trivial::warning;
    }

    boost::log::core::get()->set_filter(boost::log::trivial::severity >=
                                        desired_log_level);
}

/// Gets the current time of day using the Linux syscall
/// and converts the timeval struct to microseconds
///
/// @return Time in microseconds
static uint64_t get_time_usec() {
    static struct timeval time_stamp;
    gettimeofday(&time_stamp, NULL);
    return time_stamp.tv_sec * USEC_PER_SEC + time_stamp.tv_usec;
}

const char *generate_default_log_file_name() {
    auto t = std::time(nullptr);
    auto tm = *std::localtime(&t);

    std::ostringstream filename;
    filename << "RSSI_" << std::put_time(&tm, "%d-%m-%Y_%H-%M-%S") << ".csv";

    return filename.str().c_str();
}
