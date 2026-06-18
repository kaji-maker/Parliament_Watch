"use client";

import React, { useState, useEffect } from "react";

// ==========================================
// Mock Fallback Data (Self-contained)
// ==========================================
const MOCK_MPS = [
  {
    id: 1,
    name: "Ram Bahadur Thapa",
    party: "CPN-UML",
    constituency: "Kathmandu-4",
    term: "2022-2027",
    profile_pic_url: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80",
    gender: "Male",
    is_active: true,
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
    ]
  },
  {
    id: 2,
    name: "Sita Devi Shrestha",
    party: "Nepali Congress",
    constituency: "Kaski-2",
    term: "2022-2027",
    profile_pic_url: "https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=150&q=80",
    gender: "Female",
    is_active: true,
    cash_balances: [
      { id: 103, bank_name: "Global IME Bank", account_type: "Current Account", currency: "NPR", balance: 2100000.00, reported_date: "2026-02-22" }
    ],
    land_holdings: [
      {
        id: 202, district: "Kaski", municipality_ward: "Pokhara-15", measurement_system: "ROPANI",
        ropanis: 0.0, aanas: 12.0, paisas: 0.0, daams: 0.0, bighas: 0.0, kathas: 0.0, dhurs: 0.0,
        total_area_sq_ft: 4107.00, estimated_value: 18000000.00, acquisition_source: "Purchased from Savings", reported_date: "2026-03-01"
      }
    ],
    gold_weights: [
      { id: 302, asset_type: "GOLD", weight_tolas: 30.0, estimated_value: 3900000.00, acquisition_source: "Inherited", reported_date: "2026-02-18" }
    ],
    equity_portfolios: [
      { id: 402, company_name: "Nabil Bank Ltd.", ticker: "NABIL", shares_count: 8500.0, share_type: "ORDINARY", nominal_value: 100.00, market_value: 5950000.00, ownership_percentage: 0.01, reported_date: "2026-05-02" }
    ]
  },
  {
    id: 3,
    name: "Hari Prasad Chaudhary",
    party: "CPN-Maoist Center",
    constituency: "Bara-1",
    term: "2022-2027",
    profile_pic_url: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=150&q=80",
    gender: "Male",
    is_active: true,
    cash_balances: [
      { id: 104, bank_name: "Rastriya Banijya Bank", account_type: "Savings", currency: "NPR", balance: 850000.00, reported_date: "2026-01-30" }
    ],
    land_holdings: [
      {
        id: 203, district: "Bara", municipality_ward: "Kalaiya-02", measurement_system: "BIGHA",
        ropanis: 0.0, aanas: 0.0, paisas: 0.0, daams: 0.0, bighas: 2.0, kathas: 5.0, dhurs: 10.0,
        total_area_sq_ft: 165847.50, estimated_value: 45000000.00, acquisition_source: "Agriculture Earnings & Inheritance", reported_date: "2026-02-14"
      }
    ],
    gold_weights: [
      { id: 303, asset_type: "GOLD", weight_tolas: 15.0, estimated_value: 1950000.00, acquisition_source: "Purchased", reported_date: "2026-03-05" }
    ],
    equity_portfolios: [
      { id: 403, company_name: "Nepal Telecom", ticker: "NTC", shares_count: 3200.0, share_type: "ORDINARY", nominal_value: 100.00, market_value: 2880000.00, ownership_percentage: 0.00, reported_date: "2026-04-20" }
    ]
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

export default function Home() {
  const [mps, setMps] = useState<any[]>(MOCK_MPS);
  const [stats, setStats] = useState<any>(MOCK_STATS);
  const [search, setSearch] = useState("");
  const [partyFilter, setPartyFilter] = useState("");
  const [selectedMp, setSelectedMp] = useState<any>(null);
  const [activeTab, setActiveTab] = useState<"cash" | "land" | "gold" | "equity">("cash");
  const [apiStatus, setApiStatus] = useState("Local Dev Mode");

  // Fetch data from backend on mount
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
        } else {
          console.warn("Backend API returned non-200, staying on mock data");
        }
      } catch (err) {
        console.warn("Could not connect to FastAPI, keeping local seed fallback: ", err);
      }
    }
    fetchData();
  }, []);

  // Filter MPs based on search and party
  const filteredMps = mps.filter((mp) => {
    const matchesSearch =
      mp.name.toLowerCase().includes(search.toLowerCase()) ||
      mp.constituency.toLowerCase().includes(search.toLowerCase());
    const matchesParty = partyFilter === "" || mp.party.toLowerCase() === partyFilter.toLowerCase();
    return matchesSearch && matchesParty;
  });

  // Numeric formatting helper
  const formatNpr = (val: number) => {
    if (val === undefined || val === null) return "0.00";
    if (val >= 10000000) {
      return `${(val / 10000000).toFixed(2)} करोड़`;
    } else if (val >= 100000) {
      return `${(val / 100000).toFixed(2)} लाख`;
    }
    return val.toLocaleString("en-NP", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  };

  const calculateMpTotalAssets = (mp: any) => {
    const cash = mp.cash_balances.reduce((acc: number, c: any) => acc + c.balance, 0);
    const land = mp.land_holdings.reduce((acc: number, l: any) => acc + (l.estimated_value || 0), 0);
    const gold = mp.gold_weights.reduce((acc: number, g: any) => acc + (g.estimated_value || 0), 0);
    const equity = mp.equity_portfolios.reduce((acc: number, e: any) => acc + (e.market_value || 0), 0);
    return cash + land + gold + equity;
  };

  return (
    <div className="dashboard-container">
      {/* Header */}
      <header className="main-header">
        <div className="title-section">
          <h1>🏛️ Parliament Watch</h1>
          <p>Nepalese Parliamentary Transparency & Wealth Conflict Monitor</p>
        </div>
        <div className="api-badge-wrapper">
          <span 
            className="profile-badge" 
            style={{
              background: apiStatus === "API Connected" ? "rgba(16, 185, 129, 0.15)" : "rgba(245, 158, 11, 0.15)",
              color: apiStatus === "API Connected" ? "#34d399" : "#fbbf24",
              border: `1px solid ${apiStatus === "API Connected" ? "rgba(16, 185, 129, 0.2)" : "rgba(245, 158, 11, 0.2)"}`
            }}
          >
            {apiStatus}
          </span>
        </div>
      </header>

      {/* Cumulative Stats Grid */}
      <section className="stats-grid">
        <div className="glass-panel stat-card cyan">
          <div className="stat-label">Total MPs Tracked</div>
          <div className="stat-value">{stats.total_mps_monitored}</div>
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
          <div className="stat-value">{stats.cumulative_gold_weight_tolas.toFixed(1)} Tolas</div>
          <div className="stat-subtext">Value: रू {formatNpr(stats.cumulative_gold_value_npr)}</div>
        </div>
      </section>

      {/* Filters */}
      <section className="filter-bar">
        <input
          type="text"
          placeholder="Search by MP name or constituency..."
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
          <option value="CPN-UML">CPN-UML</option>
          <option value="Nepali Congress">Nepali Congress</option>
          <option value="CPN-Maoist Center">CPN-Maoist Center</option>
        </select>
      </section>

      {/* Profiles Grid */}
      <section className="profiles-grid">
        {filteredMps.map((mp) => {
          const partyClass = 
            mp.party === "CPN-UML" ? "uml" : 
            mp.party === "Nepali Congress" ? "nc" : 
            mp.party === "CPN-Maoist Center" ? "mc" : "other";

          const totalAssetVal = calculateMpTotalAssets(mp);

          return (
            <div
              key={mp.id}
              className="glass-panel profile-card"
              onClick={() => {
                setSelectedMp(mp);
                setActiveTab("cash");
              }}
            >
              <div className="profile-header">
                <img src={mp.profile_pic_url || "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150"} alt={mp.name} className="profile-pic" />
                <div className="profile-meta">
                  <h3>{mp.name}</h3>
                  <span className={`profile-badge ${partyClass}`}>{mp.party}</span>
                  <div style={{ fontSize: "0.8rem", color: "var(--text-secondary)", marginTop: "0.25rem" }}>
                    📍 {mp.constituency}
                  </div>
                </div>
              </div>

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
                    {mp.gold_weights.reduce((sum: number, g: any) => sum + g.weight_tolas, 0)} Tolas
                  </span>
                </div>
                <div className="preview-item">
                  <span className="preview-label">Land Area</span>
                  <span className="preview-val">
                    {mp.land_holdings.map((lh: any) => {
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
                    {mp.equity_portfolios.length} companies
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </section>

      {/* Detail Modal */}
      {selectedMp && (
        <div className="modal-overlay" onClick={() => setSelectedMp(null)}>
          <div className="glass-panel modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="close-btn" onClick={() => setSelectedMp(null)}>×</button>
            
            <div className="profile-header" style={{ marginBottom: "1.5rem" }}>
              <img src={selectedMp.profile_pic_url || "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150"} alt={selectedMp.name} className="profile-pic" style={{ width: "80px", height: "80px" }} />
              <div>
                <h2>{selectedMp.name}</h2>
                <span className={`profile-badge ${selectedMp.party === "CPN-UML" ? "uml" : selectedMp.party === "Nepali Congress" ? "nc" : selectedMp.party === "CPN-Maoist Center" ? "mc" : "other"}`}>{selectedMp.party}</span>
                <p style={{ marginTop: "0.5rem", color: "var(--text-secondary)" }}>
                  Representative of **{selectedMp.constituency}** | Term: {selectedMp.term} | Gender: {selectedMp.gender}
                </p>
              </div>
            </div>

            <div className="modal-tabs">
              <button className={`tab-btn ${activeTab === "cash" ? "active" : ""}`} onClick={() => setActiveTab("cash")}>💵 Cash Balances</button>
              <button className={`tab-btn ${activeTab === "land" ? "active" : ""}`} onClick={() => setActiveTab("land")}>🏔️ Land Holdings</button>
              <button className={`tab-btn ${activeTab === "gold" ? "active" : ""}`} onClick={() => setActiveTab("gold")}>🪙 Gold & Precious Metals</button>
              <button className={`tab-btn ${activeTab === "equity" ? "active" : ""}`} onClick={() => setActiveTab("equity")}>📈 Equity Portfolios</button>
            </div>

            {/* Cash Tab */}
            {activeTab === "cash" && (
              <div className="data-table-container">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Financial Institution</th>
                      <th>Account Type</th>
                      <th>Currency</th>
                      <th style={{ textAlign: "right" }}>Declared Balance</th>
                    </tr>
                  </thead>
                  <tbody>
                    {selectedMp.cash_balances.map((cb: any) => (
                      <tr key={cb.id}>
                        <td>{cb.bank_name}</td>
                        <td>{cb.account_type}</td>
                        <td>{cb.currency}</td>
                        <td className="value-col" style={{ textAlign: "right" }}>{cb.balance.toLocaleString("en-NP")}</td>
                      </tr>
                    ))}
                    {selectedMp.cash_balances.length === 0 && (
                      <tr><td colSpan={4} style={{ textAlign: "center", color: "var(--text-muted)" }}>No declared cash balances.</td></tr>
                    )}
                  </tbody>
                </table>
              </div>
            )}

            {/* Land Tab */}
            {activeTab === "land" && (
              <div className="data-table-container">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>District</th>
                      <th>Location/Ward</th>
                      <th>Native Measurement</th>
                      <th>Standardized Area</th>
                      <th>Acquisition</th>
                      <th style={{ textAlign: "right" }}>Estimated Value</th>
                    </tr>
                  </thead>
                  <tbody>
                    {selectedMp.land_holdings.map((lh: any) => (
                      <tr key={lh.id}>
                        <td>{lh.district}</td>
                        <td>{lh.municipality_ward}</td>
                        <td>
                          {lh.measurement_system === "ROPANI" ? (
                            <span>{lh.ropanis} Ropani, {lh.aanas} Aana, {lh.paisas} Paisa, {lh.daams} Daam</span>
                          ) : (
                            <span>{lh.bighas} Bigha, {lh.kathas} Katha, {lh.dhurs} Dhur</span>
                          )}
                        </td>
                        <td style={{ fontFamily: "var(--font-mono)", fontSize: "0.85rem" }}>{lh.total_area_sq_ft.toLocaleString()} sq. ft.</td>
                        <td>{lh.acquisition_source}</td>
                        <td className="value-col" style={{ textAlign: "right" }}>रू {lh.estimated_value ? lh.estimated_value.toLocaleString("en-NP") : "N/A"}</td>
                      </tr>
                    ))}
                    {selectedMp.land_holdings.length === 0 && (
                      <tr><td colSpan={6} style={{ textAlign: "center", color: "var(--text-muted)" }}>No declared land holdings.</td></tr>
                    )}
                  </tbody>
                </table>
              </div>
            )}

            {/* Gold Tab */}
            {activeTab === "gold" && (
              <div className="data-table-container">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Asset Class</th>
                      <th>Declared Weight</th>
                      <th>Source of Acquisition</th>
                      <th style={{ textAlign: "right" }}>Estimated Value</th>
                    </tr>
                  </thead>
                  <tbody>
                    {selectedMp.gold_weights.map((gw: any) => (
                      <tr key={gw.id}>
                        <td>{gw.asset_type}</td>
                        <td style={{ fontWeight: 600 }}>{gw.weight_tolas} Tolas</td>
                        <td>{gw.acquisition_source || "N/A"}</td>
                        <td className="value-col" style={{ textAlign: "right" }}>रू {gw.estimated_value ? gw.estimated_value.toLocaleString("en-NP") : "N/A"}</td>
                      </tr>
                    ))}
                    {selectedMp.gold_weights.length === 0 && (
                      <tr><td colSpan={4} style={{ textAlign: "center", color: "var(--text-muted)" }}>No declared gold or precious metals.</td></tr>
                    )}
                  </tbody>
                </table>
              </div>
            )}

            {/* Equity Tab */}
            {activeTab === "equity" && (
              <div className="data-table-container">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Company Name</th>
                      <th>Ticker</th>
                      <th>Share Class</th>
                      <th>Total Shares</th>
                      <th>Ownership %</th>
                      <th style={{ textAlign: "right" }}>Declared Market Value</th>
                    </tr>
                  </thead>
                  <tbody>
                    {selectedMp.equity_portfolios.map((ep: any) => (
                      <tr key={ep.id}>
                        <td>{ep.company_name}</td>
                        <td style={{ fontFamily: "var(--font-mono)", fontSize: "0.85rem" }}>{ep.ticker || "N/A"}</td>
                        <td>{ep.share_type}</td>
                        <td>{ep.shares_count.toLocaleString()}</td>
                        <td>{ep.ownership_percentage}%</td>
                        <td className="value-col" style={{ textAlign: "right" }}>रू {ep.market_value ? ep.market_value.toLocaleString("en-NP") : "N/A"}</td>
                      </tr>
                    ))}
                    {selectedMp.equity_portfolios.length === 0 && (
                      <tr><td colSpan={6} style={{ textAlign: "center", color: "var(--text-muted)" }}>No declared corporate equity.</td></tr>
                    )}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
