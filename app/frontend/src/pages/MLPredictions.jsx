import React, { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import { mlAPI } from '../services/api';
import {
  Target, RefreshCw, CheckCircle2, TrendingUp,
  Sliders, Activity, Users, Clock, Shield
} from 'lucide-react';

export default function MLPredictions() {
  const [running, setRunning] = useState(false);
  const [logs, setLogs] = useState([]);
  const [featureWeights, setFeatureWeights] = useState([]);
  const [results, setResults] = useState([]);
  const [metrics, setMetrics] = useState({
    accuracy: null, precision: null, recall: null, f1_score: null,
    cv_accuracy: null, nEstimators: null, model_version: null,
    n_training_samples: null, max_depth: null,
  });
  const [error, setError] = useState('');

  useEffect(() => {
    Promise.all([mlAPI.getFeatureImportance(), mlAPI.getResults()])
      .then(([importanceResponse, resultsResponse]) => {
        const data = importanceResponse.data;
        setFeatureWeights((data.feature_weights || []).map((feature) => ({
          ...feature,
          pct: `${feature.percentage}%`,
          desc: feature.description,
        })));
        setMetrics({
          accuracy: data.accuracy,
          precision: data.precision,
          recall: data.recall,
          f1_score: data.f1_score,
          cv_accuracy: data.cv_accuracy,
          nEstimators: data.n_estimators,
          model_version: data.model_version,
          n_training_samples: data.n_training_samples,
          max_depth: data.max_depth,
        });
        setResults(resultsResponse.data?.results || []);
      })
      .catch(() => setError('Unable to load model information from the server.'));
  }, []);

  const handleReRunInference = async () => {
    setRunning(true);
    setError('');
    try {
      const { data } = await mlAPI.runBatch();
      setLogs(data.logs || []);
      const resultsResponse = await mlAPI.getResults();
      setResults(resultsResponse.data?.results || []);
      toast.success(`Batch inference complete — ${data.counts?.total || 0} doctors scored`);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Batch inference failed.');
    } finally {
      setRunning(false);
    }
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

      {error && <div className="alert-error-banner mb-4">{error}</div>}

      {/* Model Performance Overview Cards */}
      <div className="stats-grid mb-4">
        <div className="stat-card">
          <div className="stat-card-header">
            <span className="stat-card-label">Test Accuracy</span>
            <div className="stat-card-icon"><TrendingUp size={16} /></div>
          </div>
          <div className="stat-card-value">{metrics.accuracy == null ? '—' : `${(metrics.accuracy * 100).toFixed(1)}%`}</div>
          <div className="stat-card-subtitle">Held-out test set evaluation</div>
        </div>

        <div className="stat-card">
          <div className="stat-card-header">
            <span className="stat-card-label">Weighted Precision</span>
            <div className="stat-card-icon"><Target size={16} /></div>
          </div>
          <div className="stat-card-value">{metrics.precision == null ? '—' : `${(metrics.precision * 100).toFixed(1)}%`}</div>
          <div className="stat-card-subtitle">Correct positive predictions</div>
        </div>

        <div className="stat-card">
          <div className="stat-card-header">
            <span className="stat-card-label">Weighted Recall</span>
            <div className="stat-card-icon"><Activity size={16} /></div>
          </div>
          <div className="stat-card-value">{metrics.recall == null ? '—' : `${(metrics.recall * 100).toFixed(1)}%`}</div>
          <div className="stat-card-subtitle">True positive capture rate</div>
        </div>

        <div className="stat-card">
          <div className="stat-card-header">
            <span className="stat-card-label">F1 Score</span>
            <div className="stat-card-icon"><Shield size={16} /></div>
          </div>
          <div className="stat-card-value">{metrics.f1_score == null ? '—' : `${(metrics.f1_score * 100).toFixed(1)}%`}</div>
          <div className="stat-card-subtitle">Harmonic mean of precision & recall</div>
        </div>
      </div>

      {/* Model Configuration Card */}
      <div className="card mb-4">
        <div className="card-header">
          <div className="card-title-group">
            <Shield size={18} />
            <h3>Model Configuration</h3>
          </div>
          <span className="badge-subtle">{metrics.model_version || 'Loading...'}</span>
        </div>
        <div className="card-body">
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '16px' }}>
            {[
              { label: 'Algorithm', value: 'Random Forest' },
              { label: 'Estimators', value: metrics.nEstimators || '—' },
              { label: 'Max Depth', value: metrics.max_depth || '—' },
              { label: 'Cross-Validation', value: metrics.cv_accuracy != null ? `${(metrics.cv_accuracy * 100).toFixed(1)}%` : '—' },
              { label: 'Training Samples', value: metrics.n_training_samples ? metrics.n_training_samples.toLocaleString() : '—' },
              { label: 'Class Balancing', value: 'Balanced Weights' },
            ].map((item) => (
              <div key={item.label} style={{
                padding: '12px 16px',
                background: 'rgba(99, 102, 241, 0.06)',
                borderRadius: '8px',
                border: '1px solid rgba(99, 102, 241, 0.1)',
              }}>
                <div style={{ fontSize: '11px', color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '4px' }}>
                  {item.label}
                </div>
                <div style={{ fontSize: '15px', fontWeight: 600, color: '#e2e8f0' }}>
                  {item.value}
                </div>
              </div>
            ))}
          </div>
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
                  {results.length === 0 ? (
                    <tr><td colSpan="7" className="text-muted">Run batch inference to load current priority results.</td></tr>
                  ) : results.map((doctor) => (
                    <tr key={doctor.id}>
                      <td className="fw-semibold">{doctor.name}</td>
                      <td>{doctor.specialty}</td>
                      <td>—</td>
                      <td>—</td>
                      <td><strong>{Number(doctor.score).toFixed(2)}</strong></td>
                      <td><span className={`priority-badge ${doctor.priority}`}>{doctor.priority}</span></td>
                      <td>—</td>
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
