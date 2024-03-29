import os
import re
import sys
import sysconfig
import platform
import subprocess

from shutil import copyfile, copymode

from distutils.version import LooseVersion
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext

MODE = ""


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        """ Verify CMAKE and Ninja version """
        try:
            cmake_out = subprocess.check_output(['cmake', '--version'])
            ninja_out = subprocess.check_output(['ninja', '--version'])
        except OSError:
            raise RuntimeError(
                "CMake and Ninja must be installed to build the following "
                "extensions: " + ", ".join(e.name for e in self.extensions))

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        """ Generate CMAKE build commands and run them with Ninja """
        print("MODE:", MODE)
        extdir = os.path.abspath(
            os.path.dirname(self.get_ext_fullpath(ext.name)))

        cfg = 'Debug' if self.debug else 'Release'
        # make sure .so is stored in  the correct directory
        # path to the python interpreter
        # generate ninja build file
        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
                      '-DPYTHON_EXECUTABLE=' + sys.executable,
                      '-DCMAKE_BUILD_TYPE=' + cfg,
                      '-GNinja']

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(
            env.get('CXXFLAGS', ''),
            self.distribution.get_version())

        # build to build, not self.build_temp=build/temp.macosx-10.7-x86_64-3.7
        build_dir = os.path.join(ext.sourcedir, "build")
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)

        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args,
                              cwd=build_dir, env=env)
        subprocess.check_call(['ninja'], cwd=build_dir)

        # Copy *_test file to tests directory
        test_bin = os.path.join(build_dir, 'MonteCarlo_test')
        self.copy_test_file(test_bin)

        print()  # Add an empty line for cleaner output

    def copy_test_file(self, src_file):
        """
        Copy 'src_file' to 'tests/bin' directory, ensuring parent directory
        exists. Messages like 'creating directory /path/to/package' and
        'copying directory /src/path/to/package -> path/to/package' are
        displayed on standard output. Adapted from scikit-build.
        The original file in the build directory is not moved/deleted.
        """
        # Create directory if needed
        dest_dir = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'tests', 'bin')
        if dest_dir != "" and not os.path.exists(dest_dir):
            print("creating directory {}".format(dest_dir))
            os.makedirs(dest_dir)

        # Copy file
        dest_file = os.path.join(dest_dir, os.path.basename(src_file))
        print("copying {} -> {}".format(src_file, dest_file))
        copyfile(src_file, dest_file)
        copymode(src_file, dest_file)


def produce_cmake_files(path_to_template, include_sections, output_dir):
    sections = []
    include = True
    lines = []
    with open(path_to_template, "r") as f:
        for line in f:
            begin_name = re.search(
                r"<begin_section>(.*)</begin_section>", line)
            if begin_name:
                sections.append(begin_name.group(1))
                include = sections[-1] in include_sections

            if include:
                lines.append(line)

            end_name = re.search(r"<end_section>(.*)</end_section>", line)
            if end_name:
                if sections.pop() == end_name.group(1):
                    include = sections == [] or sections[-1] in include_sections
                else:
                    raise RuntimeError(
                        "Tag scopes must be concentric or disjoint")

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    with open(os.path.join(output_dir, "CMakeLists.txt"), "w") as f:
        f.write(''.join(lines).strip())


if __name__ == "__main__":
    MODE = sys.argv[1]

    #produce_cmake_files("CMakeLists.txt", [
    #                    "pybind11"], "src/MonteCarlo/.src")

    setup(
        name='MonteCarlo',
        version='0.1',
        author='Kieran Parrott',
        author_email='kieransparrott@gmail.com',
        description='A Monte Carlo Python/C++ simulation package',
        long_description='',
        # tell setuptools to look for any packages under 'src'
        packages=find_packages('src'),
        # tell setuptools that all packages will be under the 'src' directory
        # and nowhere else
        package_dir={'': 'src'},
        # add an extension module named 'MonteCarlo' to the package
        # 'MonteCarlo'
        ext_modules=[CMakeExtension('MonteCarlo/MonteCarlo')],
        # tell setup tools to use the following test suite
        # tests/*_test.py files will all be run
        test_suite='tests',
        # add custom build_ext command
        cmdclass=dict(build_ext=CMakeBuild),
        zip_safe=False,
    )
