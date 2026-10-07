import DashboardClient from "./DashboardClient";
import { getPublicationStatus } from "../lib/backend";

// No build-time dataset snapshot and no synthetic SSR fallback.
export const dynamic = "force-dynamic";

export default async function ParliamentDashboard() {
  return <DashboardClient initialState={await getPublicationStatus()} />;
}
