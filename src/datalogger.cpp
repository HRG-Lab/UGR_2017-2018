/**
 * @file datalogger.cpp
 *
 * @author Ryan Campbell
 */

#include "datalogger.hpp"

/// Entry point for the program
///
/// Creates a PixhawkInterface and attempts to read from it
///
/// @param argc Number of arguments
/// @param argv Each argument as a string
///
/// @return Result of execution
int main(int argc, char **argv) {
    char *device = DEFAULT_SERIAL_PORT;
    int baudrate = DEFAULT_BAUDRATE;
    char *log_level = DEFAULT_LOGLEVEL;

    char ch;

    const struct option long_options[] = {{"help", no_argument, 0, 'h'},
        {"device", required_argument, 0, 'd'},
        {"baudrate", required_argument, 0, 'b'},
        {"loglevel", required_argument, 0, 'l'}};

    while ((ch = getopt_long(argc, argv, "d:b:l:", long_options, NULL)) != -1) {
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
        pixhawk_interface =
            std::make_unique<PixhawkInterface>(device, baudrate);

        for(;;) {
            if(sigprocmask(SIG_BLOCK, &mask, NULL) != 0) {
                break;
            }
            auto read_fut = std::async(std::launch::async, &PixhawkInterface::read_thread, pixhawk_interface.get());
            auto message = read_fut.get();
            if(message != "") {
                std::cout << message << std::endl;
            }
            if(sigprocmask(SIG_UNBLOCK, &mask, NULL) != 0) {
                break;
            }
            usleep(10);
        }

    } catch (std::exception &e) {
        BOOST_LOG_TRIVIAL(fatal) << "Unhandled Exception: " << e.what();
    }
}

void sighandler(int signo) {
    printf("\nRECEIVED QUIT REQUEST\n\n");
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

    boost::log::core::get()->set_filter(
        boost::log::trivial::severity >= desired_log_level);
}

/// Prints the help text
void print_help() {
    printf("Usage: datalogger [OPTIONS]\n");
    printf("Starts datalogger program with Pixhawk on specified ");
    printf("serial port at the specified baudrate\n\n");
    printf("Options:\n");
    printf("\t-h, --help\tDisplay this help text\n");
    printf("\t-d, --device\tThe device id for the Pixhawk [default: "
           "/dev/ttyUSB0]\n");
    printf("\t-b, --baudrate\tThe baudrate for communicating with the "
           "Pixhawk [default: 57600]\n\n");
    printf("\t-l --loglevel\tThe level of logs to display from:\n");
    printf("\t\t\t{trace, debug, info, warning, error, fatal}\n\t\t\t[default: "
           "warning]\n");
    exit(EXIT_FAILURE);
}
