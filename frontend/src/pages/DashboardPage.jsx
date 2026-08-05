import React, { useState, useEffect } from 'react';
import { dashboardAPI, reportsAPI } from '../services/api';

function ScoreBar({ label, value, color = 'blue' }) {
  return (
    <div className="score-bar-wrap">
      <div className="score-bar-header">
        <span className="score-bar-label">{label}</span>
        <span className="score-bar-value">{value}%</span>
      </div>
      <div className="score-bar-track">
        <div className={`score-bar-fill ${color}`} style={{ width: `${value}%` }} />
      </div>
    </div>
  );
}

function StatCard({ icon, value, label, trend, color }) {
  return (
    <div className="stat-card">
      <div className={`stat-icon ${color}`}>{icon}</div>
      <div>
        <div className="stat-value">{value}</div>
        <div className="stat-label">{label}</div>
        {trend && <div className={`stat-trend ${trend > 0 ? 'up' : 'down'}`}>
          {trend > 0 ? '▲' : '▼'} {Math.abs(trend)}% vs last session
        </div>}
      </div>
    </div>
  );
}

export default function DashboardPage() {
  const [data, setData]     = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError]   = useState('');

  useEffect(() => {
    dashboardAPI.get()
      .then(r => setData(r.data))
      .catch(() => setError('Failed to load dashboard data.'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return (
    <div className="loading-state">
      <span className="spinner spinner-lg" />
      <span>Loading your dashboard…</span>
    </div>
  );

  if (error) return <div className="alert alert-error card-p" style={{margin:32}}>{error}</div>;

  const m = data?.metrics || {};

  return (
    <div className="animate-fadeIn">
      {/* Welcome Banner */}
      <div style={{
        background: 'linear-gradient(135deg, rgba(59,130,246,0.12) 0%, rgba(99,102,241,0.08) 100%)',
        border: '1px solid var(--color-border)',
        borderRadius: 'var(--radius-xl)',
        padding: '28px 32px',
        marginBottom: 28,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: 16,
      }}>
        <div>
          <div style={{ fontSize: 13, color: 'var(--text-muted)', marginBottom: 4 }}>Good day 👋</div>
          <h1 style={{ fontSize: 26, fontWeight: 800, color: 'var(--text-primary)', marginBottom: 6 }}>
            {data?.candidate_name || 'Candidate'}
          </h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: 14 }}>
            Here's a summary of your interview readiness.
          </p>
        </div>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: 48, fontWeight: 900, background: 'linear-gradient(135deg,#3b82f6,#10b981)', WebkitBackgroundClip:'text', WebkitTextFillColor:'transparent' }}>
            {data?.overall_readiness_score ?? 0}%
          </div>
          <div style={{ fontSize: 12, color: 'var(--text-muted)', fontWeight: 600 }}>Overall Readiness</div>
        </div>
      </div>

      {/* Stat Cards */}
      <div className="dashboard-grid mb-6">
        <StatCard icon="📄" value={`${data?.resume_ats_score ?? 0}%`}  label="ATS Score"       color="blue"   trend={4}  />
        <StatCard icon="🎯" value={`${data?.skill_match_percentage ?? 0}%`} label="Skill Match"  color="green"  trend={2}  />
        <StatCard icon="💻" value={`${m.coding_score ?? 0}%`}           label="Coding Score"    color="purple" trend={-1} />
        <StatCard icon="🤝" value={`${m.hr_score ?? 0}%`}               label="HR Score"        color="amber"  />
      </div>

      {/* Bottom 2-col */}
      <div className="grid-2 mb-6">
        {/* Performance Metrics */}
        <div className="card">
          <div className="card-header">
            <div>
              <div className="card-title">📊 Performance Metrics</div>
              <div className="card-subtitle">Across all interview dimensions</div>
            </div>
          </div>
          <div className="card-body" style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            <ScoreBar label="Technical"     value={m.technical_score    ?? 84} color="blue"  />
            <ScoreBar label="Communication" value={m.communication_score ?? 86} color="green" />
            <ScoreBar label="Grammar"       value={m.grammar_score      ?? 92} color="green" />
            <ScoreBar label="Confidence"    value={m.confidence_score   ?? 78} color="amber" />
            <ScoreBar label="Coding"        value={m.coding_score       ?? 80} color="blue"  />
          </div>
        </div>

        {/* Weak Skills & Recommendations */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          <div className="card">
            <div className="card-header">
              <div className="card-title">⚠️ Skill Gaps to Address</div>
            </div>
            <div className="card-body">
              <div className="skill-tags">
                {(data?.weak_skills || []).map(s => (
                  <span key={s} className="skill-tag missing">{s}</span>
                ))}
              </div>
            </div>
          </div>

          <div className="card">
            <div className="card-header">
              <div className="card-title">💡 Recommended Topics</div>
            </div>
            <div className="card-body" style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              {(data?.recommended_topics || []).map((t, i) => (
                <div key={i} style={{
                  display: 'flex', alignItems: 'flex-start', gap: 10,
                  padding: '10px 12px', background: 'rgba(59,130,246,0.06)',
                  border: '1px solid rgba(59,130,246,0.12)', borderRadius: 8,
                  fontSize: 13, color: 'var(--text-secondary)'
                }}>
                  <span style={{ color: '#60a5fa', flexShrink: 0 }}>→</span> {t}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Recent Sessions */}
      {data?.recent_sessions?.length > 0 && (
        <div className="card">
          <div className="card-header">
            <div className="card-title">🕐 Recent Interview Sessions</div>
          </div>
          <table className="data-table">
            <thead>
              <tr>
                <th>Session ID</th>
                <th>Date</th>
                <th>Status</th>
                <th>Report</th>
              </tr>
            </thead>
            <tbody>
              {data.recent_sessions.map(s => (
                <tr key={s.id}>
                  <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>#{s.id}</td>
                  <td>{s.date}</td>
                  <td>
                    <span className={`badge ${s.status === 'completed' ? 'badge-green' : s.status === 'in_progress' ? 'badge-amber' : 'badge-blue'}`}>
                      {s.status}
                    </span>
                  </td>
                  <td>
                    {s.report_id ? (
                      <a href={reportsAPI.downloadPdf(s.report_id)} target="_blank" rel="noopener noreferrer" className="btn btn-ghost btn-xs">
                        📥 Download PDF
                      </a>
                    ) : (
                      <span style={{ color: 'var(--text-muted)', fontSize: 12 }}>—</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
