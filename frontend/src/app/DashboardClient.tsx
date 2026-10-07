"use client";

import { useState } from "react";
import type { PublicationState } from "../lib/status";

const COPY = {
  en: {
    title: "Parliament Watch Nepal",
    subtitle: "An independent portal for parliamentary transparency",
    pendingTitle: "Verified parliamentary records are being prepared",
    pendingBody: "MP profiles, attendance and bill records will appear after their sources have been checked. Unverified records are withheld. Missing information does not mean zero attendance, zero activity or zero assets.",
    unavailableTitle: "The service is temporarily unavailable",
    unavailableBody: "We cannot check data availability right now. Please try again. No substitute profiles or statistics are displayed.",
    retry: "Check availability again",
    checking: "Checking…",
    sources: "Explore the official sources",
    members: "Members of Parliament",
    meetings: "Meetings and attendance",
    bills: "House of Representatives bill registry",
    note: "Source links are provided for reference. Parliament Watch is independent of the Federal Parliament of Nepal.",
  },
  ne: {
    title: "पार्लियामेन्ट वाच नेपाल",
    subtitle: "संसदीय पारदर्शिताका लागि स्वतन्त्र पोर्टल",
    pendingTitle: "प्रमाणित संसदीय अभिलेख तयार हुँदैछन्",
    pendingBody: "स्रोत जाँच भएपछि सांसद परिचय, उपस्थिति र विधेयकका विवरण उपलब्ध हुनेछन्। अप्रमाणित विवरण देखाइएको छैन। जानकारी उपलब्ध नहुनुको अर्थ उपस्थिति, गतिविधि वा सम्पत्ति शून्य हुनु होइन।",
    unavailableTitle: "सेवा अहिले उपलब्ध छैन",
    unavailableBody: "अहिले विवरणको उपलब्धता जाँच गर्न सकिएन। कृपया फेरि प्रयास गर्नुहोस्। सट्टामा काल्पनिक परिचय वा तथ्याङ्क देखाइएको छैन।",
    retry: "उपलब्धता फेरि जाँच गर्नुहोस्",
    checking: "जाँच हुँदैछ…",
    sources: "आधिकारिक स्रोत हेर्नुहोस्",
    members: "सङ्घीय सांसदहरू",
    meetings: "बैठक र उपस्थिति",
    bills: "प्रतिनिधि सभाको विधेयक अभिलेख",
    note: "स्रोतका लिङ्क सन्दर्भका लागि दिइएका हुन्। पार्लियामेन्ट वाच नेपालको सङ्घीय संसद्बाट स्वतन्त्र परियोजना हो।",
  },
};

export default function DashboardClient({
  initialState,
}: {
  initialState: PublicationState;
}) {
  const [state, setState] = useState(initialState);
  const [language, setLanguage] = useState<"en" | "ne">("ne");
  const [checking, setChecking] = useState(false);
  const copy = COPY[language];
  const pending = state.kind === "verification_pending";

  async function retry() {
    setChecking(true);
    try {
      const response = await fetch("/api/status", {
        cache: "no-store",
        signal: AbortSignal.timeout(7000),
      });
      const value: unknown = await response.json();
      const kind = typeof value === "object" && value !== null
        ? (value as Record<string, unknown>).kind
        : undefined;
      setState(response.ok && kind === "verification_pending"
        ? { kind: "verification_pending" }
        : { kind: "unavailable" });
    } catch {
      setState({ kind: "unavailable" });
    } finally {
      setChecking(false);
    }
  }

  return (
    <main className="dashboard-container" lang={language}>
      <header className="main-header">
        <div className="title-section">
          <h1>{copy.title}</h1>
          <p>{copy.subtitle}</p>
        </div>
        <nav aria-label="Language / भाषा" className="language-controls">
          <button type="button" lang="ne" aria-pressed={language === "ne"} onClick={() => setLanguage("ne")}>नेपाली</button>
          <button type="button" lang="en" aria-pressed={language === "en"} onClick={() => setLanguage("en")}>English</button>
        </nav>
      </header>
      <section className="glass-panel availability-panel" aria-labelledby="availability-title" aria-busy={checking}>
        <div role="status" aria-live="polite">
          <h2 id="availability-title">{pending ? copy.pendingTitle : copy.unavailableTitle}</h2>
          <p>{pending ? copy.pendingBody : copy.unavailableBody}</p>
        </div>
        <button type="button" onClick={retry} disabled={checking}>
          {checking ? copy.checking : copy.retry}
        </button>
      </section>
      <section className="glass-panel availability-panel" aria-labelledby="sources-title">
        <h2 id="sources-title">{copy.sources}</h2>
        <ul className="source-links">
          <li><a href="https://digital.parliament.gov.np/members">{copy.members}</a></li>
          <li><a href="https://digital.parliament.gov.np/baithak">{copy.meetings}</a></li>
          <li><a href="https://hr.parliament.gov.np/np/bills?type=state">{copy.bills}</a></li>
        </ul>
      </section>
      <footer className="availability-footer">{copy.note}</footer>
    </main>
  );
}
