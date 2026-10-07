import importlib.util
import unittest
from datetime import date
from unittest.mock import patch

from scrapers.utils import convert_bs_to_ad


class DateTests(unittest.TestCase):
    def test_missing_invalid_or_arbitrary_text_remains_unknown(self):
        for value in [
            None, "", "unparseable", "2083-13-04", "2083-06-00",
            "2083-06-99", "9999-01-01",
            "बैठक 68 - 2083 आश्विन 16 गते", "2026-10-02T10:00:00Z",
        ]:
            with self.subTest(value=value):
                self.assertIsNone(convert_bs_to_ad(value))

    def test_dependency_failure_is_not_silently_reported_as_missing_data(self):
        with patch.dict("sys.modules", {"nepali_datetime": None}):
            with self.assertRaises(ModuleNotFoundError):
                convert_bs_to_ad("2083-06-16")

    @unittest.skipUnless(importlib.util.find_spec("nepali_datetime"), "nepali-datetime is not installed")
    def test_official_meeting_date_and_nepali_digits(self):
        # Official HoR meeting 68: Ashwin 16, 2083 / October 2, 2026.
        for value in ["2083-06-16", "२०८३/०६/१६", "२०८३ आश्विन १६ गते"]:
            with self.subTest(value=value):
                self.assertEqual(convert_bs_to_ad(value), date(2026, 10, 2))


if __name__ == "__main__":
    unittest.main()

