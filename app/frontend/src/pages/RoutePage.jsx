import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { visitsAPI, routesAPI } from '../services/api';
import { Route as RouteIcon, Loader2 } from 'lucide-react';
import RouteMap from '../components/RouteMap';

export default function RoutePage() {
  const { user } = useAuth();
  const mrId = user?.mr_id;
  const today = new Date().toISOString().split('T')[0];

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
      const res = await visitsAPI.daily(mrId, today);
      setVisits(res.data.visits || []);
    } catch (err) {
      console.error('Failed to load visits:', err);
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

  if (loading) {
    return (
      <div className="page-loader">
        <Loader2 size={24} className="animate-spin" style={{ animation: 'spin 1s linear infinite' }} />
      </div>
    );
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Interactive Route Map</h2>
          <p>Optimize your travel path across all visits</p>
        </div>
        <div className="page-header-actions">
          <button className="btn btn-primary" onClick={generateRoute} disabled={generating}>
            {generating ? (
              <><Loader2 size={14} style={{ animation: 'spin 1s linear infinite' }} /> Generating...</>
            ) : (
              <><RouteIcon size={14} /> Generate Optimized Route</>
            )}
          </button>
        </div>
      </div>

      <div className="card" style={{ marginBottom: 24 }}>
        <div className="card-header">
          <h3>Map View</h3>
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
      
      {route?.stops?.length > 0 && (
        <div className="card full-width">
          <div className="card-header">
            <h3>Optimized Sequence</h3>
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
                  <th>Travel (min)</th>
                  <th>Priority</th>
                </tr>
              </thead>
              <tbody>
                {route.stops.map((stop) => (
                  <tr key={stop.sequence_number}>
                    <td>{stop.sequence_number}</td>
                    <td style={{ fontWeight: 500 }}>{stop.doctor_name}</td>
                    <td>{stop.estimated_arrival}</td>
                    <td>{stop.travel_time_minutes}</td>
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
  );
}
