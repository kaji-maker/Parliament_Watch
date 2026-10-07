# Phase 1 implementation and handoff

Updated 2026-10-07. Safety implementation is ready for review; this is not a
verified-data release. The source adapters and public imports remain paused.

## Implemented

- Removed name-generated metrics, quotations, assets and pledges from runtime.
- Removed browser mock profiles/statistics and misleading wealth/activity views.
- Withheld all legacy dataset routes with explicit 503 verification-pending
  responses. Old `live`/`offline_cache` tags cannot bypass quarantine.
- Disabled API mutations and scraper triggers (405) without DB work.
- Removed DB access, schema creation, collection and workers from API startup.
- Preserved old database volumes and reference snapshot; no deletion/migration.
- Added separate process liveness, dataset readiness and candidate-source status.
- Added bilingual pending/unavailable states and same-origin availability retry.
- Removed hardcoded credentials, public DB port and development container entry
  points. Existing database credentials still require operator-controlled rotation.
- Added explicit unknown-date parsing, source contracts, publication policy,
  audit, phased roadmap, regression tests and GitHub CI.

## Local verification

| Check | Result |
| --- | --- |
| Backend ASGI/unit suite | 8 passed; 1 calendar conversion test skipped because nepali-datetime is not installed locally |
| Frontend availability contract tests | 4 passed using Node's in-process test runner |
| Python syntax compilation | Passed |
| `git diff --check` | Passed |
| `docker compose config --quiet` with temporary validation password | Passed |
| Frontend dependency install / lint / typecheck / build | Blocked by workspace network access; not claimed passed |
| Container runtime / production build | Not run; Docker socket access unavailable locally |
| PostgreSQL integration / data migration | Not performed; Phase 1 API intentionally does not access PostgreSQL |

Local API tests used available Python 3.12 / FastAPI 0.141.1 / httpx 0.28.1.
GitHub CI installs the project's declared Python 3.11 dependencies and runs the
calendar test, frontend lint/type/build checks and Compose validation. Consult
the PR checks for their actual result; configuration alone is not a passing run.

## Source-validation boundary

Official listing/profile/meeting sources were researched and source contracts
were written, including a reviewed manual-import fallback. No production parser,
complete source capture, documented public API or reuse permission has been
validated. Runtime metadata explicitly says `not_validated` and publishes null
counts and import timestamps. Public records resume only after evidence-backed
ingestion, review and schema work in later phases.

## GitHub CI follow-up

The declared backend dependencies passed all 9 tests, including real BS/AD
calendar conversion; Compose validation passed. Frontend lint passed after
removing an unused manifest dependency absent from the original lockfile.
The test command was corrected for Node 22 compatibility. Consult the current
PR checks for the final frontend type/build result.

Dependency installation reports 14 existing npm advisories (1 moderate, 12 high,
1 critical). They have not been individually triaged or fixed in this safety
change. Dependency security review and remediation are required before deployment;
passing functional CI is not a security clearance.

## Before proceeding

1. Review the quarantine behavior and CI results. Do not describe this as an
   attendance/bill release or claim complete Phase 1 source validation.
2. Preserve and back up existing DB volumes; recreate the old API container to
   stop its former worker. Never use `down -v` or change an existing role's
   password solely through environment configuration.
3. Capture authorized representative source fixtures and settle access/reuse
   conditions before implementing adapters. Keep unresolved identity/date fields
   explicit; do not publish the snapshot.
4. Begin Phase 2 only after review: migrations, evidence storage, stable identity,
   staged ingestion, authorized review and atomic publication.

No hosted deployment, secret rotation, merge or existing database mutation is
included in this change.
