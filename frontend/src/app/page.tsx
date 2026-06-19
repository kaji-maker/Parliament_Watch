import React from 'react';
import DashboardClient from './DashboardClient';

interface MPProfile {
  id: number;
  name: string;
  party: string;
  constituency: string;
  gender: string;
  created_at: string;
  data_source: string;
}

async function getParliamentData(): Promise<{ mps: MPProfile[], stats: any }> {
  try {
    // Communicating container-to-container on the Docker network bridge
    // Keep data completely real-time for live audits using cache: 'no-store'
    const mpsRes = await fetch('http://backend:8000/api/v1/mps/', { 
      cache: 'no-store'
    });
    const statsRes = await fetch('http://backend:8000/api/v1/mps/stats/totals', {
      cache: 'no-store'
    });
    
    if (!mpsRes.ok || !statsRes.ok) throw new Error('Failed to fetch from backend pipeline');
    const mps = await mpsRes.json();
    const stats = await statsRes.json();
    return { mps, stats };
  } catch (error) {
    console.error("Dashboard data extraction error:", error);
    return { mps: [], stats: null }; // Resilient fallback to protect layout compilation
  }
}

export default async function ParliamentDashboard() {
  const { mps, stats } = await getParliamentData();
  return <DashboardClient initialMps={mps} initialStats={stats} />;
}
