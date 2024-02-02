"""Renity Utils."""

from inspect import getmembers
from inspect import isclass
from types import ModuleType
from typing import Any
from typing import Callable
from typing import Optional
from typing import Type


def is_class_wrapper(func: Callable) -> Callable:
    """Return func if 'cls' is a class."""

    def wrapper(cls, *args):
        if not isclass(cls):
            return False
        return func(cls, *args)

    return wrapper


@is_class_wrapper
def subclassonly(cls: Type[Any], _type: type) -> bool:
    """Return whether 'cls' is derived from another class but is not the same class."""
    if issubclass(cls, _type) and not issubclass(_type, cls):
        return True
    return False


def modulesubclasses(__module: ModuleType, _type: Any) -> list:
    """Get Module Subclasses.

    Args:
        __module(ModuleType): Python Module
        _type(Any): Object Type

    Returns:
        list(key,value): name, and class
    """
    return getmembers(__module, lambda cls: subclassonly(cls, _type))


class Inventory:
    """Inventory Object.

    * Queue like dict object
    """

    def __init__(self):
        self.__value = {}

    def add(self, key: str, value: Any = None) -> None:
        """Add item to inventory.

        * Increment count
        * Append value to list
        """
        if key in self.__value:
            self.__value[key]["count"] += 1
            self.__value[key]["values"].append(value)
            return
        self.__value[key] = {"count": 1, "values": [value]}

    def pop(self, key: str) -> Optional[Any]:
        """Remove item to inventory.

        * Pop value from key->list
        * Remove key if list isEmpty
        """
        if key in self.__value:
            self.__value[key]["count"] -= 1
            item = self.__value[key]["values"].pop()
            if not self.__value[key]["count"]:
                self.__value.pop(key)
            return item
        return None

    def __len__(self) -> bool:
        """Not Empty?"""
        if self.__value:
            return True
        return False

    def __iter__(self):
        """Return all values."""
        for _, val in self.__value.items():
            yield from val["values"]
