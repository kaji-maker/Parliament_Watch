# Parliament Watch Nepal

An independent civic portal for citizens, in Nepali and English. The first
release will cover verified MP profiles, attendance and bills. Public asset
declarations and reviewed interests analysis follow later.

**Current stage: Phase 1 — trustworthy baseline.** The previous prototype could
generate activity, wealth, pledges and speech text, including for profiles tagged
`live`. That dataset is withheld from public routes. No verified records are
published yet, and the service never substitutes invented records during outages.

## Project documents

- [Audit and research](docs/audit-2026-10-06.md)
- [Detailed phased implementation plan](docs/implementation-plan.md)
- [Source contracts and manual-import fallback](docs/source-contracts.md)
- [Data publication policy](docs/data-policy.md)
- [Phase 1 changes, verification and handoff](docs/phase-1.md)

## Stack

- Python 3.11+, FastAPI, SQLAlchemy, PostgreSQL 15
- Next.js 16.2.9, React 19.2.4, TypeScript
- Docker Compose; Node.js 22 for frontend builds and contract tests

The legacy database models are retained for controlled inspection and migration.
The Phase 1 API does not import, connect to, seed, or mutate that database.

## Run locally

For a new local installation:

1. Copy `.env.example` to `.env` and set a unique `POSTGRES_PASSWORD`.
2. Run `docker compose up -d --build`.
3. Open http://localhost:3002. The bilingual availability page is intentional.
4. API metadata is at http://localhost:8002/api/v1/status and API documentation
   at http://localhost:8002/docs.

PostgreSQL is not exposed to the host. Frontend and API ports bind to loopback;
configure a production ingress separately in Phase 7.

**Existing installations:** take a PostgreSQL backup before any upgrade. Keep
the existing Compose project name and `watch-db-data` volume. Never run
`docker compose down -v`. Setting a new environment password does not rotate
an existing PostgreSQL role's password. Match existing database configuration
while preserving the volume, then rotate the previously committed credential
through a controlled administrator procedure. Phase 1 does not perform that
rotation or migrate existing data. Recreate the old backend container to stop
its previous worker; do not run old and new API versions together.

For frontend development, copy `frontend/.env.example` to
`frontend/.env.local`, then run `npm ci` and `npm run dev` in `frontend`.
`API_INTERNAL_URL` is a server-only backend origin. Browsers retry availability
through the same-origin `/api/status` route; there is no public localhost URL.

For backend development:

```sh
cd backend
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
uvicorn main:app --host 127.0.0.1 --port 8002
```

## API behavior in Phase 1

| Route | Response |
| --- | --- |
| `GET /healthz` | 200 process liveness; no dataset-readiness claim |
| `GET /readyz` | 503 `verification_pending` |
| `GET /api/v1/status` | 200 candidate-source metadata; adapter status `not_validated`, counts and import timestamps `null` |
| Legacy MP, total, attendance and bill reads | 503 `verification_pending`; no legacy records or statistics |
| `POST/PUT/PATCH/DELETE /api/*` | 405 `writes_disabled`; no DB or scraper work |

Old database rows and the historical snapshot are reference material, not a
verified cache. A source URL in metadata is a candidate, not proof of integration.
Publication resumes only after provenance-aware ingestion and review.

## Verification

```sh
cd backend
python -m unittest discover -s tests -v
```

```sh
cd frontend
npm ci
npm run lint
node --experimental-strip-types --test --test-isolation=none tests/*.test.mjs
npx tsc --noEmit
npm run build
```

The backend suite uses real ASGI requests without a database or network. Calendar
conversion requires `nepali-datetime`; missing-dependency skips must be reported.
GitHub CI installs the declared dependencies and runs backend, frontend and
Compose checks. See [Phase 1](docs/phase-1.md) for actual results and limitations.

## Licence

Source code is MIT licensed. Upstream parliamentary documents, photos and data
retain their own rights; the code licence does not grant reuse rights for them.
