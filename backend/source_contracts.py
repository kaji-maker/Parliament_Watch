"""Source candidates, not claims of live integration or verified data."""
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class SourceContract:
    dataset: str
    publisher: str
    url: str
    adapter_status: str = "not_validated"
    publication_status: str = "verification_pending"


SOURCES = (
    SourceContract("members", "Federal Parliament of Nepal",
                   "https://digital.parliament.gov.np/members"),
    SourceContract("attendance", "Federal Parliament of Nepal",
                   "https://digital.parliament.gov.np/baithak"),
    SourceContract("bills", "House of Representatives, Nepal",
                   "https://hr.parliament.gov.np/np/bills?type=state"),
)


def dataset_status():
    # Unknown is null, not an invented count of zero.
    return {
        source.dataset: {
            **asdict(source),
            "published_records": None,
            "last_successful_import": None,
        }
        for source in SOURCES
    }

