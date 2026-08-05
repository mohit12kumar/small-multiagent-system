import React, { useState, useEffect, useRef } from 'react';
import { resumeAPI } from '../services/api';

export default function ResumePage() {
  const [resumes, setResumes]     = useState([]);
  const [loading, setLoading]     = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError]         = useState('');
  const [success, setSuccess]     = useState('');
  const [dragOver, setDragOver]   = useState(false);
  const [selected, setSelected]   = useState(null);
  const fileRef = useRef();

  const fetchResumes = async () => {
    try {
      const r = await resumeAPI.list();
      setResumes(r.data);
    } catch { setError('Failed to load resumes.'); }
    finally { setLoading(false); }
  };

  useEffect(() => { fetchResumes(); }, []);

  const handleFile = async (file) => {
    if (!file) return;
    const ext = file.name.split('.').pop().toLowerCase();
    if (!['pdf','docx','txt'].includes(ext)) {
      setError('Only .pdf, .docx, and .txt files are supported.'); return;
    }
    setError(''); setSuccess('');
    setUploading(true);
    try {
      const r = await resumeAPI.upload(file);
      setSuccess(`✅ Resume analyzed! ATS Score: ${r.data.ats_score}%`);
      await fetchResumes();
    } catch (err) {
      setError(err?.response?.data?.detail || 'Upload failed.');
    } finally { setUploading(false); }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this resume?')) return;
    try {
      await resumeAPI.delete(id);
      setResumes(r => r.filter(x => x.id !== id));
      if (selected?.id === id) setSelected(null);
    } catch { setError('Delete failed.'); }
  };

  return (
    <div className="animate-fadeIn">
      <div style={{ marginBottom: 28 }}>
        <h1 style={{ fontSize: 24, fontWeight: 800 }}>📄 Resume Manager</h1>
        <p className="text-secondary text-sm mt-4">Upload your resume for AI-powered ATS scoring and skill extraction</p>
      </div>

      {error   && <div className="alert alert-error mb-4">{error}</div>}
      {success && <div className="alert alert-success mb-4">{success}</div>}

      {/* Upload Zone */}
      <div
        className={`upload-zone mb-6 ${dragOver ? 'drag-over' : ''}`}
        onClick={() => fileRef.current?.click()}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={(e) => {
          e.preventDefault(); setDragOver(false);
          handleFile(e.dataTransfer.files[0]);
        }}
      >
        <input ref={fileRef} type="file" accept=".pdf,.docx,.txt" style={{ display:'none' }}
          onChange={e => handleFile(e.target.files[0])} />
        {uploading ? (
          <div style={{ display:'flex', flexDirection:'column', alignItems:'center', gap:12 }}>
            <span className="spinner spinner-lg" />
            <span style={{ color:'var(--text-secondary)', fontSize:14 }}>Uploading & analyzing with AI…</span>
          </div>
        ) : (
          <>
            <div className="upload-icon">📤</div>
            <div className="upload-title">Drop your resume here</div>
            <div className="upload-sub">or click to browse · PDF, DOCX, TXT supported</div>
          </>
        )}
      </div>

      {/* Resume List + Detail */}
      <div className={selected ? 'grid-2' : ''}>
        <div className="card">
          <div className="card-header">
            <div className="card-title">Your Resumes</div>
            <span className="badge badge-blue">{resumes.length}</span>
          </div>
          {loading ? (
            <div className="loading-state">
              <span className="spinner" /> Loading…
            </div>
          ) : resumes.length === 0 ? (
            <div style={{ padding:'48px 24px', textAlign:'center', color:'var(--text-muted)', fontSize:14 }}>
              <div style={{ fontSize:40, marginBottom:12 }}>📭</div>
              No resumes uploaded yet
            </div>
          ) : (
            <table className="data-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>File</th>
                  <th>ATS Score</th>
                  <th>Skills</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {resumes.map(r => (
                  <tr key={r.id} style={{ cursor:'pointer' }} onClick={() => setSelected(r)}>
                    <td style={{ fontWeight:600, color:'var(--text-primary)' }}>#{r.id}</td>
                    <td style={{ fontSize:13 }}>{r.resume_path?.split(/[\\/]/).pop() || 'resume.pdf'}</td>
                    <td>
                      <span className={`badge ${r.ats_score >= 80 ? 'badge-green' : r.ats_score >= 60 ? 'badge-amber' : 'badge-red'}`}>
                        {r.ats_score}%
                      </span>
                    </td>
                    <td style={{ fontSize:12, color:'var(--text-muted)' }}>
                      {(r.skills || []).slice(0, 3).join(', ')}{r.skills?.length > 3 ? ` +${r.skills.length-3}` : ''}
                    </td>
                    <td>
                      <button className="btn btn-danger btn-sm" onClick={e => { e.stopPropagation(); handleDelete(r.id); }}>
                        🗑 Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        {/* Detail Panel */}
        {selected && (
          <div className="card animate-fadeInLeft">
            <div className="card-header">
              <div>
                <div className="card-title">Resume Details</div>
                <div className="card-subtitle">#{selected.id}</div>
              </div>
              <button className="btn btn-ghost btn-sm" onClick={() => setSelected(null)}>✕</button>
            </div>
            <div className="card-body" style={{ display:'flex', flexDirection:'column', gap:20 }}>
              {/* ATS Ring */}
              <div style={{ textAlign:'center', padding:'12px 0' }}>
                <div style={{ fontSize:52, fontWeight:900, background:'var(--gradient-brand)', WebkitBackgroundClip:'text', WebkitTextFillColor:'transparent' }}>
                  {selected.ats_score}%
                </div>
                <div style={{ fontSize:13, color:'var(--text-muted)' }}>ATS Score</div>
              </div>

              <div>
                <div style={{ fontSize:12, fontWeight:700, color:'var(--text-muted)', letterSpacing:'0.08em', textTransform:'uppercase', marginBottom:10 }}>Skills Detected</div>
                <div className="skill-tags">
                  {(selected.skills || []).map(s => <span key={s} className="skill-tag">{s}</span>)}
                </div>
              </div>

              {selected.education?.length > 0 && (
                <div>
                  <div style={{ fontSize:12, fontWeight:700, color:'var(--text-muted)', letterSpacing:'0.08em', textTransform:'uppercase', marginBottom:10 }}>Education</div>
                  {selected.education.map((e, i) => (
                    <div key={i} style={{ fontSize:13, color:'var(--text-secondary)', padding:'6px 0', borderBottom:'1px solid var(--color-border)' }}>{e}</div>
                  ))}
                </div>
              )}

              {selected.experience?.length > 0 && (
                <div>
                  <div style={{ fontSize:12, fontWeight:700, color:'var(--text-muted)', letterSpacing:'0.08em', textTransform:'uppercase', marginBottom:10 }}>Experience</div>
                  {selected.experience.map((e, i) => (
                    <div key={i} style={{ fontSize:13, color:'var(--text-secondary)', padding:'6px 0', borderBottom:'1px solid var(--color-border)' }}>{e}</div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
