import falcon as J
import falcon
from .helpers import load_controllers
import types
import sys
from collections import defaultdict
from operator import itemgetter
from inspect import getsource

CONTROLLERS = load_controllers()
MAIN_APP = falcon.API()
RESOURCES = list()
STATUS_GETTER = itemgetter("status")

for app in CONTROLLERS.keys():

    for controller in CONTROLLERS[app]:
        for resource in controller.functions:
            _fn = controller.functions[resource]
            for endpoint in _fn:
                Resource = type(f"{app}_{controller.name}_{endpoint.name}", (object,), {})
                path = f"/api/v1/{app}/{controller.name}/{endpoint.name}"

                def _func(self, req, resp):
                    # first we need to find proper endpoint code
                    resp.media = eval(self.target.bytecode, None, {"resp": "www"})

                # Resource.on_get = types.MethodType(on_get, Resource)
                funcname = f"on_{endpoint.method}"
                setattr(Resource, funcname, types.MethodType(_func, Resource))
                Resource.target = endpoint
                print(f"Jaguar endpoint: GET {path} added", file=sys.stderr)
                sys.stderr.flush()
                RESOURCES.append((path, Resource,))

for each in RESOURCES:
    path, r = each
    MAIN_APP.add_route(path, r())

application = MAIN_APP
