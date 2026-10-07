export type PublicationState =
  | { kind: "verification_pending" }
  | { kind: "unavailable" };

export function parseStatus(value: unknown): PublicationState {
  if (typeof value !== "object" || value === null) return { kind: "unavailable" };
  const status = value as Record<string, unknown>;
  // Only accept this phase's contract. Connectivity cannot verify old records.
  if (status.phase !== 1 || status.publication_status !== "verification_pending") {
    return { kind: "unavailable" };
  }
  return { kind: "verification_pending" };
}

export async function fetchPublicationStatus(
  url: string,
  fetcher: typeof fetch = fetch,
): Promise<PublicationState> {
  try {
    const response = await fetcher(url, {
      cache: "no-store",
      redirect: "error",
      signal: AbortSignal.timeout(5000),
    });
    if (!response.ok) return { kind: "unavailable" };
    return parseStatus(await response.json());
  } catch {
    return { kind: "unavailable" };
  }
}

