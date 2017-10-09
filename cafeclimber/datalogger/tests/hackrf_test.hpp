#include "hackrf_interface.hpp"
#include "gtest/gtest.h"
#include <memory>

TEST(HackRFInterfaceTest, HandlesNoneFound) {
    std::unique_ptr<HackRF::HackRFInterface> hackrf =
        std::make_unique<HackRF::HackRFInterface>();
    ASSERT_THROW(hackrf->open(), std::runtime_error);
}

TEST(HackRFInterfaceTest, AttemptsOpenAndFails) {
    std::unique_ptr<HackRF::HackRFInterface> hackrf =
        std::make_unique<HackRF::HackRFInterface>();
    ASSERT_THROW(hackrf->info(), std::runtime_error);
}
