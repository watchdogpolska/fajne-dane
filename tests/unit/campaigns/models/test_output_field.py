from django.core.exceptions import ValidationError
from django.test import TestCase

from campaigns.models import OutputField
from campaigns.models.dto import RecordDTO


def basic_field_validation() -> OutputField:
    return OutputField.objects.create(
        name="test_field",
        widget="text_label",
        answers=["yes", "no"],
        type="str",
        validation=True
    )

def basic_field_no_validation() -> OutputField:
    return OutputField.objects.create(
        name="test_field",
        widget="text_label",
        answers=["yes", "no"],
        type="str",
        validation=False
    )


def basic_field_validation_no_answers() -> OutputField:
    return OutputField.objects.create(
        name="test_field",
        widget="text_label",
        type="int",
        validation=True
    )


class OutputFieldTestCase(TestCase):

    def test_creating(self):
        field = OutputField.objects.create(
            name="test_field",
            widget="text_label",
            answers=["yes", "no"],
            type="str",
            validation=False,
            metadata={'other_name': 'Inne'},
            default_answer=0
        )
        self.assertIsInstance(field, OutputField)

    def test_creating_with_no_default(self):
        field = OutputField.objects.create(
            name="test_field",
            widget="text_label",
            answers=["yes", "no"],
            type="str",
            validation=False
        )
        self.assertIsInstance(field, OutputField)

    def test_validating_record_correct(self):
        output_field = basic_field_validation()
        try:
            output_field.validate(
                RecordDTO(
                    value="yes",
                    probability=0.4
                )
            )
        except ValidationError:
            self.fail()

    def test_validating_record_incorrect_value(self):
        output_field = basic_field_validation()
        with self.assertRaises(ValidationError):
            output_field.validate(
                RecordDTO(
                    value="maybe",
                    probability=0.4
                )
            )

    def test_validating_record_no_value_validation(self):
        output_field = basic_field_no_validation()
        try:
            output_field.validate(
                RecordDTO(
                    value="maybe",
                    probability=0.4
                )
            )
        except ValidationError:
            self.fail()


    def test_validating_record_no_answers_correct_type(self):
        output_field = basic_field_validation_no_answers()
        try:
            output_field.validate(
                RecordDTO(
                    value=4,
                    probability=0.4
                )
            )
        except ValidationError:
            self.fail()

    def test_validating_record_no_answers_wrong_type(self):
        output_field = basic_field_validation_no_answers()
        with self.assertRaises(ValidationError):
            output_field.validate(
                RecordDTO(
                    value="yes",
                    probability=0.4
                )
            )
