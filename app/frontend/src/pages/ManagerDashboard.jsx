import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { dashboardAPI } from '../services/api';
import {
  Users, CalendarDays, CheckCircle2, Clock,
  AlertTriangle, Loader2, TrendingUp, UserCog, Stethoscope, ChevronRight
} from 'lucide-react';

export default function ManagerDashboard() {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const res = await dashboardAPI.manager();
      setStats(res.data);
    } catch (err) {
      console.error('Failed to load manager dashboard:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="page-loader">
        <Loader2 size={24} style={{ animation: 'spin 1s linear infinite' }} />
      </div>
    );
  }

  const statCards = [
    { label: 'Total MRs', value: stats?.total_mrs || 0, icon: <Users size={16} /> },
    { label: 'Planned Visits', value: stats?.total_planned_visits || 0, icon: <CalendarDays size={16} /> },
    { label: 'Completed', value: stats?.total_completed || 0, icon: <CheckCircle2 size={16} /> },
    { label: 'Pending', value: stats?.total_pending || 0, icon: <Clock size={16} /> },
    { label: 'High Priority', value: stats?.high_priority_count || 0, icon: <AlertTriangle size={16} /> },
    { label: 'Completion Rate', value: `${stats?.overall_completion_rate || 0}%`, icon: <TrendingUp size={16} /> },
  ];

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Manager Dashboard</h2>
          <p>Overview of team operations, medical representative allocation, and route performance</p>
        </div>
        <div className="page-header-actions" style={{ display: 'flex', gap: '10px' }}>
          <Link to="/doctors" className="btn btn-secondary">
            <Stethoscope size={15} /> Doctors Network
          </Link>
          <Link to="/staff" className="btn btn-primary">
            <UserCog size={15} /> Manage Staff
          </Link>
        </div>
      </div>

      <div className="stats-grid">
        {statCards.map((s) => (
          <div className="stat-card" key={s.label}>
            <div className="stat-card-header">
              <span className="stat-card-label">{s.label}</span>
              <div className="stat-card-icon">{s.icon}</div>
            </div>
            <div className="stat-card-value">{s.value}</div>
          </div>
        ))}
      </div>

      {/* MR Performance Table */}
      <div className="card">
        <div className="card-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h3>MR Field Representative Performance</h3>
          <Link to="/staff" style={{ fontSize: '0.875rem', color: 'var(--primary-color, #2563eb)', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '4px', fontWeight: 500 }}>
            Manage Representatives <ChevronRight size={14} />
          </Link>
        </div>
        <div className="card-body" style={{ padding: 0 }}>
          {stats?.mr_summaries?.length > 0 ? (
            <table className="data-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Territory</th>
                  <th>Total Visits</th>
                  <th>Completed</th>
                  <th>Pending</th>
                  <th>Completion Rate</th>
                  <th style={{ width: 100, textAlign: 'right' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {stats.mr_summaries.map((mr) => (
                  <tr key={mr.mr_id}>
                    <td style={{ fontWeight: 500 }}>{mr.name}</td>
                    <td>{mr.territory}</td>
                    <td>{mr.total_visits}</td>
                    <td>{mr.completed}</td>
                    <td>{mr.pending}</td>
                    <td>
                      <span style={{
                        fontWeight: 500,
                        color: mr.completion_rate >= 75 ? '#15803d' :
                               mr.completion_rate >= 50 ? '#a16207' : '#ef4444'
                      }}>
                        {mr.completion_rate}%
                      </span>
                    </td>
                    <td style={{ textAlign: 'right' }}>
                      <Link
                        to="/staff"
                        className="btn-icon"
                        title="Manage in Staff directory"
                        style={{
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '4px',
                          padding: '5px 10px',
                          borderRadius: '6px',
                          border: '1px solid #e2e8f0',
                          background: '#fff',
                          color: '#475569',
                          fontSize: '0.8rem',
                          textDecoration: 'none'
                        }}
                      >
                        <UserCog size={13} /> Edit
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="empty-state">
              <Users size={32} />
              <p>No MR data available yet</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
