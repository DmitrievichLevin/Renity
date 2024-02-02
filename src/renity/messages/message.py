"""Message Interface."""

from typing import Any

from bitstring import BitStream

from renity.messages.interface import MessageMetaClass
from renity.serializers import Serializers as Serializer


class Message(metaclass=MessageMetaClass):
    """Message Interface.

    Args:
        _message(Any): Binary protocol message
    """

    __slots__ = ["_message", "data", "type", "serializer"]
    # prevent pytest from trying to discover tests in the class
    __test__ = False
    required: bool = False
    _length: int = 0

    def __init__(self, message: Any = None) -> None:
        self.message = message

    @property
    def message(self):
        """Message Dict."""
        return self._message

    @message.setter
    def message(self, value: Any) -> None:
        _message, data = self.__serialize(value)

        self._message = _message
        self.data = data

    def __serialize(self, message: Any) -> tuple:
        """Serialize Message.

        * Instantiate Serializer Chain on instance.

        Args:
            message(Any): message data.

        Returns:
            serialized_message(tuple): (<dict>, <bytes>)
        """
        # Instantiate Serializer Chain on instance.
        if not hasattr(self, "serializer"):
            _serializer = Serializer
            _serializer.message_cls = self
            self.serializer = _serializer()

        if message:
            self.serializer.message = message
            return self.serializer.run()

        return None, None

    def __iter__(self):
        """Generator Override.

        * Yields key/value pair from message dict.
        """
        yield from self.message.items()

    def __getitem__(self, __name: str) -> Any:
        """Dunder Override.

        * Enable Message object to be subscriptable.
        """
        return getattr(self, __name)

    def __bytes__(self):
        """Bytes Representation Override."""
        return BitStream(bytes=self.data).bytes
