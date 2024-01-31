"""Message Serializer Interface."""

from abc import ABC
from typing import Any


class MessageSerializer(ABC):
    """Message Serializer Interface.

    Attributes:
        message(dict): deserialized message.

        fields(list): <Message> sub-class fields.

        data(Any): Encoded message.

        data_type(type): data type of serializer.

        next(MessageSerializer): next node in Serializer Chain.
    """

    _message = None
    fields = None
    data = None
    _next = None
    length = 0

    @property
    def data_type(self):
        """Abstract Data Type Property.

        * Force sub-classes implementation to include "data_type" attribute.
        """
        raise Exception(
            "Serializer sub-classes must have data_type attribute."
        ) from AttributeError

    @property
    def message(self) -> dict:
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
            value = (
                _message.get(key, None)
                if _message.get(key, None) is not None
                else _message.get(bit, None)
            )

            if value:
                f.validate(value)

            # Use key from field to update Dict
            new_message.update({key: value})

        self._message = new_message

    @property
    def next(self):
        """Next Serializer Node."""
        return self._next

    @next.setter
    def next(self, _next_node):
        self._next = _next_node

    def serialize(data: Any) -> str:
        """Serialize Method.

        * Must be overriden

        Raises:
            NotImplementedError
        """
        raise NotImplementedError

    def load(self, data: Any) -> (dict, Any):
        """Validate Message Processing.

        * Validate/Serialize Data or pass to next serializer for processing.

        Args:
            data(Any): Data to serialize

        Returns:
            None: Non-Pure function(mutates <Message> sub-class).

        Raises:
            Exception: TypeError data-type serializer does not exist.
        """
        pointer = self

        if isinstance(data, self.data_type):
            self.serialize(data)
            return self.message, self.data

        if pointer.next:
            return pointer.next.load(data)
        else:
            raise Exception(
                f"Serializer does not exist for type {type(data)}"
            ) from TypeError
