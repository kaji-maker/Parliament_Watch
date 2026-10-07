"""Bill ingestion is paused until the registry layout and lifecycle are validated."""


def scrape_bills():
    # An unavailable source cannot produce mock bills.
    return []
