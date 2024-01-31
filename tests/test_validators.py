"""Burgos Validator(s) Unit Test Module."""

import pytest

from src.Burgos.fields.fields import FloatField
from src.Burgos.fields.fields import IntField
from src.Burgos.fields.fields import ListField
from src.Burgos.validators.validators import IncorrectFieldType
from src.Burgos.validators.validators import OverflowValidator
from src.Burgos.validators.validators import RequiredField
from src.Burgos.validators.validators import RequiredMessageField
from src.Burgos.validators.validators import SubFieldValidator
from src.Burgos.validators.validators import TooManyValues
from src.Burgos.validators.validators import UnorderedValidator


subjects = [IntField(), IntField(default=12)]


@pytest.mark.parametrize("field", subjects)
def test_required_field_validator(field):
    """Test Required Validator."""
    req = RequiredField(field, int)

    # Passing Validation
    assert req.verify(12345) is True

    # Validate None type
    with pytest.raises(RequiredMessageField):
        assert req.verify(None)


@pytest.mark.parametrize("field", subjects)
def test_incorrect_field_type(field):
    """Test Field Value Type Validator.

    * Verify value of field is correct type.
    """
    req = IncorrectFieldType(field, int)

    # Passing Validation
    assert req.verify(12345) is True

    # Expected int but found str, and did not raise Exception."
    with pytest.raises(TypeError):
        assert req.verify("Hello World")

    # Validate None type
    assert req.verify(None) is True


def test_subfield_validator():
    """Test SubFieldValidator.

    * Verify <Field>.sub_fields are subclass of <Field>
    """
    valid = ListField(*subjects, IntField())
    invalid = ListField(*subjects, str)
    empty = ListField()

    overflow = OverflowValidator(valid)
    valid = SubFieldValidator(valid)
    invalid = SubFieldValidator(invalid)
    empty = SubFieldValidator(empty)

    # Valid <ListField> did not pass Subfield Validation.
    assert valid.verify([]) is True

    # Valid <ListField> did not pass Overflow Validation.
    assert overflow.verify([0, 1, 2])

    # <ListField> containing positional argument of invalid type did not raise TypeError
    with pytest.raises(TypeError):
        invalid.verify([])

    # <ListField> with no positional argument(s) did not raise TypeError
    with pytest.raises(TypeError):
        empty.verify([])

    # <ListField> with too many elements did not raise TooManyValues
    with pytest.raises(TooManyValues):
        overflow.verify([1, 2, 3, 4])


def test_list_order_validators():
    """Test List Field Order."""
    fields = [IntField(), FloatField()]
    ordered = ListField(*fields)
    unordered = ListField(*fields, sorted=False)

    # Valid Sorted <ListField> did not pass validation.
    assert ordered.validate([2, 3.14])

    # Sorted <ListField> did not raise TypeError
    with pytest.raises(TypeError):
        ordered.validate([3.14, 2])

    # Valid Unsorted <ListField> did not pass validation.
    assert unordered.validate([3.14, 2])

    # Unsorted <ListField> did not raise TypeError
    unordered = UnorderedValidator(unordered)
    with pytest.raises(TypeError):
        unordered.verify([3.14, 2, 99])
