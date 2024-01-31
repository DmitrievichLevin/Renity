"""Encoder Module."""

from math import ceil
from bitstring import Bits
from ..constants import WIRE_TYPES, FIELDS


class Encoder:
    """Encoder.

    Attributes:
        _varint(dict): valid types (int32,sint32,bool)
        _i64(dict): valid types (fixed64)
        _len(dict): valid types (list(packed), string)
        _message_type(dict): string
    """

    _varint = {1: "_int32", 2: "_sint32", 3: "_bool"}
    _i64 = {1: "fixed64"}
    _len = {1: "_packed", 2: "_string"}
    _message_type = {2: "_string"}

    def __init__(self):
        pass

    @classmethod
    def encode(cls, _fields) -> str:
        """Encode Message.

        Args:
            _fields(list): field(Field), key(str), value(Any), bit(int) Quartet

        Returns:
            _bits(str): binary representation of encoded values
                - Attributes(8bit) + Records(>0bits)
        """
        # Attibutes 8-bit representation of 8 fields
        attributes = 0
        # Intialize encoded records list
        records = []
        # Initialize Message Identifier
        identifier = ""

        # iterate fields + encode
        for field, _, value, bit in _fields:
            if value is not None:
                # Get wire type from Field
                _wire_type = WIRE_TYPES[field.wire]

                # Get wire field from Field
                _wire_field = field.field

                # Get corresponding encoder protocol name
                wire = getattr(cls, _wire_type)[_wire_field]

                # Get corresponding encoder protocol from name
                _encoder = getattr(cls, wire)

                # Encode field
                record = _encoder(
                    value, field, "{0:0b}".format(field.wire).zfill(3)
                )

                # message_type(Used for constructing messages does not have a bit)
                # set and continue loop
                if bit is None:
                    identifier = record
                    continue

                # Append encoded field to records list
                records.append(record)

                # Mark corresponding attribute bit
                attributes += bit

        return (
            identifier
            + "{0:0b}".format(attributes).zfill(8)
            + "".join(records)
        )

    def __getitem__(self, wire: str) -> dict:
        """Override.

        - Makes class instance subscriptable.

        """
        return self.__getattribute__(wire)

    @classmethod
    def _bool(cls, _value: bool, _=None, __=None):
        """Boolean Protocol.

        Args:
            _value(bool)

        Returns:
            Binary Protocol VARINT: Bool bit-str
        """
        # Generate Tag
        tag = "1" + f"0{FIELDS[3]}000"
        # Convert bool to 8bit string
        value = str(int(_value)).zfill(8)

        return tag + value

    @classmethod
    def varint(cls, value, __=None):
        """Encode Variable Int.

        Args:
            value(int): integer to be encoded

        Returns:
            (str): Binary String representation of integer.
        """
        _bin = "{0:0b}".format(value)
        _len = len(_bin)
        _bytes = ceil(_len / 7)
        _b = []
        for x in range(_bytes):
            right = _len - x * 7
            left = right - 7 if right - 7 > 0 else 0
            _b.append(
                f"{1 if left != 0 else 0}{_bin[left:right if right > 0 else 1].zfill(7)}"
            )
        return "".join(_b)

    @classmethod
    def _sint32(cls, _value, _=None, __=None):
        """Encode Signed Variable Int.

        Args:
            _value(int): integer to be encoded

        Returns:
            (str): Binary String representation of signed integer.
        """
        # ZigZag encode signed int
        value = (_value << 1) ^ (_value >> 31)
        # Generate Binary Protocol Message from TLV + Varint
        _bits = "1" + f"0{FIELDS[2]}000" + cls.varint(value)
        return _bits

    @classmethod
    def _int32(cls, value, _=None, __=None):
        """Encode Variable Int.

        Args:
            value(int): integer to be encoded

        Returns:
            (str): Binary String representation of integer.
        """
        # Generate Binary Protocol Message from TLV + Varint
        _bits = "1" + f"0{FIELDS[1]}000" + cls.varint(value)
        return _bits

    @classmethod
    def fixed64(cls, value, _=None, __=None):
        """64bit Float."""
        # Encode 64-bit Float value
        _bits = Bits(float=value, length=64)
        # Return Binary Protocol Message From TLV + 64-bit Float
        return "1" + f"{FIELDS[1]}001".zfill(7) + _bits.bin

    @classmethod
    def _string(cls, value, _=None, wire="010"):
        """LEN: String.

        Args:
            value(str): value to encode.
            wire(str): wire key.

        Returns:
            Binary Protocol Message for LEN: String
        """
        # Generate Tag
        _tag = "1" + f"0{FIELDS[2]}{wire}"

        # Convert string to bits
        _bits = "".join(format(ord(i), "08b") for i in value)

        # Get 8bit length
        _length = cls._int32(int(len(_bits) / 8))

        # Return Binary Protocol for LEN: String
        return _tag + _length + _bits

    @classmethod
    def _packed(cls, values, field, __=None):
        """Packed value(list).

        Args:
            values(list): list of (any scalar type that is not sting/bytes)
            field(ListField): iterate sub_fields in ListField

        Returns:
            Packed Binary Protocol Packed List

        Raises:
            Exception: General Exception
        """
        # Generate TLV
        _tag = "1" + f"0{FIELDS[1]}010"

        # Initialize Bits String
        _bits = ""
        try:
            # Iterate Subfields
            for idx, sub in enumerate(field.sub_fields):
                try:
                    # Get TLV Field
                    _wire_field = sub.field
                except IndexError:
                    # If value is not in list continue to next iteration
                    continue

                # Get wire_type
                _wire_type = WIRE_TYPES[sub.wire]

                # Get encoder func name [wire_type]: {[tlv_field]: {...}}
                wire = getattr(cls, _wire_type)[_wire_field]

                # Get encoder func
                _encoder = getattr(cls, wire)

                # Call encoder func
                record = _encoder(values[idx], field)

                # Append returned record
                _bits += record

            # Return Binary Protocol for LEN: Packed List
            return _tag + cls._int32(int(len(_bits) / 8)) + _bits
        except Exception as e:
            raise e
