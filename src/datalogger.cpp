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
  // char *log_level = DEFAULT_LOGLEVEL;

  char ch;

  const struct option long_options[] = {
      {"help", no_argument, 0, 'h'},
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
        //log_level = optarg;
        std::cerr << "Log level not implemented" << std::endl;
      break;
    }
    case 'h': {
      print_help();
      break;
    }
    default: { print_help(); }
    }
  }

  signal(SIGINT, sighandler);

  sigset_t mask;
  sigemptyset(&mask);
  sigaddset(&mask, SIGINT);

  try {
    auto hackrf_interface = HackRF::HackRFInterface();
    hackrf_interface.open();
    std::cerr << hackrf_interface.info();

    pixhawk_interface = std::make_unique<Pixhawk::PixhawkInterface>(device, baudrate);

    for (;;) {
      if (sigprocmask(SIG_BLOCK, &mask, NULL) != 0) {
        break;
      }
      auto read_fut =
          std::async(std::launch::async, &Pixhawk::PixhawkInterface::read_thread,
                     pixhawk_interface.get());
      auto message = read_fut.get();
      if (message != "") {
        std::cout << message << std::endl;
      }
      if (sigprocmask(SIG_UNBLOCK, &mask, NULL) != 0) {
        break;
      }
      usleep(10);
    }

  } catch (std::exception &e) {
      std::cerr << "Unhandled Exception: " << e.what();
  }
}

void sighandler(int signo) {
    printf("\nRECEIVED QUIT REQUEST:%d\n\n", signo);
    pixhawk_interface->close();
    exit(EXIT_SUCCESS);
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
