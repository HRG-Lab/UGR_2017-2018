/**
 * @file hackrf_interface.cpp
 */

#include "hackrf_interface.hpp"

namespace HackRF {

HackRFException::HackRFException(int result) {
  auto err_num = static_cast<hackrf_error>(result);
  msg = hackrf_error_name(err_num);
}

HackRFInterface::HackRFInterface() {
  status = HackRFStatus::Closed;
  serial_no = 0;
  device_list = nullptr;
  device = nullptr;
}

HackRFInterface::~HackRFInterface() {}

void HackRFInterface::open() {
  int result = hackrf_init();
  check_result(result);
  device_list = hackrf_device_list();
  if (device_list->devicecount < 1) {
    throw std::runtime_error("No HackRFs Found");
  }
  if (device_list->devicecount != 1) {
      std::cerr
        << "More than one HackRF found. Choosing first available";
  }
  serial_no = device_list->serial_numbers[0];

  result = hackrf_device_list_open(device_list, 0, &device);
  check_result(result);

  result = hackrf_board_id_read(device, &board_id);
  check_result(result);

  result = hackrf_version_string_read(device, version, 255);
  check_result(result);

  result = hackrf_board_partid_serialno_read(device, &read_partid_serialno);
  check_result(result);
}

void HackRFInterface::close() {}

std::string HackRFInterface::info() {
  std::stringstream ss;

  ss << std::endl << "HackRF Information: " << std::endl;
  ss << "\tSerial number: " << std::hex << (int *)serial_no << std::endl;
  ss << "\tBoard ID number: " << (int)board_id << std::endl;
  ss << "\tPart ID number: " << std::hex << read_partid_serialno.part_id << "\t"
     << std::hex << read_partid_serialno.serial_no << std::endl;

  return ss.str();
}

void HackRFInterface::check_result(int result) {
  if (result != HACKRF_SUCCESS) {
    throw HackRF::HackRFException(result);
  }
}
} // namespace HackRF
