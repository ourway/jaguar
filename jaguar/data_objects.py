from dataclasses import dataclass
from datetime import datetime
import typing as _t


@dataclass
class Function:
    "Holds information about a function"
    name: str
    bytecode: bytes
    method: str


@dataclass
class Controller:
    "Holds information about an application controller"
    application: str
    name: str
    version: int
    module_path: str
    bytecode: bytes
    functions: _t.List[Function]
    datetime: datetime
