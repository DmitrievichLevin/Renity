"""Serializers."""

from typing import Any
from . import serializers
from .interface import MessageSerializer as Serializer
from ..fields.interface import Field
from ..utils import modulesubclasses


class FieldElement(object):
    """Serializer Field Object.

    Args:
        field(Field): Message Field.
        key(str): dict key.
        value(Any): Message property value.
        bit(int): starting bit of field.
    """

    __slots__ = ["field", "key", "_value", "bit"]

    def __init__(
        self,
        field: Field,
        key: str,
        value: Any = None,
        bit: int = None,
    ):
        self.field = field

        self.key = key

        self.value = value

        self.bit = bit

    @property
    def value(self):
        """Value Property."""
        return self._value

    @value.setter
    def value(self, val):
        # Set <Field> attribute value
        if val is not None:
            self.field.value = val

            # Validate Field Value
            self.field.validate(val)

        # Set value
        self._value = val if val is not None else self.field.default

    def __getitem__(self, __name: (str, int)) -> Any:
        """Dunder Override.

        * Enable Message object subscription.
        """
        return getattr(self, __name)

    def __iter__(self):
        """Dunder Override.

        * Iterable Attributes.
        """
        for val in [self.field, self.key, self.value, self.bit]:
            yield val


class Serializers:
    """Serializer Chain.

    Attributes:
        serializers(list): list of available <Serializer>(s).

        fields(list): list of <Message> sub-class field(s)<dict>

    Args:
        cls_name: Name of <Message> sub-class.

        message_cls: <Message> sub-class instance.
    """

    message_cls = None
    serializers = None
    fields = []

    def __init__(self):
        # Chain Serializers
        self.chain()

    @property
    def message(self):
        """Message."""
        return self._message

    @message.setter
    def message(self, _message=None):
        self._message = _message
        if _message:
            self.load()
            self.update_chain()

    @property
    def next(self):
        """First link in Serializer Chain."""
        return self.serializers

    def load(self):
        """Load Message Subclass Attributes.

        Attributes:
            fields(list)<dict>:
                { bit(int), key(str), field(Field) }
        """
        from operator import itemgetter

        cls_fields, cls_bits, cls_length = itemgetter(
            "_fields", "_bits", "_length"
        )(self.message_cls)

        message = (
            self.message if isinstance(self.message, dict) else {}
        )

        # Get type field
        type_field = FieldElement(
            field=cls_fields["type"],
            key="type",
            value=message.get("type", None),
        )

        self.fields.append(type_field)

        for x in range(cls_length):
            # Pointer
            pointer = 2**x

            # Key
            key = cls_bits.get(pointer)

            # Field
            field = cls_fields[key]

            # dict
            element = FieldElement(
                field=field,
                key=key,
                bit=pointer,
                value=message.get(key, None),
            )

            self.fields.append(element)

    def chain(self):
        """Chain of Responsibility.

        Serializer Chain
            * Class definitions of type <Serializer> from serializers module.
        """
        for _, serializer in modulesubclasses(
            serializers, Serializer
        ):
            self.add_link(serializer)

    def add_link(self, cls: Serializer):
        """Add Chain Link.

        * Set field(attr)
        * Set message max length: message_length(attr)
        * Instantiate Serializer class node.
        * Append to Linked List.

        Args:
            cls (Serializer): Next serializer in Linked List.
        """
        serializer = cls
        serializer.fields = [list(field) for field in self.fields]

        # Defined Fields + built-in 'type' field
        serializer.message_length = self.message_cls._length + 1

        if not self.serializers:
            self.serializers = serializer()
        else:
            pointer = self.serializers

            while pointer.next:
                pointer = pointer.next
            pointer.next = serializer()

    def update_chain(self):
        """Update Serializer Chain.

        * Add Updated Fields to chain.
        """
        pointer = self.serializers
        fields = [list(field) for field in self.fields]
        while pointer.next:
            pointer.fields = fields
            pointer = pointer.next
        pointer.fields = fields

    def run(self) -> tuple:
        """Run Method.

        * Traverse serializers process or pass to next.

        Returns:
            serialized_data(tuple): (<dict>, <bytes>)
        """
        _message, _data = self.serializers.load(self.message)

        return self.serializers.load(self.message)
