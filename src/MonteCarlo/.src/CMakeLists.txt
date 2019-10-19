cmake_minimum_required(VERSION 2.8.12)
set(CMAKE_CXX_STANDARD 14)

# Set the project name
project(MonteCarlo)

# Set source directory
set(SOURCE_DIR "/Users/kieran/Git/MonteCarlo/src/MonteCarlo")
set(SOURCES "${SOURCE_DIR}/maths.cpp")
set(BINDINGS "${SOURCE_DIR}/.src/temp/template_mod_51318a8bf4ff48beba5be085036869fe.cpp")

# Tell CMake that headers are also in SOURCE_DIR
include_directories(${SOURCE_DIR})

# <begin_section>pybind11</begin_section>
find_package(Pybind11 REQUIRED COMPONENTS pybind11_add_modules)
pybind11_add_module(template_mod_51318a8bf4ff48beba5be085036869fe ${SOURCES} ${BINDINGS})
# <end_section>pybind11</end_section>