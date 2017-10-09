/**
 * @file hackrf_interface.cpp
 */

#include "hackrf_interface.hpp"

namespace HackRF {

HackRFException::HackRFException(int result) {
    auto err_num = static_cast<hackrf_error>(result);
    msg = hackrf_error_name(err_num);
}

const char *HackRFException::what() { return msg.c_str(); }

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
        BOOST_LOG_TRIVIAL(warning)
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

void HackRFInterface::info() {
    if (status != HackRFStatus::Open) {
        BOOST_LOG_TRIVIAL(warning)
            << "Connection to HackRF is not open. Attempting to open";
        this->open();
    }
    BOOST_LOG_TRIVIAL(info) << "HackRF Information: ";
    BOOST_LOG_TRIVIAL(info)
        << "\t  Serial   number: " << std::hex << (int *)serial_no;
    BOOST_LOG_TRIVIAL(info) << "\t  Board ID number: " << (int)board_id;
    BOOST_LOG_TRIVIAL(info)
        << "\t  Part  ID number: " << std::hex << read_partid_serialno.part_id
        << "  " << std::hex << read_partid_serialno.serial_no;
}

void HackRFInterface::check_result(int result) {
    if (result != HACKRF_SUCCESS) {
        throw HackRF::HackRFException(result);
    }
}
} // namespace HackRF
