/**
 * @file serial_port.cpp
 *
 * @author Ryan Campbell
 */

#include "serial_port.hpp"

namespace SerialPort {

/// Creates serial port with default options:
///     * port_name: /dev/ttyUSB0
///     * baudrate: 57600
///
/// Initializes the serial port to closed and initializes
/// the pthread_mutex
SerialPort::SerialPort() {
    BOOST_LOG_TRIVIAL(trace) << "SerialPort()";
    status = Status::Closed;

    fd = -1;
    port_name = std::string("/dev/ttyUSB0");
    baudrate = 57600;
}

/// Creates a serial port with the provided parameters
///
/// Initializes the serial port to closed and initializes
/// the pthread_mutex
///
/// @param _port_name name of serial port
/// @param _baudrate baudrate of serial port
SerialPort::SerialPort(std::string _port_name, int _baudrate)
    : status(Status::Closed), fd(-1), baudrate(_baudrate),
      port_name(_port_name) {
    BOOST_LOG_TRIVIAL(trace)
        << "SerialPort(" << _port_name << ", " << _baudrate << ")";
}

/// Closes the serial port and destroys the pthread_mutex
SerialPort::~SerialPort() {
    if (status == Status::Open) {
        close();
    }
}

/// Opens the serial port based on:
///     * port_name
///     * baudrate
///
/// Will throw runtime error if any of the steps required
/// to open the serial port fails
void SerialPort::open() {
    BOOST_LOG_TRIVIAL(trace) << "SerialPort::open()";
    // Open the file descriptor
    fd = ::open(port_name.c_str(), O_RDWR | O_NOCTTY | O_NDELAY);
    if (fd == -1) {
        throw SerialPortException("Failed to open serial port");
    }
    fcntl(fd, F_SETFL,
        0); // No append, no async, no direct, no atime, no nonblocking

    // Setup the serial port for reading
    if (!isatty(fd)) {
        throw std::runtime_error("Specified file is not a serial port");
    }

    struct termios config;
    if (tcgetattr(fd, &config) < 0) {
        throw SerialPortException(strerror(errno));
    }

    // Input flags
    config.c_iflag &=
        ~(IGNBRK | BRKINT | ICRNL | INLCR | PARMRK | INPCK | ISTRIP | IXON);

    // Output flags
    config.c_oflag &= ~(OCRNL | ONLCR | ONLRET | ONOCR | OFILL | OPOST);

#ifdef OLCUC
    config.c_oflag &= ~OLCUC;
#endif
#ifdef ONOEOT
    config.c_oflag &= ~ONOEOT;
#endif

    // No line processing
    config.c_lflag &= ~(ECHO | ECHONL | ICANON | IEXTEN | ISIG);

    // No character processing
    config.c_cflag &= ~(CSIZE | PARENB);
    config.c_cflag |= CS8;

    config.c_cc[VMIN] = 1;
    config.c_cc[VTIME] = 10;

    int result;
    switch (baudrate) {
    case 1200:
        result = cfsetspeed(&config, B1200);
        break;
    case 1800:
        result = cfsetspeed(&config, B1800);
        break;
    case 9600:
        result = cfsetspeed(&config, B9600);
        break;
    case 19200:
        result = cfsetspeed(&config, B19200);
        break;
    case 38400:
        result = cfsetspeed(&config, B38400);
        break;
    case 57600:
        result = cfsetspeed(&config, B57600);
        break;
    case 115200:
        result = cfsetspeed(&config, B115200);
        break;
    case 460800:
        result = cfsetspeed(&config, B460800);
        break;
    case 921600:
        result = cfsetspeed(&config, B921600);
        break;
    default:
        // TODO: Can this be sanitized elsewhere
        throw SerialPortException("Unrecognized baud rate");
        break;
    }
    if (result != 0) {
        throw SerialPortException(strerror(errno));
    }

    // Where the configuration is actually set
    if (tcsetattr(fd, TCSAFLUSH, &config) < 0) {
        throw SerialPortException(strerror(errno));
    }

    status = Status::Open;
}

/// Closes serial port by file descriptor and sets status
/// to SerialPortStatus::Closed
void SerialPort::close() {
    BOOST_LOG_TRIVIAL(trace) << "SerialPort::close()";
    int result = ::close(fd);
    if (result) {
        perror("Serial Port");
    }
    status = Status::Closed;
}

/// Attempts to read a byte into cp. Mutex is locked during read
///
/// @param cp an unsigned 8 bit integer buffer
///
/// @return If succesful, returns the number of bytes read. Otherwise returns
/// -1.
int SerialPort::read(uint8_t &cp) {
    BOOST_LOG_TRIVIAL(trace) << "SerialPort::read(" << &cp << ")";
    if (status != Status::Open) {
        BOOST_LOG_TRIVIAL(warning)
            << "Port not opened before read. Attempting to open...";
        open();
    }

    mutex.lock();
    int result = ::read(fd, &cp, 1);
    mutex.unlock();

    BOOST_LOG_TRIVIAL(debug) << "Read result " << (int)cp;

    return result;
}

/// Attempts to write len bytes from buf into serial port
///
/// @param buf buffer of bytes to be read from
/// @param len how many bytes to read
///
/// @return If succesful, returns number of bites written. Otherwise return -1.
int SerialPort::write(char *buf, size_t len) {
    mutex.lock();
    const int bytes_written = ::write(fd, buf, len);
    tcdrain(fd); // Ensure all bytes are written
    mutex.unlock();

    return bytes_written;
}

}
