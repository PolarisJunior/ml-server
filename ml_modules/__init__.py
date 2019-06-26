
from os import listdir
from os.path import isfile, splitext, join, basename
import importlib

module_dir = join(".", "ml_modules")
modules = ["ml_modules" + "." + splitext(x)[0] for x in listdir(module_dir) if isfile(join(module_dir, x))  and x != basename(__file__)]

for m in modules:
    importlib.import_module(m)

