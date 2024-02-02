"""Message Interface Meta Module."""

from renity.fields.fields import TypeField
from renity.fields.interface import Field


class MessageMetaClass(type):
    """Message metaclass.

    Used for message class creation.

    * Creates validation chain from 'validators' attribute
    """

    def __new__(cls, name, bases, attrs):
        """Create new Message instance.

        * Initialize validators
        """
        _fields = {}
        _bits = {}
        _length = 0
        if not len(bases):
            cls._all_required = attrs["required"]

        def build(key, val, length):
            cls.strict(key, val)

            _fields.update({key: val})

            _bit = 2**length

            _bits.update({_bit: key})

        for _name, _value in attrs.items():
            if isinstance(_value, Field):
                build(_name, _value, _length)
                _length += 1

        # Add Type Field
        type_field = TypeField
        type_field.message_cls = name

        _fields.update({"type": type_field(default=name)})

        # Limit Message fields to 8bit
        if _length > 8:
            raise Exception(
                "Renity currently only supports 8 field Message Schema(s)."
            )

        attrs["_fields"] = _fields
        attrs["_bits"] = _bits
        attrs["_length"] = _length

        return super().__new__(cls, name, bases, attrs)

    @classmethod
    def strict(cls, key: str, field: Field) -> None:
        """Strict Message Schema.

        * Check Required True(flag all fields required=True)
        * Set key
        """
        if key == "type":
            raise TypeError("Attempted to overwrite protected field 'type'.")
        field.key = key
        if cls._all_required:
            field.required = True
