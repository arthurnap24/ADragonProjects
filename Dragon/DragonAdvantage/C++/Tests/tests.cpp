#include "../Analysis.cpp"
#include <gtest/gtest.h>

TEST( SimpleMovingAverageTest, Normal )
{
    std::vector closingPrices = { 2.3, 2.0, 1.6, 1.8 };
    ASSERT_EQ( 6, ADVANTAGE::ComputeSimpleMovingAverage( closingPrices) );
}