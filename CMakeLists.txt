cmake_minimum_required (VERSION 3.9 FATAL_ERROR)
project(Datalogger C CXX)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/modules/")
set(CMAKE_CXX_STANDARD 14)

if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU" OR
    "${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")
  set(warnings "-Wall -Wextra -Werror")
elseif ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "MSVC")
  set(warnings "/W4 /WX /EHsc")
endif()

if (NOT CONFIGURED_ONCE)
  set(CMAKE_CXX_FLAGS "${warnings} -pthread"
    CACHE STRING "Flags used by the compiler during all build types." FORCE)
  set(CMAKE_C_FLAGS "${warnings}"
    CACHE STRING "Flags used by the compiler during all build types." FORCE)
endif()

find_package(Threads REQUIRED)
find_package(LIBHACKRF REQUIRED)

include_directories(SYSTEM "${CMAKE_SOURCE_DIR}/lib/mavlink/v1.0")
include_directories(include)
file(GLOB SOURCES "src/*.cpp")

add_executable(datalogger ${SOURCES})
target_link_libraries(datalogger ${CMAKE_THREAD_LIBS_INIT} hackrf)
