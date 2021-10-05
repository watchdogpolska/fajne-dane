from django.test import TestCase

from campaigns.models import OutputField


class OutputFieldTestCase(TestCase):

    def test_creating(self):
        field = OutputField.objects.create(
            name="test_field",
            widget="text_label",
            answers=["Yes", "No"],
            type="str",
            validation=False,
            default_answer="Yes"
        )
        self.assertIsInstance(field, OutputField)

    def test_creating_with_no_default(self):
        field = OutputField.objects.create(
            name="test_field",
            widget="text_label",
            answers=["Yes", "No"],
            type="str",
            validation=False
        )
        self.assertIsInstance(field, OutputField)
