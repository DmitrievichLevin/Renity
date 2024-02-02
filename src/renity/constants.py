"""Renity Constants."""

WIRE_TYPES = {
    # VARINT	int32, int64, uint32, uint64, sint32, sint64, bool, enum
    0: "_varint",
    # I64	fixed64, sfixed64, double
    1: "_i64",
    # LEN	string, bytes, embedded messages, packed repeated fields
    2: "_len",
    # MESSAGE IDENTIFIER -> LEN: String
    7: "_message_type",
}

# Decoder Constants

WIRE_MASK = 0b111

# Encoder Constants

FIELDS = {1: "001", 2: "010", 3: "011"}
