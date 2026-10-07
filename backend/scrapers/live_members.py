"""Member ingestion is paused; legacy name/constituency guessing is removed."""


async def scrape_live_members():
    # Never replace a source identity with a snapshot match or guessed fields.
    return None
