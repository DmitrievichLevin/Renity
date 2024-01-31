"""Burgos Protocol Buffer.

There are many ways to optimize data transimission over the wire, but one of
the biggest impacts can be made from simply not sending data you don't need.
Burgos provides an Interface for rapidly defining the serialization format for
Network Traffic solely in Python. Using Schema's that closely resemble an
Object Relational Mapping(ORM) we are able to generate simple class definitions
that contain fields and methods to serlialze/parse to and from raw bytes.

Advantages:
    · Extendable
    · Backward Compatible Schema(s)
    · Fast Parsing
    · strict enforcement at the application level(optional)
    · Optimize size of transmissions


Example:
    class CustomMessage(Message):
        hello=StringField(default="World")
        sentence=ListField(StringField(required=True),IntField())

    example = CustomMessage({"sentence": ["Number of Apples:", 2]})

    print(example.message)

    Output:
        {"hello": "World", "sentence": ["Number of Apples:", 2]}
"""
from .decoder import decoder as MessageDecoder
from .encoder.encoder import Encoder
from .fields.fields import BoolField
from .fields.fields import FloatField
from .fields.fields import IntField
from .fields.fields import ListField
from .fields.fields import StringField
from .fields.fields import TypeField
from .messages.message import Message


__all__ = [
    "TypeField",
    "StringField",
    "IntField",
    "BoolField",
    "FloatField",
    "ListField",
    "Message",
    "Encoder",
    "MessageDecoder",
]
