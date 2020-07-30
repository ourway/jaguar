from glob import glob
import re
import typing as _t
from .data_objects import Controller, Function
from collections import defaultdict
from datetime import datetime
import os


__all__ = ("load_controllers",)


def __get_controllers_as_map():
    """
    crowl `apps/*/controllers/<version><number>/module.py` and
    map controllers to applications

    Sample output would be like:
    >>> [{'1': {'version': 1, 'module': 'monitoring.py'}}]
    """
    py_files = glob("apps/*/controllers/v[0-9]/*.py")
    pat = r"apps/(.*)/controllers/v([0-9])/(.*)"
    f = lambda x: tuple(re.findall(pat, x))[0]
    return map(f, py_files)


def __add_locals_to_returns(contents):
    # return contents.decode().replace('return', 'return locals(),')
    return contents


def __read_module_contents(application, version, module_path):
    d = os.path.dirname(os.path.dirname(__file__))
    f = f"{d}/apps/{application}/controllers/v{version}/{module_path}"
    with open(f, "rb") as handle:
        contents = handle.read()
        return __add_locals_to_returns(contents)


def __get_controllers_as_objects(map_of_controllers) -> _t.List[Controller]:
    controllers = []
    _d = map_of_controllers
    dd = defaultdict(list)
    for app in _d:
        application, version, module_path = app
        fc = __read_module_contents(application, version, module_path)
        b = compile(fc, "<string>", "exec")
        dd[application].append(
            Controller(
                application=application,
                version=version,
                name=".".join(module_path.split(".")[:-1]),
                module_path=module_path,
                bytecode=b,
                datetime=datetime.utcnow(),
                functions=__extract_functions_from_module(b),
            )
        )
    return dd


def __extract_functions_from_module(bytecode):
    "TODO: should be better implemented"
    methods = "get post put head delete patch options".split()
    endpoints = []
    functions = defaultdict(list)
    ## let's load the moudle:
    eval(bytecode)
    for each in bytecode.co_names:
        for m in methods:
            if each.startswith(f"{m}_"):
                endpoints.append(each)
    for func in endpoints:
        bc = eval(f"{func}.__code__")
        name = "_".join(bc.co_name.split("_")[1:])
        functions[name].append(Function(name=name, bytecode=bc, method=bc.co_name.split("_")[0]))
    return functions


def load_controllers():
    "Load controlers"
    m = __get_controllers_as_map()
    controllers = __get_controllers_as_objects(m)
    return controllers
