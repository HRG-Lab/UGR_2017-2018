/**
 * @file hackrf_interface.hpp
 */
#ifndef HACKRF_INTERFACE_HPP
#define HACKRF_INTERFACE_HPP

#include <exception>
#include <iostream>
#include <libhackrf/hackrf.h>
#include <memory>
#include <sstream>
#include <string>

namespace HackRF {

enum HackRFStatus { Open, Closed, Error };

class HackRFException : public std::exception {
  using std::exception::what;

public:
  HackRFException(int result);
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

  std::string info();

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
