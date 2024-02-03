"""Message Serializer Interface."""

from __future__ import annotations

from abc import ABC
from typing import Any
from typing import Optional
from typing import Type


class MessageSerializer(ABC):
    """Message Serializer Interface.

    Attributes:
        message(dict): deserialized message.

        fields(list): <Message> sub-class fields.

        data(Any): Encoded message.

        data_type(type): data type of serializer.

        next(MessageSerializer): next node in Serializer Chain.
    """

    _message: dict = {}
    fields: list = []
    data: Optional[bytes] = None
    _next: Optional[MessageSerializer] = None
    length = 0
    message_length = 0

    @property
    def data_type(self) -> Type[Any]:
        """Abstract Data Type Property.

        * Force sub-classes implementation to include "data_type" attribute.
        """
        raise Exception(
            "Serializer sub-classes must have data_type attribute."
        ) from AttributeError

    @property
    def message(self) -> Optional[dict]:
        """Message getter."""
        return self._message

    @message.setter
    def message(self, _message: dict) -> None:
        """Message setter.

        Updates:
            - Message attributes
        """
        new_message = {}

        # Iterate Fields
        for idx in range(self.message_length):
            field = self.fields[idx]

            # <Field>, Key, Current Value, Bit
            f, key, __, bit = field

            # Get value from message

            # Check key
            _key_value = _message.get(key, None)

            # Check bit
            _bit_value = _message.get(bit, None)

            # Check Default
            _field_default = f.default

            value = next(
                (
                    item
                    for item in [
                        _key_value,
                        _bit_value,
                        _field_default,
                    ]
                    if item is not None
                ),
                None,
            )

            if value:
                f.validate(value)

            # Use key from field to update Dict
            new_message.update({key: value})

        self._message = new_message

    @property
    def next(self) -> Optional[MessageSerializer]:
        """Next Serializer Node."""
        return self._next

    @next.setter
    def next(self, _next_node: Any) -> None:
        self._next = _next_node

    def serialize(self, data: Any) -> None:
        """Serialize Method.

        * Must be overriden

        Raises:
            NotImplementedError
        """
        raise NotImplementedError

    def load(self, data: Any) -> tuple:
        """Validate Message Processing.

        * Validate/Serialize Data or pass to next serializer for processing.

        Args:
            data(Any): Data to serialize

        Returns:
            (tuple): message, bytes.

        Raises:
            Exception: TypeError data-type serializer does not exist.
        """
        pointer: MessageSerializer = self

        if isinstance(data, self.data_type):
            self.serialize(data)
            return self.message, self.data

        if pointer.next:
            next: tuple = pointer.next.load(data)
            return next
        else:
            raise Exception(
                f"Serializer does not exist for type {type(data)}"
            ) from TypeError
