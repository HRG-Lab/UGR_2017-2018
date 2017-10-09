cmake_minimum_required (VERSION 3.9 FATAL_ERROR)
project(Datalogger C CXX)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/modules/")
set(CMAKE_CXX_STANDARD 14)

include(cmake/modules/clang-format.cmake)
include(cmake/modules/cppcheck.cmake)

# Set platform dependent warning flags
if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU" OR
    "${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")
  set(warnings "-Wall -Wextra -Werror")
  add_definitions(-DBOOST_LOG_DYN_LINK)
elseif ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "MSVC")
  set(warnings "/W4 /WX /EHsc")
endif()

# Set necessary compiler flags
if (NOT CONFIGURED_ONCE)
  set(CMAKE_CXX_FLAGS "${warnings} -pthread"
    CACHE STRING "Flags used by the compiler during all build types." FORCE)
  set(CMAKE_C_FLAGS "${warnings}"
    CACHE STRING "Flags used by the compiler during all build types." FORCE)
endif()

# Setup testing with google-test
configure_file(cmake/modules/CMakeLists.txt.in googletest-download/CMakeLists.txt)
execute_process(COMMAND ${CMAKE_COMMAND} -G "${CMAKE_GENERATOR}" .
  RESULT_VARIABLE result
  WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/googletest-download )
if(result)
  message(FATAL_ERROR "CMake step for googletest failed: ${result}")
endif()
execute_process(COMMAND ${CMAKE_COMMAND} --build .
  RESULT_VARIABLE result
  WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/googletest-download )
if(result)
  message(FATAL_ERROR "Build step for googletest failed: ${result}")
endif()

# Prevent overriding the parent project's compiler/linker
# settings on Windows
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)

# Add googletest directly to our build. This defines
# the gtest and gtest_main targets.
add_subdirectory(${CMAKE_BINARY_DIR}/googletest-src
                 ${CMAKE_BINARY_DIR}/googletest-build)

find_package(Threads REQUIRED)
find_package(LIBHACKRF REQUIRED)
find_package(Boost 1.63.0 COMPONENTS log log_setup date_time filesystem system REQUIRED)

include_directories(SYSTEM ${Boost_INCLUDE_DIR})  
include_directories(SYSTEM "${CMAKE_SOURCE_DIR}/lib/mavlink/v1.0")
include_directories(include)
include_directories(tests)

add_executable(datalogger
  src/datalogger.cpp
  src/serial_port.cpp
  src/pixhawk_interface.cpp
  src/hackrf_interface.cpp)
target_link_libraries(datalogger
  Threads::Threads
  ${Boost_LIBRARIES}
  hackrf)

add_executable(runTests
  tests/test.cpp
  src/serial_port.cpp
  src/pixhawk_interface.cpp
  src/hackrf_interface.cpp)
target_link_libraries(runTests
  Threads::Threads
  ${Boost_LIBRARIES}
  hackrf
  gtest_main)

add_executable(BasicRSSI
  src/basic_rssi.cpp
  src/serial_port.cpp
  src/pixhawk_interface.cpp)
target_link_libraries(BasicRSSI
  Threads::Threads
  ${Boost_LIBRARIES})
