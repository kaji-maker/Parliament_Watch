import { getPublicationStatus } from "../../../lib/backend";

export async function GET() {
  const state = await getPublicationStatus();
  return Response.json(state, {
    status: state.kind === "unavailable" ? 503 : 200,
    headers: { "Cache-Control": "no-store" },
  });
}

