from importlib import import_module
from os import getenv, listdir, makedirs
from os.path import dirname, isdir, join,isfile

from aocd import get_data

session = getenv("AOC_SESSION")

result_path="results"

for year in listdir(path='aoc'):
    for dayfile in listdir(path=join("aoc",year)):
        if not isfile(join("aoc",year,dayfile)):
            continue
        day = int(dayfile.split(".")[0])
        mod = import_module(f"aoc.{year}.{day}", package=None)
        data = get_data(session,day,int(year),block=True)
        res = mod.main(data)

        result_file = join(result_path,year,f"{day}.txt")
        result_folder = dirname(result_file)
        if not isdir(result_folder):
            makedirs(result_folder)
        with open(result_file,"w") as fp:
            fp.write(str(res))
