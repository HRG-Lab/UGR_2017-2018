/**
 * @file serial_port.hpp
 *
 * Defines the SerialPort class for interfacing with serial ports
 *
 * @author Ryan Campbell
 */

#ifndef SERIAL_PORT_HPP
#define SERIAL_PORT_HPP

#include <boost/log/trivial.hpp>
#include <errno.h>
#include <exception>
#include <fcntl.h>
#include <iostream>
#include <memory>
#include <mutex>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <string>
#include <termios.h>
#include <unistd.h>

namespace SerialPort {

class SerialPortException: public std::exception {
    using std::exception::what;
public:
    SerialPortException(std::string msg_): msg(msg_){}
    ~SerialPortException() throw() {};

    const char* what();
private:
    std::string msg;
};

/// What state the serial port is currently in
enum Status {
    Open, /// Indicates the file descriptor representing the serial port is open
    Closed, /// Indicates the file descriptor representing the serial port is
            /// closed
    Error   /// Indicates the serial port is in an error state requiring action
};

/// @brief Provides an interface to serial ports specifically for use with
/// Pixhawk
///
/// Does not provide any detailed control over serial ports. All communication
/// is assumed to be 8N1 UART.
class SerialPort {
  public:
    SerialPort();
    SerialPort(std::string _port_name, int _baudrate);
    ~SerialPort();

    void open();
    void close();

    int read(uint8_t &cp);
    int write(char *buf, size_t len);

  private:
    Status status;

    int fd;
    int baudrate;
    std::string port_name;

    std::mutex mutex; // ptr allows for move
};

}

#endif
