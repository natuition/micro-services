import os
import importlib

__globals = globals()

for file in os.listdir(os.path.dirname(__file__)):
    if not "__" in file and not "routers" in file:
        mod_name = file[:-3]
        __globals["data_gathering_route_" + mod_name] = importlib.import_module(
            '.' + mod_name, package=__name__)
