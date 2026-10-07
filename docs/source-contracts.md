# First-release source contracts

Reviewed as source candidates on 2026-10-06. **Adapter status: not validated.**
These are extraction requirements, not assertions that a functioning source
adapter exists. Runtime metadata intentionally reports null published counts and
import timestamps.

## Member directory

- Publisher: Federal Parliament of Nepal.
- Listing: https://digital.parliament.gov.np/members
- Profile example: https://digital.parliament.gov.np/members/hari-prasad-bhusal
- Required identity evidence: source identifier/profile URL, original Nepali
  name, source English name if available, chamber, membership interval,
  election type, party, constituency/PR context.
- Optional fields remain null when not evidenced: gender, image, biography,
  committee roles, election result references.
- Validation: enumerate complete listing/pagination; preserve Unicode; no
  guessed constituency/gender; quarantine ambiguous/duplicate identities.
- Snapshot mismatch and source disagreements require review; no silent overwrite.
- Election votes/margins come from independently cited EC result records.

## Attendance

- Publisher: Federal Parliament of Nepal.
- Listing: https://digital.parliament.gov.np/baithak
- Meeting example:
  https://digital.parliament.gov.np/baithak-detail/dad53bc8-57e6-4f8a-9197-fd1dc1747fac
- Required: source meeting ID, chamber/session, actual meeting date and raw BS
  text, member source identity, explicit status, evidence locator.
- Statuses: present, absent, partial, excused, unknown, not applicable, when
  supported by the source.
- Validation: distinguish chamber and committee meetings; reconcile a reviewed
  sample; retain unknown statuses; respect membership dates; no cancellation or
  duplicate meeting in the denominator.
- Preserve source-reported numerator/denominator/method separately from any
  computed figure. A source's half-weight partial rule must be documented and
  supported by individual records before being adopted.
- This phase does not claim a complete attendance dataset.

## Bills

- Publisher: House of Representatives, Nepal.
- Registry: https://hr.parliament.gov.np/np/bills?type=state
- Digital portal https://digital.parliament.gov.np/bills currently advertises a
  forthcoming section, not a working registry.
- Required: source bill ID, original title, chamber/term context, original
  registration date, sponsor entity where stated, original status, document URL.
- Validation: inspect actual column mapping and pagination; no title-derived
  bill type; separate minister/ministry/private member; preserve unknown dates.
- Status changes need separately cited events. Do not invent a past timeline
  from a current-status row.
- Direct retrieval was intermittent; no selectors or undocumented APIs approved.

## Reviewed manual-import fallback

When the official portal is accessible in a browser but automated retrieval is
unreliable, an authorized reviewer may prepare a staging submission. This
procedure is a source fallback, not a bypass of publication validation.

Each submission must contain:

| Field | Requirement |
| --- | --- |
| `dataset` | members, attendance or bills |
| `source_url`, `publisher` | Original official record; not a search-results URL |
| `retrieved_at` | UTC ISO timestamp of collection |
| `source_document_checksum` | SHA-256 of retained evidence |
| `evidence_locator` | Page/table/row/section locating each fact |
| `source_identity` | Publisher ID, or reviewed URL-based identity |
| `raw_record` | Original language, digits, dates and status text |
| `normalized_record` | Separate parsed fields; unsupported values null |
| `calendar`, `raw_date`, `event_date` | Calendar explicit; null conversion on failure |
| `reviewer`, `reviewed_at`, `review_reason` | Approval and resolution of ambiguities |

Phase 2 implements staging, evidence storage, authorization and transactional
publication. Phase 1 provides no public import route and cannot publish this
submission directly. Even manually entered records must pass the same checks.

## Acceptance before implementing an adapter

1. Capture representative authorized source documents for parser regression
   tests, including pagination, missing fields, Nepali text and changed layouts.
2. Establish source IDs and identity crosswalks; document unresolved matches.
3. Verify calendar conversion against known BS/AD pairs.
4. Document robots/access conditions and reuse/retention permissions.
5. Confirm response format, retry policy, rate limits and TLS behavior.
6. Test outages, partial extraction and schema changes without DB mutation.
7. Review extracted sample records and approve publication eligibility.

Unknown API availability and reuse permission remain open. If a source is
unavailable or incomplete, report it and keep publication pending; never
replace records with simulations.

