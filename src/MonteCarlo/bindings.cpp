#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
namespace py = pybind11;

#include <boost/hana.hpp>
namespace hana = boost::hana;
using namespace hana::literals;
using namespace std::string_literals;

#include <string>
#include <vector>

#include "maths.h"

namespace binding
{
    void init_ex1(py::module &m) {
        // define the function bindings
        m.def("add", &add, "A function which adds two numbers");
        m.def("subtract", &subtract, "A functions which subtracts two numbers");
    }

    void init_ex2(py::module &m){
        // define the function bindings
        m.def("multiply", &multiply, "A function which multiplys two numbers");
        m.def("divide", &divide, "A function which divides two numbers"); 
    };
}

struct TemplateDetails{
    TemplateDetails(int num_args, 
                    std::vector<std::string> constructors,
                    std::vector<std::string> methods_to_bind) : 
        num_args(num_args),
        constructors(constructors),
        methods_to_bind(methods_to_bind) {};
    int num_args;
    std::vector<std::string> constructors;
    std::vector<std::string> methods_to_bind;
};

PYBIND11_MODULE(MonteCarlo, m)
{
    // optional module docstring
    m.doc() = "A Monte Carlo Python/C++ simulation package";

    binding::init_ex1(m);
    binding::init_ex2(m);

    /*auto types = hana::make_tuple(
        hana::make_tuple(hana::type_c<float>), 
        hana::make_tuple(hana::type_c<int>),
        hana::make_tuple(hana::type_c<std::string>));

    hana::for_each(types, 
        [&](auto template_type){
            using T = typename decltype(+template_type[0_c])::type;
            m.def("getMax", &get_max<T>, "A function which returns the maximum of two arguments");
        });*/

    /*auto types2 = hana::make_tuple(
        hana::make_tuple(hana::type_c<int>),
        hana::make_tuple(hana::type_c<std::string>));

    hana::for_each(types2,
        [&](auto template_type){
            using T = typename decltype(+template_type[0_c])::type;
            py::class_<Stack<T>>(m, "Stack")
                .def(py::init<>())
                .def("push", &Stack<T>::push)
                .def("pop", &Stack<T>::pop)
                .def("peek", &Stack<T>::peek)
                .def("empty", &Stack<T>::empty)
                .def("height", &Stack<T>::height);
        });*/


    py::class_<TemplateDetails>(m, "TemplateDetails")
        .def(py::init<const int &, const std::vector<std::string>, const std::vector<std::string>>())
        .def_readonly("num_args", &TemplateDetails::num_args)
        .def_readonly("constructors", &TemplateDetails::constructors)
        .def_readonly("methods_to_bind", &TemplateDetails::methods_to_bind);

    m.def("template_getMax", [&](){
        return TemplateDetails(1, {}, {});
    }, "foo");

    m.def("template_Stack", [&](){
        return TemplateDetails(
            1, 
            { "py::init<>()",},
            {"push", "pop", "peek", "empty", "height"}
        );
    }, "bar");
}