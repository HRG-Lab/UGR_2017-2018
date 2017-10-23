/**
 * @file pixhawk_interface.cpp
 *
 * @brief Defines the class for interfacing with the autopilot
 *
 * @author Ryan Campbell
 */

#include "pixhawk_interface.hpp"

namespace Pixhawk {

PixhawkException::PixhawkException(std::string msg_) : msg(msg_) {}

const char *PixhawkException::what() { return msg.c_str(); }

/// Creates an instance of PixhawkInterface by constructing
/// a serial port and assigning it to the serial port member
///
/// @param port_name path to device file (e.g. "/dev/ttyUSB0")
/// @param baudrate UART communication speed
PixhawkInterface::PixhawkInterface(std::string port_name, int baudrate) {
    serial_port = std::make_unique<SerialPort::SerialPort>(port_name, baudrate);
}

PixhawkInterface::~PixhawkInterface() {}

PixhawkData PixhawkInterface::read_gps_imu_rssi() {
    bool received_gps = false;
    bool received_imu = false;
    bool received_rssi = false;

    mavlink_message_t current_message;

    PixhawkData data;

    for (int i = 0; i < 5; i++) {
        current_message = read();

        switch (current_message.msgid) {
        case MAVLINK_MSG_ID_GLOBAL_POSITION_INT: {
            received_gps = true;
            mavlink_global_position_int_t gps;
            mavlink_msg_global_position_int_decode(&current_message, &gps);
            data.lat = gps.lat;
            data.lon = gps.lon;
            data.alt = gps.alt;
            data.vx = gps.vx;
            data.vy = gps.vy;
            data.vz = gps.vz;
            data.hdg = gps.hdg;
            break;
        }
        case MAVLINK_MSG_ID_ATTITUDE: {
            received_imu = true;
            mavlink_attitude_t attitude;
            mavlink_msg_attitude_decode(&current_message, &attitude);
            data.roll = attitude.roll;
            data.pitch = attitude.pitch;
            data.yaw = attitude.yaw;
            data.rollspeed = attitude.rollspeed;
            data.pitchspeed = attitude.pitchspeed;
            data.yawspeed = attitude.yawspeed;
            break;
        }
        case MAVLINK_MSG_ID_RADIO_STATUS: {
            received_rssi = true;
            mavlink_radio_status_t radio;
            mavlink_msg_radio_status_decode(&current_message, &radio);
            data.rssi = radio.rssi;
            break;
        }
        default: { break; }
        }
        usleep(1000);
    }
    data.complete = (received_gps && received_imu && received_rssi);
    return data;
}

std::string PixhawkInterface::read_all() {
    mavlink_message_t message = read();
    return decode_message(message);
}

/// Attempts to read from the serial port and returns what message was received
mavlink_message_t PixhawkInterface::read() {
    uint8_t cp = 0;

    mavlink_message_t message;
    mavlink_status_t status;

    // Attempt to read from serial port
    int result = serial_port->read(cp);
    if (result > 0) {
        mavlink_parse_char(MAVLINK_COMM_1, cp, &message, &status);
        current_status = status;
    } else {
        throw std::runtime_error("Failed to read from port");
    }

    return message;
}

/// Closes associated serial port
void PixhawkInterface::close() {
    std::cerr << "Unhandled Message IDs: " << std::endl;
    for (auto elem : unhandled_msg_ids) {
        std::cerr << elem << " ";
    }
    std::cerr << std::endl;
    serial_port->close();
}

/// Decodes a MAVLink message and returns the string as it should be formatted
/// for logging into a file.
///
/// @param message MAVLink message to be decoded
std::string PixhawkInterface::decode_message(const mavlink_message_t &message) {
    std::stringstream message_string;

    switch (message.msgid) {
    case MAVLINK_MSG_ID_HEARTBEAT: {
        BOOST_LOG_TRIVIAL(info) << "MAVLINK_MSG_ID_HEARTBEAT";
        mavlink_heartbeat_t heartbeat;
        mavlink_msg_heartbeat_decode(&message, &heartbeat);
        break;
    }
    case MAVLINK_MSG_ID_LOCAL_POSITION_NED: {
        BOOST_LOG_TRIVIAL(info) << "MAVLINK_MSG_ID_LOCAL_POSITION_NED";
        break;
    }
    case MAVLINK_MSG_ID_GLOBAL_POSITION_INT: {
        BOOST_LOG_TRIVIAL(info) << "MAVLINK_MSG_GLOBAL_POSITION_INT";
        mavlink_global_position_int_t gps;
        mavlink_msg_global_position_int_decode(&message, &gps);
        message_string << "[GPS]     LAT: " << gps.lat << " LON: " << gps.lon;
        break;
    }
    case MAVLINK_MSG_ID_ATTITUDE: {
        BOOST_LOG_TRIVIAL(info) << "MAVLINK_MSG_ID_ATTITUDE";
        mavlink_attitude_t attitude;
        mavlink_msg_attitude_decode(&message, &attitude);
        message_string << "[ATTITUDE] ROLL: " << attitude.roll
                       << " PITCH: " << attitude.pitch
                       << " YAW: " << attitude.yaw;
        break;
    }
    case MAVLINK_MSG_ID_GPS_RAW_INT: {
        BOOST_LOG_TRIVIAL(info) << "MAVLINK_MSG_ID_GPS_RAW_INT";
        mavlink_gps_raw_int_t gps;
        mavlink_msg_gps_raw_int_decode(&message, &gps);
        message_string << "[GPS FIX] ENUM: " << (unsigned int)gps.fix_type;
        break;
    }
    default:
        //unhandled_msg_ids.insert(message.msgid);
        break;
    }
    return message_string.str();
}
}
