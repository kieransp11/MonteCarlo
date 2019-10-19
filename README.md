TODO:

- CMake Warning at /usr/local/lib/cmake/boost_unit_test_framework-1.71.0/
  libboost_unit_test_framework-variant-shared.cmake:59 (message):
  Target Boost::unit_test_framework already has an imported location

  This is a bug in boost 1.71's cmake support.
  Source: https://stackoverflow.com/questions/58081084/target-boostlibrary-already-has-an-imported-location-link-errors

- Added mode retrieval into setup.py. This may be useful to avoid tests.

- Move temporary build directory to /dev/shm or another ram location

- Add support for variadic templates, a constructors 
with template type arguments

- move from specifying types as strings and move to specifying actual types. This would require passing the types to c++, and reverse engineering their namespace and includes. At oxam typically the namespaces follow the file heirarchy structure - this would require some preprocessing. Could use oxam TypeInfo after preprocessing every header in a project (could be done at build time)

- add direct access on the class fields