import React from 'react';
import { Clock, MapPin, Navigation, CheckCircle2, AlertCircle } from 'lucide-react';

export default function RouteTimeline({ route, stops = [] }) {
  const displayStops = stops.length > 0 ? stops : (route?.stops || [
    { sequence_number: 1, doctor_name: 'Dr. Priya Deshmukh', distance_km: 3.2, estimated_arrival: '09:45 AM', service_duration: 20, wait_time_min: 0, priority_class: 'high' },
    { sequence_number: 2, doctor_name: 'Dr. Ananya Sharma', distance_km: 4.1, estimated_arrival: '10:20 AM', service_duration: 20, wait_time_min: 0, priority_class: 'high' },
    { sequence_number: 3, doctor_name: 'Dr. Rajesh Mehta', distance_km: 1.5, estimated_arrival: '10:50 AM', service_duration: 20, wait_time_min: 10, priority_class: 'medium' },
    { sequence_number: 4, doctor_name: 'Dr. Sneha Kulkarni', distance_km: 3.8, estimated_arrival: '11:30 AM', service_duration: 25, wait_time_min: 5, priority_class: 'medium' },
  ]);

  return (
    <div className="route-timeline-container">
      <div className="timeline-header">
        <div className="timeline-title-group">
          <Navigation size={16} className="text-primary" />
          <span className="timeline-title">Optimized Beat Schedule</span>
        </div>
        <span className="badge-status-ready">Route Ready</span>
      </div>

      <div className="timeline-body">
        {/* Start Point */}
        <div className="timeline-item timeline-endpoint">
          <div className="timeline-marker start-marker">
            <MapPin size={12} />
          </div>
          <div className="timeline-content">
            <div className="timeline-point-title">
              <strong>Start:</strong> Base Office / Home Depot
            </div>
            <div className="timeline-point-meta">
              <span>Departure: 09:30 AM</span>
              <span className="timeline-pill">Origin</span>
            </div>
          </div>
        </div>

        {/* Doctor Stops */}
        {displayStops.map((stop, idx) => (
          <div key={stop.sequence_number || idx} className="timeline-item">
            <div className={`timeline-marker stop-marker ${stop.priority_class || 'medium'}`}>
              <span>{stop.sequence_number || idx + 1}</span>
            </div>
            <div className="timeline-content">
              <div className="timeline-stop-header">
                <span className="timeline-stop-doctor">
                  <strong>{stop.sequence_number || idx + 1}. {stop.doctor_name}</strong>
                  {stop.distance_km && (
                    <span className="timeline-dist-tag"> ({stop.distance_km} km)</span>
                  )}
                </span>
                <span className={`timeline-wait-badge ${stop.wait_time_min > 0 ? 'has-wait' : 'no-wait'}`}>
                  Wait: {stop.wait_time_min || 0}m
                </span>
              </div>
              <div className="timeline-stop-details">
                <span>Arr: {stop.estimated_arrival || '10:00 AM'}</span>
                <span className="timeline-sep">•</span>
                <span>Svc: {stop.service_duration || 20}m</span>
                {stop.priority_class && (
                  <>
                    <span className="timeline-sep">•</span>
                    <span className={`priority-mini-pill ${stop.priority_class}`}>
                      {stop.priority_class}
                    </span>
                  </>
                )}
              </div>
            </div>
          </div>
        ))}

        {/* End Point */}
        <div className="timeline-item timeline-endpoint">
          <div className="timeline-marker end-marker">
            <CheckCircle2 size={12} />
          </div>
          <div className="timeline-content">
            <div className="timeline-point-title">
              <strong>End:</strong> Return to Base / Route Complete
            </div>
            <div className="timeline-point-meta">
              <span>Arrival: {route?.estimated_completion || '02:00 PM'}</span>
              <span className="timeline-pill">Destination</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
