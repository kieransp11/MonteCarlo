#include <pybind11/pybind11.h>
#include "maths.h"

namespace py = pybind11;

PYBIND11_MODULE(MonteCarlo, m)
{
    // optional module docstring
    m.doc() = "A Monte Carlo Python/C++ simulation package";

    // define the function bindings
    m.def("add", &add, "A function which adds two numbers");
    m.def("subtract", &subtract, "A functions which subtracts two numbers");
}