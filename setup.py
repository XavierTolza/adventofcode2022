from setuptools import setup, Extension
from Cython.Build import cythonize
from os.path import join
from glob import glob

ext_modules = [
    Extension(
        "tools.graphs.graphs",
        glob(join("tools", "graphs", "*.pyx")),
        extra_compile_args=["-O0"],
    ),
]
ext_modules_cython = cythonize(ext_modules, gdb_debug=True)

setup(
    name="AOC",
    ext_modules=ext_modules_cython,
)
