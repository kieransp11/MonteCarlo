#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
namespace py = pybind11;

#include<string>
#include<iostream>

#include <boost/hana.hpp>
namespace hana = boost::hana;
using namespace hana::literals;
using namespace std::string_literals;

{{compiler_headers}}

{{other_headers}}

PYBIND11_MODULE({{module_name}}, m)
{
{{bindings}}
}