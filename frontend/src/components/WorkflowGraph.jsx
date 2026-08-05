import React from 'react';

export default function WorkflowGraph({ activeStep = 'question_agent' }) {
  const nodes = [
    { id: 'parse_resume', label: 'Resume Agent', icon: '📄', x: 40, y: 30 },
    { id: 'parse_jd', label: 'JD Agent', icon: '🎯', x: 40, y: 110 },
    { id: 'match_skills', label: 'Skill Matcher', icon: '⚡', x: 220, y: 70 },
    { id: 'supervisor', label: 'Supervisor Router', icon: '🧠', x: 400, y: 70 },
    { id: 'question_agent', label: 'Question Agent', icon: '🤖', x: 580, y: 20 },
    { id: 'coding_agent', label: 'Coding Agent', icon: '💻', x: 580, y: 70 },
    { id: 'hr_agent', label: 'HR Agent', icon: '🤝', x: 580, y: 120 },
    { id: 'critic_agent', label: 'Critic & Reflection', icon: '🔍', x: 760, y: 70 },
    { id: 'generate_report', label: 'Report Agent', icon: '📊', x: 940, y: 70 },
  ];

  return (
    <div className="card card-p-sm" style={{ overflowX: 'auto', marginBottom: 24 }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 12 }}>
        <div style={{ fontSize: 13, fontWeight: 700, color: 'var(--text-primary)' }}>
          🧠 Dynamic Supervisor Multi-Agent Workflow DAG
        </div>
        <span className="badge badge-purple">LangGraph Autonomous Engine</span>
      </div>

      <svg width="1080" height="160" style={{ background: 'rgba(7,11,20,0.6)', borderRadius: 12, border: '1px solid var(--color-border)' }}>
        {/* Connection Lines */}
        <line x1="140" y1="45" x2="220" y2="80" stroke="rgba(99,102,241,0.3)" strokeWidth="2" />
        <line x1="140" y1="125" x2="220" y2="80" stroke="rgba(99,102,241,0.3)" strokeWidth="2" />
        <line x1="320" y1="85" x2="400" y2="85" stroke="rgba(99,102,241,0.5)" strokeWidth="2" />
        
        <line x1="490" y1="85" x2="580" y2="35" stroke="rgba(99,102,241,0.4)" strokeWidth="2" />
        <line x1="490" y1="85" x2="580" y2="85" stroke="rgba(99,102,241,0.4)" strokeWidth="2" />
        <line x1="490" y1="85" x2="580" y2="135" stroke="rgba(99,102,241,0.4)" strokeWidth="2" />

        <line x1="680" y1="85" x2="760" y2="85" stroke="rgba(99,102,241,0.5)" strokeWidth="2" />
        <line x1="860" y1="85" x2="940" y2="85" stroke="rgba(99,102,241,0.5)" strokeWidth="2" />

        {/* Nodes */}
        {nodes.map(n => {
          const isActive = n.id === activeStep || activeStep === 'all';
          return (
            <g key={n.id} transform={`translate(${n.x}, ${n.y})`}>
              <rect
                width="110"
                height="36"
                rx="8"
                fill={isActive ? 'rgba(79, 70, 229, 0.25)' : 'rgba(15, 23, 42, 0.7)'}
                stroke={isActive ? '#818cf8' : 'rgba(120, 160, 255, 0.2)'}
                strokeWidth={isActive ? '2' : '1'}
              />
              <text x="10" y="22" fontSize="13" fill="#ffffff">{n.icon}</text>
              <text x="32" y="22" fontSize="10" fontWeight="600" fill={isActive ? '#ffffff' : '#94a3b8'}>{n.label}</text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}
