cmake_minimum_required(VERSION 2.8.12)
set(CMAKE_CXX_STANDARD 11)

# Set the project name
project(MonteCarlo)

# Set source directory
set(SOURCE_DIR "src/MonteCarlo")

# Add an library for the example classes
add_library(MonteCarloLib
    "${SOURCE_DIR}/maths.cpp"
)

target_include_directories(MonteCarloLib
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}
)

target_link_libraries(MonteCarloLib
    PUBLIC
        Boost::boost
)

###############################################################################
# Pybind11
# Tell CMake that headers are also in SOURCE_DIR
include_directories(${SOURCE_DIR})
set(SOURCES "${SOURCE_DIR}/maths.cpp")


# Generate Python module
add_subdirectory(lib/pybind11)
pybind11_add_module(MonteCarlo ${SOURCES} "${SOURCE_DIR}/bindings.cpp")

###############################################################################
# Unit testing
find_package(Boost REQUIRED COMPONENTS unit_test_framework)

SET(TEST_DIR "tests")

# enable CTest testing
enable_testing()

# Add a testing executable
add_executable(unit_tests "${TEST_DIR}/test_maths.cpp")

target_link_libraries(unit_tests
    MonteCarloLib
    Boost::unit_test_framework
)

target_compile_definitions(unit_tests
    PRIVATE
        BOOST_TEST_DYN_LINK
)

add_test(test_all unit_tests)

# SET(TESTS ${SOURCES}
#    "${TEST_DIR}/test_maths.cpp")

# Generate a test executable
# add_executable("${PROJECT_NAME}_test" ${TESTS})