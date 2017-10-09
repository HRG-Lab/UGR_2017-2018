# additional target to perform clang-format

file(GLOB SOURCE_FILES
  tests/*.cpp
  tests/*.hpp
  src/*.cpp
  include/*/hpp)

add_custom_target(
  clangformat
  COMMAND /usr/bin/clang-format
  -i
  ${SOURCE_FILES}
)

