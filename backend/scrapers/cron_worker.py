"""Paused compatibility entry points.

Do not start an API-owned worker, delete profiles, or derive facts from names.
The provenance-aware worker and database migrations belong to Phase 2.
"""
from source_contracts import dataset_status


def run_scraper_cycle(db=None):
    """No network or database side effects, even with an existing session."""
    return {"status": "paused", "datasets": dataset_status()}


def start_worker():
    return {"status": "paused"}


def stop_worker():
    return None
