"use client";

import React, { useState, useEffect } from "react";
import MPModal from "../../components/mp_modal.js";
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  SortingState,
} from "@tanstack/react-table";

// ==========================================
// Mock Fallback Data (Self-contained)
// ==========================================
const MOCK_MPS = [
  {
    id: 1,
    name: "Dol Prasad Aryal",
    party: "Rastriya Swatantra Party",
    constituency: "Kathmandu-9",
    term: "2026-2031",
    profile_pic_url: "https://hr.parliament.gov.np/uploads/member/dol_prasad_aryal.jpg",
    gender: "Male",
    is_active: true,
    data_source: "offline_cache",
    votes_secured: 32450,
    margin_victory: 12140,
    constituency_promises: [
      "Upgrade technical capacity of parliamentary drafting committees.",
      "Implement live-broadcasting systems for all thematic committee meetings.",
      "Establish public consultation portals for pending legislative bills."
    ],
    delivered_reforms: [
      "Introduced automated electronic voting for HoR sessions.",
      "Established a digitized public archives portal for historical bills.",
      "Renovated parliamentary hall audio-visual system."
    ],
    speech_transcripts: [
      {
        speech_date: "2026-03-12",
        topic: "HoR Digitalization & Electronic Voting System",
        transcript: "Parliament must lead by example in transparent technology. By introducing automated electronic voting in all legislative bills, we ensure citizens know exactly how their representatives vote on every single clause.",
        context: "Inaugural Session"
      },
      {
        speech_date: "2026-04-18",
        topic: "Business Management Board Directive",
        transcript: "As Speaker, I chair the Business Management Board. We have decided to prioritize pending financial transparency bills and ensure all committee transcripts are publicly indexed within 24 hours.",
        context: "Business Management Board"
      }
    ],
    asset_ledgers: [
      { asset_class: "CASH", item_summary: "Nepal Investment Mega Bank Savings", valuation_npr: 4500000.00, acquisition_source: "Corporate Earnings", reported_date: "2026-01-15" },
      { asset_class: "LAND", item_summary: "Imadol-04 Land (1 Ropani, 4 Aanas)", valuation_npr: 35000000.00, acquisition_source: "Inherited", reported_date: "2026-02-05" },
      { asset_class: "GOLD", item_summary: "Gold Ornaments (45 Tolas)", valuation_npr: 5850000.00, acquisition_source: "Wedding Gifts", reported_date: "2026-01-20" },
      { asset_class: "EQUITY", item_summary: "Chilime Hydropower Co (15000 Shares)", valuation_npr: 7500000.00, acquisition_source: "Promoter Portfolio", reported_date: "2026-04-12" }
    ],
    cash_balances: [
      { id: 101, bank_name: "Nepal Investment Mega Bank", account_type: "Savings", currency: "NPR", balance: 4500000.00, reported_date: "2026-01-15" },
      { id: 102, bank_name: "Nabil Bank Ltd", account_type: "Fixed Deposit", currency: "NPR", balance: 12000000.00, reported_date: "2026-03-10" }
    ],
    land_holdings: [
      {
        id: 201, district: "Lalitpur", municipality_ward: "Imadol-04", measurement_system: "ROPANI",
        ropanis: 1.0, aanas: 4.0, paisas: 2.0, daams: 0.0, bighas: 0.0, kathas: 0.0, dhurs: 0.0,
        total_area_sq_ft: 6990.12, estimated_value: 35000000.00, acquisition_source: "Inherited", reported_date: "2026-02-05"
      }
    ],
    gold_weights: [
      { id: 301, asset_type: "GOLD", weight_tolas: 45.0, estimated_value: 5850000.00, acquisition_source: "Wedding Gifts", reported_date: "2026-01-20" }
    ],
    equity_portfolios: [
      { id: 401, company_name: "Chilime Hydropower Co.", ticker: "CHCL", shares_count: 15000.0, share_type: "PROMOTER", nominal_value: 100.00, market_value: 7500000.00, ownership_percentage: 0.05, reported_date: "2026-04-12" }
    ],
    activity_metrics: {
      attendance_rate: 100.00,
      total_sessions: 60,
      sessions_attended: 60,
      committee_role: "Speaker",
      committee_name: "House of Representatives",
      sponsored_bills_count: 0,
      filed_amendments_count: 0,
      speech_instances_count: 52
    }
  },
  {
    id: 2,
    name: "Balen Shah",
    party: "Rastriya Swatantra Party",
    constituency: "Jhapa-5",
    term: "2026-2031",
    profile_pic_url: "https://hr.parliament.gov.np/uploads/member/balen_shah.jpg",
    gender: "Male",
    is_active: true,
    data_source: "offline_cache",
    votes_secured: 68348,
    margin_victory: 49614,
    constituency_promises: [
      "Construct 10 new solar irrigation networks in Jhapa-5.",
      "Establish a high-tech digital citizen feedback hub in Jhapa-5.",
      "Complete the Jhapa-5 agrarian trade highway expansion."
    ],
    delivered_reforms: [
      "Pioneered waste-to-energy conversion plant in Kathmandu.",
      "Enforced 10% educational scholarship quotas in private schools.",
      "Recovered public lands and cleared river encroachment."
    ],
    speech_transcripts: [
      {
        speech_date: "2026-04-10",
        topic: "Zero Waste & Urban Environmental Reform",
        transcript: "Our commitment to waste management is absolute. Kathmandu's landfills will no longer be a toxic legacy; we are pioneering localized bio-digestion and waste-to-energy conversion systems.",
        context: "Budget Debate"
      },
      {
        speech_date: "2026-05-18",
        topic: "Corruption Free Grievance Charter",
        transcript: "Every citizen's rupee must be audited. We are implementing blockchain-inspired project ledger systems to ensure contractors deliver quality roads on time, visible to all on our municipal watch portals.",
        context: "Zero Hour"
      }
    ],
    asset_ledgers: [
      { asset_class: "CASH", item_summary: "Global IME Current Account", valuation_npr: 2100000.00, acquisition_source: "Salaries & Savings", reported_date: "2026-02-22" },
      { asset_class: "LAND", item_summary: "Damak-05 Land (12 Aanas)", valuation_npr: 18000000.00, acquisition_source: "Purchased from Savings", reported_date: "2026-03-01" },
      { asset_class: "GOLD", item_summary: "Gold Ornaments (30 Tolas)", valuation_npr: 3900000.00, acquisition_source: "Inherited", reported_date: "2026-02-18" },
      { asset_class: "EQUITY", item_summary: "Nabil Bank Ltd (8500 Shares)", valuation_npr: 5950000.00, acquisition_source: "Ordinary Portfolio", reported_date: "2026-05-02" }
    ],
    cash_balances: [
      { id: 103, bank_name: "Global IME Bank", account_type: "Current Account", currency: "NPR", balance: 2100000.00, reported_date: "2026-02-22" }
    ],
    land_holdings: [
      {
        id: 202, district: "Jhapa", municipality_ward: "Damak-05", measurement_system: "ROPANI",
        ropanis: 0.0, aanas: 12.0, paisas: 0.0, daams: 0.0, bighas: 0.0, kathas: 0.0, dhurs: 0.0,
        total_area_sq_ft: 4107.00, estimated_value: 18000000.00, acquisition_source: "Purchased from Savings", reported_date: "2026-03-01"
      }
    ],
    gold_weights: [
      { id: 302, asset_type: "GOLD", weight_tolas: 30.0, estimated_value: 3900000.00, acquisition_source: "Inherited", reported_date: "2026-02-18" }
    ],
    equity_portfolios: [
      { id: 402, company_name: "Nabil Bank Ltd.", ticker: "NABIL", shares_count: 8500.0, share_type: "ORDINARY", nominal_value: 100.00, market_value: 5950000.00, ownership_percentage: 0.01, reported_date: "2026-05-02" }
    ],
    activity_metrics: {
      attendance_rate: 88.33,
      total_sessions: 60,
      sessions_attended: 53,
      committee_role: "Leader of the House",
      committee_name: "Federal Parliament",
      sponsored_bills_count: 12,
      filed_amendments_count: 4,
      speech_instances_count: 45
    }
  },
  {
    id: 3,
    name: "Bhishma Raj Angdembe",
    party: "Nepali Congress",
    constituency: "Proportional",
    term: "2026-2031",
    profile_pic_url: "https://hr.parliament.gov.np/uploads/member/bhishma_raj_angdembe.jpg",
    gender: "Male",
    is_active: true,
    data_source: "offline_cache",
    votes_secured: 25410,
    margin_victory: 4120,
    constituency_promises: [
      "Enforce strict legislative oversight on public works procurement.",
      "Ensure regular financial auditing of major infrastructure projects.",
      "Establish a public shadow cabinet to monitor ministry performance."
    ],
    delivered_reforms: [
      "Exposed financial irregularities in national highway procurement.",
      "Introduced 4 legislative oversight resolutions on budget allocation.",
      "Successfully blocked non-transparent zoning amendments."
    ],
    speech_transcripts: [
      {
        speech_date: "2026-04-15",
        topic: "Federal Infrastructure Procurement Transparency",
        transcript: "The citizens of Nepal deserve absolute integrity in procurement. Project delays and budget inflation in national highway projects are unacceptable; we demand independent audit commissions.",
        context: "Oversight Debate"
      }
    ],
    asset_ledgers: [
      { asset_class: "CASH", item_summary: "Nabil Bank Ltd Savings Account", valuation_npr: 850000.00, acquisition_source: "Business Income", reported_date: "2026-01-30" },
      { asset_class: "LAND", item_summary: "Phidim-2 Land (2 Ropanis, 5 Aanas)", valuation_npr: 45000000.00, acquisition_source: "Inherited", reported_date: "2026-02-14" },
      { asset_class: "GOLD", item_summary: "Gold Assets (15 Tolas)", valuation_npr: 1950000.00, acquisition_source: "Purchased", reported_date: "2026-03-05" },
      { asset_class: "EQUITY", item_summary: "Nepal Telecom (3200 Shares)", valuation_npr: 2880000.00, acquisition_source: "Ordinary Portfolio", reported_date: "2026-04-20" }
    ],
    cash_balances: [
      { id: 104, bank_name: "Rastriya Banijya Bank", account_type: "Savings", currency: "NPR", balance: 850000.00, reported_date: "2026-01-30" }
    ],
    land_holdings: [
      {
        id: 203, district: "Panchthar", municipality_ward: "Phidim-02", measurement_system: "ROPANI",
        ropanis: 2.0, aanas: 5.0, paisas: 1.0, daams: 0.0, bighas: 0.0, kathas: 0.0, dhurs: 0.0,
        total_area_sq_ft: 12675.00, estimated_value: 45000000.00, acquisition_source: "Inherited", reported_date: "2026-02-14"
      }
    ],
    gold_weights: [
      { id: 303, asset_type: "GOLD", weight_tolas: 15.0, estimated_value: 1950000.00, acquisition_source: "Purchased", reported_date: "2026-03-05" }
    ],
    equity_portfolios: [
      { id: 403, company_name: "Nepal Telecom", ticker: "NTC", shares_count: 3200.0, share_type: "ORDINARY", nominal_value: 100.00, market_value: 2880000.00, ownership_percentage: 0.00, reported_date: "2026-04-20" }
    ],
    activity_metrics: {
      attendance_rate: 85.00,
      total_sessions: 60,
      sessions_attended: 51,
      committee_role: "Leader of the Opposition",
      committee_name: "Federal Parliament",
      sponsored_bills_count: 8,
      filed_amendments_count: 18,
      speech_instances_count: 40
    }
  }
];

const MOCK_STATS = {
  total_mps_monitored: 3,
  cumulative_cash_npr: 19450000.00,
  cumulative_land_value_npr: 98000000.00,
  cumulative_gold_value_npr: 11700000.00,
  cumulative_gold_weight_tolas: 90.00,
  cumulative_equity_value_npr: 16330000.00,
  total_declared_assets_npr: 145480000.00
};

export default function DashboardClient({ initialMps, initialStats }: { initialMps: any[], initialStats: any }) {
  const [mps, setMps] = useState<any[]>(initialMps && initialMps.length > 0 ? initialMps : MOCK_MPS);
  const [stats, setStats] = useState<any>(initialStats ? initialStats : MOCK_STATS);
  const [search, setSearch] = useState("");
  const [partyFilter, setPartyFilter] = useState("");
  const [selectedMp, setSelectedMp] = useState<any>(null);
  const [apiStatus, setApiStatus] = useState(initialMps && initialMps.length > 0 ? "API Connected (SSR)" : "Local Dev Mode");
  const [viewMode, setViewMode] = useState<"assets" | "activity">("activity");
  const [sortBy, setSortBy] = useState<"attendance" | "bills" | "amendments" | "speeches" | "assets">("attendance");
  const [sorting, setSorting] = useState<SortingState>([
    { id: "attendance_rate", desc: true }
  ]);

  const isOfflineCache = mps.some(mp => mp.data_source === "offline_cache");

  // Fetch data from backend on mount (hydration / sync fallback)
  useEffect(() => {
    async function fetchData() {
      try {
        const mpsRes = await fetch("http://localhost:8002/api/v1/mps");
        const statsRes = await fetch("http://localhost:8002/api/v1/mps/stats/totals");
        
        if (mpsRes.ok && statsRes.ok) {
          const mpsData = await mpsRes.json();
          const statsData = await statsRes.json();
          setMps(mpsData);
          setStats(statsData);
          setApiStatus("API Connected");
        }
      } catch (err) {
        console.warn("Client fallback API call skipped or postponed: ", err);
      }
    }
    fetchData();
  }, []);

  const calculateMpTotalAssets = (mp: any) => {
    const cash = mp.cash_balances ? mp.cash_balances.reduce((acc: number, c: any) => acc + c.balance, 0) : 0;
    const land = mp.land_holdings ? mp.land_holdings.reduce((acc: number, l: any) => acc + (l.estimated_value || 0), 0) : 0;
    const gold = mp.gold_weights ? mp.gold_weights.reduce((acc: number, g: any) => acc + (g.estimated_value || 0), 0) : 0;
    const equity = mp.equity_portfolios ? mp.equity_portfolios.reduce((acc: number, e: any) => acc + (e.market_value || 0), 0) : 0;
    return cash + land + gold + equity;
  };

  // Filter MPs based on search and party
  const filteredMps = React.useMemo(() => {
    return mps.filter((mp) => {
      const matchesSearch =
        mp.name.toLowerCase().includes(search.toLowerCase()) ||
        mp.constituency.toLowerCase().includes(search.toLowerCase());
      const matchesParty = partyFilter === "" || mp.party.toLowerCase() === partyFilter.toLowerCase();
      return matchesSearch && matchesParty;
    });
  }, [mps, search, partyFilter]);

  // Define columns for TanStack Table
  const columns = React.useMemo(() => [
    {
      accessorKey: "name",
      header: "Name",
    },
    {
      accessorKey: "attendance_rate",
      header: "Attendance Rate",
      accessorFn: (row: any) => row.activity_metrics?.attendance_rate ?? 0,
    },
    {
      accessorKey: "sponsored_bills_count",
      header: "Sponsored Bills",
      accessorFn: (row: any) => row.activity_metrics?.sponsored_bills_count ?? 0,
    },
    {
      accessorKey: "filed_amendments_count",
      header: "Amendments Filed",
      accessorFn: (row: any) => row.activity_metrics?.filed_amendments_count ?? 0,
    },
    {
      accessorKey: "speech_instances_count",
      header: "Speeches Delivered",
      accessorFn: (row: any) => row.activity_metrics?.speech_instances_count ?? 0,
    },
    {
      accessorKey: "total_assets",
      header: "Total Declared Wealth",
      accessorFn: (row: any) => calculateMpTotalAssets(row),
    }
  ], []);

  // TanStack Table setup
  const table = useReactTable({
    data: filteredMps,
    columns,
    state: {
      sorting,
    },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    enableMultiSort: true,
  });

  const sortedMps = React.useMemo(() => {
    return table.getRowModel().rows.map(row => row.original);
  }, [table, sorting, filteredMps]);

  // Synchronize sortBy dropdown with TanStack sorting state
  const handleSortByChange = (val: string) => {
    setSortBy(val as any);
    let newSortId = "attendance_rate";
    if (val === "attendance") newSortId = "attendance_rate";
    else if (val === "bills") newSortId = "sponsored_bills_count";
    else if (val === "amendments") newSortId = "filed_amendments_count";
    else if (val === "speeches") newSortId = "speech_instances_count";
    else if (val === "assets") newSortId = "total_assets";

    setSorting([{ id: newSortId, desc: true }]);
  };

  // Keep dropdown in sync with first sort key
  useEffect(() => {
    if (sorting.length > 0) {
      const primarySort = sorting[0].id;
      if (primarySort === "attendance_rate") setSortBy("attendance");
      else if (primarySort === "sponsored_bills_count") setSortBy("bills");
      else if (primarySort === "filed_amendments_count") setSortBy("amendments");
      else if (primarySort === "speech_instances_count") setSortBy("speeches");
      else if (primarySort === "total_assets") setSortBy("assets");
    }
  }, [sorting]);

  // Numeric formatting helper
  const formatNpr = (val: number) => {
    if (val === undefined || val === null) return "0.00";
    if (val >= 10000000) {
      return `${(val / 10000000).toFixed(2)} करोड`;
    } else if (val >= 100000) {
      return `${(val / 100000).toFixed(2)} लाख`;
    }
    return val.toLocaleString("en-NP", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  };

  // Get color for attendance percentage
  const getAttendanceColor = (rate: number) => {
    if (rate >= 80.0) return "var(--color-emerald)"; // High Presence
    if (rate >= 60.0) return "var(--color-amber)"; // Regular
    return "var(--color-rose)"; // Chronic Absence
  };

  const getAttendanceLabel = (rate: number) => {
    if (rate >= 80.0) return "High Presence";
    if (rate >= 60.0) return "Regular Presence";
    return "Chronic Absence";
  };

  return (
    <div className="dashboard-container">
      {/* Dynamic System Transparency Warning Banner */}
      {isOfflineCache && (
        <div 
          className="glass-panel" 
          style={{ 
            background: "rgba(239, 68, 68, 0.12)", 
            border: "1px solid rgba(239, 68, 68, 0.3)", 
            color: "#f87171", 
            padding: "0.75rem 1rem", 
            marginBottom: "1rem", 
            borderRadius: "8px", 
            display: "flex", 
            alignItems: "center", 
            gap: "0.5rem",
            fontSize: "0.9rem",
            fontWeight: "500",
            boxShadow: "0 0 15px rgba(239, 68, 68, 0.1)"
          }}
        >
          <span style={{ fontSize: "1.1rem" }}>⚠️</span>
          <span><strong>Notice:</strong> Live government streams (hr.parliament.gov.np) are temporarily stalled due to external server errors. Displaying high-fidelity offline cached dataset.</span>
        </div>
      )}

      {/* Header */}
      <header className="main-header">
        <div className="title-section">
          <h1>🏛️ Parliament Watch Nepal</h1>
          <p>Nepalese Parliamentary Transparency, Wealth Audit & Activity Monitor</p>
        </div>
        <div className="api-badge-wrapper" style={{ display: "flex", gap: "10px", alignItems: "center" }}>
          <span 
            className="profile-badge" 
            style={{
              background: apiStatus.includes("Connected") ? "rgba(16, 185, 129, 0.15)" : "rgba(245, 158, 11, 0.15)",
              color: apiStatus.includes("Connected") ? "#34d399" : "#fbbf24",
              border: `1px solid ${apiStatus.includes("Connected") ? "rgba(16, 185, 129, 0.2)" : "rgba(245, 158, 11, 0.2)"}`
            }}
          >
            {apiStatus}
          </span>
        </div>
      </header>

      {/* Main View Toggles */}
      <div className="mode-toggle-container glass-panel">
        <button 
          className={`mode-btn ${viewMode === "activity" ? "active" : ""}`}
          onClick={() => {
            setViewMode("activity");
            if (sorting.length > 0 && sorting[0].id === "total_assets") {
              setSorting([{ id: "attendance_rate", desc: true }]);
            }
          }}
        >
          🗳️ Parliamentary Activity Leaderboard
        </button>
        <button 
          className={`mode-btn ${viewMode === "assets" ? "active" : ""}`}
          onClick={() => {
            setViewMode("assets");
            setSorting([{ id: "total_assets", desc: true }]);
          }}
        >
          💰 MP Wealth Conflict Monitor
        </button>
      </div>

      {/* Cumulative Stats Grid */}
      {viewMode === "assets" ? (
        <section className="stats-grid">
          <div className="glass-panel stat-card cyan">
            <div className="stat-label">Total MPs Tracked</div>
            <div className="stat-value">{stats.total_mps_monitored || mps.length}</div>
            <div className="stat-subtext">Active Parliamentary Term</div>
          </div>
          
          <div className="glass-panel stat-card violet">
            <div className="stat-label">Total Declared Value</div>
            <div className="stat-value currency">{formatNpr(stats.total_declared_assets_npr)}</div>
            <div className="stat-subtext">Sum of all tracked assets</div>
          </div>

          <div className="glass-panel stat-card emerald">
            <div className="stat-label">Cumulative Land Value</div>
            <div className="stat-value currency">{formatNpr(stats.cumulative_land_value_npr)}</div>
            <div className="stat-subtext">Real estate valuations</div>
          </div>

          <div className="glass-panel stat-card amber">
            <div className="stat-label">Gold Holdings</div>
            <div className="stat-value">{stats.cumulative_gold_weight_tolas ? stats.cumulative_gold_weight_tolas.toFixed(1) : "0.0"} Tolas</div>
            <div className="stat-subtext">Value: रू {formatNpr(stats.cumulative_gold_value_npr)}</div>
          </div>
        </section>
      ) : (
        <section className="stats-grid">
          <div className="glass-panel stat-card cyan">
            <div className="stat-label">Monitored MPs</div>
            <div className="stat-value">{mps.length} / 275</div>
            <div className="stat-subtext">Federal Parliament Seats</div>
          </div>
          
          <div className="glass-panel stat-card emerald">
            <div className="stat-label">High Attendance (≥80%)</div>
            <div className="stat-value">
              {mps.filter(m => m.activity_metrics && m.activity_metrics.attendance_rate >= 80).length}
            </div>
            <div className="stat-subtext">MPs with exemplary presence</div>
          </div>

          <div className="glass-panel stat-card amber">
            <div className="stat-label">Regular Presence (60%-80%)</div>
            <div className="stat-value">
              {mps.filter(m => m.activity_metrics && m.activity_metrics.attendance_rate >= 60 && m.activity_metrics.attendance_rate < 80).length}
            </div>
            <div className="stat-subtext">MPs with moderate presence</div>
          </div>

          <div className="glass-panel stat-card rose">
            <div className="stat-label">Chronic Absences (&lt;60%)</div>
            <div className="stat-value">
              {mps.filter(m => m.activity_metrics && m.activity_metrics.attendance_rate < 60).length}
            </div>
            <div className="stat-subtext">Warning state - low attendance</div>
          </div>
        </section>
      )}

      {/* Filters Bar */}
      <section className="filter-bar glass-panel">
        <div className="filter-group">
          <input
            type="text"
            placeholder="Search MP by name or constituency..."
            className="search-input"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <select
            className="select-filter"
            value={partyFilter}
            onChange={(e) => setPartyFilter(e.target.value)}
          >
            <option value="">All Parties</option>
            <option value="Nepali Congress">Nepali Congress</option>
            <option value="CPN-UML">CPN-UML</option>
            <option value="CPN-Maoist Center">CPN-Maoist Center</option>
            <option value="Rastriya Swatantra Party">Rastriya Swatantra Party</option>
            <option value="Rastriya Prajatantra Party">Rastriya Prajatantra Party</option>
            <option value="Janata Samajbadi Party">Janata Samajbadi Party</option>
            <option value="CPN-Unified Socialist">CPN-Unified Socialist</option>
            <option value="Independent">Independent</option>
          </select>
          
          <select
            className="select-filter"
            value={sortBy}
            onChange={(e: any) => handleSortByChange(e.target.value)}
          >
            {viewMode === "activity" ? (
              <>
                <option value="attendance">Sort by Attendance Rate</option>
                <option value="bills">Sort by Sponsored Bills</option>
                <option value="amendments">Sort by Amendments Filed</option>
                <option value="speeches">Sort by Speeches Delivered</option>
              </>
            ) : (
              <option value="assets">Sort by Total Declared Wealth</option>
            )}
          </select>
        </div>
      </section>

      {/* Multi-Index Sorting Matrix Console */}
      <div 
        className="glass-panel multi-sort-console" 
        style={{ 
          padding: "1rem", 
          marginBottom: "1.5rem", 
          background: "rgba(30, 41, 59, 0.4)", 
          border: "1px solid rgba(255, 255, 255, 0.08)",
          borderRadius: "8px"
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.5rem" }}>
          <span style={{ fontSize: "0.9rem", fontWeight: "600", color: "var(--text-secondary)" }}>⚡ Multi-Index Sorting Matrix</span>
          <button 
            onClick={() => setSorting([])} 
            style={{ fontSize: "0.8rem", color: "var(--color-rose)", background: "none", border: "none", cursor: "pointer" }}
          >
            Clear All Sorts
          </button>
        </div>
        <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem", alignItems: "center" }}>
          {sorting.map((s, index) => {
            const col = columns.find(c => c.accessorKey === s.id);
            const label = col ? col.header : s.id;
            return (
              <div 
                key={s.id} 
                className="glass-panel" 
                style={{ 
                  display: "inline-flex", 
                  alignItems: "center", 
                  gap: "0.5rem", 
                  padding: "0.25rem 0.75rem", 
                  background: "rgba(99, 102, 241, 0.15)", 
                  border: "1px solid rgba(99, 102, 241, 0.3)",
                  borderRadius: "20px",
                  fontSize: "0.8rem"
                }}
              >
                <span style={{ color: "var(--color-cyan)", fontWeight: "600" }}>#{index + 1}</span>
                <span style={{ color: "var(--text-primary)" }}>{label}</span>
                <span style={{ color: s.desc ? "var(--color-rose)" : "var(--color-emerald)", fontWeight: "bold" }}>
                  {s.desc ? "▼ Desc" : "▲ Asc"}
                </span>
                <button 
                  onClick={() => {
                    setSorting(sorting.filter(x => x.id !== s.id));
                  }}
                  style={{ border: "none", background: "none", color: "var(--text-muted)", cursor: "pointer", marginLeft: "0.25rem", padding: 0 }}
                >
                  ×
                </button>
              </div>
            );
          })}
          {sorting.length === 0 && (
            <span style={{ fontSize: "0.8rem", color: "var(--text-muted)", fontStyle: "italic" }}>No active sorting keys. Profiles will be displayed in default order.</span>
          )}
        </div>
        <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap", marginTop: "1rem", borderTop: "1px solid rgba(255,255,255,0.05)", paddingTop: "0.75rem" }}>
          <span style={{ fontSize: "0.8rem", color: "var(--text-muted)", alignSelf: "center" }}>Add/Toggle Sort Key:</span>
          {columns
            .filter(col => viewMode === "activity" ? col.accessorKey !== "total_assets" : col.accessorKey === "total_assets")
            .map(col => {
              const activeSort = sorting.find(s => s.id === col.accessorKey);
              return (
                <button
                  key={col.accessorKey}
                  onClick={() => {
                    const existing = sorting.find(s => s.id === col.accessorKey);
                    if (existing) {
                      if (existing.desc) {
                        setSorting(sorting.map(s => s.id === col.accessorKey ? { ...s, desc: false } : s));
                      } else {
                        setSorting(sorting.filter(s => s.id !== col.accessorKey));
                      }
                    } else {
                      setSorting([...sorting, { id: col.accessorKey, desc: true }]);
                    }
                  }}
                  style={{
                    padding: "0.3rem 0.6rem",
                    fontSize: "0.75rem",
                    borderRadius: "6px",
                    background: activeSort ? "rgba(255,255,255,0.1)" : "rgba(255,255,255,0.02)",
                    border: activeSort ? "1px solid rgba(255,255,255,0.2)" : "1px solid rgba(255,255,255,0.05)",
                    color: activeSort ? "var(--text-primary)" : "var(--text-secondary)",
                    cursor: "pointer"
                  }}
                >
                  {col.header} {activeSort ? (activeSort.desc ? "▼" : "▲") : ""}
                </button>
              );
            })}
        </div>
      </div>

      {/* Grid of MPs */}
      <section className="profiles-grid">
        {sortedMps.map((mp, index) => {
          const totalAssetVal = calculateMpTotalAssets(mp);
          const partyCode = 
            mp.party === "CPN-UML" ? "uml" : 
            mp.party === "Nepali Congress" ? "nc" : 
            mp.party === "CPN-Maoist Center" ? "mc" : 
            mp.party === "Rastriya Swatantra Party" ? "rsp" : "other";

          const attendanceRate = mp.activity_metrics ? mp.activity_metrics.attendance_rate : 0;
          const attendanceColor = getAttendanceColor(attendanceRate);
          const attendanceLabel = getAttendanceLabel(attendanceRate);

          return (
            <div
              key={mp.id}
              className="glass-panel profile-card hover-glow"
              onClick={() => {
                setSelectedMp(mp);
              }}
            >
              {viewMode === "activity" && (
                <div className="rank-badge">
                  #{index + 1}
                </div>
              )}

              <div className="profile-header">
                <img 
                  src={mp.profile_pic_url || "https://hr.parliament.gov.np/uploads/member/member_placeholder.jpg"} 
                  alt={mp.name} 
                  className="profile-pic" 
                />
                <div className="profile-meta">
                  <h3>{mp.name}</h3>
                  <span className={`profile-badge ${partyCode}`}>{mp.party}</span>
                  <div className="meta-subtext">📍 {mp.constituency}</div>
                </div>
              </div>

              {viewMode === "activity" ? (
                // Activity metrics view
                <div className="activity-preview-container">
                  <div className="presence-donut-indicator">
                    <div className="indicator-label">Session Attendance</div>
                    <div className="indicator-value" style={{ color: attendanceColor }}>
                      {attendanceRate.toFixed(1)}%
                    </div>
                    <span 
                      className="attendance-badge-pill" 
                      style={{ 
                        backgroundColor: `${attendanceColor}15`, 
                        color: attendanceColor, 
                        border: `1px solid ${attendanceColor}30` 
                      }}
                    >
                      {attendanceLabel}
                    </span>
                  </div>

                  <div className="metrics-summary-table">
                    <div className="summary-row">
                      <span className="summary-label">Committee Role</span>
                      <span className="summary-val" style={{ fontWeight: "600" }}>
                        {mp.activity_metrics?.committee_role || "Member"}
                      </span>
                    </div>
                    <div className="summary-row">
                      <span className="summary-label">Sponsored Bills</span>
                      <span className="summary-val highlight-cyan">{mp.activity_metrics?.sponsored_bills_count || 0}</span>
                    </div>
                    <div className="summary-row">
                      <span className="summary-label">Amendments Filed</span>
                      <span className="summary-val highlight-violet">{mp.activity_metrics?.filed_amendments_count || 0}</span>
                    </div>
                    <div className="summary-row">
                      <span className="summary-label">Verified Speeches</span>
                      <span className="summary-val highlight-amber">{mp.activity_metrics?.speech_instances_count || 0}</span>
                    </div>
                  </div>
                </div>
              ) : (
                // Asset preview view
                <div className="asset-preview-list">
                  <div className="preview-item">
                    <span className="preview-label">Total Wealth</span>
                    <span className="preview-val" style={{ color: "var(--color-cyan)" }}>
                      रू {formatNpr(totalAssetVal)}
                    </span>
                  </div>
                  <div className="preview-item">
                    <span className="preview-label">Gold Declared</span>
                    <span className="preview-val">
                      {mp.gold_weights ? mp.gold_weights.reduce((sum: number, g: any) => sum + g.weight_tolas, 0) : 0} Tolas
                    </span>
                  </div>
                  <div className="preview-item">
                    <span className="preview-label">Land Area</span>
                    <span className="preview-val text-truncate" style={{ maxWidth: "150px" }}>
                      {mp.land_holdings && mp.land_holdings.map((lh: any) => {
                        if (lh.measurement_system === "ROPANI") {
                          return `${lh.ropanis}-${lh.aanas}-${lh.paisas}-${lh.daams} R`;
                        } else {
                          return `${lh.bighas}-${lh.kathas}-${lh.dhurs} B`;
                        }
                      }).join(", ") || "None"}
                    </span>
                  </div>
                  <div className="preview-item">
                    <span className="preview-label">Equities</span>
                    <span className="preview-val">
                      {mp.equity_portfolios ? mp.equity_portfolios.length : 0} companies
                    </span>
                  </div>
                </div>
              )}
            </div>
          );
        })}
        {sortedMps.length === 0 && (
          <div className="glass-panel" style={{ gridColumn: "1/-1", textAlign: "center", padding: "3rem", color: "var(--text-muted)" }}>
            No Members of Parliament found matching the query.
          </div>
        )}
      </section>

      {/* Detail Modal */}
      {selectedMp && (
        <MPModal
          selectedMp={selectedMp}
          onClose={() => setSelectedMp(null)}
          getAttendanceColor={getAttendanceColor}
          formatNpr={formatNpr}
          initialTab={viewMode === "activity" ? "transcripts" : "assets"}
        />
      )}
    </div>
  );
}
