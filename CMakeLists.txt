cmake_minimum_required(VERSION 2.8.12)
set(CMAKE_CXX_STANDARD 11)

project(MonteCarlo)

# Set source directory
set(SOURCE_DIR "src/MonteCarlo")

# Tell CMake that headers are also in SOURCE_DIR
include_directories(${SOURCE_DIR})
set(SOURCES "${SOURCE_DIR}/maths.cpp")

# Generate Python module
add_subdirectory(lib/pybind11)
pybind11_add_module(MonteCarlo ${SOURCES} "${SOURCE_DIR}/bindings.cpp")

SET(TEST_DIR "tests")
SET(TESTS ${SOURCES}
    "${TEST_DIR}/test_main.cpp"
    "${TEST_DIR}/test_maths.cpp")

# Generate a test executable
include_directories(lib/Catch2/single_include)
add_executable("${PROJECT_NAME}_test" ${TESTS})