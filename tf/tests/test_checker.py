from unittest import TestCase

from tf.checker import check_attributes
from tf.schema import Attribute
from tf.types import String
from tf.utils import Diagnostics


class CheckAttributeTest(TestCase):
    def check_error_case(self, attr) -> Diagnostics:
        diags = Diagnostics()
        check_attributes(diags, [attr])
        self.assertTrue(diags.has_errors())
        return diags

    def check_ok_case(self, attr) -> Diagnostics:
        diags = Diagnostics()
        check_attributes(diags, [attr])
        self.assertFalse(diags.has_errors())
        return diags

    def test_optional_and_required(self):
        diags = self.check_error_case(Attribute("aname", String(), optional=True, required=True))
        self.assertIn("Optionality cannot be set if required", str(diags))

    def test_not_optional_not_required_not_computed(self):
        diags = self.check_error_case(Attribute("aname", String()))
        self.assertIn("Optionality must be set if required omitted and not computed", str(diags))

    def test_required_and_optional(self):
        diags = self.check_error_case(Attribute("aname", String(), required=True, optional=True))
        self.assertIn("Required cannot be set if optional", str(diags))

    def test_required_and_computed(self):
        diags = self.check_error_case(Attribute("aname", String(), required=True, computed=True))
        self.assertIn("Required cannot be set if computed", str(diags))

    def test_not_required_not_optional_not_computed(self):
        diags = self.check_error_case(Attribute("aname", String()))
        self.assertIn("Optionality must be set if required omitted and not computed", str(diags))

    def test_computed_and_required(self):
        diags = self.check_error_case(Attribute("aname", String(), computed=True, required=True))
        self.assertIn("Computed cannot be set if required", str(diags))

    def test_default_with_optional(self):
        self.check_ok_case(Attribute("aname", String(), optional=True, default="default"))

    def test_default_with_computed(self):
        self.check_ok_case(Attribute("aname", String(), computed=True, default="default"))

    def test_default_without_optional_or_computed(self):
        diags = self.check_error_case(Attribute("aname", String(), default="default"))
        self.assertIn("Default value requires optional or computed", str(diags))

    def test_default_with_required(self):
        diags = self.check_error_case(Attribute("aname", String(), required=True, default="default"))
        self.assertIn("Default value cannot be set on required attributes", str(diags))
