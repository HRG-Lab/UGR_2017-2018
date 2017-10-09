#include "./hackrf_test.hpp"
#include "gtest/gtest.h"
#include <boost/log/core.hpp>
#include <boost/log/expressions.hpp>
#include <boost/log/trivial.hpp>
#include <iostream>

// We're only interested in error output from the unit tests;
// We don't care about the logging output.
void disable_logging() { boost::log::core::get()->set_logging_enabled(false); }

int main(int argc, char **argv) {
    testing::InitGoogleTest(&argc, argv);
    disable_logging();
    return RUN_ALL_TESTS();
}
