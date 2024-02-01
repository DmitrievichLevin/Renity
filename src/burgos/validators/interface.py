"""Validator Interface."""

from __future__ import annotations

import typing
from abc import ABCMeta
from abc import abstractmethod
from typing import Type


class ValidatorInterface(ABCMeta):
    """Validator Interface.

    The Validator interface declares a method for building the chain of validators.
    """

    @abstractmethod
    def _add(cls, validator: Validator) -> Validator:
        """Add Validator.

        Args:
            validator(Validator): next validator in chain.
        """
        pass

    @abstractmethod
    def verify(cls, *args: list) -> None:
        """Verify Field."""
        pass


class Validator(metaclass=ValidatorInterface):
    """Validator Base.

    Validation chaining is implemented within this base class.
    """

    _next: typing.Optional[Validator] = None

    def __init__(
        self, field: typing.Any, data_type: typing.Union[tuple, type]
    ) -> None:
        self._field = field
        self._data_type = data_type

    @classmethod
    def __subclasshook__(cls, subclass):  # noqa: D105
        return (
            hasattr(subclass, "add")
            and callable(subclass.add)
            and hasattr(subclass, "verify")
            and callable(subclass.verify)
            or NotImplemented
        )

    @property
    def add(self) -> typing.Callable:
        """Prevent accidental override."""
        return self.__add

    def __add(self, validator: Type[Validator]) -> None:
        """Add Validator.

        Args:
            validator(Validator): next validator in chain.
        """
        link = validator(field=self._field, data_type=self._data_type)
        pointer = self

        while pointer._next:
            pointer = pointer._next
        pointer._next = link

    def verify(self, request: typing.Any) -> bool:
        """Verify Field."""
        if self._next:
            return self._next.verify(request)
        return True
