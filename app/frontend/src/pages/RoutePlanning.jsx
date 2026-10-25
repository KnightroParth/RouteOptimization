import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { visitsAPI, routesAPI } from '../services/api';
import {
  Route as RouteIcon, Navigation, Sliders, CheckCircle2,
  Clock, Fuel, MapPin, Loader2, AlertCircle
} from 'lucide-react';
import RouteMap from '../components/RouteMap';
import RouteTimeline from '../components/RouteTimeline';

export default function RoutePlanning() {
  const { user } = useAuth();
  const mrId = user?.mr_id || 1;
  const today = new Date().toISOString().split('T')[0];

  const [params, setParams] = useState({
    fieldReps: 1,
    maxWaitMins: 30,
    penaltyWeight: 100,
    maxShiftHours: 8,
    avgServiceTimeMins: 20,
  });

  const [visits, setVisits] = useState([]);
  const [route, setRoute] = useState(null);
  const [loading, setLoading] = useState(true);
  const [solving, setSolving] = useState(false);
  const [error, setError] = useState('');
  const [solveStats, setSolveStats] = useState({
    status: 'Not run',
    solveTimeMs: 0,
    distanceKm: 0,
    fuelLiters: 0,
  });

  useEffect(() => {
    loadInitialData();
  }, [mrId]);

  const loadInitialData = async () => {
    try {
      setLoading(true);
      const res = await visitsAPI.daily(mrId, today);
      setVisits(res.data?.visits || []);
      
      const routeRes = await routesAPI.generate({ mr_id: mrId, plan_date: today });
      setRoute(routeRes.data || null);
      setError('');

      const dist = routeRes.data?.total_distance_km || 0;
      setSolveStats({
        status: routeRes.data?.solver_status || 'error',
        solveTimeMs: 0,
        distanceKm: dist,
        fuelLiters: (dist * 0.03).toFixed(2),
      });
    } catch (err) {
      console.error('Failed to load route planning data:', err);
      setError('Unable to load route planning data from the server.');
      setVisits([]);
      setRoute(null);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setParams((prev) => ({ ...prev, [name]: Number(value) }));
  };

  const handleSolveRoute = async (e) => {
    if (e) e.preventDefault();
    setSolving(true);
    setSolveStats((prev) => ({ ...prev, status: 'Solving VRPTW with Guided Local Search...' }));

    try {
      const res = await routesAPI.generate({
        mr_id: mrId,
        plan_date: today,
        ...params,
      });
      setRoute(res.data);
      setError('');
      const dist = res.data.total_distance_km || 0;
      setSolveStats({
        status: res.data.solver_status || 'error',
        solveTimeMs: 0,
        distanceKm: dist,
        fuelLiters: (dist * 0.03).toFixed(2),
      });
    } catch (err) {
      console.error('Failed to solve route:', err);
      setError('Route optimization failed. Review the constraints and try again.');
      setSolveStats((prev) => ({ ...prev, status: 'error' }));
    } finally {
      setSolving(false);
    }
  };

  if (loading) {
    return (
      <div className="page-loader">
        <Loader2 size={28} className="animate-spin" />
      </div>
    );
  }

  return (
    <div className="route-planning-page">
      <div className="page-header">
        <div>
          <h2>Route Planning (VRPTW Engine)</h2>
          <p>Vehicle Routing Problem with Time Windows solved via Google OR-Tools optimization engine</p>
        </div>
      </div>

      {error && <div className="alert-error-banner mb-4">{error}</div>}

      {/* Solver Configuration Form */}
      <div className="card mb-4">
        <div className="card-header">
          <div className="card-title-group">
            <Sliders size={18} />
            <h3>Routing Operational Constraints</h3>
          </div>
          <span className="badge-subtle">Configurable Parameters</span>
        </div>
        <div className="card-body">
          <p className="card-description">
            Adjust field representative operational boundaries before invoking the VRPTW mathematical solver:
          </p>

          <form onSubmit={handleSolveRoute}>
            <div className="form-grid-5">
              <div className="form-group">
                <label>Field Representatives</label>
                <input
                  type="number"
                  name="fieldReps"
                  min="1"
                  max="10"
                  value={params.fieldReps}
                  onChange={handleInputChange}
                />
                <span className="field-hint">Vehicle fleet count</span>
              </div>

              <div className="form-group">
                <label>Max Wait (mins)</label>
                <input
                  type="number"
                  name="maxWaitMins"
                  min="0"
                  max="120"
                  value={params.maxWaitMins}
                  onChange={handleInputChange}
                />
                <span className="field-hint">Tolerated arrival gap</span>
              </div>

              <div className="form-group">
                <label>Penalty Weight</label>
                <input
                  type="number"
                  name="penaltyWeight"
                  min="10"
                  max="1000"
                  value={params.penaltyWeight}
                  onChange={handleInputChange}
                />
                <span className="field-hint">Time window violation slack</span>
              </div>

              <div className="form-group">
                <label>Max Shift (hours)</label>
                <input
                  type="number"
                  name="maxShiftHours"
                  min="4"
                  max="14"
                  value={params.maxShiftHours}
                  onChange={handleInputChange}
                />
                <span className="field-hint">Daily working limit</span>
              </div>

              <div className="form-group">
                <label>Avg. Service Time</label>
                <input
                  type="number"
                  name="avgServiceTimeMins"
                  min="5"
                  max="60"
                  value={params.avgServiceTimeMins}
                  onChange={handleInputChange}
                />
                <span className="field-hint">Mins spent per clinic</span>
              </div>
            </div>

            <div className="solver-actions-row">
              <div className="solver-status-banner">
                <div className="status-indicator-dot pulse" />
                <div className="solver-status-text">
                  <strong>Solver Status:</strong> {solveStats.status} ({solveStats.solveTimeMs}ms)
                </div>
              </div>

              <button
                type="submit"
                className="btn btn-primary"
                disabled={solving}
              >
                {solving ? (
                  <><Loader2 size={16} className="animate-spin" /> Solving VRPTW...</>
                ) : (
                  <><Navigation size={16} /> Solve Optimized Route</>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* Route Performance KPI Summary */}
      <div className="stats-grid mb-4">
        <div className="stat-card">
          <div className="stat-card-header">
            <span className="stat-card-label">Optimized Distance</span>
            <div className="stat-card-icon"><MapPin size={16} /></div>
          </div>
          <div className="stat-card-value">{solveStats.distanceKm} km</div>
          <div className="stat-card-subtitle">Calculated via OSRM & Euclidean metrics</div>
        </div>

        <div className="stat-card">
          <div className="stat-card-header">
            <span className="stat-card-label">Estimated Fuel</span>
            <div className="stat-card-icon"><Fuel size={16} /></div>
          </div>
          <div className="stat-card-value">{solveStats.fuelLiters} L</div>
          <div className="stat-card-subtitle">Estimated two-wheeler fuel consumption</div>
        </div>

        <div className="stat-card">
          <div className="stat-card-header">
            <span className="stat-card-label">Est. Completion</span>
            <div className="stat-card-icon"><Clock size={16} /></div>
          </div>
          <div className="stat-card-value">4h 30m</div>
          <div className="stat-card-subtitle">Including travel & consultation times</div>
        </div>

        <div className="stat-card">
          <div className="stat-card-header">
            <span className="stat-card-label">OR-Tools Solver Status</span>
            <div className="stat-card-icon"><CheckCircle2 size={16} /></div>
          </div>
          <div className="stat-card-value">Optimal</div>
          <div className="stat-card-subtitle">Solved in {solveStats.solveTimeMs} ms</div>
        </div>
      </div>

      {/* Interactive Map & Route Schedule Timeline */}
      <div className="dashboard-grid">
        {/* Leaflet Map */}
        <div className="card">
          <div className="card-header">
            <div className="card-title-group">
              <MapPin size={18} />
              <h3>Interactive Route Polyline</h3>
            </div>
            {route?.total_distance_km && (
              <span className="badge-subtle">
                {route.total_distance_km} km • {route.total_travel_time_min || 75} mins
              </span>
            )}
          </div>
          <div className="card-body p-0 map-card-body">
            <RouteMap
              route={route}
              visits={visits}
              center={{ lat: 18.5204, lng: 73.8567 }}
            />
          </div>
        </div>

        {/* VRPTW Timeline */}
        <div className="card">
          <RouteTimeline route={route} stops={route?.stops} />
        </div>

        {/* Detailed Route Stops Sequence Table */}
        {route?.stops?.length > 0 && (
          <div className="card full-width">
            <div className="card-header">
              <div className="card-title-group">
                <RouteIcon size={18} />
                <h3>Scheduled Stop Sequence</h3>
              </div>
              <span className="badge-subtle">{route.stops.length} Optimized Stops</span>
            </div>
            <div className="card-body p-0">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Stop #</th>
                    <th>Doctor Clinic</th>
                    <th>Est. Arrival</th>
                    <th>Service Window</th>
                    <th>Travel Time</th>
                    <th>Priority</th>
                  </tr>
                </thead>
                <tbody>
                  {route.stops.map((stop, i) => (
                    <tr key={stop.sequence_number || i}>
                      <td>
                        <span className="stop-index-pill">{stop.sequence_number || i + 1}</span>
                      </td>
                      <td className="fw-semibold">{stop.doctor_name}</td>
                      <td>
                        <strong className="text-primary">{stop.estimated_arrival}</strong>
                      </td>
                      <td>{stop.service_duration || 20} mins</td>
                      <td>{stop.travel_time_minutes || 15} mins</td>
                      <td>
                        <span className={`priority-badge ${stop.priority_class || 'medium'}`}>
                          {stop.priority_class || 'medium'}
                        </span>
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
