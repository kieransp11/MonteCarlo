#include "maths.h"

#define BOOST_TEST_MODULE maths_test
#include <boost/test/unit_test.hpp>

BOOST_AUTO_TEST_SUITE( arithmetic_tests )

BOOST_AUTO_TEST_CASE( addition_test )
{
    BOOST_CHECK_EQUAL( add(1, 2) , 3 );
}

BOOST_AUTO_TEST_CASE( subtraction_test )
{
    BOOST_CHECK_EQUAL( subtract(1, 1), 0 );
}

BOOST_AUTO_TEST_SUITE_END()