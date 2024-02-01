"""Decoder Module Exceptions."""


class InvalidMessage(Exception):
    """Invalid Message Exception."""

    def __init__(self, _bits: str) -> None:
        _message = (
            "Message must begin with 8-Bit Message Identifier TLV \n"
            + f"expected 10010111 but found {_bits}"
        )  # noqa: B950
        self.message = _message
        self.code = 3101
        super().__init__(_message)
