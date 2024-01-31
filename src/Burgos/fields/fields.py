"""Burgos Built-in Fields."""
from __future__ import annotations
from .interface import Field
from ..validators.exceptions import (
    IncorrectMessageType,
)
from .constants import (
    VARINT,
    I64,
    LEN,
    TYPE,
    BOOL,
    PACKED,
    STR,
    FIXED64,
    INT32,
    SINT32,
)
from ..validators.validators import (
    OverflowValidator,
    SubFieldValidator,
    MessageTypeValidator,
)


class TypeField(Field):
    """Type Field.

    Default field that represents Message subclass name using LEN/string wire type.
    """

    wire = TYPE
    field = STR
    data_type = str

    def validate(self, value):
        validator = MessageTypeValidator(field=self, data_type=str)
        return validator.verify(value)


class IntField(Field):
    """Int Field.

    Built-in Field used to de/serialize Variable Integers of type/field(int32, sint64).

    Attributes:
        field(callable): returns type/field(int32, sint64).
    """

    wire = VARINT
    field = (INT32, SINT32)
    data_type = int

    def get_field_value(self):
        """Field Type From List.

        Returns:
            field(int): field type from list of options.

        Raises:
            IncorrectMessageType: Expected value of type <int>.
        """
        value = self.value
        try:
            if not value or value >= 0:
                field_type = 1
            else:
                field_type = 2
        except Exception as e:
            # Raise exception if not correct type
            raise IncorrectMessageType(
                type(value).__name__, int.__name__, value
            ) from e

        return field_type


class BoolField(Field):
    """Bool Field.

    Built-in Field used to de/serialize Variable Integers of type/field(bool).
    """

    wire = VARINT
    field = BOOL
    data_type = bool


class ListField(Field):
    """List Field.

    Built-in Field used to de/serialize LEN: Packed List.

    Attributes:
        sub_fields(list): list of subclass instances of type Field.
    """

    wire = LEN
    field = PACKED
    data_type = list
    validators = [
        SubFieldValidator,
        OverflowValidator,
    ]


class FloatField(Field):
    """Float Field.

    Built-in Field used to de/serialize I64: Fixed 64-bit float.
    """

    wire = I64
    field = FIXED64
    data_type = float


class StringField(Field):
    """String Field.

    Built-in Field used to de/serialize LEN: String.

    Attributes:
        sub_fields(list): list of subclass instances of type Field.
    """

    wire = LEN
    field = STR
    data_type = str
