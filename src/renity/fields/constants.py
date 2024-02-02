"""Exception Codes.

Field Exception codes.
"""

INVALID_MESSAGE = 3101

REQUIRED_MESSAGE_FIELD = 3013

INCORRECT_MESSAGE_TYPE = 3014

EMPTY_LIST_FIELD = 3015

TOO_MANY_VALUES = 3016

MISSING_PRIMITIVE = 3017

"""Wire Types.

Wire Type Constants
"""
VARINT = 0  #: int32, int64, uint32, uint64, sint32, sint64, bool, enum
I64 = 1  #: fixed64, sfixed64, double
LEN = 2  #: string, bytes, embedded messages, packed repeated fields
TYPE = 7  #: MESSAGE IDENTIFIER -> LEN: String

"""Wire Fields.

Wire Field Constants
"""
BOOL = 3
PACKED = 1
INT32 = 1
STR = 2
FIXED64 = 1
SINT32 = 2
