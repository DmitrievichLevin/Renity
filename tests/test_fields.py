"""Renity Field(s) Unit Test Module."""

from typing import Any
from typing import Optional

import pytest

from renity.constants import FIELDS
from renity.constants import WIRE_TYPES
from renity.fields import fields
from renity.fields.interface import Field
from renity.utils import modulesubclasses
from renity.validators.interface import Validator
from renity.validators.validators import IncorrectFieldType
from renity.validators.validators import RequiredField


@pytest.fixture
def field_classes() -> Any:
    """All Field Subclasses."""
    return modulesubclasses(fields, Field)


def fields_class_validators():
    """Get Validators Attribute From Field Subclasses."""
    return [(k, v.validators) for k, v in modulesubclasses(fields, Field)]


def test_field_wires(field_classes):
    """Prevent Explicit Singleton Wire Types."""
    for _, field in field_classes:
        assert WIRE_TYPES[
            field().wire
        ], "Wire Type not found, add to constants.py or use existing type."


def test_field_wire_field(field_classes):
    """Prevent Explicit Wire Fields Declaration."""
    for _, field in field_classes:
        assert FIELDS[
            field().field
        ], "Wire Field not found for Field, add to constants.py or use existing type."


def test_all_fields_used_in_test_dict(
    field_classes,
    invalid_dictionary_test_message_dict,
):
    """All Fields Available in Tests.

    * see conftest.py
        - valid
            - [classname]: valid_value should be present for each Field subclass.
        - invalid
            - [classname]: invalid_value should be present for each Field subclass.
    """
    valid_dct = {
        "IntField": 144,
        "BoolField": False,
        "ListField": [True, 3.14, 144, "Hello World"],
        "FloatField": 3.14,
        "StringField": "Hello World",
        "type": "TestMessage",
    }

    def sub_fields(_type):
        subs = []
        if _type is list:
            for _, f in field_classes:
                if f.data_type is not list and _ != "TypeField":
                    subs.append(f())

        return subs

    for n, field in field_classes:
        test_field = field(*sub_fields(field.data_type))

        name = n

        # 'type' field case
        if name == "TypeField":
            name = "type"

        # Test valid value
        assert test_field.validate(valid_dct[name]) is True

        # Test invalid value
        with pytest.raises(TypeError):
            test_field.validate(invalid_dictionary_test_message_dict[name])

    # Test valid_test_dict_length == field_subclasses_length == invalid_test_dict_length
    assert (
        len(valid_dct.items())
        is len(field_classes)
        is len(invalid_dictionary_test_message_dict.items())
    )


def test_sub_fields():
    """Test Sub Fields Length."""
    sub_list = fields.ListField(fields.IntField(), fields.IntField())

    assert len(sub_list.sub_fields) == 2


def test_non_list_data_type_field_sub_fields():
    """Test Non-List Field Subclass."""
    with pytest.raises(TypeError):
        fields.IntField(fields.IntField(), fields.IntField())


def test_field_required_default_validators():
    """Test Required Default Validator Chain in Field."""
    pointer: Optional[Validator] = fields.IntField(required=True).validator
    defaults = [Validator, RequiredField, IncorrectFieldType]

    for validator in defaults:
        assert isinstance(pointer, validator)
        pointer = pointer._next


def test_field_non_default_validators():
    """Test Required Default Validator Chain in Field."""
    pointer = fields.IntField().validator
    defaults = [Validator, IncorrectFieldType]

    for validator in defaults:
        assert isinstance(pointer, validator)
        pointer = pointer._next


@pytest.mark.parametrize("key, values", fields_class_validators())
def test_validators_attributes(key, values):
    """Test Field(s) validators attribute.

    * Expected type <Validator>
    """
    for value in values:
        assert issubclass(
            value, Validator
        ), f"Expected type {Validator} in subclass {key} but found {value}."
