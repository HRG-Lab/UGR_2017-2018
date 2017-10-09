#include <boost/log/core.hpp>
#include <boost/log/expressions.hpp>
#include <boost/log/trivial.hpp>
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
#include <signal.h>
#include <sstream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <thread>
#include <time.h>
#include <unistd.h>

#include "pixhawk_interface.hpp"
#include "serial_port.hpp"

#define DEFAULT_SERIAL_PORT (char *)"/dev/ttyACM0"
#define DEFAULT_BAUDRATE 57600
#define DEFAULT_LOGLEVEL (char *)"warning"

std::unique_ptr<Pixhawk::PixhawkInterface> pixhawk_interface;

void print_help();
static uint64_t get_time_usec();
const char *generate_default_log_file_name();
void set_log_level(const char *log_string);
void sighandler(int signo);
