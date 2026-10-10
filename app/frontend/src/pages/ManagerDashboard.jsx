import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { dashboardAPI } from '../services/api';
import {
  Users, CalendarDays, CheckCircle2, Clock,
  AlertTriangle, Loader2, TrendingUp
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
          <p>Overview of all medical representative activities</p>
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
        <div className="card-header">
          <h3>MR Performance</h3>
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
