#ifndef EXT_ANALYSIS_UTILS_H
#define EXT_ANALYSIS_UTILS_H
#include "AnalysisUtils.hpp"
#endif

#include <numeric>

namespace ADVANTAGE
{

float
ComputeSimpleMovingAverage( const std::vector< float > closePrices )
{
    return std::accumulate( closePrices.begin(), closePrices.end(), 0.0f ) / closePrices.size();

}

/* lower index are more recent values*/
float
ComputeExponentialMovingAverage( const std::vector< float > closePrices )
{
    int i;
    int lim = closePrices.size();
    int weight = lim;
    float weightedSum;
    for ( i=0; i<lim; i++ )
    {
        weightedSum += weight * closePrices[ i ];
        weight--;
    }
    return weightedSum / lim;
}

float
ComputeRelativeStrength( const std::vector< float > closePrices )
{
    unsigned i, numerator, lim( closePrices.size() );

    for ( i=0; i<lim; i++ )
    {
        numerator += closePrices[ i ];
    }

    return numerator / lim;
}

float
ComputeRelativeStrengthIndex( const std::vector< float > closePrices )
{
    return 100 - 100 / ( 1 + ComputeRelativeStrength( closePrices ) );
}

}