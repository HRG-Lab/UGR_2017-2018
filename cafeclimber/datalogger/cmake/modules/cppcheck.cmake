# additional target to perform cppcheck

file(GLOB SOURCE_FILES
  tests/*.cpp
  tests/*.hpp
  src/*.cpp
  include/*/hpp)

add_custom_target(
  cppcheck
  COMMAND /usr/bin/cppcheck
  --enable=warning,performance,portability,information,missingInclude
  --std=c++11
  --verbose
  --quiet
  ${SOURCE_FILES}
)

