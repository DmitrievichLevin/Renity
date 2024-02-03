"""Renity Protocol Buffer.

Renity is an [Open Source] Python Object-Binary-Mapper(OBM)
Binary Protocol Buffer that provides a way to rapidly define
the de/serialization format of packets.

Advantages:
    · Improved throughput & reduced latency by reducing the data size       transferred over the network

    · Serialization & Deserialization

    · Efficiency Compared to other formats like JSON & XML

    · Strict schema definition(s) for messages

    · Backward Compatible Schema(s)

    · Development effort is reduced with an easy-to-use interface that creates a Serialization Format from an Object Model.


Example:
    class CustomMessage(Message):
        hello=StringField(default="World")
        sentence=ListField(StringField(required=True),IntField())

    >>> example = CustomMessage({"sentence": ["Number of Apples:", 2]})

    >>> example.message
    {"type": "CustomMessage", "hello": "World", "sentence": ["Number of Apples:", 2]}
"""
