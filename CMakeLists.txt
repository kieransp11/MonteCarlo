cmake_minimum_required(VERSION 2.8.12)
set(CMAKE_CXX_STANDARD 14)

# Set the project name
project(MonteCarlo)

# Set source directory
set(SOURCE_DIR "/Users/kieran/Git/MonteCarlo/src/MonteCarlo")
set(SOURCES "${SOURCE_DIR}/maths.cpp")
set(BINDINGS "${SOURCE_DIR}/bindings.cpp")

# Tell CMake that headers are also in SOURCE_DIR
include_directories(${SOURCE_DIR})

# <begin_section>pybind11</begin_section>
find_package(Pybind11 REQUIRED COMPONENTS pybind11_add_modules)
pybind11_add_module(MonteCarlo ${SOURCES} ${BINDINGS})
# <end_section>pybind11</end_section>

# <begin_section>unit_testing</begin_section>
# Add an library for the example classes
add_library(MonteCarloLib
    "${SOURCES}"
)

find_package(Boost REQUIRED COMPONENTS unit_test_framework)
target_link_libraries(MonteCarloLib
    PUBLIC
        Boost::boost
)

SET(TEST_DIR "tests")

# enable CTest testing
enable_testing()

# Add a testing executable
add_executable(MonteCarlo_test "${TEST_DIR}/test_maths.cpp")

target_link_libraries(MonteCarlo_test
    MonteCarloLib
    Boost::unit_test_framework
)

target_compile_definitions(MonteCarlo_test
    PRIVATE
        BOOST_TEST_DYN_LINK
)

add_test(test_all MonteCarlo_test)
# <end_section>unit_testing</end_section>