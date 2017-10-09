/**
 * @file datalogger.hpp
 *
 * @brief Defines the main entry point for the Datalogger program
 *
 * @author Ryan Campbell
 */

#include "hackrf_interface.hpp"
#include "pixhawk_interface.hpp"

#include <boost/log/core.hpp>
#include <boost/log/expressions.hpp>
#include <boost/log/trivial.hpp>
#include <cmath>
#include <cstdlib>
#include <fstream>
#include <future>
#include <getopt.h>
#include <inttypes.h>
#include <iostream>
#include <memory>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <thread>
#include <time.h>
#include <unistd.h>

#include <common/mavlink.h>

#define DEFAULT_SERIAL_PORT                                                    \
    (char *)"/dev/ttyACM0" ///< Typically the serial port used with USB
#define DEFAULT_BAUDRATE                                                       \
    57600 ///< Default baudrate used by the pixhawk over USB
#define DEFAULT_LOGLEVEL                                                       \
    (char *)"warning" ///< Only show warnings and higher by default

std::unique_ptr<Pixhawk::PixhawkInterface> pixhawk_interface;

void set_log_level(const char *log_string);
void print_help();
void sighandler(int signo);

int main(int argc, char **argv);
