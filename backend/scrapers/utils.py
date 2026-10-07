"""Explicit date parsing. Missing or unparseable evidence remains unknown."""
import re
from datetime import date
from typing import Optional

NEPALI_MONTHS_MAP = {
    "वैशाख": 1, "बैशाख": 1, "जेठ": 2, "ज्येष्ठ": 2,
    "असार": 3, "आषाढ": 3, "साउन": 4, "श्रावण": 4,
    "भदौ": 5, "भाद्र": 5, "असोज": 6, "आश्विन": 6,
    "कात्तिक": 7, "कार्तिक": 7, "मंसिर": 8, "मार्ग": 8,
    "मङ्सीर": 8, "पुस": 9, "पौष": 9, "माघ": 10,
    "फागुन": 11, "फाल्गुन": 11, "चैत": 12, "चैत्र": 12,
}
NEPALI_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")


def convert_bs_to_ad(nepali_date_str: Optional[str]) -> Optional[date]:
    """Parse a BS date field, not arbitrary notice titles or Gregorian dates.

    Raw source text must be retained by the future ingestion layer. A null
    result is an extraction failure, never today's date. Dependency failures
    are surfaced rather than silently turning a valid date into missing data.
    """
    if not nepali_date_str:
        return None
    clean = str(nepali_date_str).translate(NEPALI_DIGITS).strip()
    numeric = re.fullmatch(r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})", clean)
    parts = None
    if numeric:
        parts = tuple(map(int, numeric.groups()))
    else:
        for month_name, month_number in NEPALI_MONTHS_MAP.items():
            named = re.fullmatch(
                rf"(\d{{4}})\s+{re.escape(month_name)}\s+(\d{{1,2}})(?:\s+गते)?",
                clean,
            )
            if named:
                parts = (int(named[1]), month_number, int(named[2]))
                break
    if parts is None:
        return None
    year, month, day = parts
    # Match the supported year range of nepali-datetime's calendar table.
    if not (1975 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 32):
        return None
    import nepali_datetime

    try:
        return nepali_datetime.date(year, month, day).to_datetime_date()
    except ValueError:
        return None
