"use client";

import React, { useState } from "react";

export default function MPModal({ selectedMp, onClose, getAttendanceColor, formatNpr, initialTab = "transcripts" }) {
  const getMappedTab = (tab) => {
    if (tab === "activity") return "transcripts";
    if (tab === "promises") return "promises";
    return "assets";
  };

  const [activeTab, setActiveTab] = useState(getMappedTab(initialTab));

  if (!selectedMp) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="glass-panel modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="close-btn" onClick={onClose}>×</button>
        
        <div className="profile-header" style={{ marginBottom: "1.5rem" }}>
          <img 
            src={selectedMp.profile_pic_url || "https://hr.parliament.gov.np/uploads/member/member_placeholder.jpg"} 
            alt={selectedMp.name} 
            className="profile-pic" 
            style={{ width: "80px", height: "80px" }} 
          />
          <div>
            <h2>{selectedMp.name}</h2>
            <span className={`profile-badge ${
              selectedMp.party === "CPN-UML" ? "uml" : 
              selectedMp.party === "Nepali Congress" ? "nc" : 
              selectedMp.party === "CPN-Maoist Center" ? "mc" : 
              selectedMp.party === "Rastriya Swatantra Party" ? "rsp" : "other"
            }`}>{selectedMp.party}</span>
            <p style={{ marginTop: "0.5rem", color: "var(--text-secondary)" }}>
              Representative of **{selectedMp.constituency}** | Term: {selectedMp.term} | Gender: {selectedMp.gender}
            </p>
          </div>
        </div>

        <div className="modal-tabs">
          <button className={`tab-btn ${activeTab === "transcripts" ? "active" : ""}`} onClick={() => setActiveTab("transcripts")}>🗣️ Verbatim Transcripts</button>
          <button className={`tab-btn ${activeTab === "promises" ? "active" : ""}`} onClick={() => setActiveTab("promises")}>🗳️ Electoral Mandate & Pledges</button>
          <button className={`tab-btn ${activeTab === "assets" ? "active" : ""}`} onClick={() => setActiveTab("assets")}>💰 Itemized Asset Holdings</button>
        </div>

        {/* Verbatim Transcripts Tab */}
        {activeTab === "transcripts" && (
          <div className="transcripts-detail-view" style={{ padding: "1rem 0" }}>
            <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}>
              {selectedMp.speech_transcripts && selectedMp.speech_transcripts.map((st, idx) => (
                <div key={st.id || idx} className="glass-panel" style={{ padding: "1.5rem", background: "rgba(30, 41, 59, 0.25)", border: "1px solid rgba(255, 255, 255, 0.05)" }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.75rem", flexWrap: "wrap", gap: "0.5rem" }}>
                    <h4 style={{ margin: 0, color: "var(--color-cyan)", fontSize: "1.05rem" }}>💬 {st.topic}</h4>
                    <span style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>
                      {st.speech_date} | <span style={{ color: "var(--color-violet)", fontWeight: "600" }}>{st.context || "Session"}</span>
                    </span>
                  </div>
                  <blockquote style={{
                    margin: 0,
                    padding: "0.75rem 1rem",
                    borderLeft: "4px solid var(--color-cyan)",
                    background: "rgba(255, 255, 255, 0.02)",
                    borderRadius: "0 6px 6px 0",
                    fontStyle: "italic",
                    fontSize: "0.95rem",
                    lineHeight: "1.5",
                    color: "var(--text-secondary)"
                  }}>
                    "{st.transcript}"
                  </blockquote>
                </div>
              ))}
              {(!selectedMp.speech_transcripts || selectedMp.speech_transcripts.length === 0) && (
                <div style={{ color: "var(--text-muted)", fontStyle: "italic", textAlign: "center", padding: "2rem" }}>
                  No verbatim transcripts recorded for this member.
                </div>
              )}
            </div>
          </div>
        )}

        {/* Electoral Mandate & Pledges Tab */}
        {activeTab === "promises" && (
          <div className="promises-detail-view" style={{ padding: "1rem 0" }}>
            {/* Electoral Mandate Card */}
            <div className="glass-panel electoral-mandate-card" style={{
              background: "linear-gradient(135deg, rgba(99, 102, 241, 0.12) 0%, rgba(168, 85, 247, 0.12) 100%)",
              border: "1px solid rgba(168, 85, 247, 0.2)",
              padding: "1.5rem",
              borderRadius: "12px",
              marginBottom: "1.5rem"
            }}>
              <h3 style={{ margin: "0 0 1rem 0", color: "#c084fc", fontSize: "1.1rem", fontWeight: "600", display: "flex", alignItems: "center", gap: "0.5rem" }}>
                <span>🗳️</span> 2026 Electoral Mandate
              </h3>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "1.5rem" }}>
                <div>
                  <div style={{ fontSize: "0.85rem", color: "var(--text-secondary)" }}>Votes Secured</div>
                  <div style={{ fontSize: "2rem", fontWeight: "800", color: "var(--color-cyan)", marginTop: "0.25rem" }}>
                    {selectedMp.votes_secured ? selectedMp.votes_secured.toLocaleString() : "N/A"}
                  </div>
                  <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", marginTop: "0.25rem" }}>Total popular vote count</div>
                </div>
                <div>
                  <div style={{ fontSize: "0.85rem", color: "var(--text-secondary)" }}>Victory Margin</div>
                  <div style={{ fontSize: "2rem", fontWeight: "800", color: "var(--color-emerald)", marginTop: "0.25rem" }}>
                    {selectedMp.margin_victory ? selectedMp.margin_victory.toLocaleString() : "N/A"}
                  </div>
                  <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", marginTop: "0.25rem" }}>
                    {selectedMp.name === "Balen Shah" ? "Margin over CPN-UML's KP Sharma Oli" : "Constituency victory margin"}
                  </div>
                </div>
              </div>
            </div>

            {/* Promises vs Delivered split layout */}
            <div className="split-promises-layout" style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: "1.5rem" }}>
              <div className="glass-panel" style={{ padding: "1.5rem", background: "rgba(30, 41, 59, 0.2)", border: "1px solid rgba(255, 255, 255, 0.05)" }}>
                <h4 style={{ margin: "0 0 1rem 0", color: "var(--color-cyan)", fontSize: "1.05rem", fontWeight: "600", borderBottom: "1px solid rgba(255,255,255,0.08)", paddingBottom: "0.5rem" }}>📢 Promises Made</h4>
                <ul style={{ listStyleType: "none", padding: 0, margin: 0, display: "flex", flexDirection: "column", gap: "0.75rem" }}>
                  {selectedMp.constituency_promises && selectedMp.constituency_promises.map((p, idx) => (
                    <li key={idx} style={{ display: "flex", alignItems: "flex-start", gap: "0.5rem", fontSize: "0.9rem", color: "var(--text-secondary)" }}>
                      <span style={{ color: "var(--color-cyan)", fontSize: "1rem" }}>🎯</span>
                      <div>{p}</div>
                    </li>
                  ))}
                  {(!selectedMp.constituency_promises || selectedMp.constituency_promises.length === 0) && (
                    <li style={{ color: "var(--text-muted)", fontStyle: "italic" }}>No promises recorded.</li>
                  )}
                </ul>
              </div>

              <div className="glass-panel" style={{ padding: "1.5rem", background: "rgba(30, 41, 59, 0.2)", border: "1px solid rgba(255, 255, 255, 0.05)" }}>
                <h4 style={{ margin: "0 0 1rem 0", color: "var(--color-emerald)", fontSize: "1.05rem", fontWeight: "600", borderBottom: "1px solid rgba(255,255,255,0.08)", paddingBottom: "0.5rem" }}>✅ Changes Delivered</h4>
                <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
                  {selectedMp.delivered_reforms && selectedMp.delivered_reforms.map((r, idx) => (
                    <div key={idx} style={{ display: "flex", gap: "0.75rem", alignItems: "flex-start" }}>
                      <span style={{
                        background: "rgba(16, 185, 129, 0.12)",
                        color: "var(--color-emerald)",
                        padding: "0.2rem 0.4rem",
                        borderRadius: "4px",
                        fontSize: "0.75rem",
                        fontWeight: "600",
                        whiteSpace: "nowrap"
                      }}>
                        Ref #{idx + 1}
                      </span>
                      <div style={{ fontSize: "0.9rem", color: "var(--text-secondary)" }}>
                        {r}
                      </div>
                    </div>
                  ))}
                  {(!selectedMp.delivered_reforms || selectedMp.delivered_reforms.length === 0) && (
                    <div style={{ color: "var(--text-muted)", fontStyle: "italic", fontSize: "0.9rem" }}>No reforms delivered yet.</div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Itemized Asset Holdings Tab */}
        {activeTab === "assets" && (
          <div className="assets-detail-view" style={{ padding: "1rem 0" }}>
            <div className="data-table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Asset Class</th>
                    <th>Item Description</th>
                    <th>Acquisition Source</th>
                    <th>Reported Date</th>
                    <th style={{ textAlign: "right" }}>Declared Valuation (NPR)</th>
                  </tr>
                </thead>
                <tbody>
                  {selectedMp.asset_ledgers && selectedMp.asset_ledgers.map((al, idx) => {
                    const badgeClass =
                      al.asset_class === "CASH" ? "nc" :
                      al.asset_class === "LAND" ? "uml" :
                      al.asset_class === "GOLD" ? "other" : "rsp";
                    return (
                      <tr key={al.id || idx}>
                        <td>
                          <span className={`profile-badge ${badgeClass}`} style={{ textTransform: "uppercase", fontSize: "0.75rem" }}>
                            {al.asset_class}
                          </span>
                        </td>
                        <td style={{ fontWeight: "600" }}>{al.item_summary}</td>
                        <td>{al.acquisition_source || "Declared Savings"}</td>
                        <td style={{ fontSize: "0.85rem", color: "var(--text-muted)" }}>{al.reported_date}</td>
                        <td className="value-col" style={{ textAlign: "right", fontWeight: "700", color: "var(--color-cyan)" }}>
                          रू {formatNpr(al.valuation_npr)}
                        </td>
                      </tr>
                    );
                  })}
                  {(!selectedMp.asset_ledgers || selectedMp.asset_ledgers.length === 0) && (
                    <tr>
                      <td colSpan={5} style={{ textAlign: "center", color: "var(--text-muted)", padding: "2rem" }}>
                        No consolidated asset ledger entries found.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
