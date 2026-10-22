import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import {
  Sliders, User, Clock, ShieldCheck, CheckCircle2,
  Navigation, Fuel, Bell, Save
} from 'lucide-react';

export default function Settings() {
  const { user } = useAuth();
  const [saved, setSaved] = useState(false);

  const [formData, setFormData] = useState({
    fullName: user?.name || 'Parth Lokhande',
    repId: 'MR-4092',
    territory: user?.territory || 'Pune Central (Kothrud & Deccan Zone)',
    vehicle: 'two_wheeler',
    startLocation: 'home',
    shiftStart: '09:30',
    shiftEnd: '18:30',
    avgVisitTime: '15',
    lunchStart: '13:30',
    lunchEnd: '14:30',
    targetVisits: 8,
    optStrategy: 'balanced',
    autoCarryover: true,
    trafficReroute: true,
    whatsappAlerts: true,
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSave = (e) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="settings-page">
      <div className="page-header">
        <div>
          <h2>Field Representative Preferences</h2>
          <p>Personalize operational hours, transit parameters, and VRPTW engine routing behavior</p>
        </div>
        <div className="page-header-actions">
          <span className="badge-tag">
            <User size={14} /> MR-4092 • {user?.name || 'Parth Lokhande'}
          </span>
          <button 
            type="button" 
            className="btn btn-primary"
            onClick={handleSave}
          >
            <Save size={14} />
            Save Preferences
          </button>
        </div>
      </div>

      {saved && (
        <div className="alert-success-banner mb-4">
          <CheckCircle2 size={18} />
          <span>Operational preferences saved and synchronized with routing solver.</span>
        </div>
      )}

      {/* 1. Profile & Territory */}
      <div className="card mb-4">
        <div className="card-header">
          <div className="card-title-group">
            <User size={18} />
            <h3>Representative Profile & Beat Territory</h3>
          </div>
          <span className="badge-subtle">Assigned Beat</span>
        </div>
        <div className="card-body">
          <div className="form-grid">
            <div className="form-group">
              <label>Full Name</label>
              <input
                type="text"
                name="fullName"
                value={formData.fullName}
                readOnly
                className="input-readonly"
              />
            </div>

            <div className="form-group">
              <label>Assigned Territory / Beat</label>
              <input
                type="text"
                name="territory"
                value={formData.territory}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Primary Travel Vehicle</label>
              <select name="vehicle" value={formData.vehicle} onChange={handleChange}>
                <option value="two_wheeler">Two-Wheeler (Motorcycle)</option>
                <option value="four_wheeler">Four-Wheeler (Car)</option>
                <option value="public_transit">Public Transit / Metro</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* 2. Working Hours & Schedule */}
      <div className="card mb-4">
        <div className="card-header">
          <div className="card-title-group">
            <Clock size={18} />
            <h3>Daily Working Hours & Break Constraints</h3>
          </div>
          <span className="badge-subtle">Shift Windows</span>
        </div>
        <div className="card-body">
          <div className="form-grid-4">
            <div className="form-group">
              <label>Depot / Start Location</label>
              <select name="startLocation" value={formData.startLocation} onChange={handleChange}>
                <option value="home">Home (Kothrud Base)</option>
                <option value="branch">Branch Office (Shivajinagar)</option>
                <option value="first_clinic">First Scheduled Clinic</option>
              </select>
            </div>

            <div className="form-group">
              <label>Shift Start Time</label>
              <input
                type="time"
                name="shiftStart"
                value={formData.shiftStart}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Shift End Time</label>
              <input
                type="time"
                name="shiftEnd"
                value={formData.shiftEnd}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Avg. Visit Detailing Time</label>
              <select name="avgVisitTime" value={formData.avgVisitTime} onChange={handleChange}>
                <option value="10">10 mins</option>
                <option value="15">15 mins</option>
                <option value="25">25 mins</option>
              </select>
            </div>
          </div>

          <div className="form-grid mt-3">
            <div className="form-group">
              <label>Lunch / Rest Break Window</label>
              <div className="time-range-group">
                <span>From</span>
                <input
                  type="time"
                  name="lunchStart"
                  value={formData.lunchStart}
                  onChange={handleChange}
                />
                <span>To</span>
                <input
                  type="time"
                  name="lunchEnd"
                  value={formData.lunchEnd}
                  onChange={handleChange}
                />
              </div>
              <span className="field-hint">Solver locks this window free from clinic travel</span>
            </div>

            <div className="form-group">
              <label>Target Visits Per Day (Daily Quota)</label>
              <input
                type="number"
                name="targetVisits"
                min="4"
                max="15"
                value={formData.targetVisits}
                onChange={handleChange}
              />
              <span className="field-hint">Maximum appointments scheduled per shift</span>
            </div>
          </div>
        </div>
      </div>

      {/* 3. Route Optimization Strategy */}
      <div className="card mb-4">
        <div className="card-header">
          <div className="card-title-group">
            <Navigation size={18} />
            <h3>Optimization Solver Strategy & Heuristics</h3>
          </div>
          <span className="badge-subtle">Engine Prioritization</span>
        </div>
        <div className="card-body">
          <div className="radio-cards-grid">
            <label className={`radio-card ${formData.optStrategy === 'balanced' ? 'selected' : ''}`}>
              <input
                type="radio"
                name="optStrategy"
                value="balanced"
                checked={formData.optStrategy === 'balanced'}
                onChange={handleChange}
              />
              <div className="radio-card-content">
                <strong>Balanced Engine (Recommended)</strong>
                <p>Equally weights high-conversion potential while minimizing fuel consumption and road mileage.</p>
              </div>
            </label>

            <label className={`radio-card ${formData.optStrategy === 'conversion' ? 'selected' : ''}`}>
              <input
                type="radio"
                name="optStrategy"
                value="conversion"
                checked={formData.optStrategy === 'conversion'}
                onChange={handleChange}
              />
              <div className="radio-card-content">
                <strong>Maximum Conversion Priority</strong>
                <p>Forces routes to include all Tier-1 and High-Priority prescribers regardless of distance.</p>
              </div>
            </label>

            <label className={`radio-card ${formData.optStrategy === 'distance' ? 'selected' : ''}`}>
              <input
                type="radio"
                name="optStrategy"
                value="distance"
                checked={formData.optStrategy === 'distance'}
                onChange={handleChange}
              />
              <div className="radio-card-content">
                <strong>Minimum Travel Mileage</strong>
                <p>Tight geographic clustering to conserve fuel and minimize two-wheeler commute strain.</p>
              </div>
            </label>
          </div>

          <div className="separator" />

          {/* Automation Toggles */}
          <div className="toggles-list">
            <label className="toggle-item">
              <input
                type="checkbox"
                name="autoCarryover"
                checked={formData.autoCarryover}
                onChange={handleChange}
              />
              <div className="toggle-text">
                <strong>Auto-carryover missed visits to next business day</strong>
                <p>Automatically re-injects unvisited high-priority clinics into tomorrow's priority candidate pool.</p>
              </div>
            </label>

            <label className="toggle-item">
              <input
                type="checkbox"
                name="trafficReroute"
                checked={formData.trafficReroute}
                onChange={handleChange}
              />
              <div className="toggle-text">
                <strong>Live traffic rerouting alerts</strong>
                <p>Monitors congestion spikes and calculates dynamic detour paths.</p>
              </div>
            </label>

            <label className="toggle-item">
              <input
                type="checkbox"
                name="whatsappAlerts"
                checked={formData.whatsappAlerts}
                onChange={handleChange}
              />
              <div className="toggle-text">
                <strong>Automated WhatsApp receptionist arrival notifications</strong>
                <p>Dispatches automated message when representative is 15 minutes away from clinic.</p>
              </div>
            </label>
          </div>
        </div>
      </div>
    </div>
  );
}
