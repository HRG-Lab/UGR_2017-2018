/**
 * @file pixhawk_interface.hpp
 *
 * @brief Defines the class for interfacing with a Pixhawk
 */

#ifndef AUTOPILOT_INTERFACE_H
#define AUTOPILOT_INTERFACE_H

#include "serial_port.hpp"

#include <exception>
#include <future>
#include <memory>
#include <signal.h>
#include <sstream>
#include <string>
#include <sys/time.h>
#include <time.h>
#include <unordered_set>

#include <common/mavlink.h>

#define USEC_PER_SEC 1000000 ///< Number of microseconds in one second

uint64_t get_time_usec();

namespace Pixhawk {

class PixhawkException : std::exception {
  using std::exception::what;

public:
  PixhawkException(std::string);
  ~PixhawkException() throw(){};

  const char *what();

private:
  std::string msg;
};

/// Represents a connection to a Pixhawk over a serial port
class PixhawkInterface {
public:
  PixhawkInterface() = delete;
  PixhawkInterface(std::string port_name, int baudrate);
  ~PixhawkInterface();

  std::string read_thread();
  void close();

private:
  mavlink_status_t current_status;

  std::shared_ptr<SerialPort::SerialPort> serial_port;
  std::future<void> read_fut;
  std::unordered_set<int> unhandled_msg_ids;
  std::string decode_message(const mavlink_message_t &message);
};
}

#endif // AUTOPILOT_INTERFACE_H
