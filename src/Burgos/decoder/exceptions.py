"""Decoder Module Exceptions."""


class InvalidMessage(Exception):
    """Invalid Message Exception."""

    def __init__(self, _bits):
        _message = f"Message must begin with 8-Bit Message Identifier TLV \n expected 10010111 but found {_bits}"  # noqa: B950
        super().__init__(_message)
        self.code = 3101
        self.message = _message
