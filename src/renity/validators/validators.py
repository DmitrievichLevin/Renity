"""Field Validators.

Subclasses of type Validator
"""

from __future__ import annotations

from inspect import isclass

from renity.validators.interface import Validator

from ..utils import Inventory
from .exceptions import RequiredMessageField
from .exceptions import TooManyValues


class RequiredField(Validator):
    """Validate Required Field."""

    def verify(self, request):
        """Built-in Validation.

        * Verify required case
        """
        if request is None:
            raise RequiredMessageField(self._field.key, self._field.__class__)

        return super().verify(request)


class IncorrectFieldType(Validator):
    """Built-in Validation.

    * Verify correct type(value, default).
    """

    def verify(self, request):
        """Verify Field."""
        if request is not None and not isinstance(request, self._data_type):
            raise TypeError(
                f"Expected {self._data_type} but found {type(request)}."
            )

        return super().verify(request)


class SubFieldValidator(Validator):
    """Validate Packed List Elements.

    Ensure Packed LEN has is not empty.
    """

    def __init__(self, field, **_):
        self._field = field
        self._data_type = (list, tuple)

    def verify(self, request):
        """Validate Sub-Fields(list<Field>)."""
        # Verify Subfields
        if self._field.data_type is list:
            # Missing subfields
            if not len(self._field.sub_fields):
                raise TypeError(
                    "Missing at least 1 positional argument of type: <Field>"
                )

            # Expected subfield of type <Field>
            for field in self._field.sub_fields:
                sub_class = type(field)
                base = type(self._field).__mro__[1]

                if not isclass(sub_class) or not issubclass(sub_class, base):
                    raise TypeError(
                        "Invalid field expected type"
                        + f"{type(self._field).__mro__[1]}, but found type {field}"
                    )
        return super().verify(request)


class OverflowValidator(Validator):
    """Validate Packed List Elements.

    Ensure Packed LEN does not exceed size of sub_fields array.
    """

    def __init__(self, field, **_):
        self._field = field
        self._data_type = (list, tuple)

    def verify(self, request):
        """Verify Field."""
        subs = len(self._field.sub_fields)
        _input = len(request)
        if subs < _input:
            raise TooManyValues(subs, _input)
        return super().verify(request)


class UnorderedValidator(Validator):
    """Validate Unorderd Packed List Elements(experimental)."""

    def __init__(self, field, **_):
        self._field = field
        self._data_type = (list, tuple)

    def verify(self, request):
        """Verify Field."""
        valid = Inventory()
        for v in request:
            valid.add(str(type(v)), v)
        for sub in self._field.sub_fields:
            _type = str(sub.data_type)
            item = valid.pop(_type)
            sub.validate(item)

        if len(valid):
            raise TypeError(f"Unexpected value(s) of {list(valid)}")

        return super().verify(request)


class MessageTypeValidator(Validator):
    """Validate Message Type."""

    def verify(self, request):
        """Verify Field."""
        m_type = self._field.message_cls
        if not isinstance(request, str) or m_type != request:
            raise TypeError(
                f"Expected Message type: {m_type} but found {request}"
            )

        return super().verify(request)
