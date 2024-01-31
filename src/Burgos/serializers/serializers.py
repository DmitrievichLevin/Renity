"""Message Serializer Sub-Classes."""

from .interface import MessageSerializer
from ..decoder import decoder as MessageDecoder
from ..encoder import Encoder


class DictionarySerializer(MessageSerializer):
    """Dictionary Serializer.

    * for <Message> of type <dict>
    """

    data_type = dict

    def serialize(self, message: dict = None):
        """Method Override."""
        self.message = message
        self.data = Encoder.encode(self.fields)


class ByteSerializer(MessageSerializer):
    """Byte Serializer.

    * for <Message> of type <str>(bits)
    """

    data_type = bytes

    def serialize(self, data) -> str:
        """Method Override."""
        self.data = data
        # Decode message bytes -> dict
        self.message = MessageDecoder.decode(data)
