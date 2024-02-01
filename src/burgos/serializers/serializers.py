"""Message Serializer Sub-Classes."""

from burgos.decoder import decoder as MessageDecoder
from burgos.encoder.encoder import Encoder
from burgos.serializers.interface import MessageSerializer
from typing import Optional


class DictionarySerializer(MessageSerializer):
    """Dictionary Serializer.

    * for <Message> of type <dict>
    """

    data_type = dict

    def serialize(self, message: Optional[dict] = None) -> None:
        """Method Override."""
        self.message = message
        self.data = Encoder.encode(self.fields)


class ByteSerializer(MessageSerializer):
    """Byte Serializer.

    * for <Message> of type <str>(bits)
    """

    data_type = bytes

    def serialize(self, data: bytes) -> None:
        """Method Override."""
        self.data = data
        # Decode message bytes -> dict
        self.message = MessageDecoder.decode(data)
