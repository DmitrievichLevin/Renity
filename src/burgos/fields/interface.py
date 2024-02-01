"""Field Interface.

Instances of this class are used to define a message's schema.
"""

from __future__ import annotations

from typing import Any
from typing import Union

from ..validators.exceptions import MissingPrimitiveException
from ..validators.interface import Validator
from ..validators.validators import IncorrectFieldType
from ..validators.validators import RequiredField
from ..validators.validators import UnorderedValidator


class FieldMeta(type):
    """Field metaclass.

    Used for field class creation.

    * Creates validation chain from 'validators' attribute
    """

    __field: Any = None
    field: Any = None

    def __new__(cls, name, bases, attrs):
        """Create new Field instance.

        * Initialize field property from field attribute
        """
        inst = super().__new__(cls, name, bases, attrs)
        if len(bases):
            inst.__field = attrs["field"]
            inst.field = cls._initialize_field()

            if not attrs["data_type"]:
                raise MissingPrimitiveException
        return inst

    @classmethod
    def _initialize_field(cls):
        def _field(self):
            if type(self.__field) in (list, tuple):
                return self.get_field_value()

            return self.__field

        def _set_field(self, value):
            self.__field = value

        return property(
            fget=_field,
            fset=_set_field,
            doc="""Wire Type Field Property.""",
        )

    def get_field_value(cls, *_):
        """Abstract Method.

        * Override for field type list or tuple
        """
        raise Exception(
            "Fields with multiple types must override this method."
        ) from NotImplementedError


class Field(metaclass=FieldMeta):
    """Binary Message Field Interface.

    Attributes:
        *wire(int): see 'constants.py' for valid wire types*

        *field(int, list<int>): **wire field or list of wire fields
        see 'constants.py' for valid wire fields.*

        **data_type(list, Any): Primitive or non-primitive data-type.**

        validators(Validator): see 'validators.py' for list of Validator(s).

    Args:


        key(str): name of field.

        value(Any): Set during serialization.

        required(bool): raise exception if field is missing in message.

        default(Any): default value of field.

        sub_fields(list): list of subclass instances (for packed wire type).

        sorted(bool): default=True flag for ordered list of
        subclasses **Warning: False(Experimental)**
    """

    data_type: Any = None
    validators: list = []
    field: Union[int, tuple[int, int]] = 0
    __value: Any = None
    key = ""
    message_cls: str = "Message"

    def __init__(
        cls,
        *sub_fields: Any,
        required: bool = False,
        default: Any = None,
        sorted: bool = True,
    ):
        cls.required = required
        cls.sorted = sorted
        cls.__initialize_sub_fields(sub_fields)
        cls._set_default_value(default)
        cls.__initialize_validator()

    @property
    def value(self):
        """Value Property."""
        return self.__value

    @value.setter
    def value(self, _val):
        sub_field_length = len(self.sub_fields)
        if sub_field_length:
            for idx in range(sub_field_length):
                self.sub_fields[idx].value = _val[idx]
        self.__value = _val

    @property
    def default(self):
        """Default Field Value."""
        return self.__default

    def _set_default_value(self, default: Any) -> None:
        # Validate default attribute
        if default and not isinstance(default, self.data_type):
            raise Exception(
                f"Expected default value type {self.data_type} but found {default}"
            ) from AttributeError

        self.__default = default

    def __initialize_sub_fields(self, sub_fields: Union[list, tuple]) -> None:
        if self.data_type is not list and len(sub_fields):
            name = self.__class__.__name__
            raise TypeError(
                f"{name} takse 0 positional arguments but {len(sub_fields)} was given."
            )
        self.sub_fields = sub_fields

    def __initialize_validator(self) -> None:
        data = self.data_type
        root = Validator(field=self, data_type=data)
        self.validator = root
        return self.__chain_validation()

    def __chain_validation(self) -> None:
        root: Validator = self.validator

        # RequiredField = built-in Validator
        if self.required:
            root.add(RequiredField)

        sub_fields = self.sub_fields

        if sub_fields:
            if not self.sorted:
                # Unsorted List Validation = built-in Validator *sub-fields*
                root.add(UnorderedValidator)
        elif not sub_fields or self.sorted:
            # Type Validation = built-in Validator/*sorted sub-fields validator*
            root.add(IncorrectFieldType)

        # Iterate Validator Subclasses
        if self.validators:
            for _validator_subclass in self.validators:
                if not issubclass(_validator_subclass, Validator):
                    raise TypeError(
                        f"TypeError: Expected type {Validator} but found {_validator_subclass}."
                    )
                root.add(_validator_subclass)

    def validate(self, value):
        """Field Validation.

        * Validate field
        * Traverse/validate sub_fields
        """
        results = [self.validator.verify(value)]
        if self.sorted:
            for idx, sub in enumerate(self.sub_fields):
                results.append(sub.validate(value[idx]))

        return all(results)
