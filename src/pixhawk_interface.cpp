/**
 * @file pixhawk_interface.cpp
 *
 * @brief Defines the class for interfacing with the autopilot
 *
 * @author Ryan Campbell
 */

#include "pixhawk_interface.hpp"

/// Gets the current time of day using the Linux syscall
/// and converts the timeval struct to microseconds
///
/// @return Time in microseconds
uint64_t get_time_usec() {
    static struct timeval time_stamp;
    gettimeofday(&time_stamp, NULL);
    return time_stamp.tv_sec * USEC_PER_SEC + time_stamp.tv_usec;
}

/// Creates an instance of PixhawkInterface by constructing
/// a serial port and assigning it to the serial port member
///
/// @param port_name path to device file (e.g. "/dev/ttyUSB0")
/// @param baudrate UART communication speed
PixhawkInterface::PixhawkInterface(std::string port_name, int baudrate) {
    BOOST_LOG_TRIVIAL(trace)
        << "PixhawkInterface(" << port_name << ", " << baudrate << ")";
    serial_port = std::make_unique<SerialPort>(port_name, baudrate);
}

PixhawkInterface::~PixhawkInterface() {
}

/// Private method called by start_read_thread
///
/// Attempts to read from the serial port then pass what was
/// read to decode_message
std::string PixhawkInterface::read_thread() {
    uint8_t cp = 0;
    uint8_t msgReceived = false;

    mavlink_message_t message;
    mavlink_status_t status;

    // Attempt to read from serial port
    int result = serial_port->read(cp);
    if (result > 0) {
        msgReceived =
            mavlink_parse_char(MAVLINK_COMM_1, cp, &message, &status);
        current_status = status;
    } else {
        throw std::runtime_error("Failed to read from port");
    }
    BOOST_LOG_TRIVIAL(debug) << "Message received!";
    BOOST_LOG_TRIVIAL(debug)
        << "sysid: " << (int)message.sysid << " compid: " << (int)message.compid;
    
    return decode_message(message);
}

/// Closes associated serial port
void PixhawkInterface::close(){
    BOOST_LOG_TRIVIAL(debug) << "Unhandled Message IDs: ";
    for(auto elem : unhandled_msg_ids) {
        std::cout << elem << " ";
    }
    std::cout << std::endl;
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
        BOOST_LOG_TRIVIAL(debug) << "MAVLINK_MSG_ID_HEARTBEAT";
        mavlink_heartbeat_t heartbeat;
        mavlink_msg_heartbeat_decode(&message, &heartbeat);
        break;
    }
    case MAVLINK_MSG_ID_LOCAL_POSITION_NED: {
        BOOST_LOG_TRIVIAL(debug) << "MAVLINK_MSG_ID_LOCAL_POSITION_NED";
        break;
    }
    case MAVLINK_MSG_ID_GLOBAL_POSITION_INT: {
        BOOST_LOG_TRIVIAL(debug) << "MAVLINK_MSG_GLOBAL_POSITION_INT";
        mavlink_global_position_int_t gps;
        mavlink_msg_global_position_int_decode(&message, &gps);
        message_string << "[GPS]     LAT: " << gps.lat
                       << " LON: " << gps.lon;
        break;
    }
    case MAVLINK_MSG_ID_ATTITUDE: {
        BOOST_LOG_TRIVIAL(debug) << "MAVLINK_MSG_ID_ATTITUDE";
        mavlink_attitude_t attitude;
        mavlink_msg_attitude_decode(&message, &attitude);
        message_string << "[ATTITUDE] ROLL: " << attitude.roll
                       << " PITCH: " << attitude.pitch
                       << " YAW: " << attitude.yaw;
        break;
    }
    default:
        unhandled_msg_ids.insert(message.msgid);
        break;
    }
    return message_string.str();
}
