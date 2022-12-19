from app.api.routes import *

router_files = list()

for name, value in globals().copy().items():
    if "data_gathering_route_" in name:
        router_files.append(value)
