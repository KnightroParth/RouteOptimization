import { useState, useEffect } from 'react';
import { dashboardAPI, analyticsAPI } from '../services/api';
import LoadingSkeleton from '../components/LoadingSkeleton';
import {
  BarChart3, TrendingUp, Users, Target, Loader2,
  PieChart as PieIcon, Activity, MapPin, RefreshCw,
} from 'lucide-react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, PieChart, Pie, Cell, Legend,
  LineChart, Line, Area, AreaChart,
} from 'recharts';

const COLORS = ['#ef4444', '#f59e0b', '#10b981', '#6366f1', '#ec4899', '#8b5cf6'];

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{
      background: 'rgba(15, 23, 42, 0.95)',
      border: '1px solid rgba(99, 102, 241, 0.3)',
      borderRadius: '8px',
      padding: '10px 14px',
      backdropFilter: 'blur(10px)',
    }}>
      <p style={{ color: '#94a3b8', fontSize: '12px', marginBottom: '6px' }}>{label}</p>
      {payload.map((entry, i) => (
        <p key={i} style={{ color: entry.color, fontSize: '13px', fontWeight: 600 }}>
          {entry.name}: {entry.value}
        </p>
      ))}
    </div>
  );
};

export default function Analytics() {
  const [stats, setStats] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [statsRes, analyticsRes] = await Promise.allSettled([
        dashboardAPI.manager(),
        analyticsAPI.overview(),
      ]);
      if (statsRes.status === 'fulfilled') setStats(statsRes.value.data);
      if (analyticsRes.status === 'fulfilled') setAnalytics(analyticsRes.value.data);
      setError('');
    } catch (err) {
      console.error('Failed to load analytics:', err);
      setError('Unable to load analytics from the server.');
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await loadData();
    setRefreshing(false);
  };

  if (loading) {
    return (
      <div className="analytics-page" style={{ padding: '24px' }}>
        <LoadingSkeleton variant="stat" count={4} />
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginTop: '16px' }}>
          <LoadingSkeleton variant="chart" />
          <LoadingSkeleton variant="chart" />
        </div>
        <div style={{ marginTop: '16px' }}>
          <LoadingSkeleton variant="table" count={5} />
        </div>
      </div>
    );
  }

  const statCards = [
    { label: 'Team Completion', value: `${stats?.overall_completion_rate || 0}%`, icon: <TrendingUp size={16} />, color: '#10b981' },
    { label: 'High Priority Visits', value: stats?.high_priority_count || 0, icon: <Target size={16} />, color: '#ef4444' },
    { label: 'Medical Representatives', value: stats?.total_mrs || 0, icon: <Users size={16} />, color: '#6366f1' },
    { label: 'Planned Visits', value: stats?.total_planned_visits || 0, icon: <BarChart3 size={16} />, color: '#f59e0b' },
  ];

  const priorityData = analytics?.priority_distribution || [];
  const visitTrends = analytics?.visit_trends || [];
  const specialtyCoverage = analytics?.specialty_coverage || [];
  const territoryPerf = analytics?.territory_performance || [];

  // Format trend dates to short labels
  const formattedTrends = visitTrends.map(t => ({
    ...t,
    label: new Date(t.date).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' }),
  }));

  return (
    <div>
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h2>Analytics & Reports</h2>
          <p>Deep dive into team performance and optimization metrics</p>
        </div>
        <button
          className="btn btn-secondary"
          onClick={handleRefresh}
          disabled={refreshing}
          style={{ display: 'flex', alignItems: 'center', gap: '6px' }}
        >
          <RefreshCw size={14} style={refreshing ? { animation: 'spin 1s linear infinite' } : {}} />
          Refresh
        </button>
      </div>

      {error && <div className="alert-error-banner mb-4">{error}</div>}

      {/* KPI Cards */}
      <div className="stats-grid">
        {statCards.map((s) => (
          <div className="stat-card" key={s.label}>
            <div className="stat-card-header">
              <span className="stat-card-label">{s.label}</span>
              <div className="stat-card-icon" style={{ color: s.color }}>{s.icon}</div>
            </div>
            <div className="stat-card-value">{s.value}</div>
          </div>
        ))}
      </div>

      {/* Row 1: Priority Pie + Visit Trends Line */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '20px', marginBottom: '20px' }}>
        {/* Priority Distribution Pie */}
        <div className="card">
          <div className="card-header" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <PieIcon size={16} style={{ color: '#6366f1' }} />
            <h3>Priority Distribution</h3>
          </div>
          <div className="card-body" style={{ height: 300 }}>
            {priorityData.length > 0 && priorityData.some(p => p.value > 0) ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={priorityData}
                    cx="50%"
                    cy="50%"
                    innerRadius={55}
                    outerRadius={90}
                    paddingAngle={4}
                    dataKey="value"
                    stroke="none"
                  >
                    {priorityData.map((entry, index) => (
                      <Cell key={index} fill={entry.color || COLORS[index]} />
                    ))}
                  </Pie>
                  <Tooltip content={<CustomTooltip />} />
                  <Legend
                    verticalAlign="bottom"
                    height={36}
                    formatter={(value) => (
                      <span style={{ color: '#94a3b8', fontSize: '12px' }}>{value}</span>
                    )}
                  />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="empty-state">
                <PieIcon size={32} style={{ color: '#475569', marginBottom: '8px' }} />
                <p>No prediction data yet. Run batch inference to populate.</p>
              </div>
            )}
          </div>
        </div>

        {/* Visit Trends Area Chart */}
        <div className="card">
          <div className="card-header" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Activity size={16} style={{ color: '#10b981' }} />
            <h3>Visit Trends (Last 30 Days)</h3>
          </div>
          <div className="card-body" style={{ height: 300 }}>
            {formattedTrends.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={formattedTrends} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
                  <defs>
                    <linearGradient id="gradCompleted" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="gradPlanned" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(148, 163, 184, 0.1)" />
                  <XAxis
                    dataKey="label"
                    tick={{ fill: '#64748b', fontSize: 10 }}
                    interval={4}
                    axisLine={{ stroke: 'rgba(148, 163, 184, 0.2)' }}
                  />
                  <YAxis
                    tick={{ fill: '#64748b', fontSize: 11 }}
                    axisLine={{ stroke: 'rgba(148, 163, 184, 0.2)' }}
                  />
                  <Tooltip content={<CustomTooltip />} />
                  <Area type="monotone" dataKey="completed" stroke="#10b981" fill="url(#gradCompleted)" strokeWidth={2} name="Completed" />
                  <Area type="monotone" dataKey="planned" stroke="#6366f1" fill="url(#gradPlanned)" strokeWidth={2} name="Planned" />
                  <Line type="monotone" dataKey="cancelled" stroke="#ef4444" strokeWidth={1.5} dot={false} name="Cancelled" />
                  <Legend
                    verticalAlign="top"
                    height={36}
                    formatter={(value) => (
                      <span style={{ color: '#94a3b8', fontSize: '12px' }}>{value}</span>
                    )}
                  />
                </AreaChart>
              </ResponsiveContainer>
            ) : (
              <div className="empty-state">No visit trend data available</div>
            )}
          </div>
        </div>
      </div>

      {/* Row 2: MR Performance Bar Chart */}
      <div className="card" style={{ marginBottom: '20px' }}>
        <div className="card-header" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Users size={16} style={{ color: '#6366f1' }} />
          <h3>MR Performance Breakdown</h3>
        </div>
        <div className="card-body" style={{ height: 350 }}>
          {stats?.mr_summaries?.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={stats.mr_summaries}
                margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(148, 163, 184, 0.1)" />
                <XAxis dataKey="name" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                <YAxis tick={{ fill: '#94a3b8', fontSize: 12 }} />
                <Tooltip content={<CustomTooltip />} />
                <Legend
                  formatter={(value) => (
                    <span style={{ color: '#94a3b8', fontSize: '12px' }}>{value}</span>
                  )}
                />
                <Bar dataKey="completed" stackId="a" fill="#10b981" name="Completed" radius={[0, 0, 0, 0]} />
                <Bar dataKey="pending" stackId="a" fill="#f59e0b" name="Pending" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="empty-state">No MR performance data available</div>
          )}
        </div>
      </div>

      {/* Row 3: Specialty Coverage + Territory Performance */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '20px' }}>
        {/* Specialty Coverage */}
        <div className="card">
          <div className="card-header" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Target size={16} style={{ color: '#ec4899' }} />
            <h3>Specialty Coverage</h3>
          </div>
          <div className="card-body" style={{ height: 320 }}>
            {specialtyCoverage.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={specialtyCoverage}
                  layout="vertical"
                  margin={{ top: 5, right: 30, left: 80, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(148, 163, 184, 0.1)" />
                  <XAxis type="number" tick={{ fill: '#94a3b8', fontSize: 11 }} />
                  <YAxis dataKey="specialty" type="category" tick={{ fill: '#94a3b8', fontSize: 11 }} width={75} />
                  <Tooltip content={<CustomTooltip />} />
                  <Bar dataKey="completed" fill="#10b981" name="Completed" radius={[0, 4, 4, 0]} />
                  <Bar dataKey="total_visits" fill="rgba(99, 102, 241, 0.3)" name="Total" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="empty-state">No specialty data available</div>
            )}
          </div>
        </div>

        {/* Territory Performance */}
        <div className="card">
          <div className="card-header" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <MapPin size={16} style={{ color: '#f59e0b' }} />
            <h3>Territory Performance</h3>
          </div>
          <div className="card-body" style={{ overflowY: 'auto', maxHeight: 320 }}>
            {territoryPerf.length > 0 ? (
              <table className="data-table" style={{ width: '100%' }}>
                <thead>
                  <tr>
                    <th>Territory</th>
                    <th style={{ textAlign: 'center' }}>MRs</th>
                    <th style={{ textAlign: 'center' }}>Visits</th>
                    <th style={{ textAlign: 'center' }}>Completion</th>
                  </tr>
                </thead>
                <tbody>
                  {territoryPerf.map((t, i) => (
                    <tr key={i}>
                      <td style={{ fontWeight: 500 }}>{t.territory}</td>
                      <td style={{ textAlign: 'center' }}>{t.mr_count}</td>
                      <td style={{ textAlign: 'center' }}>
                        <span style={{ color: '#10b981' }}>{t.completed}</span>
                        <span style={{ color: '#475569' }}> / {t.total_visits}</span>
                      </td>
                      <td style={{ textAlign: 'center' }}>
                        <div style={{
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '8px',
                          minWidth: '100px',
                        }}>
                          <div style={{
                            flex: 1,
                            height: '6px',
                            borderRadius: '3px',
                            background: 'rgba(148, 163, 184, 0.15)',
                            overflow: 'hidden',
                          }}>
                            <div style={{
                              width: `${t.completion_rate}%`,
                              height: '100%',
                              borderRadius: '3px',
                              background: t.completion_rate >= 75 ? '#10b981' :
                                         t.completion_rate >= 50 ? '#f59e0b' : '#ef4444',
                              transition: 'width 0.6s ease',
                            }} />
                          </div>
                          <span style={{
                            fontSize: '12px',
                            fontWeight: 600,
                            color: t.completion_rate >= 75 ? '#10b981' :
                                   t.completion_rate >= 50 ? '#f59e0b' : '#ef4444',
                            minWidth: '38px',
                            textAlign: 'right',
                          }}>
                            {t.completion_rate}%
                          </span>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <div className="empty-state">No territory data available</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
