TODO:

- CMake Warning at /usr/local/lib/cmake/boost_unit_test_framework-1.71.0/
  libboost_unit_test_framework-variant-shared.cmake:59 (message):
  Target Boost::unit_test_framework already has an imported location

  This is a bug in boost 1.71's cmake support.
  Source: https://stackoverflow.com/questions/58081084/target-boostlibrary-already-has-an-imported-location-link-errors

- Added mode retrieval into setup.py. This may be useful to avoid tests.
