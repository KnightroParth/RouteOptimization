import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { dashboardAPI, visitsAPI, routesAPI } from '../services/api';
import {
  CalendarDays, CheckCircle2, Clock, AlertTriangle,
  MapPin, Route as RouteIcon, Loader2, Fuel, Users,
  Target, MessageSquare, ExternalLink, Navigation
} from 'lucide-react';
import RouteMap from '../components/RouteMap';
import RouteTimeline from '../components/RouteTimeline';

export default function MRDashboard() {
  const { user } = useAuth();
  const mrId = user?.mr_id || 1;
  const today = new Date().toISOString().split('T')[0];

  const [stats, setStats] = useState(null);
  const [visits, setVisits] = useState([]);
  const [route, setRoute] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
  }, [mrId]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [statsRes, visitsRes, routeRes] = await Promise.all([
        dashboardAPI.mr(mrId, today),
        visitsAPI.daily(mrId, today),
        routesAPI.generate({ mr_id: mrId, plan_date: today }),
      ]);
      setError('');
      setStats(statsRes.data);
      setVisits(visitsRes.data?.visits || []);
      setRoute(routeRes.data || null);
    } catch (err) {
      console.error('Failed to load dashboard:', err);
      setError('Unable to load today\'s dashboard from the server.');
      setStats(null);
      setVisits([]);
      setRoute(null);
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
      setError('');
    } catch (err) {
      console.error('Route generation failed:', err);
      setError('Route optimization failed. Check the visit schedule and try again.');
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

  const handleQuickWhatsApp = (docName, phone = '+919876543210') => {
    const text = `Hello ${docName}, this is ${user?.name || 'Rahul Sharma'} from MedRoute Pharma. I am currently en route to your clinic with an estimated arrival in 15 minutes.`;
    const cleanPhone = phone.replace(/[^0-9]/g, '');
    window.open(`https://wa.me/${cleanPhone}?text=${encodeURIComponent(text)}`, '_blank');
  };

  if (loading) {
    return (
      <div className="page-loader">
        <Loader2 size={28} className="animate-spin" />
      </div>
    );
  }

  // Sample RF Predictions matching mockup
  const rfPredictions = [
    { doctor: 'Dr. Anand Sharma', specialty: 'Cardiologist', window: '10:00 AM - 12:00 PM', score: '0.89 (High)', scoreClass: 'high', confidence: '92%' },
    { doctor: 'Dr. Rajesh Mehta', specialty: 'General Physician', window: '11:00 AM - 01:00 PM', score: '0.85 (High)', scoreClass: 'high', confidence: '88%' },
    { doctor: 'Dr. Sneha Kulkarni', specialty: 'Orthopedic', window: '02:00 PM - 04:00 PM', score: '0.62 (Med)', scoreClass: 'medium', confidence: '75%' },
    { doctor: 'Dr. Priya Deshmukh', specialty: 'Pediatrician', window: '09:00 AM - 11:30 AM', score: '0.58 (Med)', scoreClass: 'medium', confidence: '71%' },
    { doctor: 'Dr. Vikram Patil', specialty: 'Dermatologist', window: '04:00 PM - 06:00 PM', score: '0.34 (Low)', scoreClass: 'low', confidence: '81%' },
  ];

  const totalDistance = route?.total_distance_km || 0;
  const fuelEstimate = (totalDistance * 0.03).toFixed(2); // 30 km/L standard two-wheeler

  return (
    <div className="mr-dashboard-page">
      <div className="page-header">
        <div>
          <h2>Daily Dashboard</h2>
          <p>Schedule & Route Execution for {today} • {user?.territory || 'Pune Central & Deccan'}</p>
        </div>
        <div className="page-header-actions">
          <button 
            type="button"
            className="btn btn-primary" 
            onClick={generateRoute} 
            disabled={generating}
          >
            {generating ? (
              <><Loader2 size={14} className="animate-spin" /> Optimizing...</>
            ) : (
              <><RouteIcon size={14} /> Run Route Optimization</>
            )}
          </button>
        </div>
      </div>

      {error && <div className="alert-error-banner mb-4">{error}</div>}

      {/* KPI Summary Cards */}
      <div className="stats-grid mb-4">
        <div className="stat-card">
          <div className="stat-card-header">
            <span className="stat-card-label">Assigned Doctors</span>
            <div className="stat-card-icon"><Users size={16} /></div>
          </div>
          <div className="stat-card-value">{stats?.total_visits ?? 0}</div>
          <div className="stat-card-subtitle">{visits.length} scheduled on today's beat</div>
        </div>

        <div className="stat-card">
          <div className="stat-card-header">
            <span className="stat-card-label">High Priority Visits</span>
            <div className="stat-card-icon"><AlertTriangle size={16} /></div>
          </div>
          <div className="stat-card-value text-danger">{stats?.high_priority_visits ?? 0}</div>
          <div className="stat-card-subtitle">Priority score &gt; 0.70</div>
        </div>

        <div className="stat-card">
          <div className="stat-card-header">
            <span className="stat-card-label">Optimized Distance</span>
            <div className="stat-card-icon"><Fuel size={16} /></div>
          </div>
          <div className="stat-card-value text-success">{totalDistance} km</div>
          <div className="stat-card-subtitle">Est. Fuel: ~{fuelEstimate} L (Two-wheeler)</div>
        </div>

        <div className="stat-card">
          <div className="stat-card-header">
            <span className="stat-card-label">Est. Completion</span>
            <div className="stat-card-icon"><Clock size={16} /></div>
          </div>
          <div className="stat-card-value text-info">4h 30m</div>
          <div className="stat-card-subtitle">Shift finish: ~02:00 PM</div>
        </div>
      </div>

      {/* Row 1: Interactive Route Map + Today's Visits List */}
      <div className="dashboard-grid mb-4">
        {/* Interactive Route Map */}
        <div className="card">
          <div className="card-header">
            <div className="card-title-group">
              <MapPin size={18} />
              <h3>Route Map Navigation</h3>
            </div>
            <span className="badge-subtle">
              {totalDistance} km • 4 stops
            </span>
          </div>
          <div className="card-body p-0 map-card-body">
            <RouteMap
              route={route}
              visits={visits}
              center={{ lat: 18.5204, lng: 73.8567 }}
            />
          </div>
        </div>

        {/* Today's Scheduled Visits with WhatsApp Action Triggers */}
        <div className="card">
          <div className="card-header">
            <div className="card-title-group">
              <CalendarDays size={18} />
              <h3>Today's Visits Checklist</h3>
            </div>
            <span className="badge-subtle">{today}</span>
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
                  <div className="visit-card" key={v.id || i}>
                    <div className="visit-sequence">{i + 1}</div>
                    <div className="visit-info">
                      <div className="visit-doctor-name">
                        {v.doctor_name || 'Dr. Medical Professional'}
                      </div>
                      <div className="visit-doctor-spec">
                        {v.doctor_specialization || v.specialty || 'Consultant Physician'}
                      </div>
                    </div>
                    <div className="visit-meta">
                      {v.priority_class && (
                        <span className={`priority-badge ${v.priority_class.toLowerCase()}`}>
                          {v.priority_class}
                        </span>
                      )}
                      
                      {/* WhatsApp trigger button */}
                      <button
                        type="button"
                        className="btn-whatsapp-icon"
                        title="Notify via WhatsApp"
                        onClick={() => handleQuickWhatsApp(v.doctor_name || 'Doctor')}
                      >
                        <MessageSquare size={14} />
                      </button>

                      <span className={`status-badge ${v.status || 'planned'}`}>
                        {(v.status || 'planned').replace('_', ' ')}
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
      </div>

      {/* Row 2: RF Predictions Table + VRPTW Timeline */}
      <div className="dashboard-grid">
        {/* Doctor Priority Queue */}
        <div className="card">
          <div className="card-header">
            <div className="card-title-group">
              <Target size={18} />
              <h3>Doctor Priority Queue</h3>
            </div>
            <span className="badge-subtle">Updated: 08:00 AM</span>
          </div>
          <div className="card-body p-0">
            <div className="data-table-wrapper">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Doctor Name</th>
                    <th>Specialty</th>
                    <th>Time Window</th>
                    <th>Priority Score</th>
                    <th>Confidence</th>
                  </tr>
                </thead>
                <tbody>
                  {rfPredictions.map((row) => (
                    <tr key={row.doctor}>
                      <td className="fw-semibold">{row.doctor}</td>
                      <td>{row.specialty}</td>
                      <td className="text-muted small">{row.window}</td>
                      <td>
                        <span className={`priority-text ${row.scoreClass}`}>
                          {row.score}
                        </span>
                      </td>
                      <td>{row.confidence}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* VRPTW Schedule Timeline Component */}
        <div className="card">
          <RouteTimeline route={route} stops={route?.stops} />
        </div>
      </div>
    </div>
  );
}
