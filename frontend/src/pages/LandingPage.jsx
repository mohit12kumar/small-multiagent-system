import React from 'react';
import { Link } from 'react-router-dom';

export default function LandingPage() {
  return (
    <div className="hero-page">
      {/* Background orbs */}
      <div className="hero-bg-orb hero-bg-orb-1" />
      <div className="hero-bg-orb hero-bg-orb-2" />
      <div className="hero-bg-orb hero-bg-orb-3" />

      {/* Navigation */}
      <nav className="hero-nav">
        <div style={{ display:'flex', alignItems:'center', gap:12 }}>
          <div style={{
            width:40, height:40, background:'var(--gradient-brand)', borderRadius:10,
            display:'flex', alignItems:'center', justifyContent:'center', fontSize:20
          }}>🧠</div>
          <div>
            <div style={{ fontWeight:800, fontSize:15, color:'var(--text-primary)' }}>InterviewAI</div>
            <div style={{ fontSize:11, color:'var(--text-muted)' }}>Multi-Agent System</div>
          </div>
        </div>
        <div style={{ display:'flex', alignItems:'center', gap:12 }}>
          <Link to="/login"    className="btn btn-ghost btn-sm">Sign In</Link>
          <Link to="/register" className="btn btn-primary btn-sm">Get Started Free</Link>
        </div>
      </nav>

      {/* Hero Body */}
      <div className="hero-body">
        <div className="hero-badge animate-fadeIn">
          <span>⚡</span>
          Powered by LangGraph + Groq AI
        </div>

        <h1 className="hero-title animate-fadeIn" style={{ animationDelay:'0.1s' }}>
          Ace Your Next Interview with{' '}
          <span className="text-gradient">Multi-Agent AI</span>
        </h1>

        <p className="hero-desc animate-fadeIn" style={{ animationDelay:'0.2s' }}>
          AI-driven mock interviews, resume ATS scoring, skill gap analysis, dynamic coding challenges,
          and multi-metric performance feedback — all in one platform.
        </p>

        <div className="hero-cta animate-fadeIn" style={{ animationDelay:'0.3s' }}>
          <Link to="/register" className="btn btn-primary btn-lg">
            🚀 Start Free Interview
          </Link>
          <Link to="/login" className="btn btn-ghost btn-lg">
            Sign In →
          </Link>
        </div>

        {/* Feature Pills */}
        <div className="hero-features animate-fadeIn" style={{ animationDelay:'0.4s' }}>
          {[
            { icon:'📄', label:'AI Resume Parsing & ATS Scoring' },
            { icon:'🎯', label:'Smart Job Description Matching' },
            { icon:'🤖', label:'Personalized Technical Questions' },
            { icon:'💻', label:'Dynamic Coding Challenges' },
            { icon:'🤝', label:'HR & Behavioral Interview Practice' },
            { icon:'📊', label:'Real-time Performance Metrics' },
            { icon:'📈', label:'Skill Gap Analysis & Reports' },
            { icon:'🧠', label:'LangGraph Agentic Workflow' },
          ].map(f => (
            <div key={f.label} className="feature-pill">
              <span className="feature-pill-icon">{f.icon}</span>
              {f.label}
            </div>
          ))}
        </div>
      </div>

      {/* Footer */}
      <div style={{ textAlign:'center', padding:'24px', borderTop:'1px solid var(--color-border)', fontSize:13, color:'var(--text-muted)' }}>
        © 2026 InterviewAI · Built with LangGraph, Groq, FastAPI & React
      </div>
    </div>
  );
}
