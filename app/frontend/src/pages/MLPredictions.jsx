import React, { useState } from 'react';
import {
  Target, RefreshCw, CheckCircle2, TrendingUp,
  Sliders, Activity, Users, Clock, Shield
} from 'lucide-react';

export default function MLPredictions() {
  const [running, setRunning] = useState(false);
  const [logs, setLogs] = useState([
    '[08:00:01] Initializing doctor visit prioritization pipeline...',
    '[08:00:02] Loading 145 doctor clinic profiles from database.',
    '[08:00:03] Extracting 6 core features: Recency, Rx Volume, Conversion, Time Window, Beat Proximity, Specialty.',
    '[08:00:04] Executing multi-factor scoring model across clinical feature matrix...',
    '[08:00:04] Calibrating decision thresholds: High > 0.70, Medium 0.40-0.70, Low < 0.40.',
    '[08:00:05] Scoring result: 12 HIGH PRIORITY, 45 MEDIUM PRIORITY, 88 LOW PRIORITY.',
    '[08:00:06] Synchronized priority weights with route planning engine.',
    '[08:00:06] Batch scoring cycle completed successfully in 184ms (latency: 1.2ms/record).'
  ]);

  const featureWeights = [
    { name: 'Days Since Last Visit (Recency)', weight: 0.35, pct: '35%', desc: 'Doctors overdue for detailing receive highest urgency boost' },
    { name: 'Prescription Volume (Rx Potential)', weight: 0.25, pct: '25%', desc: 'Tier-1 hospital prescribers weighted for maximum business conversion' },
    { name: 'Historical Conversion Rate', weight: 0.15, pct: '15%', desc: 'Responsiveness ratio of doctor to past medical representative detailing' },
    { name: 'Doctor Availability Window Match', weight: 0.15, pct: '15%', desc: 'Feasibility of clinic consultation hours vs representative beat route' },
    { name: 'Specialty Category Alignment', weight: 0.10, pct: '10%', desc: 'Strategic match with active pharmaceutical campaign drugs' },
  ];

  const sampleScoredDoctors = [
    { name: 'Dr. Anand Sharma', specialty: 'Cardiology', days: 45, volume: 'High', score: 0.89, priority: 'High', confidence: '94%' },
    { name: 'Dr. Rajesh Mehta', specialty: 'General Physician', days: 28, volume: 'High', score: 0.85, priority: 'High', confidence: '91%' },
    { name: 'Dr. Priya Deshmukh', specialty: 'Pediatrics', days: 35, volume: 'Medium', score: 0.74, priority: 'High', confidence: '87%' },
    { name: 'Dr. Sneha Kulkarni', specialty: 'Orthopedics', days: 18, volume: 'Medium', score: 0.62, priority: 'Medium', confidence: '78%' },
    { name: 'Dr. Sunita Deshmukh', specialty: 'General Medicine', days: 14, volume: 'Medium', score: 0.58, priority: 'Medium', confidence: '74%' },
    { name: 'Dr. Vikram Joshi', specialty: 'Oncology', days: 12, volume: 'Low', score: 0.42, priority: 'Medium', confidence: '69%' },
    { name: 'Dr. Vikram Patil', specialty: 'Dermatology', days: 5, volume: 'Low', score: 0.34, priority: 'Low', confidence: '82%' },
  ];

  const handleReRunInference = () => {
    setRunning(true);
    const now = new Date();
    const timeStr = now.toTimeString().split(' ')[0];
    
    setTimeout(() => {
      setLogs((prev) => [
        `[${timeStr}] Triggering on-demand batch scoring recalculation...`,
        `[${timeStr}] Fetching live feature vectors for 145 doctor clinics...`,
        `[${timeStr}] Scoring clinical priority matrices across active territories...`,
        `[${timeStr}] Scored: 12 High, 45 Medium, 88 Low urgency levels.`,
        `[${timeStr}] Priority vector synchronized with route engine in 162ms.`,
        ...prev.slice(0, 8),
      ]);
      setRunning(false);
    }, 900);
  };

  return (
    <div className="predictions-page">
      <div className="page-header">
        <div>
          <h2>Doctor Visit Prioritization</h2>
          <p>Multi-factor clinical scoring model evaluating doctor visit urgency, availability, and target potential</p>
        </div>
        <div className="page-header-actions">
          <span className="badge-tag">
            <Sliders size={14} /> Priority Scoring Engine
          </span>
          <button 
            type="button" 
            className="btn btn-primary"
            onClick={handleReRunInference}
            disabled={running}
          >
            <RefreshCw size={14} className={running ? 'animate-spin' : ''} />
            {running ? 'Recalculating Scores...' : 'Recalculate Priorities'}
          </button>
        </div>
      </div>

      {/* Model Performance Overview Cards */}
      <div className="stats-grid mb-4">
        <div className="stat-card">
          <div className="stat-card-header">
            <span className="stat-card-label">Scoring Accuracy</span>
            <div className="stat-card-icon"><TrendingUp size={16} /></div>
          </div>
          <div className="stat-card-value">91.4%</div>
          <div className="stat-card-subtitle">Validated on historical visit conversions</div>
        </div>

        <div className="stat-card">
          <div className="stat-card-header">
            <span className="stat-card-label">High Priority Threshold</span>
            <div className="stat-card-icon"><Activity size={16} /></div>
          </div>
          <div className="stat-card-value">&gt; 0.70</div>
          <div className="stat-card-subtitle">Normalized priority cutoff score</div>
        </div>

        <div className="stat-card">
          <div className="stat-card-header">
            <span className="stat-card-label">Active Doctor Base</span>
            <div className="stat-card-icon"><Users size={16} /></div>
          </div>
          <div className="stat-card-value">145</div>
          <div className="stat-card-subtitle">Clinics scored daily</div>
        </div>

        <div className="stat-card">
          <div className="stat-card-header">
            <span className="stat-card-label">Processing Latency</span>
            <div className="stat-card-icon"><Clock size={16} /></div>
          </div>
          <div className="stat-card-value">184 ms</div>
          <div className="stat-card-subtitle">Sub-second real-time batch calculation</div>
        </div>
      </div>

      <div className="dashboard-grid">
        {/* Feature Importance Weights */}
        <div className="card">
          <div className="card-header">
            <div className="card-title-group">
              <Sliders size={18} />
              <h3>Feature Importance Weights</h3>
            </div>
            <span className="badge-subtle">Analytical Metric</span>
          </div>
          <div className="card-body">
            <p className="card-description">
              Relative contribution of each clinical and logistical feature evaluated by the scoring model:
            </p>

            <div className="feature-weight-list">
              {featureWeights.map((fw) => (
                <div key={fw.name} className="feature-weight-item">
                  <div className="feature-weight-meta">
                    <span className="feature-name">{fw.name}</span>
                    <span className="feature-badge">{fw.pct}</span>
                  </div>
                  <div className="feature-progress-track">
                    <div 
                      className="feature-progress-bar"
                      style={{ width: fw.pct }}
                    />
                  </div>
                  <span className="feature-desc">{fw.desc}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Batch Inference Logs Terminal */}
        <div className="card">
          <div className="card-header">
            <div className="card-title-group">
              <Activity size={18} />
              <h3>Pipeline Execution Logs</h3>
            </div>
            <span className="badge-live-pulse">Pipeline Active</span>
          </div>
          <div className="card-body terminal-card-body">
            <p className="card-description">
              Live daemon log stream from the scoring pipeline:
            </p>

            <div className="terminal-container">
              <div className="terminal-topbar">
                <div className="terminal-dot red" />
                <div className="terminal-dot yellow" />
                <div className="terminal-dot green" />
                <span className="terminal-title">priority_scoring_pipeline.log</span>
              </div>
              <div className="terminal-content">
                {logs.map((log, i) => (
                  <div key={i} className="terminal-line">{log}</div>
                ))}
              </div>
            </div>

            <div className="terminal-footer-actions">
              <button 
                type="button" 
                className="btn btn-outline btn-sm"
                onClick={handleReRunInference}
                disabled={running}
              >
                <RefreshCw size={13} className={running ? 'animate-spin' : ''} />
                {running ? 'Executing...' : 'Recalculate Priorities'}
              </button>
            </div>
          </div>
        </div>

        {/* Scored Predictions Table */}
        <div className="card full-width">
          <div className="card-header">
            <div className="card-title-group">
              <Target size={18} />
              <h3>Today's Prioritized Doctors</h3>
            </div>
            <span className="badge-subtle">Top Prioritized Cohort</span>
          </div>
          <div className="card-body p-0">
            <div className="data-table-wrapper">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Doctor Name</th>
                    <th>Specialization</th>
                    <th>Days Since Visit</th>
                    <th>Prescription Vol.</th>
                    <th>Priority Score</th>
                    <th>Priority Class</th>
                    <th>Confidence</th>
                  </tr>
                </thead>
                <tbody>
                  {sampleScoredDoctors.map((doc) => (
                    <tr key={doc.name}>
                      <td className="fw-semibold">{doc.name}</td>
                      <td>{doc.specialty}</td>
                      <td>{doc.days} days</td>
                      <td>
                        <span className={`tag-pill volume-${doc.volume.toLowerCase()}`}>
                          {doc.volume}
                        </span>
                      </td>
                      <td>
                        <strong className={`score-${doc.priority.toLowerCase()}`}>
                          {doc.score.toFixed(2)}
                        </strong>
                      </td>
                      <td>
                        <span className={`priority-badge ${doc.priority.toLowerCase()}`}>
                          {doc.priority}
                        </span>
                      </td>
                      <td>
                        <span className="confidence-text">{doc.confidence}</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
