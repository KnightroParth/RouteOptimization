import { useState, useEffect } from 'react';
import { dashboardAPI } from '../services/api';
import { BarChart3, TrendingUp, Users, Target, Loader2 } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function Analytics() {
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
      console.error('Failed to load analytics:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="page-loader">
        <Loader2 size={24} className="animate-spin" style={{ animation: 'spin 1s linear infinite' }} />
      </div>
    );
  }

  const statCards = [
    { label: 'Avg Team Completion', value: `${stats?.team_completion_rate || 0}%`, icon: <TrendingUp size={16} /> },
    { label: 'High Priority Coverage', value: `${stats?.high_priority_coverage_rate || 0}%`, icon: <Target size={16} /> },
    { label: 'Active MRs', value: stats?.active_mrs_today || 0, icon: <Users size={16} /> },
    { label: 'Distance Saved (km)', value: stats?.total_distance_saved_km || 0, icon: <BarChart3 size={16} /> },
  ];

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Analytics & Reports</h2>
          <p>Deep dive into team performance and optimization metrics</p>
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

      <div className="card">
        <div className="card-header">
          <h3>MR Performance Breakdown</h3>
        </div>
        <div className="card-body" style={{ height: 400 }}>
          {stats?.mr_summaries ? (
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={stats.mr_summaries}
                margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="completed" stackId="a" fill="#10b981" name="Completed Visits" />
                <Bar dataKey="pending" stackId="a" fill="#f59e0b" name="Pending Visits" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="empty-state">No performance data available</div>
          )}
        </div>
      </div>
    </div>
  );
}
