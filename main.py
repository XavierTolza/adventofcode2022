from importlib import import_module
from os import getenv, listdir, makedirs
from os.path import dirname, isdir, isfile, join

from aocd import get_data

session = getenv("AOC_SESSION")

result_path="results"
run_demo:bool=eval(getenv("RUN_DEMO","False").capitalize())

for year in listdir(path='aoc')[::-1]:
    for dayfile in listdir(path=join("aoc",year))[::-1]:
        if not isfile(join("aoc",year,dayfile)):
            continue
        day = int(dayfile.split(".")[0])
        mod = import_module(f"aoc.{year}.{day}", package=None)
        method = mod.main
        
        if run_demo:
            # Run on demo data is any
            data = mod.demo_data
            expected_result = mod.demo_result
        else:
            data = get_data(session,day,int(year),block=True)

        res = method(data)

        if run_demo and res != expected_result:
            raise ValueError(f"Invalid output for {year}/{day}: {res} != {expected_result}")

        result_file = join(result_path,year,f"{day}.txt")
        result_folder = dirname(result_file)
        if not isdir(result_folder):
            makedirs(result_folder)
        with open(result_file,"w") as fp:
            fp.write(str(res))
