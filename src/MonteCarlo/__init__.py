Templates = type("Templates", (object,), {})()

# NOTES:
# python: method names use lower case separater by underscores
#         classes use CapsCaseLikeThis
# c++:    methods use camelCaseWithHumpsInTheMiddleLikeThis
#         classes use CapsCaseLikeThis

def __mangle_type_name(type_name):
    type_name = type_name.replace("std::", "")\
                         .replace("<", "_")\
                         .replace(">", "_")\
                         .replace("::", "_")
    if type_name[-1] == "_":
        type_name == type_name[:-1]

    return type_name


def __check_overload(templateable):
    if templateable.__name__.replace("template_", "") in dir(Templates):
        pass
        #raise RuntimeError("Cannot produce more template instances")

def __to_snake_case (camel_input):
    import re
    # TODO do this more rigorously
    regex = re.compile(r'[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+')
    words = re.findall(regex, camel_input)
    return '_'.join(map(str.lower, words))


def __build_hana_frame(templateable, types_cart_prod):
    # The i part is for classes
    details = templateable()
    binding = """
    int i = 1;
    auto types = hana::make_tuple(
        {{template_instances}}
    );
    
    hana::for_each(types,
        [&](auto instance_types){
            {{type_aliases}}
            {{bulk}}
            ++i;
        });
        
    std::cout << i;
    """
    template_instances = []
    for instance in types_cart_prod:
        hana_types = [f"hana::type_c<{t}>" for t in instance]
        hana_array = f"hana::make_tuple({','.join(hana_types)})"
        template_instances.append(hana_array)

    type_aliases = [f"using T_{i} = typename decltype(+instance_types[{i}_c])::type;" for i in range(details.num_args)]

    binding = binding.replace("{{template_instances}}", ",\n        ".join(template_instances))\
                     .replace("{{type_aliases}}", ",\n            ".join(type_aliases))

    return binding 

def __build_fn_bindings(templateable, types_cart_prod):
    details = templateable()
    binding = __build_hana_frame(templateable, types_cart_prod)
    bulk = """m.def("{{callable_name}}", &{{callable_snake_name}}<{{template_args}}>, "I'm some foo description");"""
    binding = binding.replace("{{bulk}}", bulk)

    callable_name = templateable.__name__.replace("template_", "")
    binding = binding.replace("{{callable_name}}", callable_name)\
                     .replace("{{callable_snake_name}}", __to_snake_case(callable_name))\
                     .replace("{{template_args}}", ",".join([f"T_{i}" for i in range(details.num_args)]))

    return binding


def __build_cl_bindings(templateable, types_cart_prod):

    details = templateable()
    binding = __build_hana_frame(templateable, types_cart_prod)
    bulk = """py::class_<{{callable_name}}<{{template_args}}>>(m, {{callable_name_types}})
                {{constructors}}
                {{methods}}
    """
 
    # TODO: need a list of methods of the class
    # can then just produce default constructor (arg constructors is todo)
    # then iterate over method names provided and produces the member functions
    # Assume each name is as the function is declared, then just iterate over and do
    # simple string substitution
    method_bindings = []
    for method in details.methods_to_bind:
        method_bind = """.def("{{method_snake_case}}", &{{callable_name}}<{{template_args}}>::{{method_name}})"""
        method_bind = method_bind.replace("{{method_snake_case}}", __to_snake_case(method))\
                                 .replace("{{method_name}}", method)
        method_bindings.append(method_bind)

    callable_name = templateable.__name__.replace("template_","")
    bulk = bulk.replace("{{constructors}}", '\n'.join([f".def({c})" for c in details.constructors]))\
               .replace("{{methods}}", '\n                '.join(method_bindings)+";")\
               .replace("{{callable_name}}", callable_name)\
               .replace("{{template_args}}", ','.join([f"T_{i}" for i in range(details.num_args)]))\
               .replace("{{callable_name_types}}", f'&("{callable_name}_"+std::to_string(i))[0]')
    
    return binding.replace("{{bulk}}",bulk)


def __load_from_file(module_name, module_path):
    import importlib.util
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for entry in dir(module):
        if entry[:2] != "__" or entry[-2:] != "__":
            setattr(Templates, entry, getattr(module, entry))


def __compile():
    import os
    import sys
    import subprocess

    module_dir = os.path.dirname(os.path.abspath(__file__))
    temp_dir = os.path.join(module_dir, ".src", "temp")
    build_dir = os.path.join(module_dir, ".src", "build")
    if not os.path.isdir(build_dir):
        os.makedirs(build_dir)

    cmake_path = os.path.join(module_dir, ".src", "CMakeLists.txt")
    if not os.path.isfile(cmake_path):
        raise RuntimeError(
            "No cmake file found, please rebuild.")

    cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + temp_dir,
                  '-DPYTHON_EXECUTABLE=' + sys.executable,
                  '-DCMAKE_BUILD_TYPE=Release',
                  '-GNinja']
    
    env = os.environ.copy()
    # suppress stdout and only print stderr, if any.
    subprocess.check_call(['cmake', '..'] + cmake_args,
                          cwd=build_dir, env=env, stdout=subprocess.DEVNULL)

    subprocess.check_call(['ninja'], cwd=build_dir)


def template(templateable, types_cart_prod, compiler_headers, other_headers, in_memory=True, defer_compile=False):
    import os
    import uuid
    from types import FunctionType

    __check_overload(templateable)
    
    module_name = "template_mod_" + str(uuid.uuid4()).replace("-", "")

    # write a source file
    with open("/Users/kieran/Git/MonteCarlo/src/MonteCarlo/.src/bindings_template.cpp", "r") as f:
        template = f.read()

        # add compiler headers
        if compiler_headers:
            compiler_header_lines = '\n'.join(map(lambda x: f"#include <{x}>", compiler_headers))
            template = template.replace("{{compiler_headers}}", compiler_header_lines)
        else:
            template = template.replace("{{compiler_headers}}\n", "")
        
        # add other headers
        if other_headers:
            other_header_lines = '\n'.join(map(lambda x: f'#include "{x}"', other_headers))
            template = template.replace("{{other_headers}}", other_header_lines)
        else:
            template = template.replace("{{other_headers}}\n", "")

        # build bindings
        details = templateable()
        if len(details.constructors) == 0:
            template = template.replace("{{bindings}}", __build_fn_bindings(templateable, types_cart_prod))
        else:
            template = template.replace("{{bindings}}",__build_cl_bindings(templateable, types_cart_prod))
        template = template.replace("{{module_name}}", module_name)
        
        src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".src", "temp", f"{module_name}.cpp")
        
        with open(src_path, "w") as src_file:
            src_file.write(template)

    with open("/Users/kieran/Git/MonteCarlo/src/MonteCarlo/.src/CMakeLists_template.txt", "r") as f:
        cmake_lists = f.read()
        cmake_lists = cmake_lists.replace("{{module_name}}", module_name)

        cmake_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".src", "CMakeLists.txt")
        with open(cmake_path, "w") as cmake_file:
            cmake_file.write(cmake_lists)


    module_path = f"/Users/kieran/Git/MonteCarlo/src/MonteCarlo/.src/temp/{module_name}.cpython-37m-darwin.so"

    __compile()
    __load_from_file(module_name, module_path)


from .MonteCarlo import *
from .foo import *
__all__ = [MonteCarlo, foo]
