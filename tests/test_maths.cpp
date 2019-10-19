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

BOOST_AUTO_TEST_CASE( multiplication_test )
{
    BOOST_CHECK_EQUAL( multiply(2, 2), 4 );
}

BOOST_AUTO_TEST_CASE( division_test )
{
    BOOST_CHECK_EQUAL( divide(4, 2), 2 );
}

BOOST_AUTO_TEST_CASE( max_test )
{
    BOOST_CHECK_EQUAL( get_max(2, 4), 4);
    BOOST_CHECK_EQUAL( get_max(2.1, 2.2), 2.2);
    BOOST_CHECK_EQUAL( get_max("a", "b"), "b");
}

BOOST_AUTO_TEST_SUITE_END()