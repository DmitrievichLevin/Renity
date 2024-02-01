"""Burgos Message(s) Unit Tests Module."""

from typing import Type

import pytest

from burgos.fields import fields
from burgos.messages.message import Message


class TestMessage(Message):
    """Test Message Subclass."""

    required = True
    BoolField = fields.BoolField()
    FloatField = fields.FloatField()
    IntField = fields.IntField()
    ListField = fields.ListField(
        fields.BoolField(),
        fields.FloatField(),
        fields.IntField(),
        fields.StringField(),
    )
    StringField = fields.StringField()


@pytest.fixture
def test_message_all_fields() -> Type[TestMessage]:
    """Test Message Subclass.

    * contains all valid fields see fields.py
    * required=True(all field attributes are set to required).
    * Note: TypeField is not a valid field attribute(auto-added by base class).
    """
    return TestMessage


def test_dict_serializer(
    test_message_all_fields,
    valid_dictionary_test_message_dict,
    valid_bytes_message,
):
    """Test Default Functionality (Dict Serializer)."""
    dct = valid_dictionary_test_message_dict

    message_instance = test_message_all_fields(dct)

    # Test Dict Serialization against byte representation.
    assert bytes(message_instance) == valid_bytes_message


def test_byte_serializer(
    test_message_all_fields,
    valid_bytes_message,
    invalid_bytes_message,
    valid_dictionary_test_message_dict,
):
    """Test Byte Serializer."""
    # Test Wrong message type
    with pytest.raises(TypeError):
        test_message_all_fields(invalid_bytes_message)

    message_instance = test_message_all_fields(valid_bytes_message).message

    # Test Byte Serialization against dict
    assert len(
        {
            k: message_instance[k]
            for k in message_instance
            if k in valid_dictionary_test_message_dict
            and message_instance[k] == valid_dictionary_test_message_dict[k]
        }
    ) == len(valid_dictionary_test_message_dict)
