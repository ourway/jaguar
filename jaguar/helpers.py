from glob import glob
import re
import typing as _t
from .data_objects import Controller, Function
from collections import defaultdict
from datetime import datetime
import os

all = ["get_controllers_as_map", "get_controllers_as_objects"]


def get_controllers_as_map():
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


def __read_module_contents(application, version, module_path):
    d = os.path.dirname(os.path.dirname(__file__))
    f = f'{d}/apps/{application}/controllers/v{version}/{module_path}'
    return open(f, 'rb').read()


def get_controllers_as_objects(map_of_controllers) -> _t.List[Controller]:
    controllers = []
    _d = map_of_controllers
    dd = defaultdict(list)
    for app in _d:
        application, version, module_path = app
        fc = __read_module_contents(application, version, module_path)
        b = compile(fc, '<string>', 'exec')
        dd[application].append(
            Controller(
                application=application,
                version=version,
                module_path=module_path,
                bytecode = b,
                datetime=datetime.utcnow(),
                functions = 'something'
            )
        )
    return dd
