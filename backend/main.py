"""Phase 1 publication boundary: legacy data is preserved, never published.

No database or scraper imports belong here until provenance-aware publication
and migrations are implemented in Phase 2. Old volumes may contain synthetic
records tagged "live"; neither that tag nor API connectivity verifies a fact.
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from source_contracts import dataset_status

app = FastAPI(
    title="Parliament Watch Nepal API",
    description="Independent civic portal. Verified publication is being prepared.",
    version="0.2.0",
)

PENDING = {
    "code": "verification_pending",
    "message": "Verified parliamentary records are not yet available.",
}


@app.middleware("http")
async def publication_boundary(request: Request, call_next):
    # Disable all legacy mutations, including paths not yet registered.
    if request.url.path.startswith("/api/") and request.method in {
        "POST", "PUT", "PATCH", "DELETE"
    }:
        return JSONResponse(
            status_code=405,
            content={"detail": {
                "code": "writes_disabled",
                "message": "Public writes and scraper triggers are disabled.",
            }},
            headers={"Allow": "GET", "Cache-Control": "no-store"},
        )
    response = await call_next(request)
    if request.url.path.startswith("/api/") or request.url.path == "/readyz":
        response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/")
async def read_root():
    return {
        "service": "Parliament Watch Nepal",
        "status": "verification_pending",
        "phase": 1,
    }


@app.get("/healthz")
async def health():
    """Process liveness only; this does not claim dataset readiness."""
    return {"status": "ok"}


@app.get("/readyz")
async def readiness():
    return JSONResponse(status_code=503, content={"detail": PENDING})


@app.get("/api/v1/status")
async def status():
    return {
        "phase": 1,
        "publication_status": "verification_pending",
        "datasets": dataset_status(),
    }


def unavailable():
    return JSONResponse(status_code=503, content={"detail": PENDING})


@app.get("/api/v1/mps")
@app.get("/api/v1/mps/")
@app.get("/api/v1/mps/stats/totals")
@app.get("/api/v1/scraper/attendance")
@app.get("/api/v1/scraper/bills")
async def quarantined_dataset():
    return unavailable()


@app.get("/api/v1/mps/{mp_id}")
async def quarantined_member(mp_id: int):
    return unavailable()
