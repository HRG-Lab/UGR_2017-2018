/**
 * @file hackrf_interface.hpp
 */
#ifndef HACKRF_INTERFACE_HPP
#define HACKRF_INTERFACE_HPP

#include <boost/log/trivial.hpp>
#include <exception>
#include <iostream>
#include <memory>
#include <sstream>
#include <string>

#include <libhackrf/hackrf.h>

namespace HackRF {

enum HackRFStatus { Open, Closed, Error };

class HackRFException : public std::exception {
    using std::exception::what;

  public:
    HackRFException() = delete;
    explicit HackRFException(int result);
    ~HackRFException() throw(){};

    const char *what();

  private:
    std::string msg;
};

class HackRFInterface {
  public:
    HackRFInterface();
    ~HackRFInterface();

    void open();
    void close();

    void info();

  private:
    HackRFStatus status;
    char *serial_no;
    char version[256];
    uint8_t board_id;
    read_partid_serialno_t read_partid_serialno;
    hackrf_device_list_t *device_list;
    hackrf_device *device;

    void check_result(int result);
};
}
#endif
