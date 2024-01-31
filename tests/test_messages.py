"""Burgos Message(s) Unit Tests Module."""

import pytest


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

    message_instance = test_message_all_fields(
        valid_bytes_message
    ).message

    # Test Byte Serialization against dict
    assert len(
        {
            k: message_instance[k]
            for k in message_instance
            if k in valid_dictionary_test_message_dict
            and message_instance[k]
            == valid_dictionary_test_message_dict[k]
        }
    ) == len(valid_dictionary_test_message_dict)


# from src.Burgos import (
#     Message,
#     StringField,
#     IntField,
#     BoolField,
#     FloatField,
#     ListField,
#     MessageDecoder,
# )


# class TestMessage(Message):
#     num = IntField()
#     text = StringField()


# class TestListMessage(Message):
#     text = StringField()
#     num = IntField()
#     _list = ListField(IntField(required=True), IntField(), IntField())


# class TestBoolMessage(Message):
#     text = StringField()
#     boolean = BoolField()


# class TestFloatMessage(Message):
#     _i64 = FloatField(default=0.0)


# class TestEncoder(unittest.TestCase):
#     def test_int_encoding(self):
#         c = Bits(float=-12.4543, length=64)
#         message = TestMessage({"num": 3000, "text": "Hello World"})

#         _decoded = MessageDecoder.bytes(message.data)
#         self.assertEqual(
#             bytes(message),
#             _decoded,
#         )

#     # Test encoding/decoding Int,List,StringFields
#     def test_list_encoding(self):
#         message = TestListMessage(
#             {
#                 "num": -3000,
#                 "text": "Hello World",
#                 "_list": [56, 277, 12],
#             }
#         )

#         _decoded = MessageDecoder.bytes(message.data)
#         self.assertEqual(
#             bytes(message),
#             _decoded,
#         )

#     # Test encoding/decoding Boolean value
#     def test_bool_encoding(self):
#         message = TestBoolMessage(
#             {"boolean": True, "text": "This is a true message"}
#         )

#         _decoded = MessageDecoder.bytes(message.data)

#         self.assertEqual(bytes(message), _decoded)

#     # Test encoding/decoding Boolean value
#     def test_float_default_encoding(self):
#         message = TestFloatMessage({})

#         _decoded = TestFloatMessage(message.data)
#         self.assertEqual(bytes(message), bytes(_decoded))


# if __name__ == "__main__":
#     unittest.main()
