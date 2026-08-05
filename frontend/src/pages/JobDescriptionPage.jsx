import React, { useState, useEffect } from 'react';
import { jdAPI } from '../services/api';

export default function JobDescriptionPage() {
  const [jds, setJds]           = useState([]);
  const [loading, setLoading]   = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [text, setText]         = useState('');
  const [error, setError]       = useState('');
  const [success, setSuccess]   = useState(null);
  const [selected, setSelected] = useState(null);

  const fetchJds = async () => {
    try {
      const r = await jdAPI.list();
      setJds(r.data);
    } catch { setError('Failed to load job descriptions.'); }
    finally { setLoading(false); }
  };

  useEffect(() => { fetchJds(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(''); setSuccess(null);
    if (text.trim().length < 10) { setError('Job description is too short.'); return; }
    setSubmitting(true);
    try {
      const r = await jdAPI.upload(text);
      setSuccess(r.data);
      setText('');
      await fetchJds();
    } catch (err) {
      setError(err?.response?.data?.detail || 'Failed to analyze job description.');
    } finally { setSubmitting(false); }
  };

  return (
    <div className="animate-fadeIn">
      <div style={{ marginBottom: 28 }}>
        <h1 style={{ fontSize: 24, fontWeight: 800 }}>🎯 Job Description Analyzer</h1>
        <p className="text-secondary text-sm mt-4">Paste a job description to extract required skills, experience, and match it against your resume</p>
      </div>

      <div className="grid-2" style={{ alignItems:'start' }}>
        {/* Input Form */}
        <div>
          <div className="card">
            <div className="card-header">
              <div className="card-title">Paste Job Description</div>
            </div>
            <div className="card-body">
              {error   && <div className="alert alert-error mb-4">{error}</div>}
              <form onSubmit={handleSubmit} style={{ display:'flex', flexDirection:'column', gap:16 }}>
                <div className="form-group">
                  <label className="form-label">Job Description Text</label>
                  <textarea
                    className="form-textarea"
                    style={{ minHeight: 240 }}
                    placeholder="Paste the full job description here…&#10;&#10;e.g. We are looking for a Senior React Developer with 3+ years of experience in..."
                    value={text}
                    onChange={e => setText(e.target.value)}
                    required
                  />
                  <span className="form-hint">{text.length} characters</span>
                </div>
                <button type="submit" className="btn btn-primary" disabled={submitting} style={{ justifyContent:'center' }}>
                  {submitting ? <><span className="spinner" style={{ width:16,height:16 }} /> Analyzing with AI…</> : '🔍 Analyze Job Description'}
                </button>
              </form>
            </div>
          </div>

          {/* Analysis Result */}
          {success && (
            <div className="card mt-4 animate-fadeIn">
              <div className="card-header">
                <div className="card-title">✅ Analysis Complete</div>
                <span className="badge badge-green">JD #{success.jd_id}</span>
              </div>
              <div className="card-body" style={{ display:'flex', flexDirection:'column', gap:18 }}>
                <div>
                  <div style={{ fontSize:12, fontWeight:700, color:'var(--text-muted)', letterSpacing:'0.08em', textTransform:'uppercase', marginBottom:8 }}>Role Title</div>
                  <div style={{ fontWeight:700, fontSize:16, color:'var(--text-primary)' }}>{success.role_title}</div>
                </div>
                <div>
                  <div style={{ fontSize:12, fontWeight:700, color:'var(--text-muted)', letterSpacing:'0.08em', textTransform:'uppercase', marginBottom:8 }}>Required Skills</div>
                  <div className="skill-tags">
                    {(success.required_skills || []).map(s => <span key={s} className="skill-tag">{s}</span>)}
                  </div>
                </div>
                {success.responsibilities?.length > 0 && (
                  <div>
                    <div style={{ fontSize:12, fontWeight:700, color:'var(--text-muted)', letterSpacing:'0.08em', textTransform:'uppercase', marginBottom:8 }}>Key Responsibilities</div>
                    <ul style={{ paddingLeft:16, display:'flex', flexDirection:'column', gap:6 }}>
                      {success.responsibilities.map((r, i) => (
                        <li key={i} style={{ fontSize:13, color:'var(--text-secondary)' }}>{r}</li>
                      ))}
                    </ul>
                  </div>
                )}
                <div>
                  <div style={{ fontSize:12, fontWeight:700, color:'var(--text-muted)', letterSpacing:'0.08em', textTransform:'uppercase', marginBottom:4 }}>Experience Required</div>
                  <div style={{ fontSize:14, color:'var(--text-primary)' }}>{success.experience_years} year(s)</div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* JD History */}
        <div className="card">
          <div className="card-header">
            <div className="card-title">Previous JDs</div>
            <span className="badge badge-blue">{jds.length}</span>
          </div>
          {loading ? (
            <div className="loading-state"><span className="spinner" /></div>
          ) : jds.length === 0 ? (
            <div style={{ padding:'48px 24px', textAlign:'center', color:'var(--text-muted)', fontSize:14 }}>
              <div style={{ fontSize:36, marginBottom:12 }}>📋</div>
              No job descriptions yet
            </div>
          ) : (
            <div style={{ maxHeight:500, overflowY:'auto' }}>
              {jds.map(jd => (
                <div key={jd.id}
                  onClick={() => setSelected(selected?.id === jd.id ? null : jd)}
                  style={{
                    padding:'16px 20px',
                    borderBottom:'1px solid var(--color-border)',
                    cursor:'pointer',
                    background: selected?.id === jd.id ? 'rgba(59,130,246,0.06)' : 'transparent',
                    transition:'background 0.2s',
                  }}>
                  <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:6 }}>
                    <span style={{ fontWeight:600, fontSize:14, color:'var(--text-primary)' }}>JD #{jd.id}</span>
                    <span style={{ fontSize:12, color:'var(--text-muted)' }}>{jd.experience_years}y exp</span>
                  </div>
                  <div style={{ fontSize:13, color:'var(--text-secondary)', marginBottom:8, display:'-webkit-box', WebkitLineClamp:2, WebkitBoxOrient:'vertical', overflow:'hidden' }}>
                    {jd.description}
                  </div>
                  <div className="skill-tags" style={{ gap:4 }}>
                    {(jd.skills || []).slice(0,5).map(s => (
                      <span key={s} className="skill-tag" style={{ fontSize:11, padding:'2px 8px' }}>{s}</span>
                    ))}
                    {jd.skills?.length > 5 && <span style={{ fontSize:11, color:'var(--text-muted)' }}>+{jd.skills.length - 5}</span>}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
