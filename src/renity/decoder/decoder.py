"""Decoder Module."""

import codecs
import typing

from bitstring import Bits
from bitstring import BitStream

from ..constants import WIRE_MASK
from ..constants import WIRE_TYPES
from .exceptions import InvalidMessage


# Static Module Message Decoder


# Module Vars
bits: BitStream = BitStream()
decoded_bytes: dict = dict()
length: int = 0
attributes: list = []
decoded_value: dict = dict()
# Module Vars


def decode(_bits):
    """Decode Message."""
    global bits
    global decoded_bytes
    global length
    global attributes
    global decoded_value

    # Message Start
    # Assert Message begins with 'Message Type(int): 7'
    bits = BitStream(bytes=_bits)
    decoded_bytes = bits.bytes
    length = len(bits) - 1
    attributes = []
    decoded_value = {}

    # Get Message Type For Constructing Message
    message_type = bits.read(8)

    # Raise Exception if Message does not begin with Identifier
    if message_type.int & WIRE_MASK != 7:
        raise InvalidMessage(message_type.bin)

    # Get Message Type from LEN: String Protocol
    message_type, _ = base_len(data=bits, field=2)

    # Update Decoded Dict with message_type
    decoded_value["type"] = message_type

    # Read Attributes included in message
    for idx, x in enumerate(bits.read(8).bin):
        # Attributes Included/Absent On/Off = 1/0
        if x == "1":
            attributes = [2 ** abs(idx - 7)] + attributes

    # Empty Message will not throw exception, but return message containing only type
    if bits.pos == len(bits):  # pragma: no cover
        return decoded_value

    # Wire Type of first attribute to decode
    start_wire_protocol = WIRE_TYPES[bits.peek(8).int & WIRE_MASK]

    # set next wire protocol
    next_wire = globals()[start_wire_protocol]

    # While message has next wire protocol decode
    while next_wire:
        # Decode next message
        value, _ = next_wire()

        # Get message attribute-key(int)
        key = next_attr()

        # Add decoded message to dict
        decoded_value[key] = value

        # Get next wire protocol
        next_wire = advance()

    return decoded_value


def bytes(_bits):
    """Byte representation of decoded data."""
    global decoded_bytes
    decode(_bits)
    return decoded_bytes


def tag() -> tuple:
    """Message Attribute TLV.

    Returns:
        TLV(tuple): (Wire Type(str), Wire Field(int))
    """
    global bits

    # Peek at TLV
    _tag = bits.peek(8)

    # Get Wire Type from TLV
    _wire = WIRE_TYPES[_tag.int & WIRE_MASK]

    # Get Wire Field from TLV
    _field = _tag[1:5].int

    # Wire is Message Identifier ignore tag(set 2)
    if _wire == "_message_type":  # pragma: no cover
        _field = 2

    return (_wire, _field)


def advance():
    """Advance pointer.

    * To next message in Binary Protocol

    Returns:
        Next protocol or None

    Raises:
        Exception: General Exception from advancing bit pointer.
    """
    global bits
    global length

    try:
        # Check if there are bits left
        if bits.pos < length:
            # Get tag from current position
            wire, field = tag()

            # Return appropriate protocol for wire_type
            return globals()[wire]

        # End of bytes
        return None
    except Exception as e:  # pragma: no cover
        raise e


def next_attr():
    """Pop next attribute from queue."""
    global attributes
    return attributes.pop(0)


def base_wrapper(base_func: typing.Callable) -> typing.Callable:
    """Deserialization Base Method Wrapper.

    Args:
        base_func(callable): Base Wire Deserialization Method.

    Returns:
        (tuple): Deserialized Value, Next Wire Method Call
    """

    def wrapper(*args, **kwargs):
        global bits
        # Get Wire Field Type
        _, field = tag()

        # Advance Pointer past TLV
        _bin_tag = bits.read(8)  # noqa: F841

        # Base Method Call
        value, _length = base_func(*args, data=bits, field=field, **kwargs)

        # Return Value & Next Wire Method Call
        return value, advance()  # can add _length

    return wrapper


def __get_stream(data: typing.Union[BitStream, str]) -> BitStream:
    if isinstance(data, BitStream):
        _bits = data
    else:
        _bits = BitStream(bin=data)
    return _bits


def base_varint(data, field=0, *args, **kwargs):
    """VarInt.

    * Variable length integer

    Args:
        data(BitStream, bytes, bin...): Binary Data
        field(int): Field type of VARINT wire type.
        *args(Any): Optional*
        **kwargs(Any): Optional**

    Returns:
        value(int): Variable Integer.
        length(int): Length of Wire.
    """
    _bits = __get_stream(data)

    def zig_zag(i):  # pragma: no cover
        # Signed int ZigZag Decoder (field[1] == sint32)
        return (i >> 1) ^ -(i & 1)

    # Initialize Bit stream from bits arg

    value: typing.Union[Bits, BitStream, int] = BitStream()

    # Initialize Most important bit
    msb = 1

    # Initialize length of varint
    length = 0

    # While MSB == 1 continue
    while msb:  # pragma: no cover
        # read next 8-bit sequence
        bin = _bits.read(8)

        # set MSB to current 8-bit sequence
        msb = bin.int >> 7

        # Get remaining 7-bits
        bin = bin[1:]

        # Convert sequence to big-endian
        value = bin + value if value.any(0) or value.any(1) else bin

        # Add 8-bits to length
        length += 8

        # MSB is 0 == end of varint
        if not msb:
            break

    value = int(f"0b{value.bin}", 2)

    # Value is sint32
    if field == 2:
        value = zig_zag(value)
    # Value is bool
    elif field == 3:
        value = bool(value)

    return (value, length)


@base_wrapper
def _varint(*args, **kwargs):
    """Var Int Advance Method.

    * Advance Message Deserialization and return value.

    Args:
        *args(Any): Optional*
        **kwargs(Any): Optional**

    Returns:
        Value/Function call into next Wire Type for deserialization.
    """
    return base_varint(*args, **kwargs)


def base_i64(data, *args, **kwargs):
    """I64 (Float).

    * Base call for unpacking 64-bit Floats

    Args:
        data(BitStream, bytes, bin...): Binary Data
        *args(Any): Optional*
        **kwargs(Any): Optional**

    Returns:
        (tuple): value,length
    """
    _bits = __get_stream(data)

    float = _bits.read("float64")
    return (float, 64)


@base_wrapper
def _i64(*args, **kwargs):
    """I64 Advance Method.

    * Advance Message Deserialization and return value.
    * 8 bytes for IEEE 754 binary64

    Args:
        *args(Any): Optional*
        **kwargs(Any): Optional**

    Returns:
        Value/Function call into next Wire Type for deserialization.
    """
    return base_i64(*args, **kwargs)


def base_len(data, field, *args, **kwargs):
    """Length Delimited Record.

        - 8bit(Tag)
        - 8bit(Int32) Length = Length * 8

    Args:
        data(BitStream, bytes, bin...): Binary Data
        field(int): Field type of VARINT wire type.
        *args(Any): Optional*
        **kwargs(Any): Optional**

    Raises:
        AttributeError: Invalid Field type.

    Returns:
        Case 1:
            List of Primitive Scalar Types
        Case 2:
            Decoded utf-8 String
    """
    _bits = __get_stream(data)

    # Advance pointer past LEN's length/Int32 TLV(8bits)
    _bits.read(8)  # noqa: F841

    # Decode Length Delimited Records Length(Int32)
    length, _int_len = base_varint(_bits[_bits.pos :].bin)

    # Advance pointer past Length
    _bits.read(_int_len)

    if field == 1:
        # LEN: Packed - Unpack List
        value: typing.Any = unpack(length * 8)
    elif field == 2:
        # LEN: String decode utf-8 String
        value = _bits.read(length * 8)

        value = codecs.decode(value.bytes, "utf-8")

    else:
        raise AttributeError("LEN: Field does not exist.")

    return value, (length * 8) + _int_len + 8


@base_wrapper
def _len(*args, **kwargs):
    """LEN Advance Method.

    * Advance Message Deserialization and return value.
    * Length Delimited Record

    Args:
        *args(Any): Optional*
        **kwargs(Any): Optional**

    Returns:
        Value/Function call into next Wire Type for deserialization.
    """
    return base_len(*args, **kwargs)


def unpack(_length: int) -> list:
    """LEN: PACKED.

    * Packed list of Primitives.
    * Not list, tuple, dict, bytes.

    Args:
        _length(int): Length of bits that represent list in message

    Returns:
        unpacked(list): List of Primitive Scalar Types

    Raises:
        TypeError: Expects, cannot nest list, tuple, dict etc.
    """
    global bits

    unpacked = []

    # End of Message
    end = bits.pos + _length

    # Continue decoding until end of message
    while end > bits.pos:
        # Get wire_type of value
        wire, field = tag()

        if wire == 2 and field == 1:
            raise TypeError(
                "TypeError: Expected primitive, cannot nest data structures in packed list."
            )

        # Advance pointer past TLV of value
        bits.read(8)

        # Get value of primitive from wire function
        value, pointer = globals()[f"base{wire}"](bits[bits.pos :].bin, field)

        # Advance pointer to start of next value
        bits.read(pointer)

        # Append decoded value to list
        unpacked.append(value)

    return unpacked
