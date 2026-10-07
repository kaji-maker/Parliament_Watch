import unittest
from unittest.mock import patch

import httpx

from main import app
from scrapers import (
    run_scraper_cycle, scrape_attendance_notices, scrape_bills,
    scrape_live_members, start_worker,
)


class PoisonDatabase:
    def __getattr__(self, name):
        raise AssertionError(f"Legacy database was accessed: {name}")


class PublicationBoundaryTests(unittest.IsolatedAsyncioTestCase):
    async def test_startup_does_not_import_database_or_start_ingestion(self):
        # A poisoned DB module would break the old startup path.
        with patch.dict("sys.modules", {"db": PoisonDatabase()}):
            async with app.router.lifespan_context(app):
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
                    self.assertEqual((await client.get("/healthz")).json(), {"status": "ok"})
                    self.assertEqual((await client.get("/readyz")).status_code, 503)

    async def test_all_legacy_reads_are_quarantined(self):
        paths = [
            "/api/v1/mps", "/api/v1/mps/", "/api/v1/mps/1",
            "/api/v1/mps/stats/totals", "/api/v1/scraper/attendance",
            "/api/v1/scraper/bills",
        ]
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
            for path in paths:
                with self.subTest(path=path):
                    response = await client.get(path)
                    self.assertEqual(response.status_code, 503)
                    self.assertEqual(response.json()["detail"]["code"], "verification_pending")
                    self.assertEqual(response.headers["cache-control"], "no-store")

    async def test_mutations_cannot_write_or_trigger_work(self):
        paths = [
            "/api/v1/mps", "/api/v1/mps/", "/api/v1/mps/1/cash",
            "/api/v1/mps/1/land", "/api/v1/mps/1/gold",
            "/api/v1/mps/1/equity", "/api/v1/scraper/trigger",
            "/api/v1/future-admin-path",
        ]
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
            for method in ["POST", "PUT", "PATCH", "DELETE"]:
                for path in paths:
                    with self.subTest(method=method, path=path):
                        response = await client.request(method, path, json={"name": "Injected"})
                        self.assertEqual(response.status_code, 405)
                        self.assertEqual(response.json()["detail"]["code"], "writes_disabled")

    async def test_metadata_does_not_claim_live_data_or_zero_counts(self):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/api/v1/status")
        self.assertEqual(response.status_code, 200)
        value = response.json()
        self.assertEqual(value["publication_status"], "verification_pending")
        self.assertEqual(set(value["datasets"]), {"members", "attendance", "bills"})
        for dataset in value["datasets"].values():
            self.assertEqual(dataset["adapter_status"], "not_validated")
            self.assertIsNone(dataset["published_records"])
            self.assertIsNone(dataset["last_successful_import"])

    async def test_legacy_entry_points_have_no_database_or_network_side_effects(self):
        self.assertEqual(run_scraper_cycle(PoisonDatabase())["status"], "paused")
        self.assertEqual(start_worker()["status"], "paused")
        self.assertEqual(scrape_attendance_notices(), [])
        self.assertEqual(scrape_bills(), [])
        self.assertIsNone(await scrape_live_members())

    async def test_cross_origin_credentials_are_not_enabled(self):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/api/v1/status", headers={"Origin": "https://untrusted.example"})
        self.assertNotIn("access-control-allow-origin", response.headers)
        self.assertNotIn("access-control-allow-credentials", response.headers)


if __name__ == "__main__":
    unittest.main()

