from setuptools import setup, Extension
from Cython.Build import cythonize
from os.path import abspath,dirname,join
from glob import glob
import re

cython_file_matcher = re.compile(".*\.(pyx|cpp)")
def find_cython_files(*path):
    return [i for i in glob(join(*path,"*")) if cython_file_matcher.match(i)]
    
current_folder = dirname(abspath(__file__))

files = find_cython_files(current_folder,"tools","graphs")
ext_modules = [
    Extension("graphs", files, language="c++"),
]

setup(
    name="AOC",
    ext_modules=cythonize(ext_modules),
)