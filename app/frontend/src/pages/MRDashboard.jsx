import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { dashboardAPI, visitsAPI, routesAPI } from '../services/api';
import {
  CalendarDays, CheckCircle2, Clock, AlertTriangle,
  MapPin, Route as RouteIcon, Loader2
} from 'lucide-react';
import RouteMap from '../components/RouteMap';

export default function MRDashboard() {
  const { user } = useAuth();
  const mrId = user?.mr_id;
  const today = new Date().toISOString().split('T')[0];

  const [stats, setStats] = useState(null);
  const [visits, setVisits] = useState([]);
  const [route, setRoute] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    if (!mrId) return;
    loadData();
  }, [mrId]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [statsRes, visitsRes] = await Promise.all([
        dashboardAPI.mr(mrId, today),
        visitsAPI.daily(mrId, today),
      ]);
      setStats(statsRes.data);
      setVisits(visitsRes.data.visits || []);
    } catch (err) {
      console.error('Failed to load dashboard:', err);
    } finally {
      setLoading(false);
    }
  };

  const generateRoute = async () => {
    if (!mrId) return;
    setGenerating(true);
    try {
      const res = await routesAPI.generate({ mr_id: mrId, plan_date: today });
      setRoute(res.data);
    } catch (err) {
      console.error('Route generation failed:', err);
    } finally {
      setGenerating(false);
    }
  };

  const updateVisitStatus = async (visitId, newStatus) => {
    try {
      await visitsAPI.updateStatus(visitId, { status: newStatus });
      loadData();
    } catch (err) {
      console.error('Status update failed:', err);
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
    { label: 'Total Visits', value: stats?.total_visits || 0, icon: <CalendarDays size={16} /> },
    { label: 'Completed', value: stats?.completed_visits || 0, icon: <CheckCircle2 size={16} /> },
    { label: 'Pending', value: stats?.pending_visits || 0, icon: <Clock size={16} /> },
    { label: 'High Priority', value: stats?.high_priority_visits || 0, icon: <AlertTriangle size={16} /> },
  ];

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Dashboard</h2>
          <p>Welcome back, {user?.name}. Here's your schedule for today.</p>
        </div>
        <div className="page-header-actions">
          <button className="btn btn-primary" onClick={generateRoute} disabled={generating}>
            {generating ? (
              <><Loader2 size={14} style={{ animation: 'spin 1s linear infinite' }} /> Generating...</>
            ) : (
              <><RouteIcon size={14} /> Generate Route</>
            )}
          </button>
        </div>
      </div>

      {/* Stats */}
      <div className="stats-grid">
        {statCards.map((s) => (
          <div className="stat-card" key={s.label}>
            <div className="stat-card-header">
              <span className="stat-card-label">{s.label}</span>
              <div className="stat-card-icon">{s.icon}</div>
            </div>
            <div className="stat-card-value">{s.value}</div>
            {s.label === 'Total Visits' && stats?.completion_rate !== undefined && (
              <div className="stat-card-subtitle">{stats.completion_rate}% completion rate</div>
            )}
          </div>
        ))}
      </div>

      <div className="dashboard-grid">
        {/* Today's Visits */}
        <div className="card">
          <div className="card-header">
            <h3>Today's Visits</h3>
            <span style={{ fontSize: 12, color: 'var(--muted-foreground)' }}>
              {today}
            </span>
          </div>
          <div className="card-body">
            {visits.length === 0 ? (
              <div className="empty-state">
                <CalendarDays size={32} />
                <p>No visits scheduled for today</p>
              </div>
            ) : (
              <div className="visits-list">
                {visits.map((v, i) => (
                  <div className="visit-card" key={v.id}>
                    <div className="visit-sequence">{i + 1}</div>
                    <div className="visit-info">
                      <div className="visit-doctor-name">
                        {v.doctor_name || 'Unknown Doctor'}
                      </div>
                      <div className="visit-doctor-spec">
                        {v.doctor_specialization || 'General'}
                      </div>
                    </div>
                    <div className="visit-meta">
                      {v.priority_class && (
                        <span className={`priority-badge ${v.priority_class}`}>
                          {v.priority_class}
                        </span>
                      )}
                      <span className={`status-badge ${v.status}`}>
                        {v.status?.replace('_', ' ')}
                      </span>
                      {v.status === 'planned' && (
                        <button
                          className="btn btn-ghost btn-sm"
                          onClick={() => updateVisitStatus(v.id, 'in_progress')}
                        >
                          Start
                        </button>
                      )}
                      {v.status === 'in_progress' && (
                        <button
                          className="btn btn-ghost btn-sm"
                          onClick={() => updateVisitStatus(v.id, 'completed')}
                        >
                          Complete
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Route Map */}
        <div className="card">
          <div className="card-header">
            <h3>Route Map</h3>
            {route?.total_distance_km && (
              <span style={{ fontSize: 12, color: 'var(--muted-foreground)' }}>
                {route.total_distance_km} km · {route.total_travel_time} min
              </span>
            )}
          </div>
          <div className="card-body" style={{ padding: 0 }}>
            <RouteMap
              route={route}
              visits={visits}
              center={{ lat: 18.5204, lng: 73.8567 }}
            />
          </div>
        </div>

        {/* Route Details */}
        {route?.stops?.length > 0 && (
          <div className="card full-width">
            <div className="card-header">
              <h3>Optimized Route Sequence</h3>
              <span className={`status-badge ${route.solver_status === 'success' ? 'completed' : 'missed'}`}>
                {route.solver_status}
              </span>
            </div>
            <div className="card-body" style={{ padding: 0 }}>
              <table className="data-table">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Doctor</th>
                    <th>Arrival</th>
                    <th>Departure</th>
                    <th>Travel (min)</th>
                    <th>Duration (min)</th>
                    <th>Priority</th>
                  </tr>
                </thead>
                <tbody>
                  {route.stops.map((stop) => (
                    <tr key={stop.sequence_number}>
                      <td>{stop.sequence_number}</td>
                      <td style={{ fontWeight: 500 }}>{stop.doctor_name}</td>
                      <td>{stop.estimated_arrival}</td>
                      <td>{stop.estimated_departure}</td>
                      <td>{stop.travel_time_minutes}</td>
                      <td>{stop.service_duration}</td>
                      <td>
                        {stop.priority_class && (
                          <span className={`priority-badge ${stop.priority_class}`}>
                            {stop.priority_class}
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
