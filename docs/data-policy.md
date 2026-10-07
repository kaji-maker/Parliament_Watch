# Data publication policy

## Non-negotiable rules

1. No name-derived metrics, fabricated quotations, guessed votes, assets or
   pledges in public data.
2. Unknown is distinct from zero, absent, independent party, or male gender.
3. A verified identity does not verify associated attendance, speeches or wealth.
4. Every published factual record needs its own source, evidence location,
   retrieval time, event/reporting date, parser version and review state.
5. Preserve raw Nepali names/digits/calendar text; normalize in separate fields.
6. Failed retrieval/extraction preserves the last reviewed publication. It never
   inserts substitutes, rewrites dates to today or deletes history.
7. `live`, `offline_cache`, and successful HTTP responses are not verification
   states. Legacy records with those tags remain unpublished.
8. Only authorized, reviewed imports can publish or correct records.
9. Source-reported summaries and computed summaries are distinct, dated and
   explained. Attendance coverage and denominators must be visible.
10. Synthetic development fixtures use fictional people and isolated stores;
    they cannot be routed into production publication.

## States

- `unreviewed`: collected evidence awaiting review; not public.
- `verified`: specific extracted fact reviewed against its cited evidence.
- `disputed`: conflicting evidence requiring correction/review.
- `rejected`: extraction/identity/source validation failed; not public.
- `verification_pending`: no published dataset currently available.
- `unavailable`: service/source could not be reached.
- `stale`: previously verified publication retained after freshness threshold;
  disclose last successful import and reporting period.

Phase 1 only publishes service/source metadata and availability states. It
does not add these record states to the legacy schema or approve any old rows.
Migrations and record-level publication enforcement belong to Phase 2.

## Identity and attribution

Use publisher identifiers, stable internal IDs and reviewed bilingual aliases.
Do not match solely by constituency or ASCII slug. Record election type,
membership interval and chamber. Party affiliation can change over time.

## Attendance and bills

Do not infer presence from absence of an absence mention. Record individual
meeting statuses. Unknown status cannot lower or inflate a member's percentage.
Document eligibility, partial attendance and excused-absence treatment before
calculating aggregates.

Preserve original bill status and date strings. Government ministries, individual
sponsors and private-member bills are separate concepts. Passage by one chamber
is not authentication or enactment.

## Assets and corrections

Only publish sourced disclosures with established publication rights. Preserve
owner relationship, declaration version, original units, currency and valuation
date/basis. Missing public declarations do not imply zero assets or non-filing.
Do not publish bank account numbers or unnecessary identifying details.

Corrections require cited evidence, reviewer identity, reason and before/after
history. Possible-interest relationships are not findings of wrongdoing.

