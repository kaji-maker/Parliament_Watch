import { fetchPublicationStatus, type PublicationState } from "./status";

export async function getPublicationStatus(): Promise<PublicationState> {
  const base = process.env.API_INTERNAL_URL;
  if (!base) return { kind: "unavailable" };
  try {
    const origin = new URL(base);
    if (
      !["http:", "https:"].includes(origin.protocol) ||
      origin.username || origin.password ||
      origin.pathname !== "/" || origin.search || origin.hash
    ) {
      return { kind: "unavailable" };
    }
    return await fetchPublicationStatus(new URL("/api/v1/status", origin).href);
  } catch {
    return { kind: "unavailable" };
  }
}

