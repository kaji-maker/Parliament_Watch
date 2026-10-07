# Phased implementation plan

## Accepted direction

Public citizens; Nepali and English. First release: verified MP directory,
attendance and bills. Assets follow later. Initially scope implementation to the
House of Representatives; design chamber/membership entities for National
Assembly expansion. Preserve the existing FastAPI, PostgreSQL and Next.js stack.

Product proposition: citizens can find their representative, understand their
activity, and inspect the evidence behind every displayed fact. Differentiate
through provenance, reporting periods, historical changes, coverage and
explanations rather than unsupported rankings.

## Architecture

Official sources -> independent scheduled worker -> staging/validation/review ->
published PostgreSQL records -> FastAPI read API -> bilingual Next.js portal.

An API restart must not trigger collection or rewrite data. Start with a
PostgreSQL job table and lock; add an external queue only if workload warrants it.

Core entities:

- Person, PersonAlias, SourceIdentity.
- Membership, Party, Constituency with dated changes.
- SourceDocument, IngestionRun with checksum, retrieval time and parser version.
- Meeting, AttendanceRecord with evidence and eligibility.
- Bill, BillEvent, BillDocument, sponsor entity and originating chamber.
- ReviewAction, Correction.
- Later: Declaration, AssetItem, Interest with versioned evidence.

## Phase 1 — Trustworthy behavior and source contracts

Estimate: 2–4 focused days.

- Remove synthetic production data and live-tag contamination.
- Withhold legacy rows without deleting them.
- Disable unauthenticated mutations and scraper triggers.
- Stop destructive startup/background synchronization.
- Document source candidates, data dictionary and reviewed manual fallback.
- Replace browser/Docker hostname assumptions with server-side configuration.
- Add regression checks for publication safety and source/date failures.

Deliverables: safe baseline, audit, roadmap, source contracts and corrected setup.
Gate: outages cannot invent facts or erase records; each first-release feature
has an identified evidence source or reviewed manual route. Parser captures,
reuse permissions and real imports remain explicit dependencies.
Current implementation status: see [Phase 1 handoff](phase-1.md).

## Phase 2 — Database and ingestion foundation

Estimate: 4–6 days; depends on Phase 1.

- Back up and inspect legacy data before any migration.
- Add Alembic and stable people/membership/source identity models.
- Add evidence storage, staging, validation, reviewed publication and corrections.
- Build protected administrator review/import paths.
- Separate worker process from API; add retry, job locking and run logs.
- Apply reviewed updates transactionally; never purge/reseed.

Gate: reruns are idempotent; failed/incomplete imports preserve the last
publication; API restarts perform no collection; unsupported legacy data remains
unpublished and recoverable.

## Phase 3 — Verified bilingual directory

Estimate: 3–5 days; depends on Phase 2.

- Validate/capture source layouts and listing pagination.
- Reconcile member identities, snapshot discrepancies and membership dates.
- Preserve Nepali/English names, reviewed aliases and party history.
- Distinguish FPTP and PR; verify votes/margins through EC evidence.
- Deliver searchable directory, party/constituency filters and permanent profiles.
- Include source, reporting date and freshness information.

Gate: each published identity/membership has evidence; ambiguities are
quarantined; PR members have no invented constituency vote counts.

## Phase 4 — Evidence-based attendance

Estimate: 5–8 days; depends on Phases 2–3.

- Ingest meetings and explicit member-by-meeting statuses.
- Preserve present/absent/partial/excused/unknown/not-applicable distinctions.
- Handle membership eligibility, duplicates, cancelled meetings and coverage.
- Keep source-reported and computed aggregates distinct.
- Document weighting/denominator rules; show reporting period and coverage.
- Deliver meeting pages and profile attendance history.

Gate: a manually reviewed sample reconciles with official evidence; missing
records never imply presence or absence; every percentage is reproducible.

## Phase 5 — Bill tracker

Estimate: 4–6 days; depends on Phase 2, with directory linkage from Phase 3.

- Capture actual registry layout/pagination and validate field mappings.
- Ingest original titles, source IDs, dates, sponsors and source documents.
- Store event history and normalize only understood statuses.
- Distinguish ministries, MPs, government/private-member bills.
- Preserve passage/authentication/withdrawal/lapse as distinct events.
- Deliver search, detail pages and documented timelines.

Gate: imports update identities without duplicates; unknown fields stay unknown;
titles do not determine sponsor/type; timelines only include sourced events.

## Phase 6 — Complete the citizen experience

Estimate: 5–8 days; depends on Phases 3–5.

- Integrate directory, attendance and bills into mobile-first journeys.
- Complete reviewed Nepali/English copy, search aliases and terminology.
- Add shareable filter URLs, readable Nepali typography and source panels.
- Distinguish empty, unavailable, stale and verification-pending states.
- Add methodology/corrections pages and clear independent-project attribution.
- Test keyboard, screen-reader structure, focus, zoom and mobile layouts.

Gate: citizens can find a member, inspect attendance, follow a bill and reach the
supporting source in either language; target WCAG 2.2 AA.

## Phase 7 — Production readiness and release

Estimate: 3–5 days; depends on first-release features.

- Finish ingress, authorization, secret rotation and private DB configuration.
- Expand CI with migration and critical browser journeys.
- Test deployment/rollback, backup restoration and worker failure recovery.
- Add source freshness alerts, health/readiness checks and runbooks.
- Review data coverage and operational ownership before public launch.

Gate: clean deployment, tested restore/rollback, outage-safe publication and
no anonymous mutations. Deploy only after release review.

## Phase 8 — Public asset declarations

Estimate: 6–10 days after accessible sources/publication rights are established.

- Pilot a small document set before general ingestion.
- Add declaration versions, ownership relationships, liabilities and evidence.
- Review OCR/extraction against document/page citations.
- Preserve native land/gold units, currency and declared valuation separately
  from estimates; use decimal arithmetic and tested conversion services.
- Redact account numbers and unnecessary identifying details.
- Show verified-subset coverage.

Gate: each published item traces to reviewed evidence; missing public disclosures
imply neither zero wealth nor failure to file.

## Phase 9 — Reviewed interests and possible-conflict analysis

Estimate after asset pilot; separate editorial/product milestone.

- Link supported interests with dated committee roles and legislative activity.
- Define explainable rules, date overlap and reviewed entity matches.
- Require human review of proposed relationships.
- Publish evidence/limitations and correction routes.

Gate: every flag explains its evidence; ambiguous matches cannot publish; a
possible interest relationship is never an automatic finding of wrongdoing.

## Delivery rhythm and estimates

Phases 1–7: approximately 26–42 focused engineering days, conditional on source
access, translation review and reconciliation. Later estimates are independent.

Each phase gets a focused PR, demonstration, verification report, unresolved
dependencies and updated handoff. Work phase by phase; do not silently start
later milestones.

Checks prioritize source layout/calendar/Unicode, identity ambiguity, duplicate
imports, interrupted transactions, attendance eligibility, sponsor attribution,
authorization, bilingual journeys, migration, restore and rollback. Manual source
reconciliation is required in addition to automated tests.

