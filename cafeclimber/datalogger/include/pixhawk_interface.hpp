/**
 * @file pixhawk_interface.hpp
 *
 * @brief Defines the class for interfacing with a Pixhawk
 */

#ifndef AUTOPILOT_INTERFACE_H
#define AUTOPILOT_INTERFACE_H

#include "serial_port.hpp"

#include <boost/log/trivial.hpp>
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

namespace Pixhawk {

class PixhawkException : std::exception {
    using std::exception::what;

  public:
    PixhawkException(std::string msg_);
    ~PixhawkException() throw(){};

    const char *what();

  private:
    std::string msg;
};

struct PixhawkData {
    // From ATTITUDE (#30)
    float roll{0};       ///< Roll angle (rad, -pi..+pi)
    float pitch{0};      ///< Pitch angle (rad, -pi..+pi)
    float yaw{0};        ///< Yaw angle (rad, -pi..+pi)
    float rollspeed{0};  ///< Roll angular speed (rad/s)
    float pitchspeed{0}; ///< Pitch angular speed (rad/s)
    float yawspeed{0};   ///< Yaw angular speed (rad/s)
    // From GLOBAL_POSITION_INT (#33)
    int32_t lat{0};  ///< Latitude [Degrees * 1E7]
    int32_t lon{0};  ///< Longitude [Degrees * 1E7]
    int32_t alt{0};  ///< Altitude (from sea level) [*1000 (millimeters)]
    int16_t vx{0};   ///< X Ground speed (Latitude, positive north) as m/s * 100
    int16_t vy{0};   ///< Y Ground speed (Longitude, positive east) as m/s * 100
    int16_t vz{0};   ///< Z Ground speed (Altitude, positive down) as m/s * 100
    uint16_t hdg{0}; ///< Vehicle heading in degrees * 100. 0.0..359
    // From RADIO_STATUS (#109)
    uint8_t rssi{0}; ///< Local signal strength

    bool complete{false}; ///< Whether or not the struct has been fully packed

    friend std::ostream &operator<<(std::ostream &os, const PixhawkData &data) {
        os << data.lat << "," << data.lon << "," << data.alt << "," << data.vx
           << "," << data.vy << "," << data.vz << "," << data.hdg << ","
           << data.roll << "," << data.pitch << "," << data.yaw << ","
           << data.rollspeed << "," << data.pitchspeed << "," << data.yawspeed
           << "," << data.rssi;
        return os;
    }
};

/// Represents a connection to a Pixhawk over a serial port
class PixhawkInterface {
  public:
    PixhawkInterface() = delete;
    PixhawkInterface(const std::string port_name, const int baudrate);
    ~PixhawkInterface();

    PixhawkData read_gps_imu_rssi();
    mavlink_message_t read();
    std::string read_all();
    void close();

  private:
    mavlink_status_t current_status;

    std::shared_ptr<SerialPort::SerialPort> serial_port;
    std::unordered_set<int> unhandled_msg_ids;

    std::string decode_message(const mavlink_message_t &message);
};

} // namespace Pixhawk

#endif // AUTOPILOT_INTERFACE_H
