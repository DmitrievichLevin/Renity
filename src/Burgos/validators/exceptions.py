"""Field Exceptions."""

from ..fields.constants import (
    REQUIRED_MESSAGE_FIELD,
    INCORRECT_MESSAGE_TYPE,
    EMPTY_LIST_FIELD,
    TOO_MANY_VALUES,
    MISSING_PRIMITIVE,
)


class MissingPrimitiveException(Exception):
    """Field Exception.

    Field Subclasses require primitive attribute.
    """

    def __init__(self):
        _message = (
            "Field subclass missing primitive attribute declaration."
        )
        super(MissingPrimitiveException, self).__init__(_message)
        self.code = MISSING_PRIMITIVE
        self.message = _message


class RequiredMessageField(Exception):
    """Field Exception."""

    def __init__(self, name, required_field):
        _message = f"Expected required message field {name}: {required_field.__name__}"
        super(RequiredMessageField, self).__init__(_message)
        self.code = REQUIRED_MESSAGE_FIELD
        self.message = _message


class IncorrectMessageType(Exception):
    """Field Exception."""

    def __init__(self, incorrect, correct, val):
        _message = f"Incorrect message type expected {correct} but found <{incorrect}> {val}"
        super(IncorrectMessageType, self).__init__(_message)
        self.code = INCORRECT_MESSAGE_TYPE
        self.message = _message


class InvalidField(Exception):
    """Field Exception."""

    def __init__(self):
        _message = "Invalid field expected type <Field>"
        super(InvalidField, self).__init__(_message)
        self.code = INCORRECT_MESSAGE_TYPE
        self.message = _message


class EmptyListField(Exception):
    """Field Exception."""

    def __init__(self):
        _message = "Implementation Exception: ListField must have sub-fields."
        super(EmptyListField, self).__init__(_message)
        self.code = EMPTY_LIST_FIELD
        self.message = _message


class TooManyValues(Exception):
    """Field Exception."""

    def __init__(self, size: int, found: int):
        _message = (
            f"TooManyValues: Expected {size} but found {found}."
        )
        super(TooManyValues, self).__init__(_message)
        self.code = TOO_MANY_VALUES
        self.message = _message
