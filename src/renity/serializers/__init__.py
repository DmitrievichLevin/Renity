"""Serializers."""

from __future__ import annotations

from typing import Any
from typing import Callable
from typing import Optional
from typing import Type

from typeguard import typechecked

import renity
from renity.serializers import serializers
from renity.serializers.interface import MessageSerializer as Serializer

from ..utils import modulesubclasses


class FieldElement:
    """Serializer Field Object.

    Args:
        field(Field): Message Field.
        key(str): dict key.
        value(Any): Message property value.
        bit(int): starting bit of field.
    """

    __slots__ = ["field", "key", "_value", "bit", "_message"]

    @typechecked
    def __init__(
        self,
        field: renity.fields.interface.Field,
        key: str,
        value: Any = None,
        bit: Optional[int] = None,
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

    def __getitem__(self, __name: Any[str, int]) -> Any:
        """Dunder Override.

        * Enable Message object subscription.
        """
        return getattr(self, __name)

    def __iter__(self):
        """Dunder Override.

        * Iterable Attributes.
        """
        yield from [self.field, self.key, self.value, self.bit]


@typechecked
class Serializers:
    """Serializer Chain.

    Attributes:
        serializers(list): list of available <Serializer>(s).

        fields(list): list of <Message> sub-class field(s)<dict>

    Args:
        cls_name: Name of <Message> sub-class.

        message_cls: <Message> sub-class instance.
    """

    message_cls: Any
    _message: dict
    fields: list = []
    serializers: Serializer

    def __init__(self):
        """Chain Serializers."""
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
        m_cls = self.message_cls
        cls_fields = m_cls["_fields"]
        cls_bits = m_cls["_bits"]
        cls_length = m_cls["_length"]

        message = self.message if isinstance(self.message, dict) else {}

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

    def chain(self) -> None:
        """Chain of Responsibility.

        Serializer Chain
            * Class definitions of type <Serializer> from serializers module.
        """
        for _, serializer in modulesubclasses(serializers, Serializer):
            self.add_link(serializer)

    def add_link(self, cls: Type[Serializer]) -> None:
        """Add Chain Link.

        * Set field(attr)
        * Set message max length: message_length(attr)
        * Instantiate Serializer class node.
        * Append to Linked List.

        Args:
            cls (Serializer): Next serializer in Linked List.
        """
        serializer: Type[Serializer] = cls
        serializer.fields = [list(field) for field in self.fields]

        # Defined Fields + built-in 'type' field
        serializer.message_length = self.message_cls._length + 1

        if not hasattr(self, "serializers"):
            self.serializers: Serializer = serializer()
        else:
            pointer = self.serializers

            while pointer.next:
                pointer = pointer.next
            pointer.next = serializer()

    def update_chain(self):
        """Update Serializer Chain.

        * Add Updated Fields to chain.
        """
        pointer: Serializer = self.serializers
        fields = [list(field) for field in self.fields]
        while pointer.next:
            pointer.fields = fields
            pointer: Optional[Callable] = pointer.next
        pointer.fields = fields

    def run(self) -> tuple:
        """Run Method.

        * Traverse serializers process or pass to next.

        Returns:
            serialized_data(tuple): (<dict>, <bytes>)
        """
        _message, _data = self.serializers.load(self.message)

        return self.serializers.load(self.message)
