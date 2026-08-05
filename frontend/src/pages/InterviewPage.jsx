import React, { useState, useEffect } from 'react';
import { interviewAPI, resumeAPI, jdAPI, reportsAPI } from '../services/api';

/* ─── Setup Step ────────────────────────────────────── */
function SetupStep({ onStart }) {
  const [resumes,  setResumes]  = useState([]);
  const [jds,      setJds]      = useState([]);
  const [resumeId, setResumeId] = useState('');
  const [jdId,     setJdId]     = useState('');
  const [loading,  setLoading]  = useState(true);
  const [starting, setStarting] = useState(false);
  const [error,    setError]    = useState('');

  useEffect(() => {
    Promise.all([resumeAPI.list(), jdAPI.list()])
      .then(([r, j]) => { setResumes(r.data); setJds(j.data); })
      .catch(() => setError('Failed to load your data.'))
      .finally(() => setLoading(false));
  }, []);

  const handleStart = async () => {
    if (!resumeId || !jdId) { setError('Please select both a resume and a job description.'); return; }
    setError(''); setStarting(true);
    try {
      const r = await interviewAPI.start(Number(resumeId), Number(jdId));
      onStart(r.data);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Failed to start interview.');
      setStarting(false);
    }
  };

  if (loading) return <div className="loading-state"><span className="spinner spinner-lg" /><span>Preparing…</span></div>;

  return (
    <div style={{ maxWidth: 560, margin: '0 auto' }}>
      <div style={{ textAlign:'center', marginBottom:40 }}>
        <div style={{ fontSize:56, marginBottom:16, animation:'float 4s ease-in-out infinite' }}>🎙️</div>
        <h2 style={{ fontSize:26, fontWeight:800, marginBottom:8 }}>Start AI Interview</h2>
        <p style={{ color:'var(--text-muted)', fontSize:14 }}>
          Our multi-agent AI system will generate personalized technical, coding, and HR questions based on your profile.
        </p>
      </div>

      {error && <div className="alert alert-error mb-4">{error}</div>}

      {resumes.length === 0 && (
        <div className="alert alert-warning mb-4">
          ⚠️ You need to upload a resume first before starting an interview.
        </div>
      )}
      {jds.length === 0 && (
        <div className="alert alert-warning mb-4">
          ⚠️ You need to add a job description first.
        </div>
      )}

      <div className="card card-p" style={{ display:'flex', flexDirection:'column', gap:20 }}>
        <div className="form-group">
          <label className="form-label">Select Resume</label>
          <select className="form-select" value={resumeId} onChange={e => setResumeId(e.target.value)}>
            <option value="">-- Choose your resume --</option>
            {resumes.map(r => (
              <option key={r.id} value={r.id}>Resume #{r.id} · ATS {r.ats_score}%</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label className="form-label">Select Job Description</label>
          <select className="form-select" value={jdId} onChange={e => setJdId(e.target.value)}>
            <option value="">-- Choose a job description --</option>
            {jds.map(j => (
              <option key={j.id} value={j.id}>JD #{j.id} · {j.experience_years}y exp · {(j.skills||[]).slice(0,3).join(', ')}</option>
            ))}
          </select>
        </div>

        {/* Features */}
        <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:10, margin:'4px 0' }}>
          {['🤖 Technical Questions','💻 Coding Challenge','🤝 HR Behavioral','📊 Live Feedback'].map(f => (
            <div key={f} style={{ padding:'10px 14px', background:'rgba(59,130,246,0.06)', border:'1px solid rgba(59,130,246,0.12)', borderRadius:8, fontSize:13, color:'var(--text-secondary)' }}>{f}</div>
          ))}
        </div>

        <button className="btn btn-primary btn-lg" onClick={handleStart}
          disabled={starting || !resumes.length || !jds.length}
          style={{ justifyContent:'center' }}>
          {starting ? <><span className="spinner" style={{ width:18,height:18 }} /> Generating questions…</> : '▶ Start Interview Session'}
        </button>
      </div>
    </div>
  );
}

/* ─── Question Step ─────────────────────────────────── */
function QuestionStep({ sessionData, onFinish }) {
  const [question,   setQuestion]  = useState(sessionData.first_question);
  const [qIndex,     setQIndex]    = useState(0);
  const [totalQ]                   = useState(sessionData.total_questions);
  const [answer,     setAnswer]    = useState('');
  const [feedback,   setFeedback]  = useState(null);
  const [submitting, setSubmitting]= useState(false);
  const [error,      setError]     = useState('');
  const [done,       setDone]      = useState(false);

  const submitAnswer = async () => {
    if (!answer.trim()) { setError('Please write an answer before submitting.'); return; }
    setError(''); setSubmitting(true);
    try {
      const r = await interviewAPI.submitAnswer(question.id, answer);
      setFeedback(r.data.feedback);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Failed to submit answer.');
    } finally { setSubmitting(false); }
  };

  const nextQuestion = () => {
    if (qIndex + 1 >= totalQ) { setDone(true); return; }
    const nextIdx = qIndex + 1;
    setQIndex(nextIdx);
    if (sessionData.questions && sessionData.questions[nextIdx]) {
      setQuestion(sessionData.questions[nextIdx]);
    }
    setAnswer('');
    setFeedback(null);
  };

  if (done) {
    return (
      <div style={{ textAlign:'center', padding:'60px 24px' }}>
        <div style={{ fontSize:64, marginBottom:20 }}>🎉</div>
        <h2 style={{ fontSize:26, fontWeight:800, marginBottom:12 }}>Interview Complete!</h2>
        <p style={{ color:'var(--text-muted)', marginBottom:32, fontSize:15 }}>
          All {totalQ} questions answered. Generate your detailed performance report now.
        </p>
        <button className="btn btn-success btn-lg" onClick={() => onFinish(sessionData.session_id)}>
          📊 Generate My Report
        </button>
      </div>
    );
  }

  const scoreColor = (s) => s >= 80 ? '#34d399' : s >= 60 ? '#fcd34d' : '#f87171';

  return (
    <div className="interview-layout">
      {/* Main Question Panel */}
      <div className="question-card">
        <div className="question-header">
          <div>
            <span className={`badge ${question.type === 'technical' ? 'badge-blue' : question.type === 'coding' ? 'badge-purple' : 'badge-green'}`}>
              {question.type}
            </span>
            <span className={`badge ml-2 ${question.difficulty === 'easy' ? 'badge-green' : question.difficulty === 'hard' ? 'badge-red' : 'badge-amber'}`}
              style={{ marginLeft: 8 }}>
              {question.difficulty}
            </span>
          </div>
          <span style={{ fontSize:13, color:'var(--text-muted)' }}>Q{qIndex+1} of {totalQ}</span>
        </div>

        {/* Progress bar */}
        <div style={{ height:3, background:'rgba(255,255,255,0.05)' }}>
          <div style={{ height:'100%', background:'var(--gradient-brand)', width:`${((qIndex+1)/totalQ)*100}%`, transition:'width 0.5s ease' }} />
        </div>

        <div className="answer-panel">
          <p className="question-text" style={{ marginBottom:24 }}>{question.question_text}</p>

          {error && <div className="alert alert-error mb-4">{error}</div>}

          {!feedback ? (
            <div style={{ display:'flex', flexDirection:'column', gap:16 }}>
              <div className="form-group">
                <label className="form-label">Your Answer</label>
                <textarea
                  className="form-textarea"
                  style={{ minHeight:180 }}
                  placeholder="Type your detailed answer here…"
                  value={answer}
                  onChange={e => setAnswer(e.target.value)}
                />
              </div>
              <button className="btn btn-primary" onClick={submitAnswer} disabled={submitting}
                style={{ alignSelf:'flex-end' }}>
                {submitting ? <><span className="spinner" style={{ width:16,height:16 }} /> Evaluating…</> : '✔ Submit Answer'}
              </button>
            </div>
          ) : (
            <div className="animate-fadeIn">
              <div className="alert alert-info mb-4" style={{ fontSize:14, lineHeight:1.6 }}>
                💬 {feedback.comments}
              </div>
              <button className="btn btn-primary" onClick={nextQuestion} style={{ width:'100%', justifyContent:'center' }}>
                {qIndex + 1 >= totalQ ? '🏁 Finish Interview' : '→ Next Question'}
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Side Panel */}
      <div style={{ display:'flex', flexDirection:'column', gap:16 }}>
        {/* Session info */}
        <div className="card card-p-sm">
          <div style={{ fontSize:12, fontWeight:700, color:'var(--text-muted)', letterSpacing:'0.08em', textTransform:'uppercase', marginBottom:12 }}>Session</div>
          <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:8 }}>
            <span style={{ fontSize:13, color:'var(--text-secondary)' }}>Session ID</span>
            <span style={{ fontWeight:700, color:'var(--text-primary)' }}>#{sessionData.session_id}</span>
          </div>
          <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:8 }}>
            <span style={{ fontSize:13, color:'var(--text-secondary)' }}>Progress</span>
            <span style={{ fontWeight:700, color:'var(--text-primary)' }}>{qIndex+1}/{totalQ}</span>
          </div>
          <div style={{ height:6, background:'rgba(255,255,255,0.06)', borderRadius:3, overflow:'hidden', marginTop:12 }}>
            <div style={{ height:'100%', background:'var(--gradient-green)', width:`${((qIndex+1)/totalQ)*100}%`, transition:'width 0.5s' }} />
          </div>
        </div>

        {/* Live Feedback */}
        {feedback && (
          <div className="card card-p-sm animate-fadeIn">
            <div style={{ fontSize:12, fontWeight:700, color:'var(--text-muted)', letterSpacing:'0.08em', textTransform:'uppercase', marginBottom:12 }}>Live Feedback</div>
            {[
              ['Grammar',       feedback.grammar_score],
              ['Technical',     feedback.technical_score],
              ['Communication', feedback.communication_score],
              ['Confidence',    feedback.confidence_score],
              ['Completeness',  feedback.completeness_score],
            ].map(([label, val]) => (
              <div key={label} style={{ marginBottom:12 }}>
                <div style={{ display:'flex', justifyContent:'space-between', marginBottom:4 }}>
                  <span style={{ fontSize:12, color:'var(--text-secondary)' }}>{label}</span>
                  <span style={{ fontSize:12, fontWeight:700, color: scoreColor(val) }}>{val}%</span>
                </div>
                <div style={{ height:4, background:'rgba(255,255,255,0.06)', borderRadius:2, overflow:'hidden' }}>
                  <div style={{ height:'100%', background: val>=80?'var(--gradient-green)':val>=60?'var(--gradient-warm)':'linear-gradient(135deg,#ef4444,#dc2626)', width:`${val}%`, transition:'width 0.8s' }} />
                </div>
              </div>
            ))}
            <div style={{ borderTop:'1px solid var(--color-border)', paddingTop:12, marginTop:4, display:'flex', justifyContent:'space-between' }}>
              <span style={{ fontWeight:600, color:'var(--text-secondary)' }}>Overall</span>
              <span style={{ fontWeight:800, fontSize:16, color: scoreColor(feedback.overall_score) }}>{feedback.overall_score}%</span>
            </div>
          </div>
        )}

        {/* Tips */}
        <div className="card card-p-sm">
          <div style={{ fontSize:12, fontWeight:700, color:'var(--text-muted)', letterSpacing:'0.08em', textTransform:'uppercase', marginBottom:10 }}>💡 Tips</div>
          {['Be specific with examples','Use STAR method for HR questions','Show your thought process clearly','Keep answers concise and structured'].map(t => (
            <div key={t} style={{ fontSize:12, color:'var(--text-muted)', padding:'6px 0', borderBottom:'1px solid rgba(255,255,255,0.04)', display:'flex', gap:8 }}>
              <span style={{ color:'#60a5fa', flexShrink:0 }}>→</span>{t}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

/* ─── Main Interview Page ─────────────────────────────── */
export default function InterviewPage() {
  const [step,        setStep]        = useState('setup');   // setup | interview | report
  const [sessionData, setSessionData] = useState(null);
  const [report,      setReport]      = useState(null);
  const [loadingReport, setLoadingReport] = useState(false);

  const handleStart = (data) => {
    setSessionData(data);
    setStep('interview');
  };

  const handleFinish = async (sessionId) => {
    setStep('report');
    setLoadingReport(true);
    try {
      const r = await reportsAPI.generate(sessionId);
      setReport(r.data);
    } catch { setReport(null); }
    finally { setLoadingReport(false); }
  };

  return (
    <div className="animate-fadeIn">
      <div style={{ marginBottom: 28 }}>
        <h1 style={{ fontSize: 24, fontWeight: 800 }}>🎙️ AI Mock Interview</h1>
        <p className="text-secondary text-sm mt-4">
          Personalized interview powered by LangGraph multi-agent AI
        </p>
      </div>

      {/* Step Indicator */}
      <div style={{ display:'flex', alignItems:'center', gap:8, marginBottom:36 }}>
        {[['Setup','1'],['Interview','2'],['Report','3']].map(([label, num], i) => {
          const stepIndex = ['setup','interview','report'].indexOf(step);
          const active = i <= stepIndex;
          return (
            <React.Fragment key={label}>
              <div style={{ display:'flex', alignItems:'center', gap:8 }}>
                <div style={{
                  width:28, height:28, borderRadius:'50%',
                  background: active ? 'var(--gradient-brand)' : 'rgba(255,255,255,0.06)',
                  display:'flex', alignItems:'center', justifyContent:'center',
                  fontSize:13, fontWeight:700, color: active ? 'white' : 'var(--text-muted)',
                  transition:'all 0.3s'
                }}>{num}</div>
                <span style={{ fontSize:13, fontWeight:600, color: active ? 'var(--text-primary)' : 'var(--text-muted)' }}>{label}</span>
              </div>
              {i < 2 && <div style={{ flex:1, height:1, background: active && i < stepIndex ? 'var(--color-primary)' : 'var(--color-border)', transition:'background 0.3s' }} />}
            </React.Fragment>
          );
        })}
      </div>

      {step === 'setup'     && <SetupStep onStart={handleStart} />}
      {step === 'interview' && <QuestionStep sessionData={sessionData} onFinish={handleFinish} />}
      {step === 'report'    && (
        loadingReport ? (
          <div className="loading-state">
            <span className="spinner spinner-lg" />
            <span>Generating your performance report…</span>
          </div>
        ) : report ? (
          <ReportInline report={report} onRestart={() => { setStep('setup'); setSessionData(null); setReport(null); }} />
        ) : (
          <div className="alert alert-error">Failed to generate report. Please try again.</div>
        )
      )}
    </div>
  );
}

/* ─── Inline Report (after interview) ───────────────── */
function ReportInline({ report, onRestart }) {
  const scoreColor = (s) => s >= 80 ? '#34d399' : s >= 60 ? '#fcd34d' : '#f87171';

  const renderSkillGaps = (summary) => {
    if (!summary) return 'No skill gaps identified.';
    if (typeof summary === 'string') return summary;
    const missing = summary.missing_skills || summary.missing || [];
    if (Array.isArray(missing) && missing.length > 0) {
      return (
        <ul style={{ paddingLeft: 18, margin: 0 }}>
          {missing.map((s, i) => (
            <li key={i} style={{ marginBottom: 6 }}>Gain practical exposure in <strong style={{ color: '#f87171' }}>{s}</strong></li>
          ))}
        </ul>
      );
    }
    return 'No critical skill gaps identified.';
  };

  const renderImprovementPlan = (plan) => {
    if (!plan) return 'Keep practicing and improving!';
    if (typeof plan === 'string') return plan;
    const steps = plan.roadmap_steps || plan.roadmap || [];
    if (Array.isArray(steps) && steps.length > 0) {
      return (
        <ul style={{ paddingLeft: 18, margin: 0 }}>
          {steps.map((step, i) => (
            <li key={i} style={{ marginBottom: 6 }}>{step}</li>
          ))}
        </ul>
      );
    }
    return 'Review core architectural principles and system design patterns.';
  };

  return (
    <div className="animate-fadeIn" style={{ maxWidth:800, margin:'0 auto' }}>
      {/* Score Header */}
      <div className="report-header">
        <div style={{ textAlign:'center' }}>
          <div style={{ fontSize:56, fontWeight:900, color: scoreColor(report.overall_score) }}>
            {report.overall_score}%
          </div>
          <div style={{ fontSize:13, color:'var(--text-muted)', fontWeight:600, marginTop:4 }}>Overall Score</div>
        </div>
        <div style={{ flex:1 }}>
          <h2 style={{ fontSize:22, fontWeight:800, marginBottom:8 }}>🎉 Interview Complete!</h2>
          <p style={{ fontSize:14, color:'var(--text-secondary)', marginBottom:16 }}>
            Session #{report.session_id} · Report #{report.report_id}
          </p>
          <div style={{ display:'flex', gap:12, flexWrap:'wrap' }}>
            <a href={reportsAPI.downloadPdf(report.report_id)} target="_blank" rel="noopener noreferrer"
              className="btn btn-secondary btn-sm">📥 Download PDF Report</a>
            <button className="btn btn-ghost btn-sm" onClick={onRestart}>🔄 New Interview</button>
          </div>
        </div>
      </div>

      <div className="grid-2">
        <div className="card">
          <div className="card-header"><div className="card-title">📉 Skill Gap Summary</div></div>
          <div className="card-body" style={{ fontSize:14, color:'var(--text-secondary)', lineHeight:1.7 }}>
            {renderSkillGaps(report.skill_gap_summary)}
          </div>
        </div>
        <div className="card">
          <div className="card-header"><div className="card-title">📈 Improvement Plan</div></div>
          <div className="card-body" style={{ fontSize:14, color:'var(--text-secondary)', lineHeight:1.7 }}>
            {renderImprovementPlan(report.improvement_plan)}
          </div>
        </div>
      </div>
    </div>
  );
}
