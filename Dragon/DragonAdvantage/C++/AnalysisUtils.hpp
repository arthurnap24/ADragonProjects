#ifndef ANALYSIS_UTILS_H
#define ANALYSIS_UTILS_H

#include <vector>

namespace ADVANTAGE
{

float ComputeSimpleMovingAverage( const std::vector< float > closePrices );
float ComputeExponentialMovingAverage( const std::vector< float > closePrices );
float ComputeRelativeStrength( const std::vector< float > closePrices );
float ComputeRelativeStrengthIndex( const std::vector< float > closePrices );

};

#endif