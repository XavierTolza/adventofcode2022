from glob import glob
from importlib import import_module
from os import getenv, listdir, makedirs
from os.path import basename, dirname, isdir, join, isfile

from aocd import get_data as get_aoc_data

session = getenv("AOC_SESSION")
result_path = "results"
cache_path=".cache"
run_demo: bool = eval(getenv("RUN_DEMO", "False").capitalize())

def get_data(sessions,day,year,*args,**kwargs):
    dst_path = join(cache_path,str(year),f"{day}.txt")
    dst_folder = dirname(dst_path)
    if not isdir(dst_folder):
        makedirs(dst_folder)
    
    if not isfile(dst_path):
        content = get_aoc_data(sessions,day,year,*args,**kwargs)
        with open(dst_path,"w") as fp:
            fp.write(content)
        return content
    else:
        with open(dst_path,"r") as fp:
            content = fp.read()
        return content
        
for year in listdir(path="aoc")[::-1]:
    for dayfile in sorted(
        glob(join("aoc", year, "*.py")), key=lambda x: -int(basename(x).split(".")[0])
    ):
        day = int(basename(dayfile).split(".")[0])
        mod = import_module(f"aoc.{year}.{day}", package=None)
        method = mod.main

        if run_demo:
            # Run on demo data is any
            data = mod.demo_data
            expected_result = mod.demo_result
        else:
            data = get_data(session, day, int(year), block=True)

        res = method(data)

        if run_demo and res != expected_result:
            raise ValueError(
                f"Invalid output for {year}/{day}: {res} != {expected_result}"
            )

        result_file = join(result_path, year, f"{day}.txt")
        result_folder = dirname(result_file)
        if not isdir(result_folder):
            makedirs(result_folder)
        with open(result_file, "w") as fp:
            fp.write(str(res))
