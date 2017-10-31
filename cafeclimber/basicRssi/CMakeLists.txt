cmake_minimum_required (VERSION 3.9 FATAL_ERROR)
project(Datalogger C CXX)

# Set platform dependent warning flags
if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU" OR
    "${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")
  set(warnings "-Wall -Wextra -Werror -g")
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

find_package(Threads REQUIRED)

include_directories(SYSTEM ${Boost_INCLUDE_DIR})  
include_directories(include)
include_directories(tests)

add_executable(BasicRSSI
  src/basic_rssi.cpp
  src/packet.cpp)
target_link_libraries(BasicRSSI
  Threads::Threads
  xbee
  xbeep)
