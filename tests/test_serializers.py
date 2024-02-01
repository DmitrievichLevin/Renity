"""Burgos Serializer(s) Unit Test Module."""

from src.Burgos.messages.message import Message


def test_serializer_subclasses(serializer_classes):
    """Serial Subclass Data Type.

    * Verify all Serializer Subclasses have data_type attribute.
    """
    for _, serializer in serializer_classes:
        assert serializer.data_type


def test_serializer_responsibility_chain(field_classes, serializer_classes):
    """Serializer Chain.

    * Verify all subclasses are chained in Serializers instance.
    """
    fields = [field for _, field in field_classes]

    class TestMessage(Message):
        test_field_0 = fields[1]()
        test_field_1 = fields[2]()

    test_message = TestMessage()

    # Point to first subclass
    pointer = test_message.serializer.next

    # Verify all Serializer subclasses defined in serializers.py are present on Message class
    for _, serializer in serializer_classes:
        assert isinstance(pointer, serializer)
        pointer = pointer.next
